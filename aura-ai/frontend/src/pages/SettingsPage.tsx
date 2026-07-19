import { useState } from 'react'
import { useStore } from '../store/useStore'
import { Save, Download, Upload, Trash2, Shield, Palette, Cpu } from 'lucide-react'

export default function SettingsPage() {
  const { 
    theme, setTheme, systemPrompt, setSystemPrompt,
    webSearchEnabled, thinkingMode, toggleWebSearch, toggleThinkingMode
  } = useStore()
  
  const [localPrompt, setLocalPrompt] = useState(systemPrompt)
  
  const handleSave = () => {
    setSystemPrompt(localPrompt)
  }
  
  return (
    <div className="p-6 overflow-y-auto">
      <h1 className="text-2xl font-bold text-gray-200 mb-6">Settings</h1>
      
      {/* Appearance */}
      <section className="mb-8 glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <Palette className="text-purple-400" size={24} />
          <h2 className="text-lg font-semibold text-gray-200">Appearance</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-2">Theme</label>
            <div className="flex gap-2">
              <button
                onClick={() => setTheme('light')}
                className={`px-4 py-2 rounded-lg ${
                  theme === 'light' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
                }`}
              >
                Light
              </button>
              <button
                onClick={() => setTheme('dark')}
                className={`px-4 py-2 rounded-lg ${
                  theme === 'dark' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
                }`}
              >
                Dark
              </button>
            </div>
          </div>
        </div>
      </section>
      
      {/* AI Behavior */}
      <section className="mb-8 glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <Cpu className="text-blue-400" size={24} />
          <h2 className="text-lg font-semibold text-gray-200">AI Behavior</h2>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-2">System Prompt</label>
            <textarea
              value={localPrompt}
              onChange={(e) => setLocalPrompt(e.target.value)}
              className="w-full h-32 px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-blue-500 resize-none"
            />
            <button
              onClick={handleSave}
              className="mt-2 flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Save size={18} />
              Save Prompt
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-gray-200">Web Search</h3>
              <p className="text-sm text-gray-400">Enable internet search for answers</p>
            </div>
            <button
              onClick={toggleWebSearch}
              className={`w-12 h-6 rounded-full transition-colors ${
                webSearchEnabled ? 'bg-blue-600' : 'bg-gray-700'
              }`}
            >
              <div className={`w-5 h-5 bg-white rounded-full transition-transform ${
                webSearchEnabled ? 'translate-x-6' : 'translate-x-1'
              }`} />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-gray-200">Thinking Mode</h3>
              <p className="text-sm text-gray-400">Show reasoning process</p>
            </div>
            <button
              onClick={toggleThinkingMode}
              className={`w-12 h-6 rounded-full transition-colors ${
                thinkingMode ? 'bg-purple-600' : 'bg-gray-700'
              }`}
            >
              <div className={`w-5 h-5 bg-white rounded-full transition-transform ${
                thinkingMode ? 'translate-x-6' : 'translate-x-1'
              }`} />
            </button>
          </div>
        </div>
      </section>
      
      {/* Security */}
      <section className="mb-8 glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <Shield className="text-green-400" size={24} />
          <h2 className="text-lg font-semibold text-gray-200">Security</h2>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-gray-200">Local Only Mode</h3>
              <p className="text-sm text-gray-400">Disable all external connections</p>
            </div>
            <button className="w-12 h-6 rounded-full bg-gray-700">
              <div className="w-5 h-5 bg-white rounded-full translate-x-1" />
            </button>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-gray-200">Encrypted Chats</h3>
              <p className="text-sm text-gray-400">Encrypt conversation history</p>
            </div>
            <button className="w-12 h-6 rounded-full bg-gray-700">
              <div className="w-5 h-5 bg-white rounded-full translate-x-1" />
            </button>
          </div>
        </div>
      </section>
      
      {/* Data Management */}
      <section className="glass rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <Download className="text-yellow-400" size={24} />
          <h2 className="text-lg font-semibold text-gray-200">Data Management</h2>
        </div>
        
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600 transition-colors">
            <Download size={18} />
            Export Chats
          </button>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-gray-200 rounded-lg hover:bg-gray-600 transition-colors">
            <Upload size={18} />
            Import Chats
          </button>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
            <Trash2 size={18} />
            Clear All Data
          </button>
        </div>
      </section>
    </div>
  )
}
