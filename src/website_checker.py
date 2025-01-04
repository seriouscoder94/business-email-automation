import os
import re
import whois
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class WebsiteCheckResult:
    has_website: bool
    domain: Optional[str] = None
    status: str = "unknown"
    last_checked: str = ""
    is_active: bool = False
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    source: Optional[str] = None

class WebsiteChecker:
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_cse_id = os.getenv('GOOGLE_CSE_ID')
        self.logger = logging.getLogger(__name__)
        
        # Initialize Google Custom Search API
        if self.google_api_key and self.google_cse_id:
            self.google_service = build(
                "customsearch", "v1",
                developerKey=self.google_api_key
            )
        else:
            self.google_service = None
            self.logger.warning("Google API credentials not found")

    async def check_business_website(self, business_name: str, location: str) -> WebsiteCheckResult:
        """Main method to check if a business has a website"""
        self.logger.info(f"Checking website for: {business_name} in {location}")
        
        # Step 1: Search for potential domains
        domains = await self._find_potential_domains(business_name, location)
        
        if not domains:
            return WebsiteCheckResult(
                has_website=False,
                status="no_domains_found"
            )
        
        # Step 2: Verify each domain
        for domain in domains:
            result = await self._verify_domain(domain)
            if result.is_active:
                return result
        
        return WebsiteCheckResult(
            has_website=False,
            status="no_active_website"
        )

    async def _find_potential_domains(self, business_name: str, location: str) -> List[str]:
        """Find potential domain names for the business"""
        domains = set()
        
        # Method 1: Google Custom Search
        if self.google_service:
            google_domains = await self._search_google(business_name, location)
            domains.update(google_domains)
        
        # Method 2: Generate potential domain names
        generated_domains = self._generate_domain_variations(business_name)
        domains.update(generated_domains)
        
        return list(domains)

    async def _search_google(self, business_name: str, location: str) -> List[str]:
        """Search Google for business website"""
        domains = set()
        
        try:
            # Format search query
            query = f"{business_name} {location} official website"
            
            # Execute search
            result = self.google_service.cse().list(
                q=query,
                cx=self.google_cse_id,
                num=10
            ).execute()
            
            # Extract domains from search results
            for item in result.get('items', []):
                url = item.get('link', '')
                domain = self._extract_domain(url)
                if domain:
                    domains.add(domain)
                    
        except Exception as e:
            self.logger.error(f"Google search error: {str(e)}")
        
        return list(domains)

    def _generate_domain_variations(self, business_name: str) -> List[str]:
        """Generate possible domain variations"""
        # Clean business name
        name = re.sub(r'[^a-zA-Z0-9\s]', '', business_name.lower())
        words = name.split()
        
        variations = []
        
        # Generate variations
        variations.extend([
            f"{'.'.join(words)}.com",
            f"{'-'.join(words)}.com",
            f"{''.join(words)}.com"
        ])
        
        # Add common TLDs
        base_domain = '-'.join(words)
        tlds = ['.net', '.org', '.biz', '.co']
        variations.extend([f"{base_domain}{tld}" for tld in tlds])
        
        return variations

    async def _verify_domain(self, domain: str) -> WebsiteCheckResult:
        """Verify if a domain exists and is active"""
        try:
            # Step 1: WHOIS lookup
            domain_info = whois.whois(domain)
            
            if not domain_info.domain_name:
                return WebsiteCheckResult(
                    has_website=False,
                    domain=domain,
                    status="domain_not_registered"
                )
            
            # Step 2: Check if website is active
            is_active = await self._check_website_active(domain)
            
            return WebsiteCheckResult(
                has_website=True,
                domain=domain,
                status="active" if is_active else "inactive",
                is_active=is_active,
                registrar=domain_info.registrar,
                creation_date=str(domain_info.creation_date),
                source="whois"
            )
            
        except Exception as e:
            self.logger.error(f"Domain verification error for {domain}: {str(e)}")
            return WebsiteCheckResult(
                has_website=False,
                domain=domain,
                status="verification_error"
            )

    async def _check_website_active(self, domain: str) -> bool:
        """Check if website is active by making HTTP request"""
        urls = [f"https://{domain}", f"http://{domain}"]
        
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            # Check if it's a real website (not a parked domain)
                            text = await response.text()
                            if not self._is_parked_domain(text):
                                return True
                except:
                    continue
        
        return False

    def _is_parked_domain(self, html_content: str) -> bool:
        """Check if the page is a parked domain"""
        parked_indicators = [
            "domain is parked",
            "buy this domain",
            "domain not configured",
            "parked free",
            "domain parking"
        ]
        
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text().lower()
        
        return any(indicator in text for indicator in parked_indicators)

    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract clean domain from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Remove www. if present
            if domain.startswith('www.'):
                domain = domain[4:]
                
            return domain if domain else None
            
        except:
            return None

# Example usage
async def main():
    checker = WebsiteChecker()
    result = await checker.check_business_website(
        "Joe's Pizza",
        "Atlanta, GA"
    )
    print(f"Website check result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
