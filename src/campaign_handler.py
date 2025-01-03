from flask import Blueprint, jsonify
from email_sender import EmailSender
from lead_finder import LeadFinder
import traceback

campaign_bp = Blueprint('campaign', __name__)
email_sender = EmailSender()
lead_finder = LeadFinder()

@campaign_bp.route('/api/campaign/start', methods=['POST'])
def start_campaign():
    try:
        print("Starting campaign...")
        
        # Get active leads
        leads = lead_finder.get_all_leads()
        print(f"Found {len(leads) if leads else 0} leads")
        
        if not leads:
            print("No active leads found")
            return jsonify({
                'success': False,
                'error': 'No active leads found. Please find leads first.'
            })

        # Get active template
        template = email_sender.get_active_template()
        print(f"Template found: {bool(template)}")
        
        if not template:
            print("No active template found")
            return jsonify({
                'success': False,
                'error': 'No active template found. Please create a template first.'
            })

        # Start the campaign
        campaign_id = email_sender.start_campaign(leads, template)
        print(f"Campaign started with ID: {campaign_id}")
        
        return jsonify({
            'success': True,
            'message': 'Campaign started successfully',
            'campaign_id': campaign_id
        })

    except Exception as e:
        print(f"Error starting campaign: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Failed to start campaign. Please try again.'
        })
