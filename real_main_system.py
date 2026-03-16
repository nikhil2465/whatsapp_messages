#!/usr/bin/env python3
"""
🚀 PROFESSIONAL WHATSAPP BUSINESS SYSTEM
====================================
✅ Real WhatsApp Business API integration
✅ Automated replies for +8861655542
✅ Bulk messaging with anti-blocking measures
✅ Google Sheets/Drive integration
✅ Fallback to WhatsApp Web if API not configured
✅ Professional features: Contacts, Templates, Scheduling
✅ Enhanced dashboard with modern UI
"""

import os
import sys
import json
import time
import logging
import sqlite3
import threading
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Import our real messaging API system
from whatsapp_real_messaging import WhatsAppRealMessaging
from professional_features import ProfessionalFeatures

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/real_system.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class ProfessionalMainSystem:
    """
    Professional WhatsApp Business System with Enhanced Features
    Includes contact management, templates, scheduling, and modern UI
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize the real WhatsApp API
        self.whatsapp_api = WhatsAppRealMessaging()
        
        # Initialize professional features
        self.professional_features = ProfessionalFeatures(self.whatsapp_api.conn)
        
        # Setup routes
        self.setup_routes()
        
        # Setup professional dashboard
        self.setup_professional_dashboard()
        
        log.info("🚀 Professional WhatsApp Business System Initialized")
        log.info(f"📱 Business Number: {self.whatsapp_api.config['BUSINESS_PHONE']}")
        log.info(f"🤖 Auto-replies: {'Enabled' if self.whatsapp_api.config['AUTO_REPLY_ENABLED'] else 'Disabled'}")
        log.info(f"📊 Google Sheets: {'Enabled' if self.whatsapp_api.config['GOOGLE_ENABLED'] else 'Disabled'}")
        log.info(f"🔗 API Status: {'Configured' if self.whatsapp_api.api_configured else 'Using WhatsApp Web fallback'}")
        log.info("✅ Professional features and enhanced UI ready")
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard"""
            return self.dashboard_html
        
        @self.app.route('/api/send-single', methods=['POST'])
        def send_single_message():
            """Send a single WhatsApp message"""
            try:
                # Handle both JSON and multipart form data
                if request.content_type.startswith('multipart/form-data'):
                    recipient = request.form.get('recipient')
                    message = request.form.get('message')
                    attachment_file = request.files.get('attachment')
                    
                    # Process attachment if provided
                    attachment_data = None
                    if attachment_file and attachment_file.filename:
                        file_data = attachment_file.read()
                        attachment_data = self.whatsapp_api.process_attachment(file_data, attachment_file.filename)
                        if attachment_data:
                            attachment_data = self.whatsapp_api.prepare_attachment_for_api(attachment_data)
                else:
                    data = request.get_json()
                    recipient = data.get('recipient')
                    message = data.get('message')
                    attachment_data = None
                
                if not recipient or not message:
                    return jsonify({
                        'success': False,
                        'error': 'Recipient and message are required'
                    }), 400
                
                result = self.whatsapp_api.send_whatsapp_message(recipient, message, attachment_data=attachment_data)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Send single message error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/send-bulk', methods=['POST'])
        def send_bulk_messages():
            """Send bulk WhatsApp messages"""
            try:
                # Handle both JSON and multipart form data
                if request.content_type.startswith('multipart/form-data'):
                    recipients_str = request.form.get('recipients', '')
                    message = request.form.get('message')
                    campaign_name = request.form.get('campaign_name', 'Bulk Campaign')
                    attachment_file = request.files.get('attachment')
                    
                    # Parse recipients
                    recipients = [r.strip() for r in recipients_str.split(',') if r.strip()]
                    
                    # Process attachment if provided
                    attachment_data = None
                    if attachment_file and attachment_file.filename:
                        file_data = attachment_file.read()
                        attachment_data = self.whatsapp_api.process_attachment(file_data, attachment_file.filename)
                        if attachment_data:
                            attachment_data = self.whatsapp_api.prepare_attachment_for_api(attachment_data)
                else:
                    data = request.get_json()
                    recipients = data.get('recipients', [])
                    message = data.get('message')
                    campaign_name = data.get('campaign_name', 'Bulk Campaign')
                    attachment_data = None
                
                if not recipients or not message:
                    return jsonify({
                        'success': False,
                        'error': 'Recipients list and message are required'
                    }), 400
                
                # Validate recipients
                if len(recipients) > 1000:
                    return jsonify({
                        'success': False,
                        'error': 'Maximum 1000 recipients per campaign'
                    }), 400
                
                result = self.whatsapp_api.send_bulk_messages(recipients, message, campaign_name)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Send bulk messages error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/attachment/<attachment_id>', methods=['GET'])
        def serve_attachment(attachment_id):
            """Serve attachment file"""
            try:
                cursor = self.whatsapp_api.conn.cursor()
                cursor.execute('SELECT * FROM attachments WHERE attachment_id = ?', (attachment_id,))
                attachment = cursor.fetchone()
                
                if not attachment:
                    return jsonify({'error': 'Attachment not found'}), 404
                
                file_path = attachment['file_path']
                if not os.path.exists(file_path):
                    return jsonify({'error': 'File not found'}), 404
                
                return send_file(file_path, as_attachment=True, download_name=attachment['filename'])
                
            except Exception as e:
                log.error(f"Serve attachment error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/upload-attachment', methods=['POST'])
        def upload_attachment():
            """Upload attachment file and return attachment info"""
            try:
                if 'file' not in request.files:
                    return jsonify({'success': False, 'error': 'No file provided'}), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'success': False, 'error': 'No file selected'}), 400
                
                # Process attachment
                file_data = file.read()
                attachment_info = self.whatsapp_api.process_attachment(file_data, file.filename)
                
                if attachment_info:
                    return jsonify({
                        'success': True,
                        'attachment': attachment_info
                    })
                else:
                    return jsonify({'success': False, 'error': 'Failed to process attachment'}), 500
                    
            except Exception as e:
                log.error(f"Upload attachment error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/campaigns', methods=['GET'])
        def get_campaigns():
            """Get all campaigns"""
            try:
                cursor = self.whatsapp_api.conn.cursor()
                cursor.execute('SELECT * FROM bulk_campaigns ORDER BY created_at DESC')
                campaigns = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'campaigns': campaigns
                })
                
            except Exception as e:
                log.error(f"Get campaigns error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/campaign/<campaign_id>', methods=['GET'])
        def get_campaign_details(campaign_id):
            """Get specific campaign details"""
            try:
                campaign = self.whatsapp_api.get_campaign_status(campaign_id)
                if campaign:
                    return jsonify({'success': True, 'campaign': campaign})
                else:
                    return jsonify({'success': False, 'error': 'Campaign not found'}), 404
                    
            except Exception as e:
                log.error(f"Get campaign details error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/messages', methods=['GET'])
        def get_messages():
            """Get message history"""
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                
                cursor = self.whatsapp_api.conn.cursor()
                cursor.execute('''
                    SELECT * FROM messages 
                    ORDER BY created_at DESC 
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
                messages = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'messages': messages,
                    'total': len(messages)
                })
                
            except Exception as e:
                log.error(f"Get messages error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get system statistics"""
            try:
                stats = self.whatsapp_api.get_message_stats()
                
                # Add additional stats
                cursor = self.whatsapp_api.conn.cursor()
                
                # Active campaigns
                cursor.execute('SELECT COUNT(*) FROM bulk_campaigns WHERE status = "running"')
                active_campaigns = cursor.fetchone()[0]
                
                # Today's campaigns
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('SELECT COUNT(*) FROM bulk_campaigns WHERE DATE(created_at) = ?', (today,))
                today_campaigns = cursor.fetchone()[0]
                
                stats.update({
                    'active_campaigns': active_campaigns,
                    'today_campaigns': today_campaigns,
                    'rate_limit_status': {
                        'per_minute': f"{self.whatsapp_api.rate_limiter.messages_sent['minute']}/{self.whatsapp_api.config['MESSAGES_PER_MINUTE']}",
                        'per_hour': f"{self.whatsapp_api.rate_limiter.messages_sent['hour']}/{self.whatsapp_api.config['MESSAGES_PER_HOUR']}",
                        'per_day': f"{self.whatsapp_api.rate_limiter.messages_sent['day']}/{self.whatsapp_api.config['MESSAGES_PER_DAY']}"
                    }
                })
                
                return jsonify({
                    'success': True,
                    'stats': stats
                })
                
            except Exception as e:
                log.error(f"Get stats error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/test-auto-reply', methods=['POST'])
        def test_auto_reply():
            """Test auto-reply functionality"""
            try:
                data = request.get_json()
                sender = data.get('sender', '+1234567890')
                message = data.get('message', 'Hello, I need help')
                
                result = self.whatsapp_api.process_incoming_message(sender, message)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Test auto-reply error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """System health check"""
            try:
                health = {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'services': {
                        'database': True,
                        'rate_limiter': True,
                        'google_integration': self.whatsapp_api.config['GOOGLE_ENABLED'],
                        'auto_reply': self.whatsapp_api.config['AUTO_REPLY_ENABLED'],
                        'whatsapp_api': self.whatsapp_api.api_configured,
                        'web_fallback': self.whatsapp_api.config['USE_WHATSAPP_WEB_FALLBACK']
                    },
                    'config': {
                        'business_phone': self.whatsapp_api.config['BUSINESS_PHONE'],
                        'auto_reply_enabled': self.whatsapp_api.config['AUTO_REPLY_ENABLED'],
                        'google_enabled': self.whatsapp_api.config['GOOGLE_ENABLED'],
                        'api_configured': self.whatsapp_api.api_configured,
                        'delivery_methods': {
                            'api_available': self.whatsapp_api.api_configured,
                            'web_fallback': self.whatsapp_api.config['USE_WHATSAPP_WEB_FALLBACK']
                        },
                        'rate_limits': {
                            'per_minute': self.whatsapp_api.config['MESSAGES_PER_MINUTE'],
                            'per_hour': self.whatsapp_api.config['MESSAGES_PER_HOUR'],
                            'per_day': self.whatsapp_api.config['MESSAGES_PER_DAY']
                        }
                    }
                }
                
                return jsonify(health)
                
            except Exception as e:
                log.error(f"Health check error: {e}")
                return jsonify({
                    'status': 'unhealthy',
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/export-google-sheets', methods=['GET'])
        def export_google_sheets():
            """Export messages to Google Sheets CSV"""
            try:
                csv_file = os.path.join('exports', self.whatsapp_api.config['GOOGLE_SHEET_FILE'])
                if os.path.exists(csv_file):
                    return send_file(csv_file, as_attachment=True, download_name='whatsapp_messages.csv')
                else:
                    return jsonify({'success': False, 'error': 'No data to export'}), 404
                    
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/configure-api', methods=['POST'])
        def configure_api():
            """Configure WhatsApp Business API"""
            try:
                data = request.get_json()
                access_token = data.get('access_token')
                phone_number_id = data.get('phone_number_id')
                
                if not access_token or not phone_number_id:
                    return jsonify({
                        'success': False,
                        'error': 'Access token and phone number ID required'
                    }), 400
                
                # Update environment variables (in memory)
                self.whatsapp_api.config['WHATSAPP_ACCESS_TOKEN'] = access_token
                self.whatsapp_api.config['WHATSAPP_PHONE_NUMBER_ID'] = phone_number_id
                
                # Re-check API configuration
                self.whatsapp_api.api_configured = self.whatsapp_api.check_api_configuration()
                
                return jsonify({
                    'success': True,
                    'message': 'API configuration updated',
                    'api_configured': self.whatsapp_api.api_configured
                })
                
            except Exception as e:
                log.error(f"Configure API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # Include the webhook from the real API
        @self.app.route('/webhook/whatsapp', methods=['POST'])
        def whatsapp_webhook():
            """Handle incoming WhatsApp messages"""
            try:
                data = request.get_json()
                
                # Handle webhook verification
                if request.args.get('hub.mode') == 'subscribe':
                    return jsonify({
                        'hub.challenge': request.args.get('hub.challenge')
                    })
                
                # Process incoming messages
                if data and 'entry' in data:
                    for entry in data['entry']:
                        for change in entry.get('changes', []):
                            if 'messages' in change.get('value', {}):
                                messages = change['value']['messages']
                                for message in messages:
                                    if message.get('type') == 'text':
                                        sender = message.get('from')
                                        text = message.get('text', {}).get('body', '')
                                        message_id = message.get('id')
                                        
                                        # Process incoming message
                                        result = self.whatsapp_api.process_incoming_message(sender, text, message_id)
                                        
                                        if not result['success']:
                                            log.error(f"Webhook processing failed: {result['error']}")
                
                return jsonify(result), 200 if result.get('success') else 500
                
            except Exception as e:
                log.error(f"Webhook error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # Professional Features API Endpoints
        
        @self.app.route('/api/contacts', methods=['GET', 'POST'])
        def manage_contacts():
            """Manage contacts"""
            try:
                if request.method == 'GET':
                    segment = request.args.get('segment')
                    limit = int(request.args.get('limit', 50))
                    offset = int(request.args.get('offset', 0))
                    
                    result = self.professional_features.get_contacts(segment, limit, offset)
                    return jsonify(result)
                
                elif request.method == 'POST':
                    data = request.get_json()
                    name = data.get('name')
                    phone = data.get('phone')
                    email = data.get('email')
                    company = data.get('company')
                    tags = data.get('tags', [])
                    segment = data.get('segment')
                    
                    if not name or not phone:
                        return jsonify({'success': False, 'error': 'Name and phone required'}), 400
                    
                    result = self.professional_features.add_contact(name, phone, email, company, tags, segment)
                    return jsonify(result)
                    
            except Exception as e:
                log.error(f"Contacts API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/templates', methods=['GET', 'POST'])
        def manage_templates():
            """Manage message templates"""
            try:
                if request.method == 'GET':
                    category = request.args.get('category')
                    result = self.professional_features.get_templates(category)
                    return jsonify(result)
                
                elif request.method == 'POST':
                    data = request.get_json()
                    name = data.get('name')
                    category = data.get('category')
                    content = data.get('content')
                    variables = data.get('variables', [])
                    
                    if not name or not content:
                        return jsonify({'success': False, 'error': 'Name and content required'}), 400
                    
                    result = self.professional_features.create_template(name, category, content, variables)
                    return jsonify(result)
                    
            except Exception as e:
                log.error(f"Templates API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/schedule-message', methods=['POST'])
        def schedule_message():
            """Schedule a message"""
            try:
                data = request.get_json()
                recipient = data.get('recipient')
                message = data.get('message')
                scheduled_time = data.get('scheduled_time')
                template_id = data.get('template_id')
                attachment_path = data.get('attachment_path')
                
                if not recipient or not message or not scheduled_time:
                    return jsonify({'success': False, 'error': 'Recipient, message, and scheduled time required'}), 400
                
                result = self.professional_features.schedule_message(recipient, message, scheduled_time, template_id, attachment_path)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Schedule message API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/quick-replies', methods=['GET', 'POST'])
        def manage_quick_replies():
            """Manage quick replies"""
            try:
                if request.method == 'GET':
                    category = request.args.get('category')
                    result = self.professional_features.get_quick_replies(category)
                    return jsonify(result)
                
                elif request.method == 'POST':
                    data = request.get_json()
                    keyword = data.get('keyword')
                    message = data.get('message')
                    category = data.get('category', 'general')
                    
                    if not keyword or not message:
                        return jsonify({'success': False, 'error': 'Keyword and message required'}), 400
                    
                    result = self.professional_features.add_quick_reply(keyword, message, category)
                    return jsonify(result)
                    
            except Exception as e:
                log.error(f"Quick replies API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/segments', methods=['GET', 'POST'])
        def manage_segments():
            """Manage customer segments"""
            try:
                if request.method == 'POST':
                    data = request.get_json()
                    name = data.get('name')
                    description = data.get('description')
                    criteria = data.get('criteria', {})
                    
                    if not name:
                        return jsonify({'success': False, 'error': 'Name required'}), 400
                    
                    result = self.professional_features.create_segment(name, description, criteria)
                    return jsonify(result)
                    
            except Exception as e:
                log.error(f"Segments API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/analytics', methods=['GET'])
        def get_analytics():
            """Get analytics data"""
            try:
                metric_type = request.args.get('metric_type', 'all')
                days = int(request.args.get('days', 7))
                
                result = self.professional_features.get_analytics(metric_type, days)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Analytics API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/dashboard-analytics', methods=['GET'])
        def get_dashboard_analytics():
            """Get comprehensive dashboard analytics"""
            try:
                result = self.professional_features.get_dashboard_analytics()
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Dashboard analytics API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/search-contacts', methods=['GET'])
        def search_contacts():
            """Search contacts"""
            try:
                query = request.args.get('query', '')
                
                if not query:
                    return jsonify({'success': False, 'error': 'Search query required'}), 400
                
                result = self.professional_features.search_contacts(query)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Search contacts API error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def setup_professional_dashboard(self):
        """Setup the professional HTML dashboard"""
        # Read the enhanced dashboard HTML
        try:
            with open('enhanced_dashboard.html', 'r', encoding='utf-8') as f:
                self.dashboard_html = f.read()
            log.info("✅ Professional dashboard loaded from enhanced_dashboard.html")
            log.info(f"📄 Dashboard HTML length: {len(self.dashboard_html)} characters")
        except FileNotFoundError:
            log.warning("⚠️ Enhanced dashboard file not found, using fallback")
            self.setup_fallback_dashboard()
    
    def setup_fallback_dashboard(self):
        """Setup fallback dashboard if enhanced file not found"""
        self.dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Professional WhatsApp Business System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #25D366;
            --primary-dark: #128C7E;
            --secondary: #075E54;
            --success: #00C851;
            --danger: #FF4444;
            --warning: #FF8800;
            --info: #33B5E5;
            --light: #F8F9FA;
            --dark: #2C3E50;
            --white: #FFFFFF;
            --gray: #6C757D;
            --border: #E9ECEF;
            --shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            color: var(--dark);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: var(--white);
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: var(--shadow);
        }

        .header h1 {
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--white);
            padding: 30px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--primary-dark));
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .stat-icon {
            font-size: 3em;
            color: var(--primary);
            margin-bottom: 15px;
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 5px;
        }

        .stat-label {
            color: var(--gray);
            font-size: 1.1em;
            font-weight: 500;
        }

        .section {
            background: var(--white);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
        }

        .section h2 {
            color: var(--dark);
            margin-bottom: 25px;
            font-size: 1.8em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section h2 i {
            color: var(--primary);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
        }

        .form-control {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 211, 102, 0.1);
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: var(--white);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3);
        }

        .btn-secondary {
            background: var(--gray);
            color: var(--white);
        }

        .btn-success {
            background: var(--success);
            color: var(--white);
        }

        .btn-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .alert {
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .alert-success {
            background: rgba(0, 200, 81, 0.1);
            color: var(--success);
            border: 1px solid rgba(0, 200, 81, 0.3);
        }

        .alert-danger {
            background: rgba(255, 68, 68, 0.1);
            color: var(--danger);
            border: 1px solid rgba(255, 68, 68, 0.3);
        }

        .alert-warning {
            background: rgba(255, 136, 0, 0.1);
            color: var(--warning);
            border: 1px solid rgba(255, 136, 0, 0.3);
        }

        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid var(--border);
        }

        .tab {
            padding: 12px 20px;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            font-weight: 500;
            color: var(--gray);
            transition: all 0.3s ease;
        }

        .tab:hover {
            color: var(--primary);
        }

        .tab.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        .table th {
            background: var(--light);
            font-weight: 600;
            color: var(--dark);
        }

        .badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }

        .badge-success {
            background: var(--success);
            color: var(--white);
        }

        .badge-warning {
            background: var(--warning);
            color: var(--white);
        }

        .badge-info {
            background: var(--info);
            color: var(--white);
        }

        .loading {
            text-align: center;
            padding: 40px;
        }

        .spinner {
            border: 4px solid var(--border);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .feature-card {
            background: var(--light);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
        }

        .feature-card h4 {
            color: var(--primary);
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fab fa-whatsapp"></i> Professional WhatsApp Business System</h1>
            <p>Advanced Customer Communication Platform with Enterprise Features</p>
        </div>
        
        <div id="alerts"></div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-comments"></i>
                </div>
                <div class="stat-number" id="total-messages">0</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-paper-plane"></i>
                </div>
                <div class="stat-number" id="sent-messages">0</div>
                <div class="stat-label">Messages Sent</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-download"></i>
                </div>
                <div class="stat-number" id="received-messages">0</div>
                <div class="stat-label">Messages Received</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-number" id="active-campaigns">0</div>
                <div class="stat-label">Active Campaigns</div>
            </div>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-paper-plane"></i> Send Message</h2>
            <div class="tabs">
                <button class="tab active" onclick="showTab('single-message')">Single Message</button>
                <button class="tab" onclick="showTab('bulk-message')">Bulk Message</button>
                <button class="tab" onclick="showTab('scheduled-message')">Scheduled Message</button>
            </div>
            
            <div id="single-message-tab" class="tab-content active">
                <div class="form-group">
                    <label class="form-label">Recipient Phone Number</label>
                    <input type="text" id="single-recipient" class="form-control" placeholder="+1234567890">
                </div>
                <div class="form-group">
                    <label class="form-label">Message</label>
                    <textarea id="single-message" class="form-control" rows="4" placeholder="Enter your message here..."></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Attachment (Optional)</label>
                    <input type="file" id="single-attachment" class="form-control" accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx">
                    <small>Supported: Images, Videos, Audio, PDF, Documents (Max 10MB)</small>
                </div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="sendSingleMessage()">
                        <i class="fas fa-paper-plane"></i> Send Message
                    </button>
                    <button class="btn btn-success" onclick="saveTemplate()">
                        <i class="fas fa-save"></i> Save as Template
                    </button>
                </div>
            </div>
            
            <div id="bulk-message-tab" class="tab-content">
                <div class="form-group">
                    <label class="form-label">Recipients (comma-separated)</label>
                    <textarea id="bulk-recipients" class="form-control" rows="3" placeholder="+1234567890,+9876543210,+1122334455"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Message</label>
                    <textarea id="bulk-message" class="form-control" rows="4" placeholder="Enter your bulk message here..."></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Attachment (Optional)</label>
                    <input type="file" id="bulk-attachment" class="form-control" accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx">
                    <small>Same attachment will be sent to all recipients (Max 10MB)</small>
                </div>
                <div class="form-group">
                    <label class="form-label">Campaign Name</label>
                    <input type="text" id="campaign-name" class="form-control" placeholder="My Campaign">
                </div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="sendBulkMessages()">
                        <i class="fas fa-bullhorn"></i> Send Bulk Messages
                    </button>
                    <button class="btn btn-secondary" onclick="previewBulkMessage()">
                        <i class="fas fa-eye"></i> Preview
                    </button>
                </div>
            </div>
            
            <div id="scheduled-message-tab" class="tab-content">
                <div class="form-group">
                    <label class="form-label">Schedule Date & Time</label>
                    <input type="datetime-local" id="schedule-datetime" class="form-control">
                </div>
                <div class="form-group">
                    <label class="form-label">Recipients</label>
                    <textarea id="scheduled-recipients" class="form-control" rows="3" placeholder="+1234567890,+9876543210"></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Message</label>
                    <textarea id="scheduled-message" class="form-control" rows="4" placeholder="Enter your message here..."></textarea>
                </div>
                <div class="btn-group">
                    <button class="btn btn-warning" onclick="scheduleMessage()">
                        <i class="fas fa-clock"></i> Schedule Message
                    </button>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-chart-line"></i> Professional Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4><i class="fas fa-address-book"></i> Contact Management</h4>
                    <p>Organize your contacts with tags, segments, and detailed profiles</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-file-alt"></i> Message Templates</h4>
                    <p>Create reusable message templates with variables for personalization</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-clock"></i> Scheduled Messages</h4>
                    <p>Schedule messages to be sent at specific times automatically</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-bolt"></i> Quick Replies</h4>
                    <p>Set up quick replies for common questions and responses</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-users"></i> Customer Segmentation</h4>
                    <p>Segment your customers based on criteria for targeted messaging</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-chart-bar"></i> Advanced Analytics</h4>
                    <p>Track engagement, delivery rates, and customer behavior</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-cog"></i> API Configuration</h2>
            <div class="form-group">
                <label class="form-label">Access Token</label>
                <input type="password" id="access-token" class="form-control" placeholder="Enter WhatsApp Business API access token">
            </div>
            <div class="form-group">
                <label class="form-label">Phone Number ID</label>
                <input type="text" id="phone-number-id" class="form-control" placeholder="Enter WhatsApp Business phone number ID">
            </div>
            <div class="btn-group">
                <button class="btn btn-primary" onclick="configureAPI()">
                    <i class="fas fa-save"></i> Configure API
                </button>
                <button class="btn btn-secondary" onclick="checkHealth()">
                    <i class="fas fa-heartbeat"></i> Check Status
                </button>
            </div>
        </div>
        
        <div class="section">
            <h2><i class="fas fa-history"></i> Recent Messages</h2>
            <div id="messages-list">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading messages...</p>
                </div>
            </div>
            <button class="btn btn-secondary" onclick="loadMessages()">Refresh Messages</button>
        </div>
    </div>

    <script>
        let currentTab = 'single-message';

        function showTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(el => {
                el.classList.remove('active');
            });
            
            document.getElementById(tab + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            currentTab = tab;
        }

        function showAlert(message, type = 'info') {
            const alertsContainer = document.getElementById('alerts');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                ${message}
            `;
            alertsContainer.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }

        function sendSingleMessage() {
            const recipient = document.getElementById('single-recipient').value;
            const message = document.getElementById('single-message').value;
            const attachmentFile = document.getElementById('single-attachment').files[0];
            
            if (!recipient || !message) {
                showAlert('Please fill in all required fields', 'error');
                return;
            }
            
            const formData = new FormData();
            formData.append('recipient', recipient);
            formData.append('message', message);
            if (attachmentFile) {
                formData.append('attachment', attachmentFile);
            }
            
            fetch('/api/send-single', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Message sent successfully!', 'success');
                    document.getElementById('single-recipient').value = '';
                    document.getElementById('single-message').value = '';
                    document.getElementById('single-attachment').value = '';
                    loadStats();
                    loadMessages();
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            });
        }

        function sendBulkMessages() {
            const recipients = document.getElementById('bulk-recipients').value;
            const message = document.getElementById('bulk-message').value;
            const campaignName = document.getElementById('campaign-name').value;
            const attachmentFile = document.getElementById('bulk-attachment').files[0];
            
            if (!recipients || !message) {
                showAlert('Please fill in recipients and message', 'error');
                return;
            }
            
            const formData = new FormData();
            formData.append('recipients', recipients);
            formData.append('message', message);
            formData.append('campaign_name', campaignName || 'Bulk Campaign');
            if (attachmentFile) {
                formData.append('attachment', attachmentFile);
            }
            
            fetch('/api/send-bulk', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Bulk campaign started successfully!', 'success');
                    document.getElementById('bulk-recipients').value = '';
                    document.getElementById('bulk-message').value = '';
                    document.getElementById('campaign-name').value = '';
                    document.getElementById('bulk-attachment').value = '';
                    loadStats();
                    loadMessages();
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            });
        }

        function scheduleMessage() {
            const scheduledTime = document.getElementById('schedule-datetime').value;
            const recipients = document.getElementById('scheduled-recipients').value;
            const message = document.getElementById('scheduled-message').value;
            
            if (!scheduledTime || !recipients || !message) {
                showAlert('Please fill in all fields', 'error');
                return;
            }
            
            fetch('/api/schedule-message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    recipients: recipients.split(',').map(r => r.trim()),
                    message: message,
                    scheduled_time: scheduledTime
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Message scheduled successfully!', 'success');
                    document.getElementById('schedule-datetime').value = '';
                    document.getElementById('scheduled-recipients').value = '';
                    document.getElementById('scheduled-message').value = '';
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            });
        }

        function configureAPI() {
            const accessToken = document.getElementById('access-token').value;
            const phoneNumberId = document.getElementById('phone-number-id').value;
            
            if (!accessToken || !phoneNumberId) {
                showAlert('Please fill in both access token and phone number ID', 'error');
                return;
            }
            
            fetch('/api/configure-api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    access_token: accessToken,
                    phone_number_id: phoneNumberId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('API configuration updated successfully!', 'success');
                    document.getElementById('access-token').value = '';
                    document.getElementById('phone-number-id').value = '';
                    checkHealth();
                } else {
                    showAlert('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('Network error: ' + error, 'error');
            });
        }

        function checkHealth() {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'healthy') {
                        let healthInfo = '✅ System Status: Healthy<br>';
                        healthInfo += `📱 Business Phone: ${data.config.business_phone}<br>`;
                        healthInfo += `🤖 Auto-reply: ${data.config.auto_reply_enabled ? 'Enabled' : 'Disabled'}<br>`;
                        healthInfo += `📊 Google Integration: ${data.config.google_enabled ? 'Enabled' : 'Disabled'}<br>`;
                        healthInfo += `🔗 WhatsApp API: ${data.config.api_configured ? 'Configured' : 'Using WhatsApp Web fallback'}`;
                        
                        showAlert(healthInfo, 'success');
                    } else {
                        showAlert('❌ System Status: Unhealthy - ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showAlert('❌ Health check failed: ' + error, 'error');
                });
        }

        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const stats = data.stats;
                        document.getElementById('total-messages').textContent = stats.total_messages || 0;
                        document.getElementById('sent-messages').textContent = stats.sent_messages || 0;
                        document.getElementById('received-messages').textContent = stats.received_messages || 0;
                        document.getElementById('active-campaigns').textContent = stats.active_campaigns || 0;
                    }
                })
                .catch(error => console.error('Stats load error:', error));
        }

        function loadMessages() {
            fetch('/api/messages?limit=20')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let html = '<table class="table"><thead><tr><th>Direction</th><th>Contact</th><th>Message</th><th>Status</th><th>Time</th></tr></thead><tbody>';
                        
                        data.messages.forEach(message => {
                            const messagePreview = message.message.length > 50 ? 
                                message.message.substring(0, 50) + '...' : message.message;
                            
                            html += `<tr>
                                <td><span class="badge badge-${message.direction === 'OUT' ? 'success' : 'info'}">${message.direction}</span></td>
                                <td>${message.direction === 'OUT' ? message.recipient : message.sender}</td>
                                <td>${messagePreview}</td>
                                <td><span class="badge badge-${message.status === 'sent' ? 'success' : 'warning'}">${message.status}</span></td>
                                <td>${new Date(message.created_at).toLocaleString()}</td>
                            </tr>`;
                        });
                        
                        html += '</tbody></table>';
                        document.getElementById('messages-list').innerHTML = html;
                    } else {
                        document.getElementById('messages-list').innerHTML = '<p>Error loading messages</p>';
                    }
                })
                .catch(error => {
                    document.getElementById('messages-list').innerHTML = '<p>Error loading messages</p>';
                    console.error('Messages load error:', error);
                });
        }

        function saveTemplate() {
            showAlert('Template feature coming soon!', 'info');
        }

        function previewBulkMessage() {
            showAlert('Preview feature coming soon!', 'info');
        }

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadMessages();
        });
    </script>
</body>
</html>
        .rate-limits { background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .rate-limits h5 { color: #856404; margin-bottom: 10px; }
        .rate-item { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .loading { display: none; text-align: center; padding: 20px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #25D366; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .whatsapp-link { color: #25D366; text-decoration: none; font-weight: 500; }
        .whatsapp-link:hover { text-decoration: underline; }
        .delivery-method { padding: 2px 6px; border-radius: 3px; font-size: 0.8em; font-weight: 500; }
        .delivery-api { background: #28a745; color: white; }
        .delivery-web { background: #17a2b8; color: white; }
        .delivery-webhook { background: #6f42c1; color: white; }
        .note { background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 0.9em; color: #0066cc; }
        .api-config-section { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .api-config-section h5 { color: #495057; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Real WhatsApp Business System</h1>
            <p>Real API Integration • Automated Replies • Bulk Messaging • Google Sheets • Fallback Support</p>
            <div class="api-status" id="api-status">
                <div id="api-status-content">Checking API configuration...</div>
            </div>
        </div>
        
        <div id="alerts"></div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number" id="total-messages">0</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="sent-messages">0</div>
                <div class="stat-label">Messages Sent</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="received-messages">0</div>
                <div class="stat-label">Messages Received</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="active-campaigns">0</div>
                <div class="stat-label">Active Campaigns</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔧 API Configuration</h2>
            <div class="api-config-section">
                <h5>Configure WhatsApp Business API for real messaging</h5>
                <div class="form-group">
                    <label for="access-token">Access Token</label>
                    <input type="password" id="access-token" class="form-control" placeholder="Enter your WhatsApp Business API access token">
                </div>
                <div class="form-group">
                    <label for="phone-number-id">Phone Number ID</label>
                    <input type="text" id="phone-number-id" class="form-control" placeholder="Enter your WhatsApp Business phone number ID">
                </div>
                <button onclick="configureAPI()" class="btn">Configure API</button>
                <button onclick="checkHealth()" class="btn btn-secondary">Check Status</button>
            </div>
            <div class="note">
                💡 Leave empty to use WhatsApp Web fallback (no registration required). Messages will be sent via real API when configured, otherwise WhatsApp Web links will be generated.
            </div>
        </div>
        
        <div class="section">
            <h2>📤 Send Single Message</h2>
            <div class="form-group">
                <label for="single-recipient">Recipient Phone Number</label>
                <input type="text" id="single-recipient" class="form-control" placeholder="+1234567890">
            </div>
            <div class="form-group">
                <label for="single-message">Message</label>
                <textarea id="single-message" class="form-control" rows="3" placeholder="Enter your message here..."></textarea>
            </div>
            <div class="form-group">
                <label for="single-attachment">Attachment (Optional)</label>
                <input type="file" id="single-attachment" class="form-control" accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx">
                <small>Supported: Images, Videos, Audio, PDF, Documents (Max 10MB)</small>
            </div>
            <button onclick="sendSingleMessage()" class="btn">Send Message</button>
        </div>
        
        <div class="section">
            <h2>📊 Send Bulk Messages</h2>
            <div class="form-group">
                <label for="bulk-recipients">Recipients (comma-separated)</label>
                <textarea id="bulk-recipients" class="form-control" rows="3" placeholder="+1234567890,+9876543210,+1122334455"></textarea>
            </div>
            <div class="form-group">
                <label for="bulk-message">Message</label>
                <textarea id="bulk-message" class="form-control" rows="3" placeholder="Enter your bulk message here..."></textarea>
            </div>
            <div class="form-group">
                <label for="bulk-attachment">Attachment (Optional)</label>
                <input type="file" id="bulk-attachment" class="form-control" accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx">
                <small>Same attachment will be sent to all recipients (Max 10MB)</small>
            </div>
            <div class="form-group">
                <label for="campaign-name">Campaign Name</label>
                <input type="text" id="campaign-name" class="form-control" placeholder="My Campaign">
            </div>
            <button onclick="sendBulkMessages()" class="btn">Send Bulk Messages</button>
        </div>
        
        <div class="section">
            <h2>🤖 Test Auto-Reply</h2>
            <div class="form-group">
                <label for="test-sender">Sender Phone Number</label>
                <input type="text" id="test-sender" class="form-control" placeholder="+1234567890">
            </div>
            <div class="form-group">
                <label for="test-message">Test Message</label>
                <input type="text" id="test-message" class="form-control" placeholder="Hello, I need help">
            </div>
            <button onclick="testAutoReply()" class="btn">Test Auto-Reply</button>
        </div>
        
        <div class="section">
            <h2>📈 System Status</h2>
            <div class="rate-limits">
                <h5>🛡️ Rate Limits (Anti-Blocking)</h5>
                <div class="rate-item">
                    <span>Per Minute:</span>
                    <span id="rate-minute">0/30</span>
                </div>
                <div class="rate-item">
                    <span>Per Hour:</span>
                    <span id="rate-hour">0/1000</span>
                </div>
                <div class="rate-item">
                    <span>Per Day:</span>
                    <span id="rate-day">0/10000</span>
                </div>
            </div>
            <button onclick="loadStats()" class="btn">Refresh Stats</button>
            <button onclick="checkHealth()" class="btn btn-secondary">Check Health</button>
            <button onclick="exportGoogleSheets()" class="btn btn-secondary">Export to Google Sheets</button>
        </div>
        
        <div class="section">
            <h2>📋 Recent Campaigns</h2>
            <div id="campaigns-list">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading campaigns...</p>
                </div>
            </div>
            <button onclick="loadCampaigns()" class="btn btn-secondary">Refresh Campaigns</button>
        </div>
        
        <div class="section">
            <h2>📱 Recent Messages</h2>
            <div id="messages-list">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading messages...</p>
                </div>
            </div>
            <button onclick="loadMessages()" class="btn btn-secondary">Refresh Messages</button>
        </div>
        
        <div class="section">
            <h2>✨ Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🤖 Automated Replies</h4>
                    <p>Intelligent auto-replies for incoming messages on +8861655542</p>
                </div>
                <div class="feature-card">
                    <h4>📊 Bulk Messaging</h4>
                    <p>Send real WhatsApp messages or generate links for thousands of customers</p>
                </div>
                <div class="feature-card">
                    <h4>📈 Google Sheets Integration</h4>
                    <p>Automatic CSV export for easy import to Google Sheets with duplicate prevention</p>
                </div>
                <div class="feature-card">
                    <h4>🛡️ Rate Limiting</h4>
                    <p>Advanced rate limiting to prevent WhatsApp account blocking</p>
                </div>
                <div class="feature-card">
                    <h4>📱 Real API + Fallback</h4>
                    <p>Uses real WhatsApp Business API when configured, falls back to WhatsApp Web</p>
                </div>
                <div class="feature-card">
                    <h4>📊 Analytics</h4>
                    <p>Real-time statistics and campaign monitoring with delivery method tracking</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load initial data
        loadStats();
        checkHealth();
        loadCampaigns();
        loadMessages();
        
        // Auto-refresh every 30 seconds
        setInterval(loadStats, 30000);
        setInterval(loadCampaigns, 60000);
        setInterval(loadMessages, 30000);
        
        function showAlert(message, type = 'info') {
            const alertsContainer = document.getElementById('alerts');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.innerHTML = message;
            alertsContainer.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
        
        function configureAPI() {
            const accessToken = document.getElementById('access-token').value;
            const phoneNumberId = document.getElementById('phone-number-id').value;
            
            if (!accessToken || !phoneNumberId) {
                showAlert('Please fill in both access token and phone number ID', 'error');
                return;
            }
            
            fetch('/api/configure-api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    access_token: accessToken,
                    phone_number_id: phoneNumberId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('✅ API configuration updated successfully!', 'success');
                    document.getElementById('access-token').value = '';
                    document.getElementById('phone-number-id').value = '';
                    checkHealth();
                } else {
                    showAlert('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('❌ Network error: ' + error, 'error');
            });
        }
        
        function sendSingleMessage() {
            const recipient = document.getElementById('single-recipient').value;
            const message = document.getElementById('single-message').value;
            const attachmentFile = document.getElementById('single-attachment').files[0];
            
            if (!recipient || !message) {
                showAlert('Please fill in all fields', 'error');
                return;
            }
            
            // Create FormData for file upload
            const formData = new FormData();
            formData.append('recipient', recipient);
            formData.append('message', message);
            if (attachmentFile) {
                formData.append('attachment', attachmentFile);
            }
            
            fetch('/api/send-single', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let alertHtml = `✅ Message sent successfully!<br>`;
                    alertHtml += `Delivery Method: <span class="delivery-method delivery-${data.delivery_method}">${data.delivery_method.toUpperCase()}</span><br>`;
                    if (data.whatsapp_link) {
                        alertHtml += `<a href="${data.whatsapp_link}" target="_blank" class="whatsapp-link">Click to send WhatsApp message</a>`;
                    }
                    if (attachmentFile) {
                        alertHtml += `<br>📎 Attachment: ${attachmentFile.name}`;
                    }
                    showAlert(alertHtml, 'success');
                    document.getElementById('single-recipient').value = '';
                    document.getElementById('single-message').value = '';
                    document.getElementById('single-attachment').value = '';
                    loadStats();
                    loadMessages();
                } else {
                    showAlert('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('❌ Network error: ' + error, 'error');
            });
        }
        
        function sendBulkMessages() {
            const recipients = document.getElementById('bulk-recipients').value;
            const message = document.getElementById('bulk-message').value;
            const campaignName = document.getElementById('campaign-name').value;
            const attachmentFile = document.getElementById('bulk-attachment').files[0];
            
            if (!recipients || !message) {
                showAlert('Please fill in recipients and message', 'error');
                return;
            }
            
            // Create FormData for file upload
            const formData = new FormData();
            formData.append('recipients', recipients);
            formData.append('message', message);
            formData.append('campaign_name', campaignName || 'Bulk Campaign');
            if (attachmentFile) {
                formData.append('attachment', attachmentFile);
            }
            
            fetch('/api/send-bulk', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let alertHtml = `✅ Bulk campaign started! Campaign ID: ${data.campaign_id}<br>`;
                    alertHtml += `API Configured: ${data.api_configured ? 'Yes' : 'No (using WhatsApp Web)'}<br>`;
                    if (attachmentFile) {
                        alertHtml += `📎 Attachment: ${attachmentFile.name}<br>`;
                    }
                    showAlert(alertHtml, 'success');
                    document.getElementById('bulk-recipients').value = '';
                    document.getElementById('bulk-message').value = '';
                    document.getElementById('campaign-name').value = '';
                    document.getElementById('bulk-attachment').value = '';
                    loadStats();
                    loadCampaigns();
                } else {
                    showAlert('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('❌ Network error: ' + error, 'error');
            });
        }
        
        function testAutoReply() {
            const sender = document.getElementById('test-sender').value;
            const message = document.getElementById('test-message').value;
            
            if (!sender || !message) {
                showAlert('Please fill in sender and message', 'error');
                return;
            }
            
            fetch('/api/test-auto-reply', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender, message})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let alertHtml = `✅ Auto-reply test successful!<br>`;
                    alertHtml += `Reply: ${data.auto_reply}<br>`;
                    if (data.auto_reply_result) {
                        alertHtml += `Delivery Method: <span class="delivery-method delivery-${data.auto_reply_result.delivery_method}">${data.auto_reply_result.delivery_method.toUpperCase()}</span>`;
                    }
                    showAlert(alertHtml, 'success');
                    loadStats();
                    loadMessages();
                } else {
                    showAlert('❌ Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showAlert('❌ Network error: ' + error, 'error');
            });
        }
        
        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const stats = data.stats;
                        document.getElementById('total-messages').textContent = stats.total_messages || 0;
                        document.getElementById('sent-messages').textContent = stats.sent_messages || 0;
                        document.getElementById('received-messages').textContent = stats.received_messages || 0;
                        document.getElementById('active-campaigns').textContent = stats.active_campaigns || 0;
                        
                        if (stats.rate_limit_status) {
                            document.getElementById('rate-minute').textContent = stats.rate_limit_status.per_minute;
                            document.getElementById('rate-hour').textContent = stats.rate_limit_status.per_hour;
                            document.getElementById('rate-day').textContent = stats.rate_limit_status.per_day;
                        }
                    }
                })
                .catch(error => console.error('Stats load error:', error));
        }
        
        function loadCampaigns() {
            const container = document.getElementById('campaigns-list');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading campaigns...</p></div>';
            
            fetch('/api/campaigns')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let html = '<table class="table"><thead><tr><th>Name</th><th>Status</th><th>Progress</th><th>Created</th></tr></thead><tbody>';
                        
                        data.campaigns.forEach(campaign => {
                            const progress = campaign.total_recipients > 0 ? 
                                (campaign.sent_count / campaign.total_recipients * 100) : 0;
                            
                            html += `<tr>
                                <td>${campaign.name}</td>
                                <td><span class="status-badge status-${campaign.status}">${campaign.status}</span></td>
                                <td>
                                    <div class="progress-bar">
                                        <div class="progress-fill" style="width: ${progress}%"></div>
                                    </div>
                                    ${campaign.sent_count}/${campaign.total_recipients}
                                </td>
                                <td>${new Date(campaign.created_at).toLocaleString()}</td>
                            </tr>`;
                        });
                        
                        html += '</tbody></table>';
                        container.innerHTML = html;
                    } else {
                        container.innerHTML = '<p>Error loading campaigns</p>';
                    }
                })
                .catch(error => {
                    container.innerHTML = '<p>Error loading campaigns</p>';
                    console.error('Campaigns load error:', error);
                });
        }
        
        function loadMessages() {
            const container = document.getElementById('messages-list');
            container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading messages...</p></div>';
            
            fetch('/api/messages?limit=20')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        let html = '<table class="table"><thead><tr><th>Direction</th><th>Contact</th><th>Message</th><th>Status</th><th>Delivery Method</th><th>Time</th></tr></thead><tbody>';
                        
                        data.messages.forEach(message => {
                            const messagePreview = message.message.length > 50 ? 
                                message.message.substring(0, 50) + '...' : message.message;
                            
                            let contactCell = message.direction === 'OUT' ? message.recipient : message.sender;
                            if (message.whatsapp_link && message.direction === 'OUT') {
                                contactCell = `<a href="${message.whatsapp_link}" target="_blank" class="whatsapp-link">${message.recipient}</a>`;
                            }
                            
                            html += `<tr>
                                <td><span class="status-badge status-${message.direction}">${message.direction}</span></td>
                                <td>${contactCell}</td>
                                <td>${messagePreview}</td>
                                <td><span class="status-badge status-${message.status}">${message.status}</span></td>
                                <td><span class="delivery-method delivery-${message.delivery_method}">${message.delivery_method.toUpperCase()}</span></td>
                                <td>${new Date(message.created_at).toLocaleString()}</td>
                            </tr>`;
                        });
                        
                        html += '</tbody></table>';
                        container.innerHTML = html;
                    } else {
                        container.innerHTML = '<p>Error loading messages</p>';
                    }
                })
                .catch(error => {
                    container.innerHTML = '<p>Error loading messages</p>';
                    console.error('Messages load error:', error);
                });
        }
        
        function checkHealth() {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'healthy') {
                        let healthInfo = '✅ System Status: Healthy<br>';
                        healthInfo += `📱 Business Phone: ${data.config.business_phone}<br>`;
                        healthInfo += `🤖 Auto-reply: ${data.config.auto_reply_enabled ? 'Enabled' : 'Disabled'}<br>`;
                        healthInfo += `📊 Google Integration: ${data.config.google_enabled ? 'Enabled' : 'Disabled'}<br>`;
                        healthInfo += `🔗 WhatsApp API: ${data.config.api_configured ? 'Configured' : 'Using WhatsApp Web fallback'}`;
                        
                        showAlert(healthInfo, 'success');
                        
                        // Update API status in header
                        const apiStatus = document.getElementById('api-status');
                        const apiStatusContent = document.getElementById('api-status-content');
                        
                        if (data.config.api_configured) {
                            apiStatus.className = 'api-status api-configured';
                            apiStatusContent.innerHTML = '🔗 WhatsApp Business API Configured - Real messaging enabled';
                        } else {
                            apiStatus.className = 'api-status api-not-configured';
                            apiStatusContent.innerHTML = '📱 Using WhatsApp Web Fallback - Configure API for real messaging';
                        }
                    } else {
                        showAlert('❌ System Status: Unhealthy - ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showAlert('❌ Health check failed: ' + error, 'error');
                });
        }
        
        function exportGoogleSheets() {
            window.open('/api/export-google-sheets', '_blank');
            showAlert('📊 Google Sheets CSV exported! Check your downloads folder.', 'success');
        }
    </script>
</body>
</html>
        '''
    
    def run(self):
        """Run the professional system"""
        # Create logs and exports directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        
        # Get port from environment
        port = int(os.getenv('FLASK_PORT', 5000))
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        
        log.info(f"🚀 Starting Professional WhatsApp System on {host}:{port}")
        log.info(f"📱 Dashboard: http://localhost:{port}")
        log.info(f"🔗 Webhook: http://localhost:{port}/webhook/whatsapp")
        log.info(f"📊 Google Sheets Export: http://localhost:{port}/api/export-google-sheets")
        log.info(f"🔗 API Status: {'Configured' if self.whatsapp_api.api_configured else 'Using WhatsApp Web fallback'}")
        log.info("✅ Professional features: Contacts, Templates, Scheduling, Analytics")
        
        self.app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    system = ProfessionalMainSystem()
    system.run()
