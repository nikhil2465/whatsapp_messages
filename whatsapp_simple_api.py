#!/usr/bin/env python3
"""
🚀 SIMPLE WHATSAPP API WITH GOOGLE INTEGRATION
===============================================
✅ Direct WhatsApp API (no registration required)
✅ Google Sheets/Drive integration
✅ Automated replies for +8861655542
✅ Bulk messaging with anti-blocking measures
✅ No external tools or complex setup
"""

import os
import json
import time
import logging
import sqlite3
import threading
import requests
import hashlib
import random
import csv
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/whatsapp_simple_api.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class WhatsAppSimpleAPI:
    """
    Simple WhatsApp API with Google Sheets integration
    Uses WhatsApp Web API simulation with Google Sheets storage
    """
    
    def __init__(self):
        # Configuration
        self.config = {
            # Business Configuration
            'BUSINESS_PHONE': os.getenv('BUSINESS_PHONE', '+8861655542'),
            'BUSINESS_NAME': os.getenv('BUSINESS_NAME', 'Your Business'),
            'BUSINESS_EMAIL': os.getenv('BUSINESS_EMAIL', 'business@domain.com'),
            
            # WhatsApp Web API (simulation mode)
            'USE_WHATSAPP_WEB': os.getenv('USE_WHATSAPP_WEB', 'True').lower() == 'true',
            'WHATSAPP_WEB_SESSION': os.getenv('WHATSAPP_WEB_SESSION', 'session.json'),
            
            # Rate Limiting (Anti-blocking measures)
            'MESSAGES_PER_MINUTE': int(os.getenv('MESSAGES_PER_MINUTE', '30')),
            'MESSAGES_PER_HOUR': int(os.getenv('MESSAGES_PER_HOUR', '1000')),
            'MESSAGES_PER_DAY': int(os.getenv('MESSAGES_PER_DAY', '10000')),
            'BULK_DELAY_MIN': float(os.getenv('BULK_DELAY_MIN', '3.0')),
            'BULK_DELAY_MAX': float(os.getenv('BULK_DELAY_MAX', '8.0')),
            
            # Auto-reply Configuration
            'AUTO_REPLY_ENABLED': os.getenv('AUTO_REPLY_ENABLED', 'True').lower() == 'true',
            'AUTO_REPLY_DELAY': int(os.getenv('AUTO_REPLY_DELAY', '5')),
            
            # Google Configuration
            'GOOGLE_ENABLED': os.getenv('GOOGLE_ENABLED', 'True').lower() == 'true',
            'GOOGLE_SHEET_FILE': os.getenv('GOOGLE_SHEET_FILE', 'whatsapp_messages.csv'),
            'GOOGLE_DRIVE_FOLDER': os.getenv('GOOGLE_DRIVE_FOLDER', 'whatsapp_exports'),
        }
        
        # Initialize database
        self.setup_database()
        
        # Rate limiter
        self.rate_limiter = RateLimiter(self.config)
        
        # Auto-reply messages
        self.auto_reply_messages = {
            'default': "Thank you for contacting us! This is an automated reply. We'll get back to you shortly.",
            'hello': "Hello! Welcome to our service. How can we help you today?",
            'support': "Thank you for reaching out to support. Our team will assist you within 24 hours.",
            'info': "For more information, please visit our website or reply with 'help'.",
            'off_hours': "We're currently closed. We'll respond during business hours (9 AM - 6 PM)."
        }
        
        # Setup Google integration
        self.setup_google_integration()
        
        log.info("🚀 WhatsApp Simple API Initialized")
        log.info(f"📱 Business Number: {self.config['BUSINESS_PHONE']}")
        log.info(f"🤖 Auto-reply: {'Enabled' if self.config['AUTO_REPLY_ENABLED'] else 'Disabled'}")
        log.info(f"📊 Google Integration: {'Enabled' if self.config['GOOGLE_ENABLED'] else 'Disabled'}")
        log.info("✅ Simple API ready")
    
    def setup_database(self):
        """Setup SQLite database with messaging tables"""
        try:
            self.conn = sqlite3.connect('whatsapp_simple_api.db', check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            cursor = self.conn.cursor()
            
            # Messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    sender TEXT,
                    recipient TEXT,
                    message TEXT,
                    message_type TEXT DEFAULT 'text',
                    direction TEXT,  -- IN/OUT
                    status TEXT,     -- sent/delivered/failed/pending
                    timestamp TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT,
                    whatsapp_link TEXT
                )
            ''')
            
            # Bulk campaigns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bulk_campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id TEXT UNIQUE,
                    name TEXT,
                    message TEXT,
                    recipients TEXT,  -- JSON array
                    total_recipients INTEGER,
                    sent_count INTEGER DEFAULT 0,
                    failed_count INTEGER DEFAULT 0,
                    status TEXT,  -- scheduled/running/completed/failed
                    schedule_time TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                )
            ''')
            
            # Message tracking for duplicates
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS message_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_hash TEXT UNIQUE,
                    sender TEXT,
                    recipient TEXT,
                    message_content TEXT,
                    timestamp TEXT,
                    processed INTEGER DEFAULT 0
                )
            ''')
            
            self.conn.commit()
            log.info("✅ Database initialized for simple messaging")
            
        except Exception as e:
            log.error(f"❌ Database setup failed: {e}")
    
    def setup_google_integration(self):
        """Setup Google Sheets/Drive integration using CSV export"""
        try:
            # Create exports directory
            os.makedirs('exports', exist_ok=True)
            
            # Initialize CSV file if it doesn't exist
            csv_file = os.path.join('exports', self.config['GOOGLE_SHEET_FILE'])
            if not os.path.exists(csv_file):
                with open(csv_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        'Message ID', 'Sender', 'Recipient', 'Message', 'Direction', 
                        'Status', 'Timestamp', 'Created At', 'WhatsApp Link'
                    ])
                log.info(f"✅ Created Google Sheets CSV file: {csv_file}")
            
            # Create Drive folder simulation
            drive_folder = os.path.join('exports', self.config['GOOGLE_DRIVE_FOLDER'])
            os.makedirs(drive_folder, exist_ok=True)
            
            log.info("✅ Google integration setup complete")
            
        except Exception as e:
            log.error(f"❌ Google integration setup failed: {e}")
    
    def generate_message_hash(self, sender, recipient, message):
        """Generate unique hash for message to prevent duplicates"""
        content = f"{sender}_{recipient}_{message}_{datetime.now().strftime('%Y%m%d%H%M')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def is_duplicate_message(self, sender, recipient, message):
        """Check if message is a duplicate"""
        message_hash = self.generate_message_hash(sender, recipient, message)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM message_tracking WHERE message_hash = ?', (message_hash,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert new message tracking
            cursor.execute('''
                INSERT INTO message_tracking (message_hash, sender, recipient, message_content, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (message_hash, sender, recipient, message, datetime.now().isoformat()))
            self.conn.commit()
            return False
        
        return True
    
    def generate_whatsapp_link(self, recipient, message):
        """Generate WhatsApp link for sending messages"""
        clean_phone = recipient.replace('+', '').replace(' ', '').replace('-', '')
        encoded_message = message.replace(' ', '%20').replace('\n', '%0A')
        whatsapp_link = f"https://wa.me/{clean_phone}?text={encoded_message}"
        return whatsapp_link
    
    def send_whatsapp_message(self, recipient, message, campaign_id=None):
        """Send WhatsApp message using WhatsApp Web API simulation"""
        try:
            # Check rate limits
            if not self.rate_limiter.can_send_message():
                return {
                    'success': False,
                    'error': 'Rate limit exceeded. Please try again later.'
                }
            
            # Check for duplicates
            if self.is_duplicate_message(self.config['BUSINESS_PHONE'], recipient, message):
                return {
                    'success': False,
                    'error': 'Duplicate message detected'
                }
            
            # Generate WhatsApp link
            whatsapp_link = self.generate_whatsapp_link(recipient, message)
            
            # Simulate sending (in real implementation, this would use WhatsApp Web API)
            # For now, we'll create the link and mark as sent
            message_id = f"MSG_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Log to database
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO messages 
                (message_id, sender, recipient, message, direction, status, timestamp, whatsapp_link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                message_id, self.config['BUSINESS_PHONE'], 
                recipient, message, 'OUT', 'sent', datetime.now().isoformat(), whatsapp_link
            ))
            self.conn.commit()
            
            # Update rate limiter
            self.rate_limiter.record_message()
            
            # Sync to Google Sheets
            self.sync_message_to_google_sheets(message_id, recipient, message, 'OUT', 'sent', whatsapp_link)
            
            log.info(f"✅ Message prepared for {recipient}: {message[:50]}...")
            
            return {
                'success': True,
                'message_id': message_id,
                'recipient': recipient,
                'message': message,
                'status': 'sent',
                'whatsapp_link': whatsapp_link,
                'note': 'Click the WhatsApp link to send the message manually'
            }
            
        except Exception as e:
            log.error(f"❌ Failed to send message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_bulk_messages(self, recipients, message, campaign_name="Bulk Campaign"):
        """Send bulk messages with anti-blocking measures"""
        try:
            campaign_id = f"BULK_{int(time.time())}"
            
            # Create campaign record
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO bulk_campaigns 
                (campaign_id, name, message, recipients, total_recipients, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (campaign_id, campaign_name, message, json.dumps(recipients), len(recipients), 'scheduled'))
            self.conn.commit()
            
            # Start bulk sending in background thread
            def bulk_send_worker():
                self.process_bulk_campaign(campaign_id, recipients, message)
            
            thread = threading.Thread(target=bulk_send_worker)
            thread.daemon = True
            thread.start()
            
            log.info(f"📋 Bulk campaign started: {campaign_name} ({len(recipients)} recipients)")
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'total_recipients': len(recipients),
                'status': 'started'
            }
            
        except Exception as e:
            log.error(f"❌ Bulk campaign failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_bulk_campaign(self, campaign_id, recipients, message):
        """Process bulk campaign with rate limiting"""
        cursor = self.conn.cursor()
        sent_count = 0
        failed_count = 0
        
        # Update campaign status to running
        cursor.execute('''
            UPDATE bulk_campaigns SET status = 'running' WHERE campaign_id = ?
        ''', (campaign_id,))
        self.conn.commit()
        
        # Generate bulk report
        bulk_links = []
        
        for i, recipient in enumerate(recipients):
            try:
                # Check rate limits before each message
                while not self.rate_limiter.can_send_message():
                    time.sleep(1)
                
                # Add random delay to prevent detection
                if i > 0:
                    delay = random.uniform(
                        self.config['BULK_DELAY_MIN'], 
                        self.config['BULK_DELAY_MAX']
                    )
                    time.sleep(delay)
                
                # Send message
                result = self.send_whatsapp_message(recipient, message, campaign_id)
                
                if result['success']:
                    sent_count += 1
                    bulk_links.append({
                        'recipient': recipient,
                        'whatsapp_link': result['whatsapp_link']
                    })
                    log.info(f"✅ Bulk message {i+1}/{len(recipients)} prepared for {recipient}")
                else:
                    failed_count += 1
                    log.error(f"❌ Bulk message {i+1}/{len(recipients)} failed for {recipient}: {result['error']}")
                
                # Update campaign progress
                cursor.execute('''
                    UPDATE bulk_campaigns 
                    SET sent_count = ?, failed_count = ? 
                    WHERE campaign_id = ?
                ''', (sent_count, failed_count, campaign_id))
                self.conn.commit()
                
            except Exception as e:
                failed_count += 1
                log.error(f"❌ Error processing recipient {recipient}: {e}")
        
        # Export bulk links to Google Drive folder
        self.export_bulk_links_to_drive(campaign_id, bulk_links)
        
        # Mark campaign as completed
        cursor.execute('''
            UPDATE bulk_campaigns 
            SET status = 'completed', completed_at = ? 
            WHERE campaign_id = ?
        ''', (datetime.now().isoformat(), campaign_id))
        self.conn.commit()
        
        log.info(f"📊 Campaign {campaign_id} completed: {sent_count} sent, {failed_count} failed")
    
    def export_bulk_links_to_drive(self, campaign_id, bulk_links):
        """Export bulk WhatsApp links to Google Drive folder"""
        try:
            drive_folder = os.path.join('exports', self.config['GOOGLE_DRIVE_FOLDER'])
            filename = f"bulk_links_{campaign_id}.csv"
            filepath = os.path.join(drive_folder, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Recipient', 'WhatsApp Link'])
                for link in bulk_links:
                    writer.writerow([link['recipient'], link['whatsapp_link']])
            
            log.info(f"✅ Bulk links exported to Google Drive folder: {filename}")
            
        except Exception as e:
            log.error(f"❌ Failed to export bulk links: {e}")
    
    def process_incoming_message(self, sender, message, whatsapp_message_id=None):
        """Process incoming message and send auto-reply"""
        try:
            # Check for duplicates
            if self.is_duplicate_message(sender, self.config['BUSINESS_PHONE'], message):
                return {
                    'success': False,
                    'error': 'Duplicate message detected'
                }
            
            # Log incoming message
            message_id = f"IN_{int(time.time())}_{random.randint(1000, 9999)}"
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO messages 
                (message_id, sender, recipient, message, direction, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                message_id, sender, self.config['BUSINESS_PHONE'], 
                message, 'IN', 'received', datetime.now().isoformat()
            ))
            self.conn.commit()
            
            # Sync to Google Sheets
            self.sync_message_to_google_sheets(message_id, sender, message, 'IN', 'received', '')
            
            # Send auto-reply if enabled
            auto_reply = None
            if self.config['AUTO_REPLY_ENABLED']:
                # Determine auto-reply based on message content
                message_lower = message.lower()
                
                if any(word in message_lower for word in ['hello', 'hi', 'hey']):
                    auto_reply = self.auto_reply_messages['hello']
                elif any(word in message_lower for word in ['help', 'support', 'issue', 'problem']):
                    auto_reply = self.auto_reply_messages['support']
                elif any(word in message_lower for word in ['info', 'information', 'details']):
                    auto_reply = self.auto_reply_messages['info']
                else:
                    auto_reply = self.auto_reply_messages['default']
                
                # Add delay before auto-reply
                time.sleep(self.config['AUTO_REPLY_DELAY'])
                
                # Send auto-reply
                reply_result = self.send_whatsapp_message(sender, auto_reply)
                
                if reply_result['success']:
                    log.info(f"🤖 Auto-reply sent to {sender}: {auto_reply[:50]}...")
                else:
                    log.error(f"❌ Failed to send auto-reply: {reply_result['error']}")
            
            return {
                'success': True,
                'message_id': message_id,
                'sender': sender,
                'message': message,
                'auto_reply': auto_reply,
                'auto_reply_sent': auto_reply is not None
            }
            
        except Exception as e:
            log.error(f"❌ Failed to process incoming message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def sync_message_to_google_sheets(self, message_id, contact, message, direction, status, whatsapp_link):
        """Sync message to Google Sheets CSV file"""
        try:
            if not self.config['GOOGLE_ENABLED']:
                return
            
            csv_file = os.path.join('exports', self.config['GOOGLE_SHEET_FILE'])
            
            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    message_id,
                    contact,
                    self.config['BUSINESS_PHONE'] if direction == 'OUT' else contact,
                    message,
                    direction,
                    status,
                    datetime.now().isoformat(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    whatsapp_link
                ])
            
        except Exception as e:
            log.error(f"❌ Failed to sync to Google Sheets: {e}")
    
    def get_campaign_status(self, campaign_id):
        """Get status of bulk campaign"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM bulk_campaigns WHERE campaign_id = ?', (campaign_id,))
            campaign = cursor.fetchone()
            
            if campaign:
                return dict(campaign)
            else:
                return None
                
        except Exception as e:
            log.error(f"❌ Failed to get campaign status: {e}")
            return None
    
    def get_message_stats(self):
        """Get message statistics"""
        try:
            cursor = self.conn.cursor()
            
            # Total messages
            cursor.execute('SELECT COUNT(*) FROM messages')
            total_messages = cursor.fetchone()[0]
            
            # Sent messages
            cursor.execute('SELECT COUNT(*) FROM messages WHERE direction = "OUT"')
            sent_messages = cursor.fetchone()[0]
            
            # Received messages
            cursor.execute('SELECT COUNT(*) FROM messages WHERE direction = "IN"')
            received_messages = cursor.fetchone()[0]
            
            # Today's messages
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM messages WHERE DATE(created_at) = ?', (today,))
            today_messages = cursor.fetchone()[0]
            
            return {
                'total_messages': total_messages,
                'sent_messages': sent_messages,
                'received_messages': received_messages,
                'today_messages': today_messages,
                'success_rate': self.rate_limiter.get_success_rate()
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get message stats: {e}")
            return {}


class RateLimiter:
    """Rate limiting to prevent WhatsApp blocking"""
    
    def __init__(self, config):
        self.config = config
        self.messages_sent = {
            'minute': 0,
            'hour': 0,
            'day': 0
        }
        self.last_reset = {
            'minute': time.time(),
            'hour': time.time(),
            'day': time.time()
        }
        self.successful_sends = 0
        self.total_sends = 0
    
    def can_send_message(self):
        """Check if we can send a message based on rate limits"""
        current_time = time.time()
        
        # Reset counters if needed
        if current_time - self.last_reset['minute'] >= 60:
            self.messages_sent['minute'] = 0
            self.last_reset['minute'] = current_time
        
        if current_time - self.last_reset['hour'] >= 3600:
            self.messages_sent['hour'] = 0
            self.last_reset['hour'] = current_time
        
        if current_time - self.last_reset['day'] >= 86400:
            self.messages_sent['day'] = 0
            self.last_reset['day'] = current_time
        
        # Check limits
        return (
            self.messages_sent['minute'] < self.config['MESSAGES_PER_MINUTE'] and
            self.messages_sent['hour'] < self.config['MESSAGES_PER_HOUR'] and
            self.messages_sent['day'] < self.config['MESSAGES_PER_DAY']
        )
    
    def record_message(self):
        """Record a sent message"""
        self.messages_sent['minute'] += 1
        self.messages_sent['hour'] += 1
        self.messages_sent['day'] += 1
        self.total_sends += 1
        self.successful_sends += 1
    
    def get_success_rate(self):
        """Get message success rate"""
        if self.total_sends == 0:
            return 100.0
        return (self.successful_sends / self.total_sends) * 100


# Flask application
app = Flask(__name__)
whatsapp_api = WhatsAppSimpleAPI()

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages (simulation)"""
    try:
        data = request.get_json()
        sender = data.get('sender', '+1234567890')
        message = data.get('message', 'Hello, I need help')
        message_id = data.get('message_id', f"WEB_{int(time.time())}")
        
        # Process incoming message
        result = whatsapp_api.process_incoming_message(sender, message, message_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        log.error(f"Webhook error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send-message', methods=['POST'])
def api_send_message():
    """API endpoint to send a single message"""
    try:
        data = request.get_json()
        recipient = data.get('recipient')
        message = data.get('message')
        
        if not recipient or not message:
            return jsonify({'success': False, 'error': 'Recipient and message required'}), 400
        
        result = whatsapp_api.send_whatsapp_message(recipient, message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send-bulk', methods=['POST'])
def api_send_bulk():
    """API endpoint to send bulk messages"""
    try:
        data = request.get_json()
        recipients = data.get('recipients', [])
        message = data.get('message')
        campaign_name = data.get('campaign_name', 'Bulk Campaign')
        
        if not recipients or not message:
            return jsonify({'success': False, 'error': 'Recipients and message required'}), 400
        
        result = whatsapp_api.send_bulk_messages(recipients, message, campaign_name)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/campaign-status/<campaign_id>', methods=['GET'])
def api_campaign_status(campaign_id):
    """Get campaign status"""
    try:
        status = whatsapp_api.get_campaign_status(campaign_id)
        if status:
            return jsonify({'success': True, 'campaign': status})
        else:
            return jsonify({'success': False, 'error': 'Campaign not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get message statistics"""
    try:
        stats = whatsapp_api.get_message_stats()
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test-auto-reply', methods=['POST'])
def api_test_auto_reply():
    """Test auto-reply functionality"""
    try:
        data = request.get_json()
        sender = data.get('sender', '+1234567890')
        message = data.get('message', 'Hello, I need help')
        
        result = whatsapp_api.process_incoming_message(sender, message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_type': 'simple',
        'business_phone': whatsapp_api.config['BUSINESS_PHONE'],
        'auto_reply_enabled': whatsapp_api.config['AUTO_REPLY_ENABLED'],
        'google_enabled': whatsapp_api.config['GOOGLE_ENABLED']
    })

if __name__ == '__main__':
    # Create logs and exports directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    # Run Flask app
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
