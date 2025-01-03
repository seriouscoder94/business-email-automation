from lead_finder import LeadFinder
from email_sender import EmailSender
from datetime import datetime
import json

def main():
    # Initialize components
    lead_finder = LeadFinder()
    email_sender = EmailSender()
    
    print("Starting lead search...")
    new_leads = lead_finder.find_leads()
    print(f"Found {len(new_leads)} new leads!")
    
    if new_leads:
        # Create a new campaign
        campaign_name = f"Website Outreach {datetime.now().strftime('%Y-%m-%d')}"
        campaign_id = email_sender.create_campaign(
            name=campaign_name,
            template_id="business_template",
            leads=new_leads
        )
        
        print(f"\nCreated campaign: {campaign_name}")
        print(f"Number of leads: {len(new_leads)}")
        print("\nStarting email processing...")
        
        # Process the campaign
        email_sender.process_campaigns()
        
        print("\nCampaign is running!")
        print("- Emails will be sent according to daily and hourly limits")
        print("- Check the dashboard at http://localhost:5000 for progress")
        print("- Responses will come to webreachconnect@gmail.com")

if __name__ == "__main__":
    main()
