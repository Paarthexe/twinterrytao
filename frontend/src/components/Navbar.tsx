import React from 'react';
import { MessageSquare, BrainCircuit, Network, RefreshCw, Trash2, Cpu, Database } from 'lucide-react';

interface NavbarProps {
  activeTab: 'chat' | 'memory' | 'explore';
  setActiveTab: (tab: 'chat' | 'memory' | 'explore') => void;
  onNewChat: () => void;
  onClearMemory: () => void;
  systemStatus: {
    status: string;
    chroma_items: number;
    model: string;
  } | null;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onNewChat,
  onClearMemory,
  systemStatus,
}) => {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/90 bg-[#0B0F17]/95 backdrop-blur-md px-4 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700/80 flex items-center justify-center text-slate-100 font-mono font-semibold text-base shadow-sm">
            π
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-semibold text-slate-100 text-sm tracking-tight">Terence Tao AI</h1>
              <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border border-slate-700 bg-slate-800/80 text-slate-300 font-mono">
                Digital Twin
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-mono">Hybrid RAG • RRF • Peer Verification</p>
          </div>
        </div>

        {/* Center Tabs */}
        <nav className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'chat'
                ? 'bg-slate-800 text-slate-100 border border-slate-700 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Chat Workspace</span>
          </button>

          <button
            onClick={() => setActiveTab('memory')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'memory'
                ? 'bg-slate-800 text-slate-100 border border-slate-700 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <BrainCircuit className="w-3.5 h-3.5" />
            <span>Memory Matrix</span>
          </button>

          <button
            onClick={() => setActiveTab('explore')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'explore'
                ? 'bg-slate-800 text-slate-100 border border-slate-700 shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <Network className="w-3.5 h-3.5" />
            <span>Concept Map</span>
          </button>
        </nav>

        {/* Right Actions & Status */}
        <div className="flex items-center gap-3">
          {/* Status Badges */}
          <div className="hidden lg:flex items-center gap-2 border-r border-slate-800 pr-3">
            <div className="flex items-center gap-1.5 text-[11px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-md border border-slate-800">
              <Cpu className="w-3 h-3 text-slate-400" />
              <span>{systemStatus?.model || 'gemma4:e4b'}</span>
            </div>
            <div className="flex items-center gap-1.5 text-[11px] font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-md border border-slate-800">
              <Database className="w-3 h-3 text-slate-400" />
              <span>{systemStatus ? `${systemStatus.chroma_items} vectors` : 'Chroma RAG'}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onNewChat}
              className="flex items-center gap-1.5 text-xs font-medium text-slate-300 hover:text-slate-100 bg-slate-800/80 hover:bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700 transition"
              title="Reset current chat session"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>New Session</span>
            </button>

            <button
              onClick={onClearMemory}
              className="flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-rose-400 bg-slate-900 hover:bg-rose-950/30 px-3 py-1.5 rounded-lg border border-slate-800 hover:border-rose-900/40 transition"
              title="Clear long-term user memory"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear Memory</span>
            </button>
          </div>
        </div>

      </div>
    </header>
  );
};
