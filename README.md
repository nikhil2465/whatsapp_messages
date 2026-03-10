# WhatsApp Business Messaging System

A comprehensive WhatsApp Business messaging system with real API integration, campaign management, and automation capabilities.

## 🚀 Features

- **Real WhatsApp API Integration**: Ready for official WhatsApp Business API
- **Primary Account Management**: Dedicated support for +8861655542
- **Multi-Number Support**: Send and receive from multiple numbers
- **Campaign Management**: Create and manage automated campaigns
- **Auto-Reply System**: Intelligent responses to incoming messages
- **Real-time Dashboard**: Live statistics and monitoring
- **Google Sheets Integration**: Automatic logging to spreadsheets
- **WhatsApp Link Generation**: Create clickable WhatsApp links
- **Simulation Mode**: Test without real API costs
- **Database Logging**: Complete message tracking

## 📱 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Run System
```bash
python automated_messaging_system.py
```

## 🔧 API Endpoints

### Primary Account (+8861655542)
- `POST /api/primary/send` - Send message from primary account
- `POST /api/primary/receive` - Receive message to primary account
- `GET /api/primary/status` - Get primary account status
- `GET /api/primary/dashboard` - Primary account dashboard

### General Messaging
- `POST /api/send-as-number` - Send from any number
- `POST /api/receive-reply-for-number` - Receive replies
- `POST /api/whatsapp-link` - Generate WhatsApp link
- `POST /api/simulate-incoming` - Simulate incoming message

### Campaign Management
- `POST /api/create-campaign` - Create new campaign
- `POST /api/trigger-campaign` - Trigger campaign
- `GET /api/campaigns` - List campaigns
- `GET /api/templates` - Message templates

### System Monitoring
- `GET /api/stats` - System statistics
- `POST /api/test-connection` - Test connectivity
- `GET /health` - Health check

## 📊 Usage Examples

### Send Message from Primary Account
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/primary/send" -Method POST -ContentType "application/json" -Body @{
    "recipient" = "+1234567890"
    "message" = "Hello from primary account!"
}
```

### Generate WhatsApp Link
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/whatsapp-link" -Method POST -ContentType "application/json" -Body @{
    "phone" = "+1234567890"
    "message" = "Hello! This is a test message."
}
```

### Create Campaign
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/create-campaign" -Method POST -ContentType "application/json" -Body @{
    "name" = "Test Campaign"
    "template_name" = "welcome_message"
    "recipients" = @["+1234567890", "+9876543210"]
    "schedule_type" = "immediate"
}
```

## 🔐 Configuration

### Environment Variables
```bash
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
USE_REAL_WHATSAPP=False

# Google Services
GOOGLE_CREDS_FILE=google_credentials.json
GOOGLE_SHEET_NAME=WhatsApp_Messages

# System Configuration
FLASK_PORT=5000
BUSINESS_PHONE=+8861655542
```

## 📁 Project Structure

```
whatsapp_messages_clean/
├── automated_messaging_system.py    # Main application
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore file
├── README.md                        # This file
└── logs/                           # Log files directory
```

## 🎯 Primary Account Features

The system includes exclusive support for the primary account +8861655542:

- **Dedicated endpoints** for primary account operations
- **Isolated functionality** from other numbers
- **Complete message tracking** and logging
- **Auto-reply capabilities** with intelligent responses
- **Real-time statistics** and monitoring

## 🔧 WhatsApp API Integration

### Real API Setup
1. Create WhatsApp Business App at [Meta Developers](https://developers.facebook.com/)
2. Get Access Token and Phone Number ID
3. Set up webhook endpoint
4. Update `.env` with credentials
5. Set `USE_REAL_WHATSAPP=True`

### Simulation Mode
The system works in simulation mode by default:
- 95% message success rate
- No API costs
- Full functionality testing
- Easy switching to real API

## 📊 Database Schema

### Messages Table
- `message_id` - Unique message identifier
- `sender` - Sender phone number
- `recipient` - Recipient phone number
- `message` - Message content
- `direction` - IN/OUT
- `status` - sent/failed/pending
- `campaign_id` - Associated campaign

### Campaigns Table
- `campaign_id` - Unique campaign identifier
- `name` - Campaign name
- `message` - Campaign message
- `recipients` - JSON array of recipients
- `status` - active/completed/failed

## 🚀 Deployment

### Development
```bash
python automated_messaging_system.py
```

### Production
```bash
# Use production WSGI server
gunicorn --workers 4 --bind 0.0.0.0:5000 automated_messaging_system:app
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For support and questions:
- Create an issue in this repository
- Check the documentation
- Review the API endpoints

---

**Built with ❤️ for WhatsApp Business automation**
