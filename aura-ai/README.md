# 🌟 Aura AI - Max Level AI Assistant

<div align="center">

![Aura AI](https://img.shields.io/badge/Aura-AI-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)

**The ultimate local AI assistant with LM Studio & Ollama support**

</div>

---

## ✨ Features

### Core Capabilities
- 💬 **Streaming Chat** - Real-time token-by-token responses
- 🤖 **Multi-Provider** - Switch between Ollama & LM Studio seamlessly
- 🧠 **Smart Memory** - Long-term + short-term conversation memory
- 📁 **File Upload** - PDF, DOCX, TXT, CSV, Excel, Images support
- 🔎 **RAG** - Ask questions about your uploaded documents
- 🌐 **Web Search** - DuckDuckGo, Google, Wikipedia integration
- 📸 **Vision** - Image understanding (LLaVA, Qwen-VL)
- 🎤 **Voice Input** - Whisper speech-to-text
- 🔊 **Voice Output** - Text-to-speech synthesis
- ⚡ **Thinking Mode** - See AI reasoning process

### Developer Tools
- 💻 Live code generation & execution
- 🐍 Python sandbox environment
- 🌍 HTML/CSS/JS live preview
- 🐛 AI debugger
- 📦 GitHub repository analysis
- 🔧 Terminal assistant
- 🔍 Project-wide code search
- ✨ AI code refactoring

### Advanced Intelligence
- 🧠 Auto model selection based on task
- 📊 System monitoring (GPU, CPU, RAM)
- 🎨 Glassmorphism UI themes
- 🔒 Local-only mode & encryption
- 📤 Export chats (PDF, Markdown, HTML)
- 🗂️ Multi-chat workspace with folders

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install Ollama (optional)
curl -fsSL https://ollama.com/install.sh | sh

# Or download LM Studio
# https://lmstudio.ai
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aura-ai.git
cd aura-ai

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Start both services
cd ..
npm run dev
```

### Running Separately

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

---

## 📁 Project Structure

```
aura-ai/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── services/
│   │   ├── llm_service.py   # Ollama & LM Studio integration
│   │   ├── rag_service.py   # Document retrieval
│   │   ├── file_service.py  # File processing
│   │   ├── voice_service.py # Speech I/O
│   │   └── ...
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # App pages
│   │   ├── store/           # Zustand state
│   │   └── styles/          # CSS & Tailwind
│   └── package.json
└── docs/
    └── FEATURES.md          # Full feature list
```

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env`:
```env
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
SECRET_KEY=your-secret-key-here
```

### Model Configuration

Aura automatically detects available models from:
- **Ollama**: `http://localhost:11434`
- **LM Studio**: `http://localhost:1234`

---

## 🎯 Usage Examples

### Basic Chat
```python
# The UI provides a ChatGPT-like interface
# Just type your message and get streaming responses
```

### File Analysis
```
1. Drag & drop any supported file
2. Ask questions about the content
3. Get AI-powered insights
```

### Code Generation
```
1. Describe what you want to build
2. Get live code with syntax highlighting
3. Execute Python code in sandbox
4. Preview web code instantly
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/models` | GET | List available models |
| `/api/chat` | POST | Send chat message |
| `/ws/chat/{id}` | WS | Streaming chat |
| `/api/upload` | POST | Upload files |
| `/api/sessions` | GET/POST | Manage sessions |
| `/api/search/web` | GET | Web search |
| `/api/code/execute` | POST | Run code |
| `/api/stats/system` | GET | System metrics |

---

## 🛡️ Security Features

- ✅ Local-only mode (no external connections)
- ✅ Encrypted chat storage
- ✅ API key vault
- ✅ Permission system
- ✅ Safe execution sandbox

---

## 🎨 Themes

Aura supports multiple themes:
- 🌙 Dark mode (default)
- ☀️ Light mode
- ✨ Glassmorphism
- 🎨 Custom CSS support

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Storage | 10 GB | 50+ GB SSD |
| GPU | Optional | NVIDIA 8GB+ VRAM |

---

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM runtime
- [LM Studio](https://lmstudio.ai) - Local AI inference
- [FastAPI](https://fastapi.tiangolo.com) - Backend framework
- [React](https://react.dev) - Frontend library
- [TailwindCSS](https://tailwindcss.com) - Styling

---

<div align="center">

**Made with ❤️ by the Aura AI Team**

[Documentation](docs/FEATURES.md) • [Issues](../../issues) • [Discussions](../../discussions)

</div>
