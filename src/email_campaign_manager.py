import os
from typing import List, Dict
from datetime import datetime
import json
from crm_integration import CRMIntegration

class EmailCampaignManager:
    def __init__(self):
        self.crm = CRMIntegration()
        self.templates_file = os.path.join(os.path.dirname(__file__), 'data', 'templates.json')
        self.load_templates()

    def load_templates(self):
        """Load email templates from JSON file."""
        try:
            with open(self.templates_file, 'r') as f:
                self.templates = json.load(f)
        except FileNotFoundError:
            self.templates = {
                "no_website": {
                    "subject": "Boost Your Online Presence with a Professional Website",
                    "template_id": "d-xxxxxxxxxxxxx",  # SendGrid template ID
                    "tags": ["No Website", "High Priority"]
                }
            }
            # Create templates file if it doesn't exist
            os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
            with open(self.templates_file, 'w') as f:
                json.dump(self.templates, f, indent=4)

    def process_businesses(self, businesses: List[Dict]) -> Dict:
        """Process businesses and export to CRM/email systems."""
        results = {
            'hubspot_contacts': [],
            'mailchimp_subscribers': [],
            'emails_sent': 0,
            'errors': []
        }

        # Filter businesses without websites
        no_website_businesses = [b for b in businesses if not b.get('website')]

        try:
            # Export to HubSpot
            results['hubspot_contacts'] = self.crm.export_to_hubspot(no_website_businesses)

            # Add to Mailchimp list
            mailchimp_list_id = os.getenv('MAILCHIMP_LIST_ID')
            if mailchimp_list_id:
                results['mailchimp_subscribers'] = self.crm.add_to_mailchimp_list(
                    no_website_businesses,
                    mailchimp_list_id
                )

            # Send email campaigns
            template_id = self.templates.get('no_website', {}).get('template_id')
            if template_id:
                for business in no_website_businesses:
                    if self.crm.send_email_campaign(business, template_id):
                        results['emails_sent'] += 1

        except Exception as e:
            results['errors'].append(str(e))

        # Log results
        self._log_campaign_results(results, len(no_website_businesses))
        
        return results

    def _log_campaign_results(self, results: Dict, total_businesses: int):
        """Log campaign results."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'total_businesses': total_businesses,
            'hubspot_contacts_created': len(results['hubspot_contacts']),
            'mailchimp_subscribers_added': len(results['mailchimp_subscribers']),
            'emails_sent': results['emails_sent'],
            'errors': results['errors']
        }

        log_file = os.path.join(os.path.dirname(__file__), 'data', 'campaign_logs.json')
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []

        logs.append(log_entry)

        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)
