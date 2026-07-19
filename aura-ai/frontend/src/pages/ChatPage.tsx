import { useState, useRef, useEffect } from 'react'
import { Send, Mic, Upload, Paperclip, Globe, Brain, Sparkles } from 'lucide-react'
import { useStore } from '../store/useStore'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function ChatPage() {
  const { 
    currentSessionId, sessions, addMessage, createSession,
    webSearchEnabled, toggleWebSearch, thinkingMode, toggleThinkingMode, systemPrompt,
    selectedModel, provider, setSelectedModel, availableModels, loadModels,
    uploadFile, theme
  } = useStore()
  
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const currentSession = sessions.find(s => s.id === currentSessionId)
  const messages = currentSession?.messages || []
  
  useEffect(() => {
    loadModels()
    if (!currentSessionId) {
      createSession()
    }
  }, [])
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !currentSessionId) return
    
    const userMessage = {
      id: crypto.randomUUID(),
      role: 'user' as const,
      content: input.trim(),
      timestamp: new Date().toISOString()
    }
    
    addMessage(currentSessionId, userMessage)
    setInput('')
    setIsLoading(true)
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage.content,
          session_id: currentSessionId,
          model_config: { provider, model_name: selectedModel },
          system_prompt: systemPrompt,
          web_search: webSearchEnabled,
          thinking_mode: thinkingMode
        })
      })
      
      const data = await response.json()
      
      const assistantMessage = {
        id: crypto.randomUUID(),
        role: 'assistant' as const,
        content: data.content || 'Error: No response',
        timestamp: new Date().toISOString()
      }
      
      addMessage(currentSessionId, assistantMessage)
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        id: crypto.randomUUID(),
        role: 'assistant' as const,
        content: 'Sorry, an error occurred. Please try again.',
        timestamp: new Date().toISOString()
      }
      addMessage(currentSessionId, errorMessage)
    } finally {
      setIsLoading(false)
    }
  }
  
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      try {
        await uploadFile(file)
      } catch (error) {
        console.error('Upload error:', error)
      }
    }
  }
  
  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400">
            <Sparkles size={64} className="mb-4 opacity-50" />
            <h2 className="text-2xl font-semibold mb-2">Welcome to Aura AI</h2>
            <p className="text-center max-w-md">
              Start a conversation with your local AI models. Choose between Ollama and LM Studio providers.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-200'
                }`}
              >
                {message.role === 'assistant' ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]} className="markdown-body">
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  <p className="whitespace-pre-wrap">{message.content}</p>
                )}
              </div>
            </div>
          ))
        )}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-2xl px-4 py-3">
              <div className="typing-indicator flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="border-t border-gray-700/30 p-4 glass">
        {/* Controls */}
        <div className="flex items-center gap-2 mb-3">
          <select
            value={`${provider}/${selectedModel}`}
            onChange={(e) => {
              const [newProvider, newModel] = e.target.value.split('/')
              setSelectedModel(newModel)
            }}
            className="px-3 py-1.5 bg-gray-800/50 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none"
          >
            {availableModels.ollama?.map((m) => (
              <option key={m.name} value={`ollama/${m.name}`}>
                🦙 {m.name}
              </option>
            ))}
            {availableModels.lmstudio?.map((m) => (
              <option key={m.name} value={`lmstudio/${m.name}`}>
                🔬 {m.name}
              </option>
            ))}
          </select>
          
          <button
            onClick={toggleWebSearch}
            className={`p-2 rounded-lg transition-colors ${
              webSearchEnabled ? 'bg-blue-600 text-white' : 'hover:bg-gray-800/50 text-gray-400'
            }`}
            title="Web Search"
          >
            <Globe size={18} />
          </button>
          
          <button
            onClick={toggleThinkingMode}
            className={`p-2 rounded-lg transition-colors ${
              thinkingMode ? 'bg-purple-600 text-white' : 'hover:bg-gray-800/50 text-gray-400'
            }`}
            title="Thinking Mode"
          >
            <Brain size={18} />
          </button>
        </div>
        
        {/* Input Form */}
        <form onSubmit={handleSubmit} className="flex items-center gap-3">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="hidden"
            accept=".pdf,.docx,.txt,.csv,.xlsx,.png,.jpg,.jpeg"
          />
          
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-3 hover:bg-gray-800/50 rounded-xl transition-colors text-gray-400"
          >
            <Paperclip size={20} />
          </button>
          
          <button
            type="button"
            className="p-3 hover:bg-gray-800/50 rounded-xl transition-colors text-gray-400"
          >
            <Mic size={20} />
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:outline-none focus:border-blue-500"
          />
          
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  )
}
