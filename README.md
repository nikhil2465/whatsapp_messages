# 🚀 Professional WhatsApp Business Platform

A comprehensive WhatsApp Business messaging system with professional features, real API integration, campaign management, and enterprise-grade capabilities.

## ✨ Key Features

### 🎨 **Professional Dashboard**
- Modern, responsive UI with Font Awesome icons
- Real-time statistics and analytics
- Tabbed interface for different message types
- Mobile-responsive design

### 📎 **Attachment Support**
- Send images, videos, audio, documents
- Automatic attachment saving and management
- Download and open attachments directly
- File manager integration

### 🤖 **Professional Features Module**
- **Contact Management**: Organize contacts with tags and segments
- **Message Templates**: Create reusable templates with variables
- **Scheduled Messages**: Schedule messages with APScheduler
- **Quick Replies**: Set up automated responses
- **Customer Segmentation**: Target specific customer groups
- **Advanced Analytics**: Track engagement and delivery rates

### 📱 **WhatsApp Integration**
- **Real WhatsApp Business API** ready
- **WhatsApp Web fallback** with auto-opening
- **Bulk messaging** with anti-blocking measures
- **Message status tracking**

### 📊 **Data Management**
- **SQLite Database** with full schema
- **Google Sheets integration**
- **Message export functionality**
- **Comprehensive logging**

## 🛠️ Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/nikhil2465/whatsapp_messages1.git
cd whatsapp_messages1

# Install dependencies
pip install -r requirements_simple.txt

# Start the professional system
python real_main_system.py
```

### Environment Setup
```bash
# Copy the environment template
cp .env.real_api .env

# Edit with your credentials
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
USE_WHATSAPP_WEB_FALLBACK=False
```

## 🚀 Usage

### Starting the System
```bash
# Professional System (Recommended)
python real_main_system.py

# Simple System
python simple_main_system.py
```

### Access Points
- **Dashboard**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **Message Stats**: http://localhost:5000/api/stats

## 📱 Features in Detail

### Message Types
- **Single Messages**: Send to individual recipients
- **Bulk Messages**: Send to multiple recipients
- **Scheduled Messages**: Schedule for future delivery
- **Attachment Support**: Include files with messages

### Professional Features
- **Contact Management**: Add, edit, and segment contacts
- **Template Library**: Save and reuse message templates
- **Quick Replies**: Automated responses for common queries
- **Analytics Dashboard**: Track performance metrics

### API Endpoints
```
POST /api/send-single          - Send single message
POST /api/send-bulk            - Send bulk messages
POST /api/schedule-message     - Schedule message
GET  /api/contacts             - Manage contacts
GET  /api/templates            - Manage templates
GET  /api/analytics             - View analytics
GET  /api/health               - System health check
```

## 🔧 Configuration

### WhatsApp Business API Setup
1. Create app at [Meta Developers](https://developers.facebook.com/apps)
2. Get Access Token and Phone Number ID
3. Configure environment variables
4. Restart the system

### Environment Variables
```bash
BUSINESS_PHONE=+8861655542
WHATSAPP_ACCESS_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
FLASK_PORT=5000
GOOGLE_ENABLED=False
```

## 📊 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Database      │
│                 │    │                  │    │                 │
│ Professional    │◄──►│ Flask Routes     │◄──►│ SQLite          │
│ Dashboard       │    │ Business Logic   │    │ Messages        │
│ Attachment UI   │    │ WhatsApp API     │    │ Contacts        │
│ Analytics       │    │ File Management  │    │ Templates       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🎯 Use Cases

### Business Communication
- **Customer Support**: Automated responses and templates
- **Marketing Campaigns**: Bulk messaging with analytics
- **Appointment Reminders**: Scheduled messages
- **Document Sharing**: Attachment support

### Professional Features
- **Contact Segmentation**: Target specific customer groups
- **Message Templates**: Consistent branding
- **Analytics**: Track engagement and delivery
- **Multi-channel**: WhatsApp Web + API fallback

## 🔒 Security Features

- **Environment Variables**: Secure credential management
- **Input Validation**: Protect against injection attacks
- **Rate Limiting**: Anti-blocking measures
- **Error Handling**: Comprehensive error management

## 📈 Performance

- **Optimized Database**: Efficient queries and indexing
- **Background Processing**: Non-blocking operations
- **Caching**: Improved response times
- **Scalability**: Handle bulk messaging efficiently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Issues**: [GitHub Issues](https://github.com/nikhil2465/whatsapp_messages1/issues)
- **Documentation**: Check README files in the repository
- **Quick Start**: Run `START_REAL.bat` for immediate setup

## 🔄 Updates

### Latest Version Features
- ✅ Professional dashboard with modern UI
- ✅ Attachment support with file management
- ✅ Professional features module
- ✅ Enhanced error handling
- ✅ Auto-opening WhatsApp links
- ✅ Comprehensive analytics

### Planned Features
- 🔄 Multi-language support
- 🔄 Advanced reporting
- 🔄 Integration with more platforms
- 🔄 AI-powered message suggestions

---

**🚀 Ready for Production Use!**

This WhatsApp Business Platform is production-ready with enterprise-grade features, comprehensive error handling, and professional UI/UX design.
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
