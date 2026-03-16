# 🚀 Simple WhatsApp Business System

A **no-registration-required** WhatsApp messaging system with Google Sheets integration and automated replies.

## ✨ Key Features

- 🤖 **Automated Replies** for +8861655542 with intelligent responses
- 📊 **Bulk Messaging** with WhatsApp Web links generation
- 📱 **No Registration Required** - Uses WhatsApp Web links
- 📈 **Google Sheets Integration** via CSV export
- 🛡️ **Anti-Blocking System** with advanced rate limiting
- 🎯 **Campaign Management** with real-time tracking
- 📊 **Analytics Dashboard** with live statistics
- 🔗 **WhatsApp Web Links** - Click to send messages

## 🚀 Quick Start (2 minutes)

### 1. Run the System

**Windows:**
```bash
double-click START_SIMPLE.bat
```

**Manual:**
```bash
pip install -r requirements_simple.txt
python simple_main_system.py
```

### 2. Access Dashboard

Visit: `http://localhost:5000`

### 3. Send Messages

1. **Single Message**: Enter phone number and message → Click "Generate WhatsApp Link"
2. **Bulk Messages**: Add recipients → Enter message → Click "Generate Bulk Links"
3. **Auto-Reply**: Test with "Test Auto-Reply" section

## 📱 How It Works

### WhatsApp Web Links
- System generates WhatsApp Web links (wa.me/...)
- Click link to open WhatsApp with pre-filled message
- Send message manually in WhatsApp
- No API registration required

### Google Sheets Integration
- All messages automatically exported to CSV
- Import CSV to Google Sheets in one click
- Duplicate prevention with message hashing
- Organized data structure

### Automated Replies
- Intelligent responses for +8861655542
- Context-aware replies based on message content
- 5-second delay for natural conversation
- Customizable response templates

## 📊 API Endpoints

### Messaging
- `POST /api/send-single` - Generate WhatsApp link for single message
- `POST /api/send-bulk` - Generate WhatsApp links for bulk messages
- `POST /api/test-auto-reply` - Test auto-reply functionality

### Analytics
- `GET /api/stats` - System statistics
- `GET /api/campaigns` - List all campaigns
- `GET /api/messages` - Message history
- `GET /api/health` - System health check

### Google Integration
- `GET /api/export-google-sheets` - Export messages to CSV

### Webhook
- `POST /webhook/whatsapp` - Handle incoming messages (simulation)

## 🤖 Automated Replies

### Default Responses
- **Hello messages**: "Hello! Welcome to our service. How can we help you today?"
- **Support requests**: "Thank you for reaching out to support. Our team will assist you within 24 hours."
- **Information requests**: "For more information, please visit our website or reply with 'help'."
- **Default**: "Thank you for contacting us! This is an automated reply. We'll get back to you shortly."

### Customization
Edit `auto_reply_messages` in `whatsapp_simple_api.py` to customize responses.

## 📊 Bulk Messaging

### Process
1. Add recipients (comma-separated)
2. Enter message content
3. Provide campaign name
4. System generates WhatsApp links for all recipients
5. Links exported to CSV in `exports/whatsapp_exports/`
6. Click links to send messages manually

### Anti-Blocking Features
- **Rate Limiting**: 30 messages/minute, 1000/hour, 10,000/day
- **Random Delays**: 3-8 seconds between link generation
- **Duplicate Prevention**: Message hashing and deduplication
- **Progress Tracking**: Real-time campaign monitoring

## 📈 Google Sheets Integration

### Automatic Export
- All messages logged to `exports/whatsapp_messages.csv`
- Bulk links exported to `exports/whatsapp_exports/`
- CSV format for easy Google Sheets import
- Real-time synchronization

### Import to Google Sheets
1. Open Google Sheets
2. File → Import → Upload
3. Select CSV file from `exports/` folder
4. Choose "Replace spreadsheet" or "Insert new sheet(s)"

### Data Structure
```
Message ID, Sender, Recipient, Message, Direction, Status, Timestamp, Created At, WhatsApp Link
```

## 🛡️ Rate Limiting

### Configurable Limits
```env
MESSAGES_PER_MINUTE=30
MESSAGES_PER_HOUR=1000
MESSAGES_PER_DAY=10000
BULK_DELAY_MIN=3.0
BULK_DELAY_MAX=8.0
```

### Protection Features
- Automatic rate limiting
- Message queuing
- Failed message tracking
- Real-time monitoring

## 📊 Dashboard Features

### Real-time Statistics
- Total messages sent/received
- Active campaigns
- Rate limiting status
- System health indicators

### Campaign Management
- Create new campaigns
- Monitor progress
- View delivery statistics
- Export campaign data

### Message History
- View all messages
- Filter by direction/status
- WhatsApp links for sent messages
- Export capabilities

## 🔧 Configuration

### Environment Variables

```env
# Business Configuration
BUSINESS_PHONE=+8861655542
BUSINESS_NAME=Your Business Name
BUSINESS_EMAIL=business@yourdomain.com

# WhatsApp Web Configuration
USE_WHATSAPP_WEB=True
WHATSAPP_WEB_SESSION=session.json

# Rate Limiting
MESSAGES_PER_MINUTE=30
MESSAGES_PER_HOUR=1000
MESSAGES_PER_DAY=10000
BULK_DELAY_MIN=3.0
BULK_DELAY_MAX=8.0

# Auto-Reply
AUTO_REPLY_ENABLED=True
AUTO_REPLY_DELAY=5

# Google Integration
GOOGLE_ENABLED=True
GOOGLE_SHEET_FILE=whatsapp_messages.csv
GOOGLE_DRIVE_FOLDER=whatsapp_exports

# Flask
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
```

## 📋 Usage Examples

### Send Single Message

```bash
curl -X POST http://localhost:5000/api/send-single \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": "+1234567890",
    "message": "Hello from WhatsApp Business!"
  }'
```

### Send Bulk Messages

```bash
curl -X POST http://localhost:5000/api/send-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "recipients": ["+1234567890", "+9876543210"],
    "message": "Hello everyone! This is a bulk message.",
    "campaign_name": "Marketing Campaign"
  }'
```

### Test Auto-Reply

```bash
curl -X POST http://localhost:5000/api/test-auto-reply \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "+1234567890",
    "message": "Hello, I need help with your service"
  }'
```

## 📁 Project Structure

```
whatsapp_messages_clean/
├── simple_main_system.py        # Main application with dashboard
├── whatsapp_simple_api.py       # Core WhatsApp functionality
├── requirements_simple.txt      # Dependencies
├── .env.simple                  # Environment template
├── README_SIMPLE.md             # This file
├── QUICK_START.md               # Quick start guide
├── START_SIMPLE.bat             # Windows startup script
├── logs/                        # Application logs
├── exports/                     # CSV exports for Google Sheets
│   ├── whatsapp_messages.csv    # Message log
│   └── whatsapp_exports/        # Bulk campaign exports
└── uploads/                     # File uploads
```

## 🚨 Important Notes

### No Registration Required
- Uses WhatsApp Web links (wa.me/...)
- No API registration needed
- No developer accounts required
- Works with any WhatsApp account

### Manual Message Sending
- Generated links open WhatsApp with pre-filled messages
- Click link to send message manually
- No automated sending without user action
- Full compliance with WhatsApp terms

### Best Practices
1. **Test links** before sending to customers
2. **Personalize messages** for better engagement
3. **Use rate limiting** to avoid spam detection
4. **Import to Google Sheets** for better analytics
5. **Monitor campaigns** for delivery rates

## 🆘 Troubleshooting

### Common Issues

#### "WhatsApp link not working"
- Check phone number format (+countrycode)
- Ensure recipient has WhatsApp
- Try opening link in different browser

#### "CSV export not working"
- Check `exports/` folder permissions
- Ensure Google Sheets import format is correct
- Verify CSV file is not corrupted

#### "Auto-reply not working"
- Check AUTO_REPLY_ENABLED is True
- Verify message content matches keywords
- Check logs for errors

### Getting Help

1. Check the logs in `logs/` directory
2. Use the health check endpoint: `GET /api/health`
3. Verify CSV files in `exports/` folder
4. Test with single messages first

## 📞 Support

For additional support:
- **WhatsApp Web**: https://web.whatsapp.com
- **Google Sheets**: https://sheets.google.com
- **System Issues**: Check logs and health endpoints

---

## 🎯 What's Included

✅ **No Registration Required** - Uses WhatsApp Web links  
✅ **Automated Replies** - Intelligent responses for +8861655542  
✅ **Bulk Messaging** - Generate links for thousands of contacts  
✅ **Google Sheets Integration** - CSV export with one-click import  
✅ **Rate Limiting** - Advanced protection against spam detection  
✅ **Campaign Management** - Create and track messaging campaigns  
✅ **Analytics Dashboard** - Real-time statistics and monitoring  
✅ **WhatsApp Web Links** - Click-to-send functionality  
✅ **Duplicate Prevention** - Advanced message deduplication  
✅ **Error Handling** - Comprehensive error tracking and recovery  

**Ready to start messaging without registration! 🚀**
