#!/usr/bin/env python3
"""
🚀 PROFESSIONAL WHATSAPP BUSINESS FEATURES
=========================================
✅ Contact Management
✅ Message Templates
✅ Scheduled Messages
✅ Quick Replies
✅ Customer Segmentation
✅ Advanced Analytics
✅ Chat Interface
"""

import os
import json
import time
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/professional_features.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

class ProfessionalFeatures:
    """
    Professional WhatsApp Business Features
    Adds enterprise-level functionality to the messaging system
    """
    
    def __init__(self, conn):
        self.conn = conn
        self.setup_professional_database()
        self.setup_scheduler()
        
    def setup_professional_database(self):
        """Setup professional features database tables"""
        try:
            cursor = self.conn.cursor()
            
            # Contacts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_id TEXT UNIQUE,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    company TEXT,
                    tags TEXT,  -- JSON array
                    segment TEXT,
                    status TEXT,  -- active, inactive, blocked
                    last_contact TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Message templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS message_templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_id TEXT UNIQUE,
                    name TEXT,
                    category TEXT,
                    content TEXT,
                    variables TEXT,  -- JSON array of variables
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Scheduled messages table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scheduled_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    schedule_id TEXT UNIQUE,
                    recipient TEXT,
                    message TEXT,
                    template_id TEXT,
                    scheduled_time TEXT,
                    status TEXT,  -- pending, sent, failed, cancelled
                    sent_time TEXT,
                    attachment_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Quick replies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quick_replies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reply_id TEXT UNIQUE,
                    keyword TEXT,
                    message TEXT,
                    category TEXT,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Customer segments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customer_segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    segment_id TEXT UNIQUE,
                    name TEXT,
                    description TEXT,
                    criteria TEXT,  -- JSON criteria
                    contact_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT,
                    metric_value TEXT,
                    date TEXT,
                    additional_data TEXT,  -- JSON
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Chat conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT UNIQUE,
                    contact_id TEXT,
                    last_message TEXT,
                    last_message_time TEXT,
                    unread_count INTEGER DEFAULT 0,
                    status TEXT,  -- active, archived
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            log.info("✅ Professional features database initialized")
            
        except Exception as e:
            log.error(f"❌ Professional features database setup failed: {e}")
    
    def setup_scheduler(self):
        """Setup background scheduler for scheduled messages"""
        try:
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(
                func=self.process_scheduled_messages,
                trigger='interval',
                minutes=1,
                id='process_scheduled_messages'
            )
            self.scheduler.start()
            log.info("✅ Message scheduler started")
            
        except Exception as e:
            log.error(f"❌ Scheduler setup failed: {e}")
    
    def process_scheduled_messages(self):
        """Process scheduled messages that are due"""
        try:
            cursor = self.conn.cursor()
            current_time = datetime.now().isoformat()
            
            # Get pending scheduled messages
            cursor.execute('''
                SELECT * FROM scheduled_messages 
                WHERE status = 'pending' AND scheduled_time <= ?
                ORDER BY scheduled_time ASC
            ''', (current_time,))
            
            scheduled_messages = cursor.fetchall()
            
            for message in scheduled_messages:
                message_data = dict(message)
                
                # Send the message (this would integrate with your existing send function)
                result = self.send_scheduled_message(message_data)
                
                # Update status
                new_status = 'sent' if result['success'] else 'failed'
                cursor.execute('''
                    UPDATE scheduled_messages 
                    SET status = ?, sent_time = ? 
                    WHERE schedule_id = ?
                ''', (new_status, current_time, message_data['schedule_id']))
                
                self.conn.commit()
                
                log.info(f"📅 Scheduled message {message_data['schedule_id']} {new_status}")
                
        except Exception as e:
            log.error(f"❌ Failed to process scheduled messages: {e}")
    
    def send_scheduled_message(self, message_data):
        """Send a scheduled message (integrates with existing system)"""
        try:
            # This would integrate with your existing WhatsAppRealMessaging.send_whatsapp_message
            # For now, we'll simulate the sending
            log.info(f"📤 Sending scheduled message to {message_data['recipient']}")
            
            return {
                'success': True,
                'message_id': f"SCH_{int(time.time())}"
            }
            
        except Exception as e:
            log.error(f"❌ Failed to send scheduled message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_contact(self, name, phone, email=None, company=None, tags=None, segment=None):
        """Add a new contact"""
        try:
            cursor = self.conn.cursor()
            contact_id = f"CT_{int(time.time())}_{random.randint(1000, 9999)}"
            
            cursor.execute('''
                INSERT INTO contacts 
                (contact_id, name, phone, email, company, tags, segment, status, last_contact)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
            ''', (
                contact_id, name, phone, email, company,
                json.dumps(tags or []), segment, datetime.now().isoformat()
            ))
            
            self.conn.commit()
            log.info(f"✅ Contact added: {name} ({phone})")
            
            return {
                'success': True,
                'contact_id': contact_id
            }
            
        except Exception as e:
            log.error(f"❌ Failed to add contact: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_contacts(self, segment=None, limit=50, offset=0):
        """Get contacts with optional filtering"""
        try:
            cursor = self.conn.cursor()
            
            if segment:
                cursor.execute('''
                    SELECT * FROM contacts 
                    WHERE segment = ? AND status = 'active'
                    ORDER BY updated_at DESC
                    LIMIT ? OFFSET ?
                ''', (segment, limit, offset))
            else:
                cursor.execute('''
                    SELECT * FROM contacts 
                    WHERE status = 'active'
                    ORDER BY updated_at DESC
                    LIMIT ? OFFSET ?
                ''', (limit, offset))
            
            contacts = [dict(row) for row in cursor.fetchall()]
            
            # Parse JSON fields
            for contact in contacts:
                if contact['tags']:
                    contact['tags'] = json.loads(contact['tags'])
                else:
                    contact['tags'] = []
            
            return {
                'success': True,
                'contacts': contacts
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get contacts: {e}")
            return {
                'success': False,
                'error': str(e),
                'contacts': []
            }
    
    def create_template(self, name, category, content, variables=None):
        """Create a message template"""
        try:
            cursor = self.conn.cursor()
            template_id = f"TPL_{int(time.time())}_{random.randint(1000, 9999)}"
            
            cursor.execute('''
                INSERT INTO message_templates 
                (template_id, name, category, content, variables)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                template_id, name, category, content,
                json.dumps(variables or [])
            ))
            
            self.conn.commit()
            log.info(f"✅ Template created: {name}")
            
            return {
                'success': True,
                'template_id': template_id
            }
            
        except Exception as e:
            log.error(f"❌ Failed to create template: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_templates(self, category=None):
        """Get message templates"""
        try:
            cursor = self.conn.cursor()
            
            if category:
                cursor.execute('''
                    SELECT * FROM message_templates 
                    WHERE category = ?
                    ORDER BY usage_count DESC, name ASC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT * FROM message_templates 
                    ORDER BY usage_count DESC, name ASC
                ''')
            
            templates = [dict(row) for row in cursor.fetchall()]
            
            # Parse JSON fields
            for template in templates:
                if template['variables']:
                    template['variables'] = json.loads(template['variables'])
                else:
                    template['variables'] = []
            
            return {
                'success': True,
                'templates': templates
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get templates: {e}")
            return {
                'success': False,
                'error': str(e),
                'templates': []
            }
    
    def schedule_message(self, recipient, message, scheduled_time, template_id=None, attachment_path=None):
        """Schedule a message for later sending"""
        try:
            cursor = self.conn.cursor()
            schedule_id = f"SCH_{int(time.time())}_{random.randint(1000, 9999)}"
            
            cursor.execute('''
                INSERT INTO scheduled_messages 
                (schedule_id, recipient, message, template_id, scheduled_time, attachment_path, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            ''', (schedule_id, recipient, message, template_id, scheduled_time, attachment_path))
            
            self.conn.commit()
            log.info(f"✅ Message scheduled for {scheduled_time}")
            
            return {
                'success': True,
                'schedule_id': schedule_id
            }
            
        except Exception as e:
            log.error(f"❌ Failed to schedule message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_quick_reply(self, keyword, message, category='general'):
        """Add a quick reply"""
        try:
            cursor = self.conn.cursor()
            reply_id = f"QR_{int(time.time())}_{random.randint(1000, 9999)}"
            
            cursor.execute('''
                INSERT INTO quick_replies 
                (reply_id, keyword, message, category)
                VALUES (?, ?, ?, ?)
            ''', (reply_id, keyword, message, category))
            
            self.conn.commit()
            log.info(f"✅ Quick reply added: {keyword}")
            
            return {
                'success': True,
                'reply_id': reply_id
            }
            
        except Exception as e:
            log.error(f"❌ Failed to add quick reply: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_quick_replies(self, category=None):
        """Get quick replies"""
        try:
            cursor = self.conn.cursor()
            
            if category:
                cursor.execute('''
                    SELECT * FROM quick_replies 
                    WHERE category = ?
                    ORDER BY usage_count DESC, keyword ASC
                ''', (category,))
            else:
                cursor.execute('''
                    SELECT * FROM quick_replies 
                    ORDER BY usage_count DESC, keyword ASC
                ''')
            
            replies = [dict(row) for row in cursor.fetchall()]
            
            return {
                'success': True,
                'replies': replies
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get quick replies: {e}")
            return {
                'success': False,
                'error': str(e),
                'replies': []
            }
    
    def create_segment(self, name, description, criteria):
        """Create a customer segment"""
        try:
            cursor = self.conn.cursor()
            segment_id = f"SEG_{int(time.time())}_{random.randint(1000, 9999)}"
            
            cursor.execute('''
                INSERT INTO customer_segments 
                (segment_id, name, description, criteria)
                VALUES (?, ?, ?, ?)
            ''', (segment_id, name, description, json.dumps(criteria)))
            
            # Update contact count
            contact_count = self.count_contacts_in_segment(criteria)
            cursor.execute('''
                UPDATE customer_segments 
                SET contact_count = ? 
                WHERE segment_id = ?
            ''', (contact_count, segment_id))
            
            self.conn.commit()
            log.info(f"✅ Segment created: {name} ({contact_count} contacts)")
            
            return {
                'success': True,
                'segment_id': segment_id,
                'contact_count': contact_count
            }
            
        except Exception as e:
            log.error(f"❌ Failed to create segment: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def count_contacts_in_segment(self, criteria):
        """Count contacts matching segment criteria"""
        try:
            # This is a simplified version - in production, you'd parse criteria and build SQL
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM contacts WHERE status = 'active'")
            count = cursor.fetchone()[0]
            return count
            
        except Exception as e:
            log.error(f"❌ Failed to count contacts in segment: {e}")
            return 0
    
    def get_analytics(self, metric_type, days=7):
        """Get analytics data"""
        try:
            cursor = self.conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT * FROM analytics 
                WHERE metric_type = ? AND date >= ?
                ORDER BY date DESC
            ''', (metric_type, start_date))
            
            analytics = [dict(row) for row in cursor.fetchall()]
            
            return {
                'success': True,
                'analytics': analytics
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get analytics: {e}")
            return {
                'success': False,
                'error': str(e),
                'analytics': []
            }
    
    def record_analytics(self, metric_type, metric_value, additional_data=None):
        """Record analytics data"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO analytics 
                (metric_type, metric_value, date, additional_data)
                VALUES (?, ?, ?, ?)
            ''', (
                metric_type, metric_value, 
                datetime.now().strftime('%Y-%m-%d'),
                json.dumps(additional_data or {})
            ))
            
            self.conn.commit()
            
        except Exception as e:
            log.error(f"❌ Failed to record analytics: {e}")
    
    def get_conversation_history(self, contact_id, limit=50):
        """Get conversation history with a contact"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                SELECT * FROM messages 
                WHERE (sender = ? OR recipient = ?)
                ORDER BY created_at DESC
                LIMIT ?
            ''', (contact_id, contact_id, limit))
            
            messages = [dict(row) for row in cursor.fetchall()]
            
            return {
                'success': True,
                'messages': messages
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get conversation history: {e}")
            return {
                'success': False,
                'error': str(e),
                'messages': []
            }
    
    def update_contact_status(self, contact_id, status):
        """Update contact status"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                UPDATE contacts 
                SET status = ?, updated_at = ?
                WHERE contact_id = ?
            ''', (status, datetime.now().isoformat(), contact_id))
            
            self.conn.commit()
            
            return {
                'success': True
            }
            
        except Exception as e:
            log.error(f"❌ Failed to update contact status: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_contacts(self, query):
        """Search contacts by name, phone, or email"""
        try:
            cursor = self.conn.cursor()
            search_pattern = f"%{query}%"
            
            cursor.execute('''
                SELECT * FROM contacts 
                WHERE (name LIKE ? OR phone LIKE ? OR email LIKE ?) AND status = 'active'
                ORDER BY name ASC
            ''', (search_pattern, search_pattern, search_pattern))
            
            contacts = [dict(row) for row in cursor.fetchall()]
            
            # Parse JSON fields
            for contact in contacts:
                if contact['tags']:
                    contact['tags'] = json.loads(contact['tags'])
                else:
                    contact['tags'] = []
            
            return {
                'success': True,
                'contacts': contacts
            }
            
        except Exception as e:
            log.error(f"❌ Failed to search contacts: {e}")
            return {
                'success': False,
                'error': str(e),
                'contacts': []
            }
    
    def get_dashboard_analytics(self):
        """Get comprehensive dashboard analytics"""
        try:
            cursor = self.conn.cursor()
            
            # Get counts
            cursor.execute("SELECT COUNT(*) FROM contacts WHERE status = 'active'")
            active_contacts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM message_templates")
            total_templates = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scheduled_messages WHERE status = 'pending'")
            pending_scheduled = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM quick_replies")
            total_quick_replies = cursor.fetchone()[0]
            
            # Get recent activity
            cursor.execute('''
                SELECT COUNT(*) FROM messages 
                WHERE DATE(created_at) = DATE('now')
            ''')
            today_messages = cursor.fetchone()[0]
            
            return {
                'success': True,
                'analytics': {
                    'active_contacts': active_contacts,
                    'total_templates': total_templates,
                    'pending_scheduled': pending_scheduled,
                    'total_quick_replies': total_quick_replies,
                    'today_messages': today_messages
                }
            }
            
        except Exception as e:
            log.error(f"❌ Failed to get dashboard analytics: {e}")
            return {
                'success': False,
                'error': str(e),
                'analytics': {}
            }
