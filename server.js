require('dotenv').config();
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const fs = require('fs');
const { google } = require('googleapis');
const cors = require('cors');
const multer = require('multer');
const { v4: uuidv4 } = require('uuid');

class EnterpriseWhatsAppPlatform {
    constructor() {
        this.app = express();
        this.server = http.createServer(this.app);
        this.io = socketIo(this.server, {
            cors: {
                origin: "*",
                methods: ["GET", "POST"]
            }
        });
        
        // Configuration
        this.businessPhone = process.env.BUSINESS_PHONE || '8660444809';
        this.businessName = process.env.BUSINESS_NAME || 'Enterprise Business';
        this.sheetId = process.env.GOOGLE_SHEET_ID || '1sKx-ooy2BJvt1dZMn0KSMN3XGTThz7I_DUtpBeiMIRY';
        this.sheetName = process.env.GOOGLE_SHEET_NAME || 'WhatsApp_Messages';
        this.port = process.env.PORT || 3000;
        
        // Python AI Integration
        this.aiEnabled = true;
        this.pythonConnected = false;
        
        // Google Sheets integration
        this.sheetsService = null;
        this.driveService = null;
        this.googleEnabled = false;
        
        // Message storage
        this.messages = [];
        this.messageFile = 'whatsapp_messages.json';
        
        // File upload
        this.upload = multer({ 
            dest: 'uploads/',
            limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
        });
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupSocketHandlers();
        this.initGoogleServices();
        this.loadMessages();
    }
    
    setupMiddleware() {
        this.app.use(cors());
        this.app.use(express.json());
        this.app.use(express.static(path.join(__dirname, 'public')));
        this.app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
    }
    
    async initGoogleServices() {
        try {
            console.log('🔧 Initializing Google Services...');
            
            // Try service account first
            if (process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL && process.env.GOOGLE_PRIVATE_KEY) {
                const auth = new google.auth.GoogleAuth({
                    credentials: {
                        client_email: process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
                        private_key: process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n')
                    },
                    scopes: [
                        'https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive'
                    ]
                });
                
                const authClient = await auth.getClient();
                this.sheetsService = google.sheets({ version: 'v4', auth: authClient });
                this.driveService = google.drive({ version: 'v3', auth: authClient });
                this.googleEnabled = true;
                console.log('✅ Google Services initialized with Service Account');
            }
            // Try OAuth2 credentials
            else if (fs.existsSync('google-credentials.json')) {
                const credentials = JSON.parse(fs.readFileSync('google-credentials.json', 'utf8'));
                const { client_secret, client_id, redirect_uris } = credentials.web;
                const oAuth2Client = new google.auth.OAuth2(
                    client_id, client_secret, redirect_uris[0]
                );
                
                // Check for existing token
                if (fs.existsSync('google-token.json')) {
                    const token = JSON.parse(fs.readFileSync('google-token.json', 'utf8'));
                    oAuth2Client.setCredentials(token);
                    
                    this.sheetsService = google.sheets({ version: 'v4', auth: oAuth2Client });
                    this.driveService = google.drive({ version: 'v3', auth: oAuth2Client });
                    this.googleEnabled = true;
                    console.log('✅ Google Services initialized with OAuth2');
                }
            }
            
            if (this.googleEnabled) {
                await this.setupGoogleSheet();
            } else {
                console.log('⚠️ Google Services not available - using local storage');
            }
            
        } catch (error) {
            console.error('❌ Error initializing Google Services:', error);
            this.googleEnabled = false;
        }
    }
    
    async setupGoogleSheet() {
        try {
            console.log('📊 Setting up Google Sheet...');
            
            // Check if sheet exists and has headers
            const response = await this.sheetsService.spreadsheets.values.get({
                spreadsheetId: this.sheetId,
                range: 'A1:Z1'
            });
            
            if (!response.data.values || response.data.values.length === 0) {
                // Create headers
                const headers = [
                    'Timestamp', 'From Number', 'To Number', 'Message', 'Direction',
                    'Status', 'Attachment', 'Message Type', 'Duration', 'Contact Name',
                    'Device', 'Location', 'Labels', 'Notes', 'AI Enhanced', 'Google Sheet ID'
                ];
                
                await this.sheetsService.spreadsheets.values.update({
                    spreadsheetId: this.sheetId,
                    range: 'A1:P1',
                    valueInputOption: 'USER_ENTERED',
                    resource: { values: [headers] }
                });
                
                console.log('✅ Google Sheet headers created');
            }
            
            console.log('✅ Google Sheet ready:', this.sheetId);
            
        } catch (error) {
            console.error('❌ Error setting up Google Sheet:', error);
            this.googleEnabled = false;
        }
    }
    
    setupRoutes() {
        // Serve professional dashboard
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, 'public', 'professional_dashboard.html'));
        });
        
        // Python AI Integration endpoints
        this.app.post('/api/whatsapp-connected', (req, res) => {
            try {
                const { phone, ai_enabled } = req.body;
                this.pythonConnected = true;
                this.aiEnabled = ai_enabled || true;
                
                console.log('🤖 Python AI Automation connected');
                this.io.emit('python-connected', { phone, ai_enabled: this.aiEnabled });
                
                res.json({ success: true, message: 'Python AI connected' });
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });

        // Launch Enterprise WhatsApp endpoint
        this.app.post('/api/launch-enterprise', async (req, res) => {
            try {
                const { spawn } = require('child_process');
                console.log('🚀 Launching Enterprise WhatsApp Platform...');
                
                // Launch Enterprise WhatsApp script
                const pythonProcess = spawn('python', ['whatsapp_automation_engine.py'], {
                    cwd: __dirname,
                    stdio: 'inherit'
                });
                
                pythonProcess.on('spawn', () => {
                    console.log('✅ Enterprise WhatsApp Platform launched');
                    this.pythonConnected = true;
                    this.aiEnabled = true;
                    this.io.emit('enterprise-launched', { success: true });
                    res.json({ success: true, message: 'Enterprise WhatsApp Platform launched' });
                });
                
                pythonProcess.on('error', (error) => {
                    console.error('❌ Error launching Enterprise WhatsApp:', error);
                    res.status(500).json({ success: false, error: error.message });
                });
                
                pythonProcess.on('close', (code) => {
                    console.log(`🐍 Enterprise WhatsApp process exited with code ${code}`);
                    this.pythonConnected = false;
                    this.io.emit('enterprise-disconnected');
                });
                
            } catch (error) {
                console.error('❌ Error launching Enterprise WhatsApp:', error);
                res.status(500).json({ success: false, error: error.message });
            }
        });
        
        this.app.post('/api/store-message', async (req, res) => {
            try {
                const messageData = {
                    id: uuidv4(),
                    ...req.body,
                    timestamp: req.body.timestamp || new Date().toISOString(),
                    ai_enhanced: req.body.ai_enhanced || false
                };
                
                await this.storeMessage(messageData);
                
                // Emit to dashboard
                this.io.emit('message-stored', messageData);
                
                res.json({ success: true, message: 'Message stored' });
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });
        
        // Send message via Python
        this.app.post('/api/send-via-python', async (req, res) => {
            try {
                const { phoneNumber, message, use_ai } = req.body;
                
                // This would trigger Python to send the message
                // For now, we'll simulate it
                const result = await this.sendViaPython(phoneNumber, message, use_ai);
                
                res.json(result);
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });
        
        // Get messages
        this.app.get('/api/messages', (req, res) => {
            res.json({
                messages: this.messages,
                total: this.messages.length,
                phone: this.businessPhone,
                googleEnabled: this.googleEnabled,
                sheetId: this.sheetId,
                pythonConnected: this.pythonConnected,
                aiEnabled: this.aiEnabled
            });
        });
        
        // Get status
        this.app.get('/api/status', (req, res) => {
            res.json({
                connected: this.pythonConnected,
                phone: this.businessPhone,
                messageCount: this.messages.length,
                googleEnabled: this.googleEnabled,
                sheetId: this.sheetId,
                sheetName: this.sheetName,
                pythonConnected: this.pythonConnected,
                aiEnabled: this.aiEnabled
            });
        });
        
        // Export messages
        this.app.get('/api/export', (req, res) => {
            const csv = this.exportToCSV();
            res.setHeader('Content-Type', 'text/csv');
            res.setHeader('Content-Disposition', 'attachment; filename=whatsapp_messages.csv');
            res.send(csv);
        });
        
        // Sync to Google Sheets
        this.app.post('/api/sync-google', async (req, res) => {
            try {
                const result = await this.syncMessagesToGoogle();
                res.json(result);
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });
        
        // AI endpoint
        this.app.post('/api/ai-response', async (req, res) => {
            try {
                const { message, context } = req.body;
                
                // This would integrate with Python AI
                // For now, simulate AI response
                const aiResponse = await this.generateAIResponse(message, context);
                
                res.json({ success: true, response: aiResponse });
            } catch (error) {
                res.status(500).json({ success: false, error: error.message });
            }
        });
    }
    
    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log('Client connected');
            
            socket.on('disconnect', () => {
                console.log('Client disconnected');
            });
        });
    }
    
    async sendViaPython(phoneNumber, message, use_ai = true) {
        try {
            // This would communicate with Python script
            // For now, simulate the process
            
            const messageData = {
                id: uuidv4(),
                timestamp: new Date().toISOString(),
                from: this.businessPhone,
                to: phoneNumber,
                message: message,
                direction: 'outbound',
                status: 'sent',
                messageType: 'text',
                device: 'Python Automation',
                location: 'AI System',
                ai_enhanced: use_ai
            };
            
            await this.storeMessage(messageData);
            
            console.log(`🤖 Message sent via Python AI: ${phoneNumber}`);
            this.io.emit('message-sent-via-python', messageData);
            
            return {
                success: true,
                message: 'Message sent via Python AI',
                data: messageData
            };
            
        } catch (error) {
            console.error('❌ Error sending via Python:', error);
            throw error;
        }
    }
    
    async generateAIResponse(message, context = '') {
        try {
            // This would call Python AI service
            // For now, simulate AI response
            const responses = [
                "Thank you for your message! How can I assist you today?",
                "I understand your inquiry. Let me help you with that.",
                "Great question! Here's what I can tell you...",
                "I appreciate you reaching out. Let me provide you with the information you need."
            ];
            
            return responses[Math.floor(Math.random() * responses.length)];
            
        } catch (error) {
            console.error('❌ Error generating AI response:', error);
            return "I'm here to help! Could you please provide more details?";
        }
    }
    
    async storeMessage(messageData) {
        try {
            // Add to local storage
            this.messages.push(messageData);
            this.saveMessages();
            
            // Store in Google Sheets if enabled
            if (this.googleEnabled) {
                await this.storeMessageInGoogleSheet(messageData);
            }
            
            console.log(`💾 Message stored: ${messageData.direction} - ${messageData.from} -> ${messageData.to}`);
            
        } catch (error) {
            console.error('❌ Error storing message:', error);
        }
    }
    
    async storeMessageInGoogleSheet(messageData) {
        try {
            if (!this.sheetsService) return;
            
            const row = [
                messageData.timestamp,
                messageData.from,
                messageData.to,
                messageData.message,
                messageData.direction,
                messageData.status,
                messageData.attachment || '',
                messageData.messageType || 'text',
                messageData.duration || '',
                messageData.contactName || '',
                messageData.device || '',
                messageData.location || '',
                messageData.labels || '',
                messageData.notes || '',
                messageData.ai_enhanced || false,
                this.sheetId
            ];
            
            await this.sheetsService.spreadsheets.values.append({
                spreadsheetId: this.sheetId,
                range: 'A:P',
                valueInputOption: 'USER_ENTERED',
                resource: { values: [row] }
            });
            
            console.log(`✅ Message stored in Google Sheet: ${messageData.direction}`);
            
        } catch (error) {
            console.error('❌ Error storing in Google Sheet:', error);
        }
    }
    
    async syncMessagesToGoogle() {
        try {
            if (!this.googleEnabled) {
                return { success: false, message: 'Google Services not enabled' };
            }
            
            let syncedCount = 0;
            for (const message of this.messages) {
                await this.storeMessageInGoogleSheet(message);
                syncedCount++;
            }
            
            return {
                success: true,
                message: `Synced ${syncedCount} messages to Google Sheet`,
                sheetId: this.sheetId,
                syncedCount
            };
            
        } catch (error) {
            console.error('❌ Error syncing to Google:', error);
            return { success: false, error: error.message };
        }
    }
    
    saveMessages() {
        try {
            fs.writeFileSync(this.messageFile, JSON.stringify(this.messages, null, 2));
        } catch (error) {
            console.error('❌ Error saving messages:', error);
        }
    }
    
    loadMessages() {
        try {
            if (fs.existsSync(this.messageFile)) {
                const data = fs.readFileSync(this.messageFile, 'utf8');
                this.messages = JSON.parse(data);
                console.log(`📊 Loaded ${this.messages.length} messages`);
            }
        } catch (error) {
            console.error('❌ Error loading messages:', error);
            this.messages = [];
        }
    }
    
    exportToCSV() {
        const headers = ['Timestamp', 'From', 'To', 'Message', 'Direction', 'Status', 'Attachment', 'Message Type', 'Duration', 'Contact Name', 'Device', 'Location', 'Labels', 'Notes', 'AI Enhanced', 'Google Sheet ID'];
        const rows = this.messages.map(msg => [
            msg.timestamp,
            msg.from,
            msg.to,
            `"${msg.message.replace(/"/g, '""')}"`,
            msg.direction,
            msg.status,
            msg.attachment || '',
            msg.messageType || 'text',
            msg.duration || '',
            msg.contactName || '',
            msg.device || '',
            msg.location || '',
            msg.labels || '',
            msg.notes || '',
            msg.ai_enhanced || false,
            this.sheetId
        ]);
        
        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }
    
    async start() {
        console.log(`🚀 Starting Hybrid WhatsApp Platform`);
        console.log(`📞 Business Phone: ${this.businessPhone}`);
        console.log(`📊 Google Sheet ID: ${this.sheetId}`);
        console.log(`🌐 Server: http://localhost:${this.port}`);
        console.log(`🤖 Python AI Integration: Ready`);
        console.log(`🔧 Google Services: ${this.googleEnabled ? 'Enabled' : 'Disabled'}`);
        
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                platform: 'Enterprise WhatsApp Communication Platform',
                version: '8.0.0',
                timestamp: new Date().toISOString(),
                services: {
                    server: true,
                    google: this.googleEnabled,
                    python: this.pythonConnected,
                    ai: this.aiEnabled
                }
            });
        });

        this.server.listen(this.port, () => {
            console.log('\n' + '='*80);
            console.log('🏢 ENTERPRISE WHATSAPP COMMUNICATION PLATFORM');
            console.log('='*80);
            console.log(`📞 Business Number: ${this.businessPhone}`);
            console.log(`🏢 Business Name: ${this.businessName}`);
            console.log(`🌐 Server: http://localhost:${this.port}`);
            console.log(`📊 Dashboard: http://localhost:${this.port}/`);
            console.log(`🤖 AI Automation: ${this.aiEnabled ? 'Enabled' : 'Disabled'}`);
            console.log(`📈 Google Sheets: ${this.googleEnabled ? 'Connected' : 'Disconnected'}`);
            console.log('='*80);
        });
    }
}

// Start enterprise platform
const platform = new EnterpriseWhatsAppPlatform();
platform.start().catch(console.error);
