import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
}

interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: string
  updatedAt: string
  model: string
  folderId?: string
  isPinned: boolean
}

interface AppState {
  // Chat State
  sessions: ChatSession[]
  currentSessionId: string | null
  isStreaming: boolean
  
  // Model State
  availableModels: { ollama: any[]; lmstudio: any[] }
  selectedModel: string
  provider: 'ollama' | 'lmstudio'
  
  // Settings
  theme: 'light' | 'dark'
  webSearchEnabled: boolean
  thinkingMode: boolean
  systemPrompt: string
  
  // Files
  uploadedFiles: any[]
  
  // Actions
  addMessage: (sessionId: string, message: Message) => void
  createSession: () => ChatSession
  deleteSession: (sessionId: string) => void
  setCurrentSession: (sessionId: string | null) => void
  setTheme: (theme: 'light' | 'dark') => void
  toggleWebSearch: () => void
  toggleThinkingMode: () => void
  setSystemPrompt: (prompt: string) => void
  setSelectedModel: (model: string) => void
  setProvider: (provider: 'ollama' | 'lmstudio') => void
  loadModels: () => Promise<void>
  uploadFile: (file: File) => Promise<void>
}

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial State
      sessions: [],
      currentSessionId: null,
      isStreaming: false,
      
      availableModels: { ollama: [], lmstudio: [] },
      selectedModel: 'llama2',
      provider: 'ollama',
      
      theme: 'dark',
      webSearchEnabled: false,
      thinkingMode: false,
      systemPrompt: 'You are Aura, a helpful AI assistant.',
      
      uploadedFiles: [],
      
      // Actions
      addMessage: (sessionId, message) => {
        set((state) => ({
          sessions: state.sessions.map((session) =>
            session.id === sessionId
              ? {
                  ...session,
                  messages: [...session.messages, message],
                  updatedAt: new Date().toISOString(),
                  title: session.messages.length === 0 
                    ? message.content.slice(0, 50) + '...' 
                    : session.title,
                }
              : session
          ),
        }))
      },
      
      createSession: () => {
        const newSession: ChatSession = {
          id: crypto.randomUUID(),
          title: 'New Chat',
          messages: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
          model: get().selectedModel,
          isPinned: false,
        }
        
        set((state) => ({
          sessions: [newSession, ...state.sessions],
          currentSessionId: newSession.id,
        }))
        
        return newSession
      },
      
      deleteSession: (sessionId) => {
        set((state) => ({
          sessions: state.sessions.filter((s) => s.id !== sessionId),
          currentSessionId: state.currentSessionId === sessionId 
            ? (state.sessions[0]?.id || null) 
            : state.currentSessionId,
        }))
      },
      
      setCurrentSession: (sessionId) => {
        set({ currentSessionId: sessionId })
      },
      
      setTheme: (theme) => {
        set({ theme })
        document.documentElement.classList.toggle('dark', theme === 'dark')
      },
      
      toggleWebSearch: () => {
        set((state) => ({ webSearchEnabled: !state.webSearchEnabled }))
      },
      
      toggleThinkingMode: () => {
        set((state) => ({ thinkingMode: !state.thinkingMode }))
      },
      
      setSystemPrompt: (prompt) => {
        set({ systemPrompt: prompt })
      },
      
      setSelectedModel: (model) => {
        set({ selectedModel: model })
      },
      
      setProvider: (provider) => {
        set({ provider })
      },
      
      loadModels: async () => {
        try {
          const response = await fetch('/api/models')
          const data = await response.json()
          set({ availableModels: data })
        } catch (error) {
          console.error('Failed to load models:', error)
        }
      },
      
      uploadFile: async (file: File) => {
        const formData = new FormData()
        formData.append('file', file)
        
        try {
          const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
          })
          const result = await response.json()
          set((state) => ({
            uploadedFiles: [...state.uploadedFiles, result],
          }))
        } catch (error) {
          console.error('Failed to upload file:', error)
          throw error
        }
      },
    }),
    {
      name: 'aura-storage',
      partialize: (state) => ({
        sessions: state.sessions,
        theme: state.theme,
        systemPrompt: state.systemPrompt,
        provider: state.provider,
        selectedModel: state.selectedModel,
      }),
    }
  )
)
