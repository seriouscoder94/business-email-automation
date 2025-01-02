import os
import json
import schedule
import time
from datetime import datetime
from lead_finder import LeadFinder
from email_sender import EmailSender

def save_leads(leads, filename="leads.json"):
    """Save leads to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(leads, f, indent=4)

def load_leads(filename="leads.json"):
    """Load leads from a JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def load_sent_emails(filename="sent_emails.json"):
    """Load record of sent emails."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_sent_emails(sent_emails, filename="sent_emails.json"):
    """Save record of sent emails."""
    with open(filename, 'w') as f:
        json.dump(sent_emails, f, indent=4)

def find_new_leads(location):
    """Find new leads and save them."""
    finder = LeadFinder()
    leads = finder.find_all_leads(location)
    
    # Load existing leads to avoid duplicates
    existing_leads = load_leads()
    existing_businesses = {(lead["business_name"], lead["address"]) for lead in existing_leads}
    
    # Add only new leads
    new_leads = []
    for lead in leads:
        if (lead["business_name"], lead["address"]) not in existing_businesses:
            new_leads.append(lead)
            existing_leads.append(lead)
    
    save_leads(existing_leads)
    print(f"Added {len(new_leads)} new leads to the database!")
    return new_leads

def send_emails_to_leads():
    """Send emails to leads that haven't been contacted."""
    sender = EmailSender()
    leads = load_leads()
    sent_emails = load_sent_emails()
    
    for lead in leads:
        key = f"{lead['business_name']}_{lead['address']}"
        if key not in sent_emails and lead.get("email"):  # Only send if we have email and haven't sent before
            if sender.send_email(lead["email"], lead):
                sent_emails[key] = {
                    "sent_date": datetime.now().isoformat(),
                    "business_name": lead["business_name"],
                    "email": lead["email"]
                }
                save_sent_emails(sent_emails)
                time.sleep(5)  # Add delay between emails to avoid triggering spam filters

def main():
    # Schedule lead finding daily at 9 AM
    schedule.every().day.at("09:00").do(find_new_leads, "Atlanta, GA")
    
    # Schedule email sending daily at 10 AM
    schedule.every().day.at("10:00").do(send_emails_to_leads)
    
    print("Starting automated lead finder and email sender...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # For testing, you can run these functions directly
    # find_new_leads("Atlanta, GA")
    # send_emails_to_leads()
    
    # For production, use the scheduler
    main()
