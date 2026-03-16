#!/usr/bin/env python3
"""
🚀 SIMPLE WHATSAPP MESSAGING SYSTEM
====================================
✅ No registration required
✅ Google Sheets/Drive integration
✅ Automated replies for +8861655542
✅ Bulk messaging with anti-blocking
✅ WhatsApp Web API simulation
✅ Direct CSV export to Google Sheets
"""

import os
import sys
import json
import time
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv

# Import our simple API system
from whatsapp_simple_api import WhatsAppSimpleAPI

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/simple_system.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class SimpleMainSystem:
    """
    Simple WhatsApp Messaging System with Google Integration
    No registration or external tools required
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize the simple WhatsApp API
        self.whatsapp_api = WhatsAppSimpleAPI()
        
        # Setup routes
        self.setup_routes()
        
        # Setup dashboard
        self.setup_dashboard()
        
        log.info("🚀 Simple WhatsApp Messaging System Initialized")
        log.info("📱 Business Number: +8861655542")
        log.info("🤖 Auto-replies: Enabled")
        log.info("📊 Bulk Messaging: Ready")
        log.info("📈 Google Sheets: CSV Export Ready")
        log.info("✅ No registration required")
    
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
                data = request.get_json()
                recipient = data.get('recipient')
                message = data.get('message')
                
                if not recipient or not message:
                    return jsonify({
                        'success': False,
                        'error': 'Recipient and message are required'
                    }), 400
                
                result = self.whatsapp_api.send_whatsapp_message(recipient, message)
                return jsonify(result)
                
            except Exception as e:
                log.error(f"Send single message error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/send-bulk', methods=['POST'])
        def send_bulk_messages():
            """Send bulk WhatsApp messages"""
            try:
                data = request.get_json()
                recipients = data.get('recipients', [])
                message = data.get('message')
                campaign_name = data.get('campaign_name', 'Bulk Campaign')
                
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
                        'auto_reply': self.whatsapp_api.config['AUTO_REPLY_ENABLED']
                    },
                    'config': {
                        'business_phone': self.whatsapp_api.config['BUSINESS_PHONE'],
                        'auto_reply_enabled': self.whatsapp_api.config['AUTO_REPLY_ENABLED'],
                        'google_enabled': self.whatsapp_api.config['GOOGLE_ENABLED'],
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
        
        # Include the webhook from the simple API
        @self.app.route('/webhook/whatsapp', methods=['POST'])
        def whatsapp_webhook():
            """Handle incoming WhatsApp messages"""
            try:
                data = request.get_json()
                sender = data.get('sender', '+1234567890')
                message = data.get('message', 'Hello, I need help')
                message_id = data.get('message_id', f"WEB_{int(time.time())}")
                
                result = self.whatsapp_api.process_incoming_message(sender, message, message_id)
                if result['success']:
                    return jsonify(result), 200
                else:
                    return jsonify(result), 500
                
            except Exception as e:
                log.error(f"Webhook error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def setup_dashboard(self):
        """Setup the HTML dashboard"""
        self.dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple WhatsApp Business System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #25D366, #128C7E); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #25D366; margin-bottom: 10px; }
        .stat-label { color: #666; font-size: 1.1em; }
        .section { background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .section h2 { color: #333; margin-bottom: 20px; font-size: 1.8em; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #333; }
        .form-control { width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 16px; transition: border-color 0.3s ease; }
        .form-control:focus { outline: none; border-color: #25D366; }
        .btn { background: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s ease; }
        .btn:hover { background: #128C7E; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .alert { padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .table th, .table td { padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }
        .table th { background: #f8f9fa; font-weight: 600; }
        .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: 500; }
        .status-sent { background: #d4edda; color: #155724; }
        .status-received { background: #d1ecf1; color: #0c5460; }
        .status-running { background: #fff3cd; color: #856404; }
        .status-completed { background: #d4edda; color: #155724; }
        .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; background: #25D366; transition: width 0.3s ease; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }
        .feature-card { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #25D366; }
        .feature-card h4 { color: #25D366; margin-bottom: 10px; }
        .rate-limits { background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .rate-limits h5 { color: #856404; margin-bottom: 10px; }
        .rate-item { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .loading { display: none; text-align: center; padding: 20px; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #25D366; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .whatsapp-link { color: #25D366; text-decoration: none; font-weight: 500; }
        .whatsapp-link:hover { text-decoration: underline; }
        .note { background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 0.9em; color: #0066cc; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Simple WhatsApp Business System</h1>
            <p>No Registration Required • Google Sheets Integration • Automated Replies • Bulk Messaging</p>
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
            <h2>📤 Send Single Message</h2>
            <div class="note">
                💡 This system generates WhatsApp links. Click the link to send the message manually in WhatsApp.
            </div>
            <div class="form-group">
                <label for="single-recipient">Recipient Phone Number</label>
                <input type="text" id="single-recipient" class="form-control" placeholder="+1234567890">
            </div>
            <div class="form-group">
                <label for="single-message">Message</label>
                <textarea id="single-message" class="form-control" rows="3" placeholder="Enter your message here..."></textarea>
            </div>
            <button onclick="sendSingleMessage()" class="btn">Generate WhatsApp Link</button>
        </div>
        
        <div class="section">
            <h2>📊 Send Bulk Messages</h2>
            <div class="note">
                💡 Bulk campaigns generate WhatsApp links for all recipients and export them to CSV for easy sending.
            </div>
            <div class="form-group">
                <label for="bulk-recipients">Recipients (comma-separated)</label>
                <textarea id="bulk-recipients" class="form-control" rows="3" placeholder="+1234567890,+9876543210,+1122334455"></textarea>
            </div>
            <div class="form-group">
                <label for="bulk-message">Message</label>
                <textarea id="bulk-message" class="form-control" rows="3" placeholder="Enter your bulk message here..."></textarea>
            </div>
            <div class="form-group">
                <label for="campaign-name">Campaign Name</label>
                <input type="text" id="campaign-name" class="form-control" placeholder="My Campaign">
            </div>
            <button onclick="sendBulkMessages()" class="btn">Generate Bulk Links</button>
        </div>
        
        <div class="section">
            <h2>🤖 Test Auto-Reply</h2>
            <div class="note">
                💡 Test the automated reply system for +8861655542
            </div>
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
                    <p>Generate WhatsApp links for thousands of customers with anti-blocking measures</p>
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
                    <h4>📱 No Registration Required</h4>
                    <p>Works with WhatsApp Web links - no API registration needed</p>
                </div>
                <div class="feature-card">
                    <h4>📊 Analytics</h4>
                    <p>Real-time statistics and campaign monitoring</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load initial data
        loadStats();
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
        
        function sendSingleMessage() {
            const recipient = document.getElementById('single-recipient').value;
            const message = document.getElementById('single-message').value;
            
            if (!recipient || !message) {
                showAlert('Please fill in all fields', 'error');
                return;
            }
            
            fetch('/api/send-single', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({recipient, message})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let alertHtml = `✅ WhatsApp link generated!<br>`;
                    alertHtml += `<a href="${data.whatsapp_link}" target="_blank" class="whatsapp-link">Click to send WhatsApp message</a>`;
                    showAlert(alertHtml, 'success');
                    document.getElementById('single-recipient').value = '';
                    document.getElementById('single-message').value = '';
                    loadStats();
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
            
            if (!recipients || !message) {
                showAlert('Please fill in recipients and message', 'error');
                return;
            }
            
            const recipientsArray = recipients.split(',').map(r => r.trim());
            
            fetch('/api/send-bulk', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    recipients: recipientsArray,
                    message: message,
                    campaign_name: campaignName || 'Bulk Campaign'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(`✅ Bulk campaign started! Campaign ID: ${data.campaign_id}<br>WhatsApp links will be generated and exported to CSV.`, 'success');
                    document.getElementById('bulk-recipients').value = '';
                    document.getElementById('bulk-message').value = '';
                    document.getElementById('campaign-name').value = '';
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
                    showAlert(`✅ Auto-reply test successful! Reply: ${data.auto_reply}`, 'success');
                    loadStats();
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
                        let html = '<table class="table"><thead><tr><th>Direction</th><th>Contact</th><th>Message</th><th>Status</th><th>Time</th></tr></thead><tbody>';
                        
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
                        healthInfo += `🛡️ Rate Limiting: Active`;
                        
                        showAlert(healthInfo, 'success');
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
        """Run the simple system"""
        # Create logs and exports directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        
        # Get port from environment
        port = int(os.getenv('FLASK_PORT', 5000))
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        
        log.info(f"🚀 Starting Simple WhatsApp System on {host}:{port}")
        log.info(f"📱 Dashboard: http://localhost:{port}")
        log.info(f"🔗 Webhook: http://localhost:{port}/webhook/whatsapp")
        log.info(f"📊 Google Sheets Export: http://localhost:{port}/api/export-google-sheets")
        
        self.app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    system = SimpleMainSystem()
    system.run()
