"""
Business Email Automation Web Application

This Flask application provides a web interface for managing business leads
and sending automated emails using SendGrid. It includes features for lead
management, email template previews, and campaign tracking.

Key Features:
- Lead management (add, update, list)
- Email template management
- Email sending with SendGrid integration
- Campaign tracking and management

Routes:
- / : Main application interface
- /api/leads : Lead management endpoints
- /api/email : Email sending endpoints
- /api/campaigns : Campaign management endpoints
- /agent : Agent interface
- /api/search : Search businesses
- /api/check-websites : Check websites
- /api/enrich-data : Enrich business data
- /api/export-leads : Export leads

Dependencies:
- Flask for web framework
- SendGrid for email delivery
- python-dotenv for environment variables

Author: Oscar Hernandez
Date: January 2025
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from lead_finder import LeadFinder
from email_sender import EmailSender
from campaign_handler import campaign_bp
from business_discovery import BusinessDiscoveryEngine
from website_checker import WebsiteChecker
from crm_integration import CRMIntegration
from email_campaign_manager import EmailCampaignManager
import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)

# Enable CORS
CORS(app)  # Enable CORS for all routes

# Load environment variables
load_dotenv()

# Check environment variables
logger.info("Checking environment variables...")
logger.info(f"GOOGLE_PLACES_API_KEY: {os.getenv('GOOGLE_PLACES_API_KEY')}")
required_vars = [
    'GOOGLE_PLACES_API_KEY',
    'YELP_API_KEY',
    'YELLOW_PAGES_KEY'
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
else:
    logger.info("All required environment variables are set")

# Register blueprints
app.register_blueprint(campaign_bp)

# Initialize services
lead_finder = LeadFinder()
email_sender = EmailSender()
business_discovery = BusinessDiscoveryEngine()
website_checker = WebsiteChecker()
crm_integration = CRMIntegration()
email_manager = EmailCampaignManager()

@app.before_first_request
def before_first_request():
    """Check configuration before starting the server"""
    Config.log_config_status()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agent')
def agent():
    return render_template('ai_agent.html')

@app.route('/ai_agent')
def ai_agent():
    return render_template('ai_agent.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/leads/find', methods=['POST'])
def find_leads():
    try:
        new_leads = lead_finder.find_leads()
        return jsonify({
            'success': True,
            'count': len(new_leads),
            'leads': new_leads
        })
    except Exception as e:
        print(f"Error finding leads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/leads', methods=['GET', 'POST'])
def handle_leads():
    if request.method == 'GET':
        try:
            leads = lead_finder.get_all_leads()
            return jsonify(leads)
        except Exception as e:
            print(f"Error getting leads: {e}")
            return jsonify([])
    else:  # POST
        try:
            data = request.json
            if not data.get('name') or not data.get('email'):
                return jsonify({
                    'success': False,
                    'error': 'Name and email are required'
                }), 400
                
            # Add the lead
            lead = {
                'id': str(len(lead_finder.leads) + 1),
                'name': data['name'],
                'email': data['email'],
                'type': data.get('type', 'other'),
                'status': 'new',
                'found_date': datetime.now().isoformat(),
                'source': 'manual'
            }
            
            lead_finder.leads.append(lead)
            lead_finder._save_leads()
            
            return jsonify({
                'success': True,
                'lead_id': lead['id'],
                'message': 'Lead added successfully'
            })
            
        except Exception as e:
            print(f"Error adding lead: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

@app.route('/api/leads/<lead_id>', methods=['PUT'])
def update_lead(lead_id):
    try:
        data = request.json
        success = lead_finder.update_lead_status(lead_id, data.get('status'))
        return jsonify({
            'success': success
        })
    except Exception as e:
        print(f"Error updating lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/leads/<lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    try:
        # Find and remove the lead
        success = lead_finder.delete_lead(lead_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Lead deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
            
    except Exception as e:
        print(f"Error deleting lead: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    try:
        templates = email_sender.get_all_templates()
        return jsonify(templates)
    except Exception as e:
        print(f"Error getting templates: {e}")
        return jsonify([])

@app.route('/api/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    try:
        template = email_sender.get_template(template_id)
        if template:
            return jsonify(template)
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
    except Exception as e:
        print(f"Error getting template: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates/<template_id>/preview', methods=['POST'])
def preview_template(template_id):
    try:
        print(f"\nTemplate Preview Request:")
        print(f"Template ID: {template_id}")
        
        data = request.json
        lead = data.get('lead')
        print(f"Lead Data: {lead}")
        
        # Get template
        template = email_sender.get_template(template_id)
        print(f"Found Template: {template is not None}")
        if template:
            print(f"Template Content: {template}")
        
        preview = email_sender.preview_template(template_id, lead)
        print(f"Preview Result: {preview}")
        
        if preview:
            return jsonify(preview)
            
        return jsonify({
            'success': False,
            'error': 'Template not found'
        }), 404
        
    except Exception as e:
        print(f"Error previewing template: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email/send', methods=['POST'])
def send_email():
    try:
        print("\nReceived email send request")
        data = request.json
        lead_id = data.get('lead_id')
        template_id = data.get('template_id')
        
        print(f"Lead ID: {lead_id}")
        print(f"Template ID: {template_id}")
        
        if not lead_id or not template_id:
            print("Missing lead_id or template_id")
            return jsonify({
                'success': False,
                'error': 'Missing lead_id or template_id'
            }), 400
            
        # Get lead from LeadFinder
        lead = lead_finder.get_lead(lead_id)
        if not lead:
            print(f"Lead not found: {lead_id}")
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
            
        # Send email using EmailSender
        success, message = email_sender.send_email_to_lead(lead, template_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        print(error_msg)
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/send-email', methods=['POST'])
def send_email_api():
    try:
        data = request.json
        print("Received email request:", data)  # Debug log
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
            
        if not all(key in data for key in ['to', 'subject', 'content']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: to, subject, content'
            }), 400
            
        # Initialize EmailSender
        email_sender = EmailSender()
        
        # Send email
        success, message = email_sender.send_email(
            to_email=data['to'],
            subject=data['subject'],
            content=data['content']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            print(f"Failed to send email: {message}")  # Debug log
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        print(f"Error in send_email_api: {str(e)}")  # Debug log
        import traceback
        print(f"Traceback: {traceback.format_exc()}")  # Debug log
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        campaigns = email_sender.get_all_campaigns()
        return jsonify(campaigns)
    except Exception as e:
        print(f"Error getting campaigns: {e}")
        return jsonify([])

@app.route('/api/discover-businesses', methods=['GET'])
def discover_businesses():
    """
    Unified endpoint for business discovery
    """
    try:
        business_type = request.args.get('type')
        location = request.args.get('location')
        radius = int(request.args.get('radius', 50))  # Default radius of 50 km
        
        if not business_type or not location:
            return jsonify({
                'success': False,
                'error': 'Business type and location are required'
            }), 400
        
        # Log the search request
        logger.info(f"Searching for {business_type} businesses in {location} within {radius}km radius")
        
        # Check if we have any API clients configured
        if not Config.get_google_api_key() and not Config.get_yelp_api_key():
            return jsonify({
                'success': False,
                'error': 'No API keys configured. Please check server configuration.'
            }), 500
        
        # Use the business discovery engine to search
        businesses = business_discovery.discover_businesses_sync(location, business_type, radius)
        
        logger.info(f"Found {len(businesses)} businesses")
        
        return jsonify({
            'success': True,
            'businesses': businesses
        })
        
    except Exception as e:
        logger.error(f"Error in discover_businesses: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Failed to search businesses: {str(e)}"
        }), 500

@app.route('/api/search-businesses', methods=['GET'])
def search_businesses():
    try:
        business_type = request.args.get('type')
        location = request.args.get('location')
        radius = request.args.get('radius', 50)  # Default radius of 50 km
        
        if not business_type or not location:
            return jsonify({
                'success': False,
                'error': 'Business type and location are required'
            }), 400
        
        # Log the search request
        print(f"Searching for {business_type} businesses in {location} within {radius}km radius")
        
        # Use the business discovery engine to search
        businesses = business_discovery.discover_businesses_sync(location, business_type, radius)
        
        print(f"Found {len(businesses)} businesses")
        
        return jsonify({
            'success': True,
            'businesses': businesses
        })
        
    except Exception as e:
        print(f"Error in search_businesses: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Failed to search businesses: {str(e)}"
        }), 500

@app.route('/api/check-websites', methods=['POST'])
async def check_websites():
    try:
        data = request.json
        businesses = data.get('businesses', [])
        
        # Check websites in parallel
        tasks = []
        for business in businesses:
            if business.get('website'):
                task = asyncio.create_task(website_checker.check_website(business['website']))
                tasks.append((business, task))

        # Wait for all checks to complete
        for business, task in tasks:
            result = await task
            business['has_website'] = result.exists
            business['website_status'] = result.status

        return jsonify(businesses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/enrich-data', methods=['POST'])
async def enrich_data():
    try:
        data = request.json
        businesses = data.get('businesses', [])
        
        # Enrich business data
        enriched_businesses = []
        for business in businesses:
            # Skip if already enriched
            if business.get('enriched'):
                enriched_businesses.append(business)
                continue

            # Enrich missing contact information
            if not business.get('email'):
                business['email'] = await business_discovery.find_email(business)
            if not business.get('phone'):
                business['phone'] = await business_discovery.find_phone(business)
            
            business['enriched'] = True
            enriched_businesses.append(business)

        return jsonify(enriched_businesses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-leads', methods=['POST'])
async def export_leads():
    try:
        data = request.json
        businesses = data.get('businesses', [])
        
        # Export to CRM
        exported_count = await crm_integration.export_leads(businesses)
        
        # Create email campaign
        campaign_id = await email_manager.create_campaign(businesses)
        
        return jsonify({
            'count': exported_count,
            'campaign_id': campaign_id,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(port=Config.PORT, debug=Config.DEBUG)
