import time
import schedule
from lead_finder import LeadFinder
from email_sender import EmailSender
from dotenv import load_dotenv

load_dotenv()

def process_campaigns():
    """Process all active email campaigns"""
    email_sender = EmailSender()
    email_sender.process_campaigns()

def find_new_leads():
    """Find new leads without websites"""
    lead_finder = LeadFinder()
    new_leads = lead_finder.find_leads()
    print(f"Found {len(new_leads)} new leads!")

def main():
    # Schedule lead finding every day at 9 AM
    schedule.every().day.at("09:00").do(find_new_leads)
    
    # Schedule campaign processing every 15 minutes
    schedule.every(15).minutes.do(process_campaigns)
    
    print("Campaign processor started!")
    print("- Finding new leads daily at 9 AM")
    print("- Processing campaigns every 15 minutes")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
