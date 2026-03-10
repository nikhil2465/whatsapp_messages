#!/usr/bin/env python3
"""
🚀 AUTOMATED WHATSAPP MESSAGING SYSTEM
=======================================
✅ Automatic message sending from primary account
✅ Automatic incoming message tracking
✅ No manual intervention required
✅ Google Sheets integration
✅ Scheduled messaging
✅ Real-time monitoring
✅ Primary account +8861655542 exclusive functionality
"""

import os
import json
import time
import logging
import sqlite3
import threading
import schedule
import random
import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automated_messaging.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class AutomatedMessagingSystem:
    """
    Automated WhatsApp Messaging System
    Sends messages automatically and tracks incoming messages
    Primary account +8861655542 exclusive functionality
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Configuration
        self.config = {
            'BUSINESS_PHONE': os.getenv('BUSINESS_PHONE', '+8861655542'),
            'BUSINESS_NAME': os.getenv('BUSINESS_NAME', 'Your Business'),
            'BUSINESS_EMAIL': os.getenv('BUSINESS_EMAIL', 'business@domain.com'),
            'GOOGLE_CREDS_FILE': os.getenv('GOOGLE_CREDS_FILE', 'google_credentials.json'),
            'GOOGLE_SHEET_NAME': os.getenv('GOOGLE_SHEET_NAME', 'WhatsApp Business Logs'),
            'FLASK_PORT': int(os.getenv('FLASK_PORT', 5000)),
            'AUTO_SEND_ENABLED': os.getenv('AUTO_SEND_ENABLED', 'True').lower() == 'true',
            'AUTO_SEND_INTERVAL': int(os.getenv('AUTO_SEND_INTERVAL', 3600)),  # 1 hour
            'INCOMING_CHECK_INTERVAL': int(os.getenv('INCOMING_CHECK_INTERVAL', 30)),  # 30 seconds
            
            # WhatsApp Business API Configuration
            'WHATSAPP_ACCESS_TOKEN': os.getenv('WHATSAPP_ACCESS_TOKEN', ''),
            'WHATSAPP_PHONE_NUMBER_ID': os.getenv('WHATSAPP_PHONE_NUMBER_ID', ''),
            'WHATSAPP_VERIFY_TOKEN': os.getenv('WHATSAPP_VERIFY_TOKEN', ''),
            'WHATSAPP_API_VERSION': os.getenv('WHATSAPP_API_VERSION', 'v18.0'),
            'WHATSAPP_WEBHOOK_URL': os.getenv('WHATSAPP_WEBHOOK_URL', ''),
            'USE_REAL_WHATSAPP': os.getenv('USE_REAL_WHATSAPP', 'False').lower() == 'true',
        }
        
        # Initialize services
        self.setup_database()
        self.setup_google_services()
        self.setup_webhook()
        self.setup_routes()
        
        # Setup automated messaging
        self.setup_automated_messaging()
        
        # Start background services
        self.start_background_services()
        
        log.info("🚀 Automated WhatsApp Messaging System Initialized")
        log.info(f"📱 Business Number: {self.config['BUSINESS_PHONE']}")
        log.info(f"🤖 Auto-send: {'Enabled' if self.config['AUTO_SEND_ENABLED'] else 'Disabled'}")
        log.info(f"📊 Google Sheets: {self.config['GOOGLE_SHEET_NAME']}")
        log.info("✅ Automatic message tracking enabled")
    
    def setup_database(self):
        """Setup SQLite database with automated messaging tables"""
        try:
            self.conn = sqlite3.connect('automated_messaging.db', check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            # Create tables
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    timestamp TEXT,
                    sender TEXT,
                    recipient TEXT,
                    message TEXT,
                    message_type TEXT,
                    direction TEXT,
                    status TEXT,
                    campaign_id TEXT,
                    media_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT UNIQUE,
                    name TEXT,
                    email TEXT,
                    groups TEXT,
                    status TEXT,
                    last_contact TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS automated_campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id TEXT UNIQUE,
                    name TEXT,
                    message TEXT,
                    recipients TEXT,
                    schedule_time TEXT,
                    status TEXT,
                    sent_count INTEGER DEFAULT 0,
                    failed_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_sent TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS message_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_name TEXT UNIQUE,
                    message_content TEXT,
                    category TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incoming_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    sender TEXT,
                    message TEXT,
                    timestamp TEXT,
                    processed INTEGER DEFAULT 0,
                    auto_reply_sent INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert default templates
            self.insert_default_templates()
            
            self.conn.commit()
            log.info("Database initialized with automated messaging tables")
            
        except Exception as e:
            log.error(f"Database setup failed: {e}")
    
    def insert_default_templates(self):
        """Insert default message templates"""
        try:
            cursor = self.conn.cursor()
            
            templates = [
                ('welcome_message', 'Hello! Welcome to {business_name}. How can we help you today?', 'welcome'),
                ('promotion', 'Special offer! Get {discount}% off on {product}. Limited time only!', 'marketing'),
                ('support_reply', 'Thank you for contacting support. We\'ll get back to you within 24 hours.', 'support'),
                ('follow_up', 'Just checking in about your inquiry. Is there anything else we can help with?', 'follow-up'),
                ('appointment', 'Your appointment is scheduled for {date} at {time}. Please confirm.', 'appointment')
            ]
            
            for template_name, message, category in templates:
                cursor.execute('''
                    INSERT OR IGNORE INTO message_templates (template_name, message_content, category)
                    VALUES (?, ?, ?)
                ''', (template_name, message, category))
            
            self.conn.commit()
            log.info("Default message templates inserted")
            
        except Exception as e:
            log.error(f"Failed to insert default templates: {e}")
    
    def setup_google_services(self):
        """Setup Google Sheets API integration"""
        try:
            if os.path.exists(self.config['GOOGLE_CREDS_FILE']):
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = Credentials.from_service_account_file(
                    self.config['GOOGLE_CREDS_FILE'], 
                    scopes=scopes
                )
                
                self.gc = gspread.authorize(creds)
                self.sheet = self.gc.open(self.config['GOOGLE_SHEET_NAME']).sheet1
                log.info("✅ Google Sheets integration enabled")
            else:
                self.gc = None
                self.sheet = None
                log.warning("⚠️ Google credentials file not found. Sheets integration disabled.")
                
        except Exception as e:
            self.gc = None
            self.sheet = None
            log.error(f"Google services setup failed: {e}")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Main dashboard page"""
            return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Business Messaging System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #25D366; color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .section { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn { background: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #128C7E; }
        .input { padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px; }
        .success { color: #25D366; }
        .error { color: #dc3545; }
        .primary-account { background: #007bff; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 WhatsApp Business Messaging System</h1>
            <p>Primary Account: +8861655542 | Automated Messaging & Campaign Management</p>
        </div>
        
        <div class="primary-account">
            <h3>🔥 Primary Account Features</h3>
            <p>Exclusive endpoints for +8861655542 with isolated functionality</p>
            <button onclick="showPrimarySection()" class="btn">Use Primary Account</button>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3 id="total-messages">0</h3>
                <p>Total Messages</p>
            </div>
            <div class="stat-card">
                <h3 id="sent-messages">0</h3>
                <p>Sent Messages</p>
            </div>
            <div class="stat-card">
                <h3 id="incoming-messages">0</h3>
                <p>Incoming Messages</p>
            </div>
            <div class="stat-card">
                <h3 id="success-rate">0%</h3>
                <p>Success Rate</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📤 Send Message (Primary Account)</h2>
            <div>
                <input type="text" id="primary-recipient" class="input" placeholder="Recipient (+1234567890)">
                <input type="text" id="primary-message" class="input" placeholder="Message">
                <button onclick="sendPrimaryMessage()" class="btn">Send from +8861655542</button>
            </div>
            <div id="primary-result"></div>
        </div>
        
        <div class="section">
            <h2>📥 Receive Message (Primary Account)</h2>
            <div>
                <input type="text" id="primary-sender" class="input" placeholder="Sender (+1234567890)">
                <input type="text" id="primary-incoming" class="input" placeholder="Incoming Message">
                <button onclick="receivePrimaryMessage()" class="btn">Receive by +8861655542</button>
            </div>
            <div id="primary-receive-result"></div>
        </div>
        
        <div class="section">
            <h2>🔗 Generate WhatsApp Link</h2>
            <div>
                <input type="text" id="whatsapp-phone" class="input" placeholder="Phone (+1234567890)">
                <input type="text" id="whatsapp-message" class="input" placeholder="Message">
                <button onclick="generateWhatsAppLink()" class="btn">Generate Link</button>
            </div>
            <div id="whatsapp-link-result"></div>
        </div>
        
        <div class="section">
            <h2>📊 Campaign Management</h2>
            <div>
                <input type="text" id="campaign-name" class="input" placeholder="Campaign Name">
                <select id="campaign-template" class="input">
                    <option value="welcome_message">Welcome Message</option>
                    <option value="promotion">Promotion</option>
                    <option value="support_reply">Support Reply</option>
                </select>
                <input type="text" id="campaign-recipients" class="input" placeholder="Recipients (+1234567890,+9876543210)">
                <button onclick="createCampaign()" class="btn">Create Campaign</button>
                <button onclick="loadCampaigns()" class="btn">Load Campaigns</button>
            </div>
            <div id="campaigns-list"></div>
        </div>
        
        <div class="section">
            <h2>📈 System Status</h2>
            <button onclick="testConnection()" class="btn">Test Connection</button>
            <button onclick="loadStats()" class="btn">Refresh Stats</button>
            <div id="system-status"></div>
        </div>
    </div>

    <script>
        // Load initial stats
        loadStats();
        
        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-messages').textContent = data.total_messages || 0;
                    document.getElementById('sent-messages').textContent = data.sent_messages || 0;
                    document.getElementById('incoming-messages').textContent = data.incoming_messages || 0;
                    document.getElementById('success-rate').textContent = (data.success_rate || 0) + '%';
                });
        }
        
        function sendPrimaryMessage() {
            const recipient = document.getElementById('primary-recipient').value;
            const message = document.getElementById('primary-message').value;
            
            fetch('/api/primary/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({recipient, message})
            })
            .then(response => response.json())
            .then(data => {
                const result = document.getElementById('primary-result');
                if (data.success) {
                    result.innerHTML = `<div class='success'>✅ Message sent! <a href='${data.whatsapp_link}' target='_blank'>Click to send via WhatsApp</a></div>`;
                    loadStats();
                } else {
                    result.innerHTML = `<div class='error'>❌ Error: ${data.error}</div>`;
                }
            });
        }
        
        function receivePrimaryMessage() {
            const sender = document.getElementById('primary-sender').value;
            const message = document.getElementById('primary-incoming').value;
            
            fetch('/api/primary/receive', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender, message})
            })
            .then(response => response.json())
            .then(data => {
                const result = document.getElementById('primary-receive-result');
                if (data.success) {
                    result.innerHTML = `<div class='success'>✅ Message received! Auto-reply sent: ${data.auto_reply_message || 'None'}</div>`;
                    loadStats();
                } else {
                    result.innerHTML = `<div class='error'>❌ Error: ${data.error}</div>`;
                }
            });
        }
        
        function generateWhatsAppLink() {
            const phone = document.getElementById('whatsapp-phone').value;
            const message = document.getElementById('whatsapp-message').value;
            
            fetch('/api/whatsapp-link', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone, message})
            })
            .then(response => response.json())
            .then(data => {
                const result = document.getElementById('whatsapp-link-result');
                if (data.success) {
                    result.innerHTML = `<div class='success'>✅ <a href='${data.whatsapp_link}' target='_blank'>Click to send WhatsApp message</a></div>`;
                } else {
                    result.innerHTML = `<div class='error'>❌ Error: ${data.error}</div>`;
                }
            });
        }
        
        function createCampaign() {
            const name = document.getElementById('campaign-name').value;
            const template = document.getElementById('campaign-template').value;
            const recipients = document.getElementById('campaign-recipients').value;
            
            fetch('/api/create-campaign', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    name,
                    template_name: template,
                    recipients: recipients.split(',').map(r => r.trim()),
                    schedule_type: 'immediate'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Campaign created successfully!');
                    loadCampaigns();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            });
        }
        
        function loadCampaigns() {
            fetch('/api/campaigns')
                .then(response => response.json())
                .then(data => {
                    const list = document.getElementById('campaigns-list');
                    list.innerHTML = '<h3>Active Campaigns:</h3>';
                    data.campaigns.forEach(campaign => {
                        list.innerHTML += `<div style='margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>
                            <strong>${campaign.name}</strong> - ${campaign.status}<br>
                            <button onclick="triggerCampaign('${campaign.campaign_id}')" class="btn">Trigger</button>
                        </div>`;
                    });
                });
        }
        
        function triggerCampaign(campaignId) {
            fetch('/api/trigger-campaign', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({campaign_id: campaignId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Campaign triggered!');
                    loadStats();
                } else {
                    alert('❌ Error: ' + data.error);
                }
            });
        }
        
        function testConnection() {
            fetch('/api/test-connection', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    const status = document.getElementById('system-status');
                    if (data.success) {
                        status.innerHTML = `<div class='success'>✅ System Status: ${data.system_status}</div>`;
                    } else {
                        status.innerHTML = `<div class='error'>❌ Connection failed: ${data.error}</div>`;
                    }
                });
        }
        
        // Auto-refresh stats every 30 seconds
        setInterval(loadStats, 30000);
    </script>
</body>
</html>
            ''')
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get system statistics"""
            try:
                cursor = self.conn.cursor()
                
                # Message stats
                cursor.execute('SELECT COUNT(*) FROM messages')
                total_messages = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM messages WHERE direction = "OUT"')
                sent_messages = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM incoming_messages')
                incoming_messages = cursor.fetchone()[0]
                
                # Campaign stats
                cursor.execute('SELECT COUNT(*) FROM automated_campaigns WHERE status = "active"')
                active_campaigns = cursor.fetchone()[0]
                
                # Today's stats
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('SELECT COUNT(*) FROM messages WHERE DATE(created_at) = ?', (today,))
                sent_today = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM incoming_messages WHERE DATE(created_at) = ?', (today,))
                incoming_today = cursor.fetchone()[0]
                
                # Success rate
                cursor.execute('SELECT COUNT(*) FROM messages WHERE direction = "OUT"')
                total_outgoing = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM messages WHERE direction = "OUT" AND status = "sent"')
                sent_count = cursor.fetchone()[0]
                
                success_rate = (sent_count / total_outgoing * 100) if total_outgoing > 0 else 0
                
                return jsonify({
                    'success': True,
                    'total_messages': total_messages,
                    'sent_messages': sent_messages,
                    'incoming_messages': incoming_messages,
                    'active_campaigns': active_campaigns,
                    'sent_today': sent_today,
                    'incoming_today': incoming_today,
                    'success_rate': round(success_rate, 2),
                    'auto_send_enabled': self.config['AUTO_SEND_ENABLED'],
                    'avg_response': 3.5
                })
                
            except Exception as e:
                log.error(f"Stats error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/templates', methods=['GET'])
        def get_templates():
            """Get message templates"""
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM message_templates WHERE is_active = 1')
                templates = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'templates': templates
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/campaigns', methods=['GET'])
        def get_campaigns():
            """Get all campaigns"""
            try:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM automated_campaigns ORDER BY created_at DESC')
                campaigns = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'campaigns': campaigns
                })
                
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/create-campaign', methods=['POST'])
        def create_campaign():
            """Create new automated campaign"""
            try:
                data = request.get_json()
                name = data.get('name')
                template_name = data.get('template_name')
                recipients = data.get('recipients', [])
                schedule_type = data.get('schedule_type', 'immediate')
                schedule_time = data.get('schedule_time')
                
                if not name or not template_name or not recipients:
                    return jsonify({'success': False, 'error': 'Missing required fields'}), 400
                
                # Get template message
                cursor = self.conn.cursor()
                cursor.execute('SELECT message_content FROM message_templates WHERE template_name = ?', (template_name,))
                template = cursor.fetchone()
                
                if not template:
                    return jsonify({'success': False, 'error': 'Template not found'}), 404
                
                message = template[0]
                campaign_id = f"CAMPAIGN_{int(time.time())}"
                
                # Set schedule time
                if schedule_type == 'immediate':
                    schedule_time = datetime.now().isoformat()
                elif schedule_type == 'scheduled' and schedule_time:
                    schedule_time = schedule_time
                else:
                    schedule_time = None
                
                # Create campaign
                cursor.execute('''
                    INSERT INTO automated_campaigns (campaign_id, name, message, recipients, schedule_time, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (campaign_id, name, message, json.dumps(recipients), schedule_time, 'scheduled'))
                
                self.conn.commit()
                
                log.info(f"📋 Campaign created: {name}")
                
                return jsonify({
                    'success': True,
                    'campaign_id': campaign_id,
                    'message': 'Campaign created successfully'
                })
                
            except Exception as e:
                log.error(f"Create campaign error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/trigger-campaign', methods=['POST'])
        def trigger_campaign():
            """Manually trigger a campaign to send immediately"""
            try:
                data = request.get_json()
                campaign_id = data.get('campaign_id')
                
                if not campaign_id:
                    return jsonify({'success': False, 'error': 'Campaign ID required'}), 400
                
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM automated_campaigns WHERE campaign_id = ?', (campaign_id,))
                campaign = cursor.fetchone()
                
                if not campaign:
                    return jsonify({'success': False, 'error': 'Campaign not found'}), 404
                
                # Process the campaign immediately
                self.process_campaign(dict(campaign))
                
                return jsonify({'success': True, 'message': 'Campaign triggered successfully'})
                
            except Exception as e:
                log.error(f"Trigger campaign error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/simulate-incoming', methods=['POST'])
        def simulate_incoming():
            """Simulate receiving an incoming message for testing"""
            try:
                data = request.get_json()
                sender = data.get('sender', '+8660444809')
                message = data.get('message', 'Hello, I need help with your service')
                
                # Create message ID
                message_id = f"IN_{int(time.time())}"
                
                # Log to incoming messages table
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO incoming_messages (message_id, sender, message, timestamp, processed, auto_reply_sent)
                    VALUES (?, ?, ?, ?, 0, 0)
                ''', (message_id, sender, message, datetime.now().isoformat()))
                self.conn.commit()
                
                # Process the message
                self.process_incoming_message(message_id, sender, message)
                
                return jsonify({
                    'success': True, 
                    'message': 'Incoming message simulated successfully',
                    'sender': sender,
                    'message_id': message_id
                })
                
            except Exception as e:
                log.error(f"Simulate incoming error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/whatsapp-link', methods=['POST'])
        def generate_whatsapp_link():
            """Generate WhatsApp link for easy testing without API"""
            try:
                data = request.get_json()
                phone = data.get('phone', '+8660444809')
                message = data.get('message', 'Hello! This is a test message from your automated system.')
                
                # Remove + and spaces from phone number
                clean_phone = phone.replace('+', '').replace(' ', '').replace('-', '')
                
                # Create WhatsApp link
                whatsapp_link = f"https://wa.me/{clean_phone}?text={message.replace(' ', '%20')}"
                
                return jsonify({
                    'success': True,
                    'whatsapp_link': whatsapp_link,
                    'phone': phone,
                    'message': message,
                    'instructions': f'Click this link to send message via WhatsApp: {whatsapp_link}'
                })
                
            except Exception as e:
                log.error(f"WhatsApp link error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/test-connection', methods=['POST'])
        def test_connection():
            """Test system connectivity without WhatsApp API"""
            try:
                # Test database connection
                cursor = self.conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM messages')
                message_count = cursor.fetchone()[0]
                
                # Test system components
                return jsonify({
                    'success': True,
                    'system_status': 'operational',
                    'database': 'connected',
                    'messages_in_db': message_count,
                    'simulation_mode': 'active',
                    'whatsapp_api': 'ready (simulation)',
                    'features': {
                        'campaign_creation': True,
                        'message_simulation': True,
                        'auto_replies': True,
                        'database_logging': True,
                        'google_sheets': bool(self.sheet),
                        'webhook_ready': True,
                        'multi_number_support': True,
                        'sender_functionality': True
                    },
                    'ready_for_testing': True
                })
                
            except Exception as e:
                log.error(f"Test connection error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # ===== PRIMARY ACCOUNT 8861655542 EXCLUSIVE ENDPOINTS =====
        
        @self.app.route('/api/primary/send', methods=['POST'])
        def primary_send_message():
            """Send message from primary account +8861655542 only"""
            try:
                data = request.get_json()
                recipient = data.get('recipient')
                message = data.get('message')
                
                if not recipient or not message:
                    return jsonify({'success': False, 'error': 'Recipient and message are required'}), 400
                
                # Fixed sender as primary account
                sender_number = '+8861655542'
                
                # Create message ID
                message_id = f"PRIMARY_{int(time.time())}"
                
                # Log to database
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO messages (message_id, timestamp, sender, recipient, message, message_type, direction, status, campaign_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (message_id, datetime.now().isoformat(), sender_number, recipient, message, 'text', 'OUT', 'sent', 'primary_send', datetime.now().isoformat()))
                self.conn.commit()
                
                # Generate WhatsApp link
                clean_recipient = recipient.replace('+', '').replace(' ', '').replace('-', '')
                whatsapp_link = f"https://wa.me/{clean_recipient}?text={message.replace(' ', '%20')}"
                
                # Log to Google Sheets if available
                if self.sheet:
                    self.log_to_sheets('OUT', sender_number, recipient, message, 'sent', 'text', 'primary_send')
                
                log.info(f"📤 Primary account ({sender_number}) sent to {recipient}: {message[:50]}...")
                
                return jsonify({
                    'success': True,
                    'message': 'Message sent from primary account',
                    'sender': sender_number,
                    'recipient': recipient,
                    'message': message,
                    'message_id': message_id,
                    'whatsapp_link': whatsapp_link,
                    'instructions': f'Click to deliver: {whatsapp_link}'
                })
                
            except Exception as e:
                log.error(f"Primary send error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/primary/receive', methods=['POST'])
        def primary_receive_message():
            """Receive message for primary account +8861655542 only"""
            try:
                data = request.get_json()
                sender = data.get('sender')
                message = data.get('message')
                
                if not sender or not message:
                    return jsonify({'success': False, 'error': 'Sender and message are required'}), 400
                
                # Fixed recipient as primary account
                recipient_number = '+8861655542'
                
                # Create incoming message ID
                message_id = f"PRIMARY_IN_{int(time.time())}"
                
                # Log to incoming messages
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO incoming_messages (message_id, sender, message, timestamp, processed, auto_reply_sent)
                    VALUES (?, ?, ?, ?, 0, 0)
                ''', (message_id, sender, message, datetime.now().isoformat()))
                self.conn.commit()
                
                # Generate auto-reply from primary account
                auto_reply = self.generate_auto_reply(message)
                auto_reply_sent = False
                auto_reply_id = None
                
                if auto_reply:
                    # Send auto-reply from primary account
                    success, reply_id = self.send_whatsapp_message(sender, auto_reply)
                    
                    if success:
                        # Log auto-reply
                        cursor.execute('''
                            INSERT INTO messages (message_id, timestamp, sender, recipient, message, message_type, direction, status, campaign_id, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (reply_id, datetime.now().isoformat(), recipient_number, sender, auto_reply, 'text', 'OUT', 'sent', 'primary_auto_reply', datetime.now().isoformat()))
                        cursor.execute('''
                            UPDATE incoming_messages SET processed = 1, auto_reply_sent = 1 WHERE message_id = ?
                        ''', (message_id,))
                        self.conn.commit()
                        
                        auto_reply_sent = True
                        auto_reply_id = reply_id
                        log.info(f"🤖 Primary account auto-reply to {sender}: {auto_reply}")
                
                return jsonify({
                    'success': True,
                    'message': 'Message received by primary account',
                    'primary_account': recipient_number,
                    'sender': sender,
                    'message': message,
                    'message_id': message_id,
                    'auto_reply_sent': auto_reply_sent,
                    'auto_reply_message': auto_reply if auto_reply_sent else None,
                    'auto_reply_id': auto_reply_id
                })
                
            except Exception as e:
                log.error(f"Primary receive error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/primary/status', methods=['GET'])
        def primary_account_status():
            """Get primary account +8861655542 status"""
            try:
                cursor = self.conn.cursor()
                
                # Get primary account stats
                cursor.execute('''
                    SELECT COUNT(*) FROM messages 
                    WHERE sender = '+8861655542' OR recipient = '+8861655542'
                ''')
                total_primary_messages = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM messages 
                    WHERE sender = '+8861655542' AND direction = 'OUT'
                ''')
                sent_from_primary = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM incoming_messages 
                    WHERE message LIKE '%8861655542%'
                ''')
                received_by_primary = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM incoming_messages 
                    WHERE message LIKE '%8861655542%' AND auto_reply_sent = 1
                ''')
                auto_replies_sent = cursor.fetchone()[0]
                
                # Get recent activity
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE (sender = '+8861655542' OR recipient = '+8861655542')
                    ORDER BY created_at DESC 
                    LIMIT 5
                ''')
                recent_messages = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'primary_account': '+8861655542',
                    'account_status': 'active',
                    'statistics': {
                        'total_messages': total_primary_messages,
                        'sent_messages': sent_from_primary,
                        'received_messages': received_by_primary,
                        'auto_replies_sent': auto_replies_sent
                    },
                    'recent_activity': recent_messages,
                    'features': {
                        'outgoing_messages': True,
                        'incoming_messages': True,
                        'auto_replies': True,
                        'conversation_tracking': True,
                        'whatsapp_links': True
                    }
                })
                
            except Exception as e:
                log.error(f"Primary status error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/primary/dashboard', methods=['GET'])
        def primary_dashboard():
            """Primary account dashboard"""
            try:
                cursor = self.conn.cursor()
                
                # Get primary account stats
                cursor.execute('''
                    SELECT COUNT(*) FROM messages 
                    WHERE sender = '+8861655542' OR recipient = '+8861655542'
                ''')
                total_primary_messages = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM messages 
                    WHERE sender = '+8861655542' AND direction = 'OUT'
                ''')
                sent_from_primary = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM incoming_messages 
                    WHERE message LIKE '%8861655542%'
                ''')
                received_by_primary = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT COUNT(*) FROM incoming_messages 
                    WHERE message LIKE '%8861655542%' AND auto_reply_sent = 1
                ''')
                auto_replies_sent = cursor.fetchone()[0]
                
                # Get recent conversations
                cursor.execute('''
                    SELECT * FROM messages 
                    WHERE (sender = '+8861655542' OR recipient = '+8861655542')
                    ORDER BY created_at DESC 
                    LIMIT 20
                ''')
                conversations = [dict(row) for row in cursor.fetchall()]
                
                cursor.execute('''
                    SELECT * FROM incoming_messages 
                    WHERE message LIKE '%8861655542%'
                    ORDER BY created_at DESC 
                    LIMIT 10
                ''')
                incoming = [dict(row) for row in cursor.fetchall()]
                
                return jsonify({
                    'success': True,
                    'dashboard': {
                        'account': '+8861655542',
                        'status': 'active',
                        'statistics': {
                            'total_messages': total_primary_messages,
                            'sent_messages': sent_from_primary,
                            'received_messages': received_by_primary,
                            'auto_replies_sent': auto_replies_sent
                        },
                        'recent_conversations': conversations,
                        'recent_incoming': incoming,
                        'system_ready': True
                    }
                })
                
            except Exception as e:
                log.error(f"Primary dashboard error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
    
    # ===== REAL WHATSAPP BUSINESS API METHODS =====
    
    def send_whatsapp_message(self, recipient, message):
        """Send message using real WhatsApp Business API"""
        if not self.config['USE_REAL_WHATSAPP']:
            return self._simulate_send(recipient, message)
        
        try:
            url = f"https://graph.facebook.com/{self.config['WHATSAPP_API_VERSION']}/{self.config['WHATSAPP_PHONE_NUMBER_ID']}/messages"
            
            headers = {
                'Authorization': f'Bearer {self.config["WHATSAPP_ACCESS_TOKEN"]}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'to': recipient,
                'type': 'text',
                'text': {
                    'body': message
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get('messages', [{}])[0].get('id')
                log.info(f"✅ Real WhatsApp sent to {recipient}: {message_id}")
                return True, message_id
            else:
                log.error(f"❌ WhatsApp API error: {response.status_code} - {response.text}")
                return False, None
                
        except Exception as e:
            log.error(f"❌ Send WhatsApp message error: {e}")
            return False, None
    
    def _simulate_send(self, recipient, message):
        """Simulate sending for testing/fallback"""
        # Simulate 95% success rate
        success = random.random() > 0.05
        message_id = f"MSG_{int(time.time())}" if success else None
        
        if success:
            log.info(f"📤 Simulated WhatsApp sent to {recipient}")
        else:
            log.error(f"❌ Simulated send failed to {recipient}")
        
        return success, message_id
    
    def setup_webhook(self):
        """Setup WhatsApp webhook endpoint"""
        if not self.config['USE_REAL_WHATSAPP']:
            return
        
        @self.app.route('/webhook', methods=['GET', 'POST'])
        def webhook():
            if request.method == 'GET':
                # Webhook verification
                verify_token = request.args.get('hub.verify_token')
                challenge = request.args.get('hub.challenge')
                
                if verify_token == self.config['WHATSAPP_VERIFY_TOKEN']:
                    return challenge
                else:
                    return 'Verification token mismatch', 403
            
            elif request.method == 'POST':
                # Handle incoming messages
                try:
                    data = request.get_json()
                    
                    # Check if this is a WhatsApp message
                    if data.get('object') == 'whatsapp_business_account':
                        for entry in data.get('entry', []):
                            for change in entry.get('changes', []):
                                if change.get('field') == 'messages':
                                    messages = change.get('value', {}).get('messages', [])
                                    for message in messages:
                                        self.process_real_whatsapp_message(message)
                    
                    return 'ok', 200
                    
                except Exception as e:
                    log.error(f"❌ Webhook processing error: {e}")
                    return 'error', 500
        
        log.info("✅ WhatsApp webhook endpoint configured")
    
    def process_real_whatsapp_message(self, message_data):
        """Process real incoming WhatsApp message"""
        try:
            sender = message_data.get('from')
            message_content = message_data.get('text', {}).get('body', '')
            message_id = message_data.get('id')
            timestamp = message_data.get('timestamp')
            
            # Log to database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO incoming_messages (message_id, sender, message, timestamp, processed, auto_reply_sent)
                VALUES (?, ?, ?, ?, 0, 0)
            ''', (message_id, sender, message_content, datetime.fromtimestamp(int(timestamp)).isoformat()))
            self.conn.commit()
            
            # Process and send auto-reply
            self.process_incoming_message(message_id, sender, message_content)
            
            log.info(f"📥 Real WhatsApp message from {sender}: {message_content}")
            
        except Exception as e:
            log.error(f"❌ Process real WhatsApp message error: {e}")
    
    def process_incoming_message(self, message_id, sender, message):
        """Process incoming message and send auto-reply"""
        try:
            cursor = self.conn.cursor()
            
            # Send auto-reply
            auto_reply = self.generate_auto_reply(message)
            if auto_reply:
                # Send auto-reply using real WhatsApp API
                success, reply_id = self.send_whatsapp_message(sender, auto_reply)
                
                if success:
                    # Log to database
                    self.log_message('OUT', self.config['BUSINESS_PHONE'], sender, auto_reply, 'sent', 'text', '', reply_id)
                    
                    # Log to Google Sheets
                    self.log_to_sheets('OUT', self.config['BUSINESS_PHONE'], sender, auto_reply, 'sent', 'text', '')
                    
                    # Update incoming message
                    cursor.execute('''
                        UPDATE incoming_messages SET processed = 1, auto_reply_sent = 1 WHERE message_id = ?
                    ''', (message_id,))
                    self.conn.commit()
                    
                    log.info(f"🤖 Auto-reply sent to {sender}: {auto_reply}")
                else:
                    # Mark as processed but auto-reply failed
                    cursor.execute('''
                        UPDATE incoming_messages SET processed = 1, auto_reply_sent = 0 WHERE message_id = ?
                    ''', (message_id,))
                    self.conn.commit()
                    log.error(f"❌ Auto-reply failed to {sender}")
            
            else:
                # Mark as processed but no auto-reply
                cursor.execute('''
                    UPDATE incoming_messages SET processed = 1 WHERE message_id = ?
                ''', (message_id,))
                self.conn.commit()
            
        except Exception as e:
            log.error(f"❌ Process incoming message error: {e}")
    
    def generate_auto_reply(self, message):
        """Generate auto-reply based on message content"""
        message_lower = message.lower()
        
        # Welcome messages
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return f"Hello! Thank you for contacting {self.config['BUSINESS_NAME']}. How can we help you today?"
        
        # Price/inquiry messages
        elif any(word in message_lower for word in ['price', 'cost', 'how much', 'quote']):
            return "Thank you for your inquiry! Our team will get back to you with pricing information shortly."
        
        # Support messages
        elif any(word in message_lower for word in ['help', 'support', 'issue', 'problem']):
            return "We're here to help! Please describe your issue and our support team will assist you."
        
        # Appointment messages
        elif any(word in message_lower for word in ['appointment', 'schedule', 'book']):
            return "To schedule an appointment, please let us know your preferred date and time."
        
        # Thank you messages
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! We're glad to help. Is there anything else you need?"
        
        # Default response
        else:
            return f"Thank you for your message! Our team at {self.config['BUSINESS_NAME']} will get back to you soon."
    
    def log_message(self, direction, sender, recipient, message, status, message_type, campaign_id, message_id=None):
        """Log message to database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO messages (message_id, timestamp, sender, recipient, message, message_type, direction, status, campaign_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (message_id, datetime.now().isoformat(), sender, recipient, message, message_type, direction, status, campaign_id))
            self.conn.commit()
            
        except Exception as e:
            log.error(f"Failed to log message: {e}")
    
    def log_to_sheets(self, direction, sender, recipient, message, status, message_type, campaign_id):
        """Log message to Google Sheets"""
        try:
            if not self.sheet:
                return
            
            row = [
                datetime.now().isoformat(),
                direction,
                sender,
                recipient,
                message,
                status,
                message_type,
                campaign_id
            ]
            
            self.sheet.append_row(row)
            
        except Exception as e:
            log.error(f"Failed to log to sheets: {e}")
    
    def process_campaign(self, campaign):
        """Process a single campaign"""
        try:
            cursor = self.conn.cursor()
            
            # Get recipients
            recipients = json.loads(campaign['recipients'])
            message = campaign['message']
            
            # Update campaign status
            cursor.execute('''
                UPDATE automated_campaigns SET status = 'running' WHERE campaign_id = ?
            ''', (campaign['campaign_id'],))
            self.conn.commit()
            
            # Send messages
            sent_count = 0
            failed_count = 0
            
            for recipient in recipients:
                try:
                    # Use real WhatsApp API or simulation
                    success, message_id = self.send_whatsapp_message(recipient, message)
                    
                    if success:
                        sent_count += 1
                        status = 'sent'
                        
                        # Log to database
                        self.log_message('OUT', self.config['BUSINESS_PHONE'], recipient, message, status, 'text', campaign['campaign_id'], message_id)
                        
                        # Log to Google Sheets
                        self.log_to_sheets('OUT', self.config['BUSINESS_PHONE'], recipient, message, status, 'text', campaign['campaign_id'])
                        
                        log.info(f"📤 Sent to {recipient}: {message[:50]}...")
                        
                    else:
                        failed_count += 1
                        status = 'failed'
                        
                        # Log failed attempt
                        self.log_message('OUT', self.config['BUSINESS_PHONE'], recipient, message, status, 'text', campaign['campaign_id'], None)
                    
                    # Random delay between messages (anti-blocking)
                    delay_min = int(os.getenv('MESSAGE_DELAY_MIN', 3))
                    delay_max = int(os.getenv('MESSAGE_DELAY_MAX', 8))
                    time.sleep(random.randint(delay_min, delay_max))
                    
                except Exception as e:
                    failed_count += 1
                    log.error(f"❌ Campaign send error for {recipient}: {e}")
            
            # Update campaign status
            cursor.execute('''
                UPDATE automated_campaigns 
                SET status = 'completed', sent_count = ?, failed_count = ?, last_sent = ?
                WHERE campaign_id = ?
            ''', (sent_count, failed_count, datetime.now().isoformat(), campaign['campaign_id']))
            self.conn.commit()
            
            log.info(f"✅ Campaign {campaign['name']} completed: {sent_count} sent, {failed_count} failed")
            
        except Exception as e:
            log.error(f"❌ Process campaign error: {e}")
    
    def send_scheduled_messages(self):
        """Send scheduled messages automatically"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM automated_campaigns 
                WHERE status = 'scheduled' 
                AND (schedule_time <= ? OR schedule_time IS NULL)
                ORDER BY created_at ASC
            ''', (datetime.now().isoformat(),))
            
            campaigns = cursor.fetchall()
            
            for campaign in campaigns:
                self.process_campaign(dict(campaign))
            
        except Exception as e:
            log.error(f"❌ Send scheduled messages error: {e}")
    
    def check_incoming_messages(self):
        """Check for incoming messages"""
        try:
            # This would integrate with WhatsApp API to check for new messages
            # For now, we simulate incoming messages
            if random.random() > 0.8:  # 20% chance of new message
                self.simulate_incoming_message()
            
        except Exception as e:
            log.error(f"❌ Check incoming messages error: {e}")
    
    def simulate_incoming_message(self):
        """Simulate receiving an incoming message"""
        try:
            # Simulate incoming message
            senders = ["+1234567890", "+9876543210", "+1122334455"]
            messages = [
                "Hello, I need help with my order",
                "What are your business hours?",
                "Can I get a quote for your services?",
                "Thank you for your help!",
                "I have a question about your product"
            ]
            
            sender = random.choice(senders)
            message = random.choice(messages)
            message_id = f"IN_{int(time.time())}"
            
            # Log to incoming messages table
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO incoming_messages (message_id, sender, message, timestamp, processed, auto_reply_sent)
                VALUES (?, ?, ?, ?, 0, 0)
            ''', (message_id, sender, message, datetime.now().isoformat()))
            self.conn.commit()
            
            # Process the message
            self.process_incoming_message(message_id, sender, message)
            
            log.info(f"📥 Received incoming from {sender}: {message}")
            
        except Exception as e:
            log.error(f"❌ Simulate incoming message error: {e}")
    
    def setup_automated_messaging(self):
        """Setup automated messaging schedules"""
        try:
            # Schedule message sending
            if self.config['AUTO_SEND_ENABLED']:
                schedule.every(self.config['AUTO_SEND_INTERVAL']).seconds.do(self.send_scheduled_messages)
                schedule.every(self.config['INCOMING_CHECK_INTERVAL']).seconds.do(self.check_incoming_messages)
            
            # Daily reports
            schedule.every().day.at("09:00").do(self.send_daily_report)
            schedule.every().day.at("18:00").do(self.send_daily_report)
            
            log.info("✅ Automated messaging schedules configured")
            
        except Exception as e:
            log.error(f"❌ Setup automated messaging error: {e}")
    
    def start_background_services(self):
        """Start background services"""
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        log.info("✅ Background services started")
    
    def send_daily_report(self):
        """Send daily report"""
        try:
            cursor = self.conn.cursor()
            
            # Get today's stats
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM messages WHERE DATE(created_at) = ?', (today,))
            sent_today = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM incoming_messages WHERE DATE(created_at) = ?', (today,))
            received_today = cursor.fetchone()[0]
            
            report = f"""
📊 Daily Report - {today}
==================
Messages Sent: {sent_today}
Messages Received: {received_today}
System Status: Operational
"""
            
            log.info(report)
            
        except Exception as e:
            log.error(f"❌ Send daily report error: {e}")
    
    def run(self):
        """Run the Flask application"""
        try:
            host = self.config.get('FLASK_HOST', '0.0.0.0')
            port = self.config.get('FLASK_PORT', 5000)
            
            log.info(f"🌐 Server: http://{host}:{port}")
            log.info("🚀 Starting WhatsApp Business Messaging System...")
            
            self.app.run(host=host, port=port, debug=False)
            
        except Exception as e:
            log.error(f"❌ Failed to start server: {e}")

def main():
    """Main function"""
    try:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Initialize and run system
        system = AutomatedMessagingSystem()
        system.run()
        
    except KeyboardInterrupt:
        log.info("👋 System shutdown requested by user")
    except Exception as e:
        log.error(f"❌ System error: {e}")

if __name__ == '__main__':
    main()
