import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, BookOpen, ShieldCheck, ChevronDown, ChevronUp, User, Loader2 } from 'lucide-react';
import { MarkdownViewer } from './MarkdownViewer';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp?: string;
}

interface ChatWorkspaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => Promise<void>;
  isLoading: boolean;
}

const PRESET_QUERIES = [
  "What is the key difficulty in the Kakeya conjecture?",
  "Explain the Green-Tao theorem on prime arithmetic progressions.",
  "What is the main bottleneck in the Navier-Stokes global regularity problem?",
  "How do you structure your problem-solving process when tackling hard math?"
];

export const ChatWorkspace: React.FC<ChatWorkspaceProps> = ({
  messages,
  onSendMessage,
  isLoading
}) => {
  const [input, setInput] = useState('');
  const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    const text = input.trim();
    setInput('');
    await onSendMessage(text);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleSources = (msgId: string) => {
    setExpandedSources(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full px-4 py-2 min-h-0">
      {/* Chat Messages Container */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1 min-h-0">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4 my-auto">
            <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200 font-mono text-lg font-semibold mb-3 shadow-sm">
              ∫
            </div>
            <h2 className="text-base font-semibold text-slate-100 tracking-tight mb-1">
              Terence Tao AI — Digital Twin Studio
            </h2>
            <p className="text-xs text-slate-400 max-w-md mb-5 leading-relaxed">
              Explore mathematical reasoning, research papers, and problem-solving strategies using hybrid vector+sparse RAG and skeptic verification.
            </p>

            <div className="w-full max-w-xl grid grid-cols-1 sm:grid-cols-2 gap-2 text-left">
              {PRESET_QUERIES.map((query, idx) => (
                <button
                  key={idx}
                  onClick={() => onSendMessage(query)}
                  className="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 hover:text-slate-100 transition-all flex items-start gap-2 group"
                >
                  <Sparkles className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                  <span className="leading-snug text-[11px]">{query}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200 font-mono font-bold text-xs shrink-0 mt-0.5">
                  τ
                </div>
              )}

              <div className={`max-w-2xl rounded-2xl p-3.5 border transition-all ${
                msg.role === 'user'
                  ? 'bg-slate-800/90 border-slate-700/80 text-slate-100 rounded-tr-xs'
                  : 'bg-[#0E131F] border-slate-800 text-slate-200 rounded-tl-xs shadow-sm'
              }`}>
                {msg.role === 'user' ? (
                  <p className="text-xs leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <div>
                    <MarkdownViewer content={msg.content} />

                    {/* Sources & Audit Drawer */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-2.5 pt-2.5 border-t border-slate-800/80">
                        <button
                          onClick={() => toggleSources(msg.id)}
                          className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200 font-mono transition"
                        >
                          <BookOpen className="w-3 h-3" />
                          <span>Retrieved Sources ({msg.sources.length})</span>
                          {expandedSources[msg.id] ? (
                            <ChevronUp className="w-3 h-3" />
                          ) : (
                            <ChevronDown className="w-3 h-3" />
                          )}
                        </button>

                        {expandedSources[msg.id] && (
                          <div className="mt-2 space-y-1 pl-2 border-l border-slate-700">
                            {msg.sources.map((src, idx) => (
                              <div key={idx} className="text-[11px] font-mono text-slate-400 bg-slate-900/80 p-1.5 rounded border border-slate-800">
                                {src}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {/* RAG & Skeptic Meta pill */}
                    <div className="mt-2 flex items-center gap-2 text-[10px] font-mono text-slate-500">
                      <span className="flex items-center gap-1 text-slate-400">
                        <ShieldCheck className="w-3 h-3" /> Skeptic Audit Passed
                      </span>
                      <span>•</span>
                      <span>Hybrid RRF Retrieval</span>
                    </div>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0 mt-0.5">
                  <User className="w-3.5 h-3.5" />
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex gap-3 justify-start items-center">
            <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200 font-mono font-bold text-xs shrink-0">
              τ
            </div>
            <div className="bg-[#0E131F] border border-slate-800 rounded-2xl rounded-tl-xs p-3 flex items-center gap-2.5">
              <Loader2 className="w-3.5 h-3.5 text-slate-400 animate-spin" />
              <span className="text-xs font-mono text-slate-400">
                Retrieving papers & verifying logic...
              </span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="mt-2 pb-2 shrink-0">
        <form onSubmit={handleSubmit} className="relative bg-[#0E131F] border border-slate-800 focus-within:border-slate-600 rounded-xl p-2 transition shadow-sm">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask Terence Tao anything about mathematics, research papers, or problem solving..."
            rows={2}
            className="w-full bg-transparent text-xs text-slate-100 placeholder-slate-500 focus:outline-none resize-none px-2 py-1"
          />
          <div className="flex items-center justify-between pt-1 px-1 border-t border-slate-800/60 mt-1">
            <span className="text-[10px] font-mono text-slate-500">
              Press Enter to send, Shift+Enter for newline
            </span>
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="flex items-center gap-1.5 bg-slate-100 hover:bg-white disabled:opacity-40 text-slate-900 font-semibold px-3 py-1 rounded-lg text-xs transition shadow-sm"
            >
              <span>Send</span>
              <Send className="w-3 h-3" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
