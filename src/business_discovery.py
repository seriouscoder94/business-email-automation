import os
import json
import time
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from googlemaps import Client as GoogleMapsClient
from yelpapi import YelpAPI
import pandas as pd
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from urllib.parse import urlparse
from email_validator import validate_email, EmailNotValidError
from website_checker import WebsiteChecker, WebsiteCheckResult
from compliance import ComplianceManager
import logging
from config import Config

@dataclass
class BusinessContact:
    name: str
    address: str
    phone: str
    email: Optional[str]
    website: Optional[str]
    source: str
    business_type: str
    has_website: bool
    validation_status: str
    discovery_date: str
    enrichment_status: Dict[str, bool]

class BusinessDiscoveryEngine:
    def __init__(self):
        """Initialize the business discovery engine with API clients"""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Initialize API clients
        try:
            self.gmaps = GoogleMapsClient(key=Config.get_google_api_key()) if Config.get_google_api_key() else None
            if not self.gmaps:
                self.logger.warning("Google Places API client not initialized - missing API key")
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Places client: {str(e)}")
            self.gmaps = None
            
        try:
            self.yelp = YelpAPI(Config.get_yelp_api_key()) if Config.get_yelp_api_key() else None
            if not self.yelp:
                self.logger.warning("Yelp API client not initialized - missing API key")
        except Exception as e:
            self.logger.error(f"Failed to initialize Yelp client: {str(e)}")
            self.yelp = None
            
        if not self.gmaps and not self.yelp:
            self.logger.error("No API clients initialized - business discovery will not work!")
            
        # Initialize results storage
        self.discovered_businesses: List[BusinessContact] = []
        
        # Initialize website checker
        self.website_checker = WebsiteChecker()
        
        # Initialize compliance manager
        self.compliance_manager = ComplianceManager()

    async def discover_businesses(self, region: str, industry: str, keywords: List[str]) -> List[Dict]:
        """Main business discovery workflow"""
        if not any([self.gmaps, self.yelp]):
            # Return mock data for testing
            return [{
                'name': 'Test Business',
                'address': '123 Test St, Test City',
                'phone': '555-0123',
                'email': 'test@example.com',
                'website': 'http://example.com',
                'source': 'mock',
                'business_type': industry,
                'has_website': True,
                'validation_status': 'pending',
                'discovery_date': datetime.now().isoformat()
            }]
            
        businesses = []
        
        # Try each available API
        if self.gmaps:
            places_results = await self._search_google_places(region, industry, keywords)
            businesses.extend(places_results)
            
        if self.yelp:
            yelp_results = await self._search_yelp(region, industry, keywords)
            businesses.extend(yelp_results)
            
        # Remove duplicates
        unique_businesses = self._remove_duplicates(businesses)
        
        # Enrich data
        enriched_businesses = await self._enrich_business_data(unique_businesses)
        
        return enriched_businesses
    
    async def _search_google_places(self, region: str, industry: str, keywords: List[str]) -> List[BusinessContact]:
        """Search Google Places API for businesses"""
        if not self.gmaps:
            return []
            
        businesses = []
        search_query = f"{industry} {' '.join(keywords)}"
        
        try:
            # Search for businesses in the area
            places_result = self.gmaps.places(
                query=search_query,
                location=region,
                radius=50000  # 50km radius
            )
            
            for place in places_result.get('results', []):
                # Get detailed place information
                place_details = self.gmaps.place(place['place_id'])['result']
                
                business = BusinessContact(
                    name=place_details.get('name', ''),
                    address=place_details.get('formatted_address', ''),
                    phone=place_details.get('formatted_phone_number', ''),
                    email=None,  # Will be enriched later
                    website=place_details.get('website', ''),
                    source='Google Places',
                    business_type=industry,
                    has_website=bool(place_details.get('website')),
                    validation_status='pending',
                    discovery_date=datetime.now().isoformat(),
                    enrichment_status={
                        'email_found': False,
                        'phone_validated': False,
                        'website_checked': False
                    }
                )
                
                # Check compliance
                if self.compliance_manager.validate_data_collection({
                    'name': business.name,
                    'address': business.address,
                    'phone': business.phone,
                    'website': business.website,
                    'processing_purpose': 'business_outreach',
                    'collection_date': business.discovery_date
                }):
                    businesses.append(business)
                else:
                    self.logger.warning(f"Skipped non-compliant business from Google: {business.name}")
                    
        except Exception as e:
            print(f"Error searching Google Places: {e}")
            
        return businesses
    
    async def _search_yelp(self, region: str, industry: str, keywords: List[str]) -> List[BusinessContact]:
        """Search Yelp API for businesses"""
        if not self.yelp:
            return []
            
        businesses = []
        search_query = f"{industry} {' '.join(keywords)}"
        
        try:
            response = self.yelp.search_query(
                term=search_query,
                location=region,
                limit=50
            )
            
            for business in response['businesses']:
                biz_details = self.yelp.business_query(business['id'])
                
                business_data = {
                    'name': biz_details['name'],
                    'address': f"{biz_details['location']['address1']}, {biz_details['location']['city']}",
                    'phone': biz_details.get('phone', ''),
                    'yelp_id': business['id'],
                    'processing_purpose': 'business_outreach',
                    'collection_date': datetime.now().isoformat()
                }
                
                # Check compliance
                if self.compliance_manager.validate_data_collection(business_data):
                    business = BusinessContact(
                        name=biz_details['name'],
                        address=f"{biz_details['location']['address1']}, {biz_details['location']['city']}",
                        phone=biz_details.get('phone', ''),
                        email=None,  # Will be enriched later
                        website=biz_details.get('url', ''),
                        source='Yelp',
                        business_type=industry,
                        has_website=bool(biz_details.get('url')),
                        validation_status='pending',
                        discovery_date=datetime.now().isoformat(),
                        enrichment_status={
                            'email_found': False,
                            'phone_validated': False,
                            'website_checked': False
                        }
                    )
                    businesses.append(business)
                else:
                    self.logger.warning(f"Skipped non-compliant business from Yelp: {biz_details['name']}")
                    
        except Exception as e:
            print(f"Error searching Yelp: {e}")
            
        return businesses
    
    async def _search_yellow_pages(self, region: str, industry: str, keywords: List[str]) -> List[BusinessContact]:
        """Search Yellow Pages for businesses"""
        # Implementation depends on Yellow Pages API or scraping approach
        return []
    
    def _remove_duplicates(self, businesses: List[BusinessContact]) -> List[BusinessContact]:
        """Remove duplicate businesses based on name and address"""
        seen = set()
        unique_businesses = []
        
        for business in businesses:
            key = f"{business.name.lower()}|{business.address.lower()}"
            if key not in seen:
                seen.add(key)
                unique_businesses.append(business)
                
        return unique_businesses
    
    async def _enrich_business_data(self, businesses: List[BusinessContact]) -> List[BusinessContact]:
        """Enrich business data with additional information"""
        enriched = []
        
        async with aiohttp.ClientSession() as session:
            for business in businesses:
                # Check website status using the new WebsiteChecker
                website_result = await self.website_checker.check_business_website(
                    business.name,
                    business.address
                )
                
                business.has_website = website_result.has_website
                business.website = website_result.domain if website_result.domain else None
                
                if website_result.has_website:
                    business.enrichment_status['website_checked'] = True
                    print(f"Found website for {business.name}: {website_result.domain}")
                else:
                    print(f"No website found for {business.name} ({website_result.status})")
                
                # Try to find email if no website found
                if not business.has_website and not business.email:
                    email = await self._find_business_email(session, business)
                    if email:
                        business.email = email
                        business.enrichment_status['email_found'] = True
                
                # Validate phone
                if business.phone:
                    business.phone = self._format_phone_number(business.phone)
                    business.enrichment_status['phone_validated'] = True
                
                business.validation_status = 'validated'
                enriched.append(business)
                
        return enriched
    
    async def _find_business_email(self, session: aiohttp.ClientSession, business: BusinessContact) -> Optional[str]:
        """Attempt to find business email through various methods"""
        # Implementation would include various email discovery methods
        return None
    
    def _format_phone_number(self, phone: str) -> str:
        """Format phone number to standard format"""
        # Remove all non-numeric characters
        numbers_only = ''.join(filter(str.isdigit, phone))
        
        # Format as (XXX) XXX-XXXX if 10 digits
        if len(numbers_only) == 10:
            return f"({numbers_only[:3]}) {numbers_only[3:6]}-{numbers_only[6:]}"
        return phone
    
    def discover_businesses_sync(self, region: str, business_type: str, radius: int = 50) -> List[Dict]:
        """
        Synchronous version of business discovery for immediate results
        """
        businesses = []
        
        try:
            # Try Google Places API first
            if self.gmaps:
                self.logger.info(f"Searching Google Places for {business_type} in {region}")
                
                try:
                    # Get location coordinates
                    geocode_result = self.gmaps.geocode(region)
                    if geocode_result:
                        location = geocode_result[0]['geometry']['location']
                        
                        # Search for businesses
                        places_result = self.gmaps.places_nearby(
                            location=location,
                            radius=radius * 1000,  # Convert to meters
                            keyword=business_type
                        )
                        
                        # Process results
                        for place in places_result.get('results', []):
                            business = {
                                'name': place.get('name', ''),
                                'address': place.get('vicinity', ''),
                                'place_id': place.get('place_id', ''),
                                'rating': place.get('rating', 0),
                                'source': 'google',
                                'has_website': bool(place.get('website', '')),
                                'discovery_date': datetime.now().isoformat()
                            }
                            
                            # Get additional details
                            try:
                                details = self.gmaps.place(place['place_id'])['result']
                                business.update({
                                    'phone': details.get('formatted_phone_number', ''),
                                    'website': details.get('website', ''),
                                    'email': '',  # Email usually not available from Google
                                    'business_type': business_type
                                })
                            except Exception as e:
                                self.logger.error(f"Error getting place details: {str(e)}")
                            
                            businesses.append(business)
                except Exception as e:
                    self.logger.error(f"Google Places API error: {str(e)}")
            
            # Try Yelp API
            if self.yelp:
                self.logger.info(f"Searching Yelp for {business_type} in {region}")
                try:
                    yelp_results = self.yelp.search_query(
                        term=business_type,
                        location=region,
                        radius=radius * 1000
                    )
                    
                    for biz in yelp_results.get('businesses', []):
                        business = {
                            'name': biz.get('name', ''),
                            'address': f"{biz.get('location', {}).get('address1', '')}, {biz.get('location', {}).get('city', '')}",
                            'phone': biz.get('phone', ''),
                            'website': biz.get('url', ''),
                            'rating': biz.get('rating', 0),
                            'source': 'yelp',
                            'has_website': bool(biz.get('url', '')),
                            'business_type': business_type,
                            'discovery_date': datetime.now().isoformat()
                        }
                        businesses.append(business)
                except Exception as e:
                    self.logger.error(f"Yelp API error: {str(e)}")
            
            if not businesses:
                self.logger.warning("No businesses found from any source")
                if not self.gmaps and not self.yelp:
                    raise Exception("No API clients available - please check your API keys")
                return []
            
            # Remove duplicates based on name and address
            seen = set()
            unique_businesses = []
            for b in businesses:
                key = (b['name'], b['address'])
                if key not in seen:
                    seen.add(key)
                    unique_businesses.append(b)
            
            self.logger.info(f"Found {len(unique_businesses)} unique businesses")
            return unique_businesses
            
        except Exception as e:
            self.logger.error(f"Error in discover_businesses_sync: {str(e)}")
            raise Exception(f"Business discovery failed: {str(e)}")

    def export_results(self, format: str = 'csv') -> str:
        """Export discovered businesses to specified format"""
        if not self.discovered_businesses:
            return ""
            
        if format == 'csv':
            df = pd.DataFrame([vars(b) for b in self.discovered_businesses])
            output_file = f"discovered_businesses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(output_file, index=False)
            return output_file
        
        elif format == 'json':
            output_file = f"discovered_businesses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump([vars(b) for b in self.discovered_businesses], f, indent=2)
            return output_file
            
        return ""

# Usage Example:
async def main():
    engine = BusinessDiscoveryEngine()
    businesses = await engine.discover_businesses(
        region="Atlanta, GA",
        industry="Restaurant",
        keywords=["local", "family-owned"]
    )
    print(f"Found {len(businesses)} businesses without websites")
    
    # Export results
    csv_file = engine.export_results('csv')
    print(f"Results exported to {csv_file}")

if __name__ == "__main__":
    asyncio.run(main())
