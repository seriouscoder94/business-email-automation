import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class LeadFinder:
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
        self.yelp_api_key = os.getenv('YELP_API_KEY')
        self.foursquare_api_key = os.getenv('FOURSQUARE_API_KEY')
        self.target_location = os.getenv('TARGET_LOCATION', 'Atlanta, GA')
        self.search_radius = int(os.getenv('SEARCH_RADIUS_METERS', 10000))
        
        # Define business categories and their keywords
        self.business_categories = {
            'restaurant': ['restaurant', 'cafe', 'diner', 'bistro', 'eatery', 'food'],
            'retail': ['retail', 'store', 'shop', 'boutique', 'market'],
            'salon': ['salon', 'spa', 'beauty', 'hair', 'nails', 'barber'],
            'gym': ['gym', 'fitness', 'workout', 'training', 'yoga', 'crossfit'],
            'automotive': ['auto', 'car', 'mechanic', 'repair', 'service', 'tire'],
            'professional': ['lawyer', 'accountant', 'consultant', 'insurance', 'real estate', 'professional']
        }
        
        self.leads_file = os.getenv('LEADS_FILE', 'data/leads.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.leads_file), exist_ok=True)
        
        # Load existing leads
        self.leads = self._load_leads()

    def _detect_business_type(self, business):
        """
        Detect business type based on place types, categories, and name
        Returns tuple of (primary_type, confidence_score)
        """
        # Combine all available business information
        business_info = ' '.join([
            business.get('name', '').lower(),
            ' '.join(business.get('types', [])),
            business.get('description', ''),
            ' '.join(business.get('categories', []) if isinstance(business.get('categories'), list) else [])
        ])

        # Score each category
        scores = {}
        for category, keywords in self.business_categories.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in business_info:
                    score += 1
            scores[category] = score / len(keywords)  # Normalize score

        # Get the highest scoring category
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:  # If we have any matches
                return best_category
        
        return ('professional', 0.1)  # Default to professional if no clear match

    def _search_google_places(self, business_type):
        """Search for businesses using Google Places API"""
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
        params = {
            'query': f'{business_type} in {self.target_location}',
            'radius': self.search_radius,
            'key': self.google_api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        except Exception as e:
            print(f"Error searching Google Places: {e}")
            return []

    def _search_yelp(self, business_type):
        """Search for businesses using Yelp API"""
        url = 'https://api.yelp.com/v3/businesses/search'
        headers = {'Authorization': f'Bearer {self.yelp_api_key}'}
        params = {
            'term': business_type,
            'location': self.target_location,
            'radius': self.search_radius
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get('businesses', [])
        except Exception as e:
            print(f"Error searching Yelp: {e}")
            return []

    def _has_website(self, business):
        """Check if a business has a website"""
        # Check Google Places details
        if business.get('website'):
            return True
            
        # Additional check using Place Details API
        if business.get('place_id'):
            try:
                url = 'https://maps.googleapis.com/maps/api/place/details/json'
                params = {
                    'place_id': business['place_id'],
                    'fields': 'website',
                    'key': self.google_api_key
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                result = response.json().get('result', {})
                if result.get('website'):
                    return True
            except Exception as e:
                print(f"Error checking website: {e}")
        
        return False

    def find_leads(self):
        """Find new leads without websites"""
        new_leads = []
        processed_names = set()  # To avoid duplicates
        
        # Search for each business type
        for category in self.business_categories.keys():
            print(f"Searching for {category} businesses...")
            
            # Search both Google Places and Yelp
            businesses = self._search_google_places(category) + self._search_yelp(category)
            
            for business in businesses:
                name = business.get('name')
                if not name or name in processed_names:
                    continue
                    
                processed_names.add(name)
                
                if not self._has_website(business):
                    # Detect business type
                    detected_type, confidence = self._detect_business_type(business)
                    
                    lead = {
                        'id': len(self.leads) + len(new_leads) + 1,
                        'name': name,
                        'detected_type': detected_type,
                        'type_confidence': confidence,
                        'address': business.get('formatted_address') or business.get('location', {}).get('address1', ''),
                        'phone': business.get('formatted_phone_number') or business.get('phone', ''),
                        'found_date': datetime.now().isoformat(),
                        'status': 'new'
                    }
                    
                    new_leads.append(lead)
        
        # Add new leads and save
        self.leads.extend(new_leads)
        self._save_leads()
        
        return new_leads

    def _load_leads(self):
        """Load existing leads from file"""
        try:
            with open(self.leads_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_leads(self):
        """Save leads to file"""
        with open(self.leads_file, 'w') as f:
            json.dump(self.leads, f, indent=2)

    def get_all_leads(self):
        """Get all leads"""
        return self.leads

    def get_lead(self, lead_id):
        """Get a specific lead by ID"""
        for lead in self.leads:
            if str(lead['id']) == str(lead_id):
                return lead
        return None

    def update_lead_status(self, lead_id, status):
        """Update the status of a lead"""
        for lead in self.leads:
            if lead['id'] == lead_id:
                lead['status'] = status
                self._save_leads()
                return True
        return False

    def get_leads_by_status(self, status):
        """Get leads by status"""
        return [lead for lead in self.leads if lead['status'] == status]

    def get_active_leads(self):
        """Get all leads that haven't been contacted yet"""
        try:
            with open(self.leads_file, 'r') as f:
                leads = json.load(f)
                return [lead for lead in leads if not lead.get('contacted', False)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
