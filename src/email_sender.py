"""
Email Sender Module for Business Email Automation

This module handles all email-related functionality using SendGrid API.
It manages email templates, sending emails to leads, and handling email campaigns.

Key Features:
- Send personalized emails using templates
- Support for reply-to email addresses
- Detailed logging of email sending process
- Error handling and status reporting

Dependencies:
- SendGrid API for email delivery
- python-dotenv for environment variable management

Environment Variables Required:
- SENDGRID_API_KEY: Your SendGrid API key
- SENDER_EMAIL: Verified sender email address
- SENDER_NAME: Name to appear as the sender
- COMPANY_NAME: Your company name

Author: Oscar Hernandez
Date: January 2025
"""

import json
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    """
    Handles email sending operations using SendGrid API.
    
    This class manages email templates, sends personalized emails to leads,
    and tracks email sending status. It uses environment variables for 
    configuration and supports reply-to email addresses.
    
    Attributes:
        api_key (str): SendGrid API key
        sender_email (str): Verified sender email address
        reply_to_email (str): Email address for replies
        sender_name (str): Name to appear as sender
        company_name (str): Company name for templates
    """
    def __init__(self):
        """Initialize the EmailSender with configuration from environment variables."""
        load_dotenv()
        
        # Email configuration
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.reply_to_email = 'webreachconnect@gmail.com'  # Add reply-to email
        self.sender_name = os.getenv('SENDER_NAME')
        self.company_name = os.getenv('COMPANY_NAME')
        
        self.templates_file = os.getenv('TEMPLATES_FILE', 'data/templates.json')
        self.campaigns_file = os.getenv('CAMPAIGNS_FILE', 'data/campaigns.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.campaigns_file), exist_ok=True)
        
        # Load templates and campaigns
        self.templates = self._load_templates()
        self.campaigns = self._load_campaigns()

        # Validate configuration
        if not all([self.api_key, self.sender_email, self.sender_name, self.company_name]):
            print("Warning: Missing required environment variables")
            print(f"API Key: {'Present' if self.api_key else 'Missing'}")
            print(f"Sender Email: {self.sender_email}")
            print(f"Sender Name: {self.sender_name}")
            print(f"Company Name: {self.company_name}")

    def _load_templates(self):
        """Load email templates from file"""
        try:
            with open(self.templates_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_templates(self):
        """Save email templates to file"""
        with open(self.templates_file, 'w') as f:
            json.dump(self.templates, f, indent=2)

    def _load_campaigns(self):
        """Load campaigns from file"""
        try:
            with open(self.campaigns_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_campaigns(self):
        """Save campaigns to file"""
        with open(self.campaigns_file, 'w') as f:
            json.dump(self.campaigns, f, indent=2)

    def get_all_templates(self):
        """Get all email templates"""
        return self.templates

    def get_template(self, template_id):
        """Get a specific template by ID"""
        for template in self.templates:
            if template['id'] == template_id:
                return template
        return None

    def get_active_template(self):
        """Get the currently active template"""
        for template in self.templates:
            if template.get('active'):
                return template
        return None if not self.templates else self.templates[0]

    def save_template(self, template_data):
        """Save a new template or update existing one"""
        template_id = template_data.get('id')
        
        if template_id:
            # Update existing template
            for i, template in enumerate(self.templates):
                if template['id'] == template_id:
                    self.templates[i] = template_data
                    break
        else:
            # Create new template
            template_data['id'] = str(len(self.templates) + 1)
            self.templates.append(template_data)
        
        self._save_templates()
        return template_data['id']

    def get_all_campaigns(self):
        """Get all campaigns"""
        return self.campaigns

    def get_campaign(self, campaign_id):
        """Get a specific campaign by ID"""
        for campaign in self.campaigns:
            if campaign['id'] == campaign_id:
                return campaign
        return None

    def start_campaign(self, leads, template):
        """Start an email campaign with the given leads and template"""
        try:
            campaign_id = str(len(self.campaigns) + 1)
            campaign = {
                'id': campaign_id,
                'template_id': template['id'],
                'leads': [lead['id'] for lead in leads],
                'status': 'active',
                'started_at': datetime.now().isoformat(),
                'emails_sent': 0,
                'opens': 0,
                'responses': 0
            }
            
            self.campaigns.append(campaign)
            self._save_campaigns()
            
            return campaign_id
            
        except Exception as e:
            print(f"Error starting campaign: {e}")
            raise

    def preview_template(self, template_id, lead=None):
        """Preview a template with placeholder values or lead data"""
        template = self.get_template(template_id)
        if not template:
            return None
            
        # Create preview data
        preview_data = {
            'business_name': lead['name'] if lead else 'Your Business Name',
            'sender_name': self.sender_name or 'Your Name',
            'company_name': self.company_name or 'Your Company'
        }
        
        # Replace placeholders
        subject = template['subject']
        content = template['content']
        
        for key, value in preview_data.items():
            placeholder = '{' + key + '}'
            subject = subject.replace(placeholder, value)
            content = content.replace(placeholder, value)
            
        return {
            'subject': subject,
            'content': content
        }

    def send_email(self, lead_id, template_id):
        """Send an email to a lead using the specified template."""
        try:
            print(f"\nSending email:")
            print(f"Lead ID: {lead_id}")
            print(f"Template ID: {template_id}")
            
            # Get lead and template
            lead = self.get_lead(lead_id)
            template = self.get_template(template_id)
            
            print(f"Found lead: {lead}")
            print(f"Found template: {template}")
            
            if not lead or not template:
                print("Lead or template not found")
                return False, "Lead or template not found"
            
            # Prepare email content
            subject = template['subject'].format(
                business_name=lead['name'],
                sender_name=self.sender_name,
                company_name=self.company_name
            )
            
            content = template['content'].format(
                business_name=lead['name'],
                sender_name=self.sender_name,
                company_name=self.company_name
            )
            
            print(f"Prepared email:")
            print(f"To: {lead['email']}")
            print(f"From: {self.sender_email}")
            print(f"Reply-To: {self.reply_to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {content}")
            
            # Create SendGrid message with reply-to
            message = Mail(
                from_email=self.sender_email,
                to_emails=lead['email'],
                subject=subject,
                plain_text_content=content
            )
            
            # Add reply-to
            message.reply_to = Email(self.reply_to_email)
            
            print("\nSending via SendGrid...")
            print(f"API Key (first 10 chars): {self.api_key[:10]}...")
            
            try:
                sg = SendGridAPIClient(self.api_key)
                response = sg.send(message)
                print(f"SendGrid Response Status: {response.status_code}")
                print(f"SendGrid Response Body: {response.body}")
                print(f"SendGrid Response Headers: {response.headers}")
                
                if response.status_code == 202:
                    print("Email sent successfully!")
                    # Update lead status
                    lead['status'] = 'contacted'
                    self.save_leads()  # Save the updated status
                    return True, "Email sent successfully"
                else:
                    error_msg = f"SendGrid error: Status {response.status_code}"
                    print(error_msg)
                    return False, error_msg
                    
            except Exception as e:
                error_msg = f"SendGrid error: {str(e)}"
                print(error_msg)
                return False, error_msg
            
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            print(error_msg)
            return False, error_msg

    def send_email_to_lead(self, lead, template_id):
        """Send an email to a lead using the specified template."""
        try:
            print(f"\nSending email:")
            print(f"Lead: {lead}")
            print(f"Template ID: {template_id}")
            
            # Get template
            template = self.get_template(template_id)
            print(f"Found template: {template}")
            
            if not template:
                print("Template not found")
                return False, "Template not found"
            
            # Prepare email content
            subject = template['subject'].format(
                business_name=lead['name'],
                sender_name=self.sender_name,
                company_name=self.company_name
            )
            
            content = template['content'].format(
                business_name=lead['name'],
                sender_name=self.sender_name,
                company_name=self.company_name
            )
            
            print(f"Prepared email:")
            print(f"To: {lead['email']}")
            print(f"From: {self.sender_email}")
            print(f"Reply-To: {self.reply_to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {content}")
            
            # Create SendGrid message with reply-to
            message = Mail(
                from_email=self.sender_email,
                to_emails=lead['email'],
                subject=subject,
                plain_text_content=content
            )
            
            # Add reply-to
            message.reply_to = Email(self.reply_to_email)
            
            print("\nSending via SendGrid...")
            print(f"API Key (first 10 chars): {self.api_key[:10]}...")
            
            try:
                sg = SendGridAPIClient(self.api_key)
                response = sg.send(message)
                print(f"SendGrid Response Status: {response.status_code}")
                print(f"SendGrid Response Body: {response.body}")
                print(f"SendGrid Response Headers: {response.headers}")
                
                if response.status_code == 202:
                    print("Email sent successfully!")
                    return True, "Email sent successfully"
                else:
                    error_msg = f"SendGrid error: Status {response.status_code}"
                    print(error_msg)
                    return False, error_msg
                    
            except Exception as e:
                error_msg = f"SendGrid error: {str(e)}"
                print(error_msg)
                return False, error_msg
            
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            print(error_msg)
            return False, error_msg

    def process_campaigns(self):
        """Process all active campaigns"""
        for campaign in self.campaigns:
            if campaign['status'] != 'active':
                continue
                
            template = self.get_template(campaign['template_id'])
            if not template:
                continue
                
            # Get leads that haven't been contacted
            remaining_leads = [lead for lead in campaign['leads'] if not lead.get('contacted')]
            
            if not remaining_leads:
                campaign['status'] = 'completed'
                continue
                
            # Send emails to remaining leads
            for lead in remaining_leads[:10]:  # Process 10 leads at a time
                if self.send_email(lead, template):
                    lead['contacted'] = True
                    campaign['emails_sent'] += 1
                    
            # Update campaign progress
            total_leads = len(campaign['leads'])
            contacted_leads = len([lead for lead in campaign['leads'] if lead.get('contacted')])
            campaign['progress'] = (contacted_leads / total_leads) * 100
            
            # Save changes
            self._save_campaigns()
