import os
from typing import List, Dict
import requests
import whois
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

class LeadFinder:
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        self.yelp_api_key = os.getenv('YELP_API_KEY')
        self.foursquare_api_key = os.getenv('FOURSQUARE_API_KEY')
        
    def has_website(self, domain: str) -> bool:
        """Check if a domain exists using WHOIS lookup."""
        try:
            whois.whois(domain)
            return True
        except Exception:
            return False
            
    def find_leads_google_places(self, location: str, radius: int = 5000) -> List[Dict]:
        """Find businesses using Google Places API."""
        leads = []
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        params = {
            "query": f"businesses in {location}",
            "radius": radius,
            "key": self.google_api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for place in tqdm(results, desc="Processing Google Places results"):
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
                details_params = {
                    "place_id": place["place_id"],
                    "fields": "name,formatted_address,formatted_phone_number,website",
                    "key": self.google_api_key
                }
                
                details = requests.get(details_url, params=details_params).json()
                result = details.get("result", {})
                
                if "website" not in result:
                    leads.append({
                        "business_name": place["name"],
                        "address": place.get("formatted_address"),
                        "phone": result.get("formatted_phone_number"),
                        "source": "Google Places"
                    })
                    
        return leads
        
    def find_leads_yelp(self, location: str) -> List[Dict]:
        """Find businesses using Yelp API."""
        leads = []
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization": f"Bearer {self.yelp_api_key}"}
        
        params = {
            "location": location,
            "limit": 50
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            businesses = response.json().get("businesses", [])
            for business in tqdm(businesses, desc="Processing Yelp results"):
                if not business.get("url"):  # Yelp listing URL, not business website
                    leads.append({
                        "business_name": business["name"],
                        "address": " ".join(business["location"].get("display_address", [])),
                        "phone": business.get("phone"),
                        "source": "Yelp"
                    })
                    
        return leads
        
    def find_leads_foursquare(self, location: str) -> List[Dict]:
        """Find businesses using Foursquare API."""
        leads = []
        url = "https://api.foursquare.com/v3/places/search"
        headers = {
            "Authorization": self.foursquare_api_key,
            "Accept": "application/json"
        }
        
        params = {
            "near": location,
            "limit": 50
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for place in tqdm(results, desc="Processing Foursquare results"):
                if "website" not in place:
                    leads.append({
                        "business_name": place.get("name"),
                        "address": place.get("location", {}).get("formatted_address"),
                        "phone": place.get("tel"),
                        "source": "Foursquare"
                    })
                    
        return leads

    def find_all_leads(self, location: str) -> List[Dict]:
        """Find leads from all available sources."""
        all_leads = []
        
        print("Finding leads from Google Places...")
        all_leads.extend(self.find_leads_google_places(location))
        
        print("\nFinding leads from Yelp...")
        all_leads.extend(self.find_leads_yelp(location))
        
        print("\nFinding leads from Foursquare...")
        all_leads.extend(self.find_leads_foursquare(location))
        
        # Remove duplicates based on business name and address
        unique_leads = []
        seen = set()
        
        for lead in all_leads:
            key = (lead["business_name"], lead["address"])
            if key not in seen:
                seen.add(key)
                unique_leads.append(lead)
        
        print(f"\nFound {len(unique_leads)} unique leads without websites!")
        return unique_leads
