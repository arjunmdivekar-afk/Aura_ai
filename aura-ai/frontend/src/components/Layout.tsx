import { Outlet, Link, useLocation } from 'react-router-dom'
import { 
  MessageSquare, Settings, Plus, FolderOpen, 
  Sun, Moon, Search, Mic, Upload, Send,
  MoreVertical, Trash2, Pin, FolderPlus
} from 'lucide-react'
import { useStore } from '../store/useStore'
import { useState } from 'react'

export default function Layout() {
  const location = useLocation()
  const { 
    sessions, currentSessionId, createSession, deleteSession, setCurrentSession,
    theme, setTheme, uploadedFiles
  } = useStore()
  
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  
  const filteredSessions = sessions.filter(s => 
    s.title.toLowerCase().includes(searchQuery.toLowerCase())
  )
  
  return (
    <div className={`flex h-screen ${theme === 'dark' ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-72' : 'w-0'} transition-all duration-300 glass border-r border-gray-700/30 flex flex-col overflow-hidden`}>
        {/* Header */}
        <div className="p-4 border-b border-gray-700/30">
          <button
            onClick={() => createSession()}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-medium hover:opacity-90 transition-opacity"
          >
            <Plus size={20} />
            New Chat
          </button>
        </div>
        
        {/* Search */}
        <div className="p-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              placeholder="Search chats..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
        
        {/* Sessions List */}
        <div className="flex-1 overflow-y-auto px-2">
          {filteredSessions.map((session) => (
            <div
              key={session.id}
              className={`group flex items-center gap-3 px-3 py-3 mb-1 rounded-lg cursor-pointer transition-colors ${
                currentSessionId === session.id 
                  ? 'bg-blue-600/20 border border-blue-500/30' 
                  : 'hover:bg-gray-800/50 border border-transparent'
              }`}
              onClick={() => setCurrentSession(session.id)}
            >
              <MessageSquare size={18} className="text-gray-400" />
              <span className="flex-1 truncate text-sm text-gray-200">
                {session.title}
              </span>
              <div className="opacity-0 group-hover:opacity-100 flex items-center gap-1">
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    deleteSession(session.id)
                  }}
                  className="p-1 hover:bg-red-500/20 rounded"
                >
                  <Trash2 size={14} className="text-red-400" />
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {/* Footer */}
        <div className="p-4 border-t border-gray-700/30">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2 hover:bg-gray-800/50 rounded-lg transition-colors"
            >
              {theme === 'dark' ? <Sun size={20} className="text-yellow-400" /> : <Moon size={20} className="text-gray-600" />}
            </button>
            <Link
              to="/settings"
              className="p-2 hover:bg-gray-800/50 rounded-lg transition-colors"
            >
              <Settings size={20} className="text-gray-400" />
            </Link>
          </div>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Top Bar */}
        <header className="h-14 border-b border-gray-700/30 flex items-center justify-between px-4 glass">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-800/50 rounded-lg"
            >
              <FolderOpen size={20} className="text-gray-400" />
            </button>
            <h1 className="text-lg font-semibold text-gray-200">Aura AI</h1>
          </div>
          
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400">
              {uploadedFiles.length} files
            </span>
          </div>
        </header>
        
        {/* Page Content */}
        <div className="flex-1 overflow-hidden">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
