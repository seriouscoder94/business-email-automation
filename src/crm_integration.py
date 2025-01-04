import os
from typing import List, Dict
from hubspot import HubSpot
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

class CRMIntegration:
    def __init__(self):
        self.hubspot_client = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))
        self.sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))

    def export_to_hubspot(self, businesses: List[Dict]) -> List[str]:
        """Export businesses to HubSpot and return created contact IDs."""
        contact_ids = []
        
        for business in businesses:
            properties = {
                "firstname": business.get('contact_name', ''),
                "company": business['name'],
                "email": business['email'],
                "phone": business['phone'],
                "address": business['address'],
                "website": business.get('website', ''),
                "industry": business.get('industry', ''),
                "lifecyclestage": "lead"
            }
            
            try:
                contact = self.hubspot_client.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create={"properties": properties}
                )
                contact_ids.append(contact.id)
                print(f"✅ Created HubSpot contact for {business['name']}")
            except Exception as e:
                print(f"❌ Error creating HubSpot contact for {business['name']}: {str(e)}")
        
        return contact_ids

    def send_email_campaign(self, business: Dict, template_id: str) -> bool:
        """Send personalized email using SendGrid template."""
        try:
            message = Mail(
                from_email=Email(os.getenv('SENDER_EMAIL')),
                to_emails=To(business['email']),
            )
            
            # Set template ID and dynamic template data
            message.template_id = template_id
            message.dynamic_template_data = {
                'business_name': business['name'],
                'contact_name': business.get('contact_name', ''),
                'industry': business.get('industry', ''),
                'address': business['address'],
            }
            
            response = self.sendgrid_client.send(message)
            return response.status_code == 202
            
        except Exception as e:
            print(f"Error sending email to {business['name']}: {str(e)}")
            return False
