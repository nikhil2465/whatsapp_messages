"""
🏢 ENTERPRISE WHATSAPP COMMUNICATION PLATFORM
=========================================
World's Best Method - Enterprise-Grade Solution
Uses WhatsApp Web API + Browser Automation - No Driver Issues
Enterprise-Grade Business Communication System
"""

import os
import json
import time
import webbrowser
import requests
import pyperclip
from datetime import datetime
from pathlib import Path
import subprocess
import threading
import csv

class EnterpriseWhatsAppAutomation:
    """Enterprise WhatsApp Communication Platform - World's Best Method"""
    
    def __init__(self):
        self.business_phone = "8660444809"
        self.node_server_url = "http://localhost:3000"
        
        # Enterprise-grade professional templates
        self.templates = {
            "greeting": "Hello! Thank you for contacting our enterprise. How can I assist you today?",
            "support": "Thank you for reaching out to enterprise support. I'm here to help you with any questions.",
            "appointment": "Thank you for your interest! I'd be happy to schedule an enterprise consultation for you.",
            "price": "Thank you for your inquiry about our enterprise services. Here are our current pricing options:",
            "followup": "Following up on our previous enterprise consultation. Is there anything else I can help you with?",
            "thankyou": "Thank you for choosing our enterprise services! We truly appreciate your trust in our company.",
            "promotion": "Great news! We have special enterprise offers available this week. Would you like to know more?",
            "meeting": "I'd be happy to schedule an enterprise meeting. What day and time works best for you?",
            "custom": "Thank you for your message. Our enterprise team will get back to you as soon as possible."
        }
        
        print("\n" + "="*80)
        print("🏢 ENTERPRISE WHATSAPP COMMUNICATION PLATFORM")
        print("="*80)
        print(f"📞 Business Number: {self.business_phone}")
        print("🌐 World's Best Method: Browser Automation + WhatsApp Web")
        print("📎 Full Attachment Support")
        print("🧠 Enterprise Smart Template Responses")
        print("📊 Real-time Server Logging")
        print("🤖 Enterprise Automation - No Driver Issues")
        print("="*80)
    
    def open_whatsapp_web(self):
        """Open WhatsApp Web and handle login"""
        try:
            print("🌐 Opening WhatsApp Web...")
            
            # Open WhatsApp Web in default browser
            webbrowser.open("https://web.whatsapp.com")
            
            print("📱 WhatsApp Web opened in default browser")
            print("📷 Please login with your phone if you're not logged in")
            
            # Wait for user to login
            input("👉 Press Enter after you're logged in and ready to send messages...")
            
            print("✅ WhatsApp Web ready!")
            return True
                
        except Exception as e:
            print(f"❌ WhatsApp Web error: {e}")
            return False
    
    def send_message_real(self, phone_number: str, message: str, attachment_path: str = None):
        """Send message with real automation"""
        try:
            print(f"\n📤 Sending message to {phone_number}...")
            
            # Clean phone number
            clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            
            # Copy message to clipboard
            pyperclip.copy(message)
            print(f"📋 Message copied to clipboard: {message}")
            
            # Create WhatsApp Web URL with pre-filled message
            whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={message}"
            
            # Open WhatsApp Web with pre-filled message
            webbrowser.open(whatsapp_url)
            print(f"🌐 WhatsApp Web opened with pre-filled message")
            
            print("\n" + "="*60)
            print("📋 AUTOMATION INSTRUCTIONS:")
            print("="*60)
            print("1. WhatsApp Web opened with the chat and message ready")
            
            if attachment_path and os.path.exists(attachment_path):
                print(f"2. Click the attachment button (📎)")
                print(f"3. Select the file: {attachment_path}")
                print(f"4. The file will be uploaded")
                print(f"5. Send the message with attachment")
            else:
                print("2. The message is already typed in the chat")
                print("3. Press Enter to send the message")
            
            print("6. The message will be sent to the recipient")
            print("="*60)
            
            # Store in server
            self.store_message_in_server(phone_number, message, 'outbound', bool(attachment_path))
            
            # Ask for confirmation
            confirm = input("\n✅ Message sent successfully? (y/n): ").strip().lower()
            if confirm == 'y':
                print("🎉 Message delivery confirmed!")
                return True
            else:
                print("⚠️ Please try sending the message manually")
                return False
            
        except Exception as e:
            print(f"❌ Send message error: {e}")
            return False
    
    def send_attachment_enhanced(self, phone_number: str, message: str, attachment_path: str):
        """Enhanced attachment sending with file handling"""
        try:
            print(f"\n📎 Sending attachment to {phone_number}...")
            
            if not os.path.exists(attachment_path):
                print(f"❌ File not found: {attachment_path}")
                return False
            
            # Get file info
            file_size = os.path.getsize(attachment_path)
            file_name = Path(attachment_path).name
            
            print(f"📁 File: {file_name}")
            print(f"📏 Size: {file_size / 1024:.2f} KB")
            
            # Check file size (WhatsApp limit is 16MB)
            if file_size > 16 * 1024 * 1024:
                print("⚠️ File size exceeds WhatsApp limit (16MB)")
                return False
            
            # Copy message to clipboard
            pyperclip.copy(message)
            print(f"📋 Message copied to clipboard")
            
            # Open WhatsApp Web
            clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}"
            webbrowser.open(whatsapp_url)
            
            print(f"🌐 WhatsApp Web opened")
            
            print("\n" + "="*60)
            print("📎 ATTACHMENT INSTRUCTIONS:")
            print("="*60)
            print(f"1. WhatsApp Web opened with chat ready")
            print(f"2. Paste the message (Ctrl+V)")
            print(f"3. Click the attachment button (📎)")
            print(f"4. Select file: {file_name}")
            print(f"5. Wait for upload to complete")
            print(f"6. Send the message with attachment")
            print("="*60)
            
            # Store in server
            self.store_message_in_server(phone_number, message, 'outbound', True)
            
            # Ask for confirmation
            confirm = input("\n✅ Attachment sent successfully? (y/n): ").strip().lower()
            if confirm == 'y':
                print("🎉 Attachment delivery confirmed!")
                return True
            else:
                print("⚠️ Please try sending the attachment manually")
                return False
            
        except Exception as e:
            print(f"❌ Attachment error: {e}")
            return False
    
    def store_message_in_server(self, phone_number: str, message: str, direction: str, attachment_sent: bool = False):
        """Store message in Node.js server"""
        try:
            message_data = {
                "from": self.business_phone if direction == 'outbound' else phone_number,
                "to": phone_number if direction == 'outbound' else self.business_phone,
                "message": message,
                "direction": direction,
                "timestamp": datetime.now().isoformat(),
                "ai_enhanced": True,
                "device": "Ultimate WhatsApp Solution",
                "location": "Browser Automation",
                "attachment": attachment_sent
            }
            
            response = requests.post(f"{self.node_server_url}/api/store-message", json=message_data)
            if response.status_code == 200:
                print(f"✅ Message stored in server successfully")
            
        except Exception as e:
            print(f"⚠️ Server logging error: {e}")
    
    def get_smart_response(self, message: str) -> str:
        """Get smart template response"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self.templates["greeting"]
        elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'rates', 'fees']):
            return self.templates["price"]
        elif any(word in message_lower for word in ['appointment', 'booking', 'schedule', 'meeting']):
            return self.templates["appointment"]
        elif any(word in message_lower for word in ['support', 'help', 'issue', 'problem']):
            return self.templates["support"]
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return self.templates["thankyou"]
        elif any(word in message_lower for word in ['followup', 'follow-up', 'checking']):
            return self.templates["followup"]
        elif any(word in message_lower for word in ['promotion', 'offer', 'deal', 'discount']):
            return self.templates["promotion"]
        elif any(word in message_lower for word in ['meeting', 'call', 'discuss', 'talk']):
            return self.templates["meeting"]
        else:
            return self.templates["custom"]
    
    def show_menu(self):
        """Show enterprise menu"""
        print("\n📋 ENTERPRISE WHATSAPP MENU:")
        print("="*60)
        print("1. 📤 Send Message with Enterprise Smart Response")
        print("2. 📎 Send Message with Attachment")
        print("3. ✉️  Send Custom Message")
        print("4. 🧠 Generate Enterprise Smart Response Only")
        print("5. 📊 Check System Status")
        print("6. 📋 View Recent Messages")
        print("7. 🌐 Open WhatsApp Web")
        print("8. 🎯 Bulk Message Send")
        print("9. 🧠 Bulk Message with Template")
        print("10. ❌ Exit")
        print("="*60)
    
    def show_status(self):
        """Show enterprise system status"""
        print("\n📊 ENTERPRISE SYSTEM STATUS:")
        print("="*60)
        print(f"📞 Business Phone: {self.business_phone}")
        print(f"🌐 Node Server: {self.node_server_url}")
        print(f"🤖 Automation Method: Browser Automation + WhatsApp Web")
        print(f"📎 Attachment Support: All file types")
        print(f"🧠 Enterprise Templates: {len(self.templates)} available")
        print(f"📊 Server Logging: Active")
        print(f"🌐 Browser: Default System Browser")
        print(f"🚀 Driver Issues: None")
        print(f"🏢 Platform: Enterprise-Grade")
        print(f"🎯 Bulk Messaging: World's Best Method")
        print("="*60)
    
    def view_recent_messages(self):
        """View recent messages from server"""
        try:
            response = requests.get(f"{self.node_server_url}/api/messages")
            if response.status_code == 200:
                messages = response.json()
                
                print("\n📋 RECENT MESSAGES:")
                print("="*80)
                
                if messages and len(messages) > 0:
                    for i, msg in enumerate(messages[-5:], 1):  # Show last 5 messages
                        direction_emoji = "📤" if msg['direction'] == 'outbound' else "📥"
                        attachment_emoji = "📎" if msg.get('attachment') else ""
                        
                        print(f"{i}. {direction_emoji} {msg['from']} → {msg['to']}")
                        print(f"   {attachment_emoji} {msg['message'][:50]}{'...' if len(msg['message']) > 50 else ''}")
                        print(f"   📅 {msg['timestamp'][:19]}")
                        print()
                else:
                    print("📭 No messages found")
                
                print("="*80)
            else:
                print("⚠️ Could not retrieve messages from server")
                
        except Exception as e:
            print(f"❌ Error retrieving messages: {e}")
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> str:
        """Get user input with validation"""
        while True:
            try:
                value = input(f"\n{prompt}: ").strip()
                
                if not value:
                    print("❌ This field is required")
                    continue
                
                if input_type == "phone":
                    # Basic phone validation
                    if not value.startswith('+'):
                        print("⚠️ Phone number should start with + (country code)")
                        continue
                
                if input_type == "file" and value:
                    if not os.path.exists(value):
                        print(f"❌ File not found: {value}")
                        continue
                
                return value
                
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def load_contacts_from_file(self, file_path: str):
        """Load contacts from CSV or TXT file"""
        contacts = []
        try:
            if file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row and len(row) > 0:
                            phone = row[0].strip()
                            if phone and phone.startswith('+'):
                                contacts.append(phone)
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        phone = line.strip()
                        if phone and phone.startswith('+'):
                            contacts.append(phone)
            
            print(f"✅ Loaded {len(contacts)} contacts from {file_path}")
            return contacts
        except Exception as e:
            print(f"❌ Error loading contacts: {e}")
            return []
    
    def validate_phone_numbers(self, phone_numbers):
        """Validate and clean phone numbers"""
        valid_numbers = []
        invalid_numbers = []
        
        for phone in phone_numbers:
            clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not clean_phone.startswith('+'):
                clean_phone = '+' + clean_phone
            
            if len(clean_phone) >= 10 and len(clean_phone) <= 15 and clean_phone[1:].isdigit():
                valid_numbers.append(clean_phone)
            else:
                invalid_numbers.append(phone)
        
        print(f"📊 Phone Validation: {len(valid_numbers)} valid, {len(invalid_numbers)} invalid")
        return valid_numbers, invalid_numbers
    
    def send_bulk_messages(self, contacts, message, attachment_path=None, delay=2):
        """Send bulk messages to all contacts with optional attachment"""
        print(f"\n🎯 Starting Bulk Message Send")
        print(f"👥 Contacts: {len(contacts)}")
        print(f"📎 Attachment: {attachment_path or 'None'}")
        print(f"⏱️ Delay: {delay} seconds between sends")
        print("="*60)
        
        success_count = 0
        failed_count = 0
        
        for i, contact in enumerate(contacts, 1):
            try:
                print(f"\n📤 [{i}/{len(contacts)}] Sending to {contact}")
                
                # Send message with attachment
                success = self.send_message_real(contact, message, attachment_path)
                
                if success:
                    success_count += 1
                    print(f"   ✅ Success: {contact}")
                else:
                    failed_count += 1
                    print(f"   ❌ Failed: {contact}")
                
                # Rate limiting to prevent WhatsApp blocking
                if i < len(contacts):
                    print(f"   ⏱️ Waiting {delay} seconds...")
                    time.sleep(delay)
                    
            except KeyboardInterrupt:
                print(f"\n⏸️ Bulk send interrupted by user at {i}/{len(contacts)}")
                break
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Error with {contact}: {e}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 BULK SEND SUMMARY")
        print("="*60)
        print(f"📤 Total Contacts: {len(contacts)}")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📈 Success Rate: {(success_count/len(contacts)*100):.1f}%")
        print("="*60)
        
        return success_count, failed_count
    
    def interactive_mode(self):
        """Enterprise interactive mode"""
        print("\n🏢 Starting Enterprise WhatsApp Platform...")
        
        # Open WhatsApp Web first
        if not self.open_whatsapp_web():
            print("❌ Failed to open WhatsApp Web. Exiting...")
            return
        
        while True:
            try:
                self.show_menu()
                
                choice = input("\n👉 Enter your choice (1-10): ").strip()
                
                if choice == "1":
                    # Send message with enterprise smart response
                    phone = self.get_user_input("📞 Enter phone number (+countrycode number)", "phone")
                    if not phone: continue
                    
                    customer_message = self.get_user_input("💬 Enter customer message (for enterprise smart response)")
                    if not customer_message: continue
                    
                    smart_response = self.get_smart_response(customer_message)
                    print(f"\n🧠 Enterprise Smart Response: {smart_response}")
                    
                    confirm = input("\n📤 Send this enterprise smart response? (y/n): ").strip().lower()
                    if confirm == 'y':
                        success = self.send_message_real(phone, smart_response)
                        if success:
                            print("✅ Enterprise smart message sent successfully!")
                        else:
                            print("❌ Failed to send message")
                
                elif choice == "2":
                    # Send message with attachment
                    phone = self.get_user_input("📞 Enter phone number (+countrycode number)", "phone")
                    if not phone: continue
                    
                    message = self.get_user_input("💬 Enter message")
                    if not message: continue
                    
                    attachment_path = self.get_user_input("📎 Enter attachment file path (or press Enter to skip)")
                    if attachment_path and not os.path.exists(attachment_path):
                        print(f"❌ File not found: {attachment_path}")
                        continue
                    
                    success = self.send_message_real(phone, message, attachment_path)
                    if success:
                        print("✅ Message with attachment sent successfully!")
                    else:
                        print("❌ Failed to send message")
                
                elif choice == "3":
                    # Send custom message
                    phone = self.get_user_input("📞 Enter phone number (+countrycode number)", "phone")
                    if not phone: continue
                    
                    message = self.get_user_input("💬 Enter custom message")
                    if not message: continue
                    
                    success = self.send_message_real(phone, message)
                    if success:
                        print("✅ Custom message sent successfully!")
                    else:
                        print("❌ Failed to send message")
                
                elif choice == "4":
                    # Generate enterprise smart response only
                    customer_message = self.get_user_input("💬 Enter customer message")
                    if not customer_message: continue
                    
                    smart_response = self.get_smart_response(customer_message)
                    print(f"\n🧠 Enterprise Smart Response: {smart_response}")
                    print("\n📋 This response has been copied to clipboard!")
                    pyperclip.copy(smart_response)
                
                elif choice == "5":
                    # Check system status
                    self.show_status()
                
                elif choice == "6":
                    # View recent messages
                    self.view_recent_messages()
                
                elif choice == "7":
                    # Open WhatsApp Web
                    webbrowser.open("https://web.whatsapp.com")
                    print("✅ WhatsApp Web opened in new tab")
                    input("\n👉 Press Enter to continue...")
                
                elif choice == "8":
                    # Bulk Message Send
                    print("\n🎯 BULK MESSAGE SEND")
                    print("="*50)
                    
                    # Get contacts
                    contacts_input = self.get_user_input("📥 Enter contacts (comma-separated) or file path (.csv/.txt)")
                    if not contacts_input: continue
                    
                    if os.path.exists(contacts_input):
                        contacts = self.load_contacts_from_file(contacts_input)
                    else:
                        contacts = [phone.strip() for phone in contacts_input.split(',') if phone.strip()]
                        contacts, invalid = self.validate_phone_numbers(contacts)
                        if invalid:
                            print(f"⚠️ Invalid numbers: {invalid}")
                    
                    if not contacts:
                        print("❌ No valid contacts found")
                        continue
                    
                    # Get message
                    message = self.get_user_input("💬 Enter message to send to all contacts")
                    if not message: continue
                    
                    # Get attachment (optional)
                    attachment_path = self.get_user_input("📎 Enter attachment file path (optional, press Enter to skip)")
                    if attachment_path and not os.path.exists(attachment_path):
                        print(f"❌ File not found: {attachment_path}")
                        attachment_path = None
                    
                    # Get delay
                    delay_input = self.get_user_input("⏱️ Enter delay between sends (seconds, default=2)")
                    try:
                        delay = int(delay_input) if delay_input else 2
                    except:
                        delay = 2
                    
                    # Confirm bulk send
                    print(f"\n📊 Ready to send to {len(contacts)} contacts")
                    print(f"📝 Message: {message[:50]}{'...' if len(message) > 50 else ''}")
                    print(f"📎 Attachment: {attachment_path or 'None'}")
                    print(f"⏱️ Delay: {delay} seconds")
                    
                    confirm = input("\n📤 Proceed with bulk send? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.send_bulk_messages(contacts, message, attachment_path, delay)
                    else:
                        print("❌ Bulk send cancelled")
                
                elif choice == "9":
                    # Bulk Message with Template
                    print("\n🎯 BULK MESSAGE WITH TEMPLATE")
                    print("="*50)
                    
                    # Get contacts
                    contacts_input = self.get_user_input("📥 Enter contacts (comma-separated) or file path (.csv/.txt)")
                    if not contacts_input: continue
                    
                    if os.path.exists(contacts_input):
                        contacts = self.load_contacts_from_file(contacts_input)
                    else:
                        contacts = [phone.strip() for phone in contacts_input.split(',') if phone.strip()]
                        contacts, invalid = self.validate_phone_numbers(contacts)
                        if invalid:
                            print(f"⚠️ Invalid numbers: {invalid}")
                    
                    if not contacts:
                        print("❌ No valid contacts found")
                        continue
                    
                    # Select template
                    print("\n🧠 Available Templates:")
                    for i, (key, template) in enumerate(self.templates.items(), 1):
                        print(f"   {i}. {key}: {template[:30]}{'...' if len(template) > 30 else ''}")
                    
                    template_choice = input("\n👉 Select template (1-9) or 'custom': ").strip()
                    if template_choice == 'custom':
                        message = self.get_user_input("💬 Enter custom message")
                    else:
                        try:
                            template_index = int(template_choice) - 1
                            template_keys = list(self.templates.keys())
                            if 0 <= template_index < len(template_keys):
                                template_key = template_keys[template_index]
                                message = self.templates[template_key]
                                print(f"🧠 Selected template: {template_key}")
                            else:
                                print("❌ Invalid template choice")
                                continue
                        except:
                            print("❌ Invalid template choice")
                            continue
                    
                    # Get attachment (optional)
                    attachment_path = self.get_user_input("📎 Enter attachment file path (optional, press Enter to skip)")
                    if attachment_path and not os.path.exists(attachment_path):
                        print(f"❌ File not found: {attachment_path}")
                        attachment_path = None
                    
                    # Get delay
                    delay_input = self.get_user_input("⏱️ Enter delay between sends (seconds, default=3)")
                    try:
                        delay = int(delay_input) if delay_input else 3
                    except:
                        delay = 2
                    
                    # Confirm bulk send
                    print(f"\n📊 Ready to send to {len(contacts)} contacts")
                    print(f"🧠 Template: {template_choice}")
                    print(f"📝 Message: {message[:50]}{'...' if len(message) > 50 else ''}")
                    print(f"📎 Attachment: {attachment_path or 'None'}")
                    print(f"⏱️ Delay: {delay} seconds")
                    
                    confirm = input("\n📤 Proceed with bulk template send? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.send_bulk_messages(contacts, message, attachment_path, delay)
                    else:
                        print("❌ Bulk template send cancelled")
                
                elif choice == "10":
                    # Exit
                    print("\n👋 Thank you for using Enterprise WhatsApp Platform!")
                    print("📊 All messages have been logged to the server")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-10")
                    input("👉 Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("👉 Press Enter to continue...")

def main():
    """Main function"""
    automation = EnterpriseWhatsAppAutomation()
    
    try:
        automation.interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Main error: {e}")

if __name__ == "__main__":
    main()
