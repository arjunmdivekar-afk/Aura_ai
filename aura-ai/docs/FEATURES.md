# Aura AI - Feature Documentation

## Core Features

### 1. 💬 Streaming AI Chat (token-by-token)
Real-time streaming responses from AI models with typewriter effect.

### 2. 🤖 Switch between LM Studio & Ollama models
Seamlessly switch between local LLM providers with automatic model detection.

### 3. 🧠 Conversation Memory (long-term + short-term)
Persistent chat history with session management and context compression.

### 4. 📁 Drag & Drop File Upload
Support for PDF, DOCX, TXT, CSV, Excel, Images with automatic content extraction.

### 5. 🔎 RAG (Ask questions about uploaded files)
Retrieval Augmented Generation for querying your documents.

### 6. 🌐 Web Search Toggle
Enable/disable internet search integration (DuckDuckGo, Google, Wikipedia).

### 7. 📸 Vision Support
Image understanding with Qwen-VL, Gemma Vision, LLaVA models.

### 8. 🎤 Voice Input (Whisper)
Speech-to-text transcription using Whisper.

### 9. 🔊 AI Voice Reply (TTS)
Text-to-speech synthesis for audio responses.

### 10. ⚡ Thinking Mode Toggle
Show AI reasoning process before final answer.

## Coding & Developer Features

### 11-20. Code Intelligence
- Live code generation
- Python sandbox execution
- HTML/CSS/JS live preview
- AI debugger
- GitHub repository chat
- Terminal assistant
- Project-wide code search
- Multi-file editing
- AI code refactoring

## Productivity Features

### 21-29. Advanced Tools
- AI Notes & Knowledge Base
- Smart Prompt Library
- AI Agent Mode
- Workflow Automation
- OCR from Images & PDFs
- Image Generation
- Chat Export (PDF, Markdown, HTML)
- Multi-chat Workspace
- Plugin System

## Advanced Features

### 🧠 Intelligence
- Auto title generation
- Auto summarize chats
- Context compression
- Semantic search
- Memory importance scoring
- User profile learning
- AI personas
- Custom system prompts
- Temporary chats
- Shared memory across chats

### ⚡ AI Routing
- Automatic model selection
- Small model for easy questions
- Large model for coding
- Vision model for images
- Reasoning model for math

### 📂 File Intelligence
- Folder upload
- ZIP upload
- GitHub repository upload
- Excel understanding
- PowerPoint understanding
- PDF OCR
- Image OCR
- Audio/video transcription

### 🌍 Internet
- Multiple search engines
- Wikipedia integration
- News search
- Weather data
- Stock prices
- Webpage reader
- URL summarizer

### 👨‍💻 Coding Assistant
- VS Code Extension (planned)
- Live Preview
- Terminal Control
- Git Integration
- Commit Message Generator
- Code Explanation
- Bug Fixing
- Unit Test Generation
- API Tester
- Docker Assistant

### 📊 Dashboard
- GPU Usage monitoring
- RAM Usage tracking
- CPU Usage metrics
- Model VRAM Usage
- Response Speed
- Tokens/sec measurement
- Context Usage display
- Chat Statistics
- Model Benchmark tools
- Temperature Control

### ⚙️ Settings
- Theme System (Light/Dark/Glassmorphism)
- Custom CSS support
- Keyboard Shortcuts
- Model Parameters tuning
- API Management
- Download Models
- Backup & Restore
- Import/Export Settings
- Multi-language support
- Accessibility Options

### Security
- Local-only mode
- Password lock
- Encrypted chats
- API key vault
- Safe mode
- Permission system

### UI Features
- ChatGPT-like layout
- Sidebar folders
- Pinned chats
- Search chats
- Markdown rendering
- Code syntax highlighting
- Mermaid diagrams
- Drag & drop uploads
- Right-click menus
- Split-screen chat
- Multiple chat tabs
- Floating command palette (Ctrl+K)
- Glassmorphism themes

## Installation

### Prerequisites
- Node.js 18+
- Python 3.10+
- Ollama or LM Studio running locally

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Configuration

### Environment Variables
Create `.env` file in backend directory:

```
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
SECRET_KEY=your-secret-key
```

## API Endpoints

- `GET /api/models` - Get available models
- `POST /api/chat` - Send chat message
- `WS /ws/chat/{client_id}` - WebSocket for streaming
- `POST /api/upload` - Upload files
- `GET /api/sessions` - Manage chat sessions
- `GET /api/stats/system` - System monitoring

## License

MIT License
