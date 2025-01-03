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

Dependencies:
- Flask for web framework
- SendGrid for email delivery
- python-dotenv for environment variables

Author: Oscar Hernandez
Date: January 2025
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from lead_finder import LeadFinder
from email_sender import EmailSender
from campaign_handler import campaign_bp
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(campaign_bp)

# Initialize services
lead_finder = LeadFinder()
email_sender = EmailSender()

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        campaigns = email_sender.get_all_campaigns()
        return jsonify(campaigns)
    except Exception as e:
        print(f"Error getting campaigns: {e}")
        return jsonify([])

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, port=5003)
