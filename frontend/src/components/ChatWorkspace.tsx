import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Sparkles,
  BookOpen,
  ShieldCheck,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
  User,
  Loader2,
  FileCode,
  FileCheck2,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { MarkdownViewer } from './MarkdownViewer';

export interface PeerReviewAudit {
  status: 'pass' | 'revise';
  issues?: string[];
  advice?: string;
  draft?: string;
  extra_sources?: string[];
  checked_sources?: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  audit?: PeerReviewAudit;
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
  const [expandedAudits, setExpandedAudits] = useState<Record<string, boolean>>({});
  const [showDrafts, setShowDrafts] = useState<Record<string, boolean>>({});
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

  const toggleAudit = (msgId: string) => {
    setExpandedAudits(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const toggleDraft = (msgId: string) => {
    setShowDrafts(prev => ({ ...prev, [msgId]: !prev[msgId] }));
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
              Explore mathematical reasoning, research papers, and problem-solving strategies using hybrid vector+sparse RAG with multi-stage skeptic peer review.
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
                  : 'bg-[#0E131F] border-slate-800 text-slate-200 rounded-tl-xs shadow-sm w-full'
              }`}>
                {msg.role === 'user' ? (
                  <p className="text-xs leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <div>
                    {/* Collapsible Skeptic Peer Review Audit Drawer */}
                    {msg.audit && (
                      <div className="mb-3 rounded-xl border border-slate-800/90 bg-slate-950/60 overflow-hidden text-xs">
                        <button
                          onClick={() => toggleAudit(msg.id)}
                          className={`w-full flex items-center justify-between px-3 py-2 text-left font-mono transition-colors ${
                            msg.audit.status === 'revise'
                              ? 'bg-amber-950/20 hover:bg-amber-950/30 text-amber-300'
                              : 'bg-emerald-950/20 hover:bg-emerald-950/30 text-emerald-300'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            {msg.audit.status === 'revise' ? (
                              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
                            ) : (
                              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                            )}
                            <span className="font-semibold text-[11px] tracking-wide">
                              {msg.audit.status === 'revise'
                                ? `Peer Review Audit: Revised (${msg.audit.issues?.length || 1} issues resolved)`
                                : 'Peer Review Audit: Passed (Verified against literature)'}
                            </span>
                          </div>
                          <div className="flex items-center gap-1 text-slate-400 text-[10px]">
                            <span>{expandedAudits[msg.id] ? 'Hide Audit' : 'Inspect Audit'}</span>
                            {expandedAudits[msg.id] ? (
                              <ChevronUp className="w-3.5 h-3.5" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5" />
                            )}
                          </div>
                        </button>

                        {expandedAudits[msg.id] && (
                          <div className="p-3 space-y-2.5 border-t border-slate-800/80 bg-slate-900/50">
                            {/* Issues Checked */}
                            <div>
                              <div className="flex items-center gap-1.5 font-semibold text-slate-300 text-[11px] mb-1">
                                {msg.audit.status === 'revise' ? (
                                  <AlertTriangle className="w-3 h-3 text-amber-400" />
                                ) : (
                                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                                )}
                                <span>Mathematical Rigor & Factuality Assessment</span>
                              </div>
                              {msg.audit.issues && msg.audit.issues.length > 0 ? (
                                <ul className="space-y-1 pl-2 border-l-2 border-amber-500/40 my-1">
                                  {msg.audit.issues.map((issue, idx) => (
                                    <li key={idx} className="text-[11px] text-amber-200/90 font-mono">
                                      • {issue}
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-[11px] text-emerald-300/80 font-mono pl-2 border-l-2 border-emerald-500/40">
                                  All mathematical assertions, bounds, and reasoning steps are strictly grounded in retrieved literature.
                                </p>
                              )}
                            </div>

                            {/* Skeptic Advice */}
                            {msg.audit.advice && (
                              <div className="pt-1.5 border-t border-slate-800">
                                <span className="font-semibold text-slate-400 text-[10px] uppercase tracking-wider block mb-0.5">
                                  Skeptic Auditor Notes & Tone Guidance
                                </span>
                                <p className="text-[11px] text-slate-300 italic bg-slate-950/40 p-2 rounded border border-slate-800/60 font-mono">
                                  "{msg.audit.advice}"
                                </p>
                              </div>
                            )}

                            {/* Raw Draft vs Final Toggle */}
                            {msg.audit.draft && (
                              <div className="pt-1.5 border-t border-slate-800">
                                <button
                                  onClick={() => toggleDraft(msg.id)}
                                  className="flex items-center gap-1.5 text-[11px] font-mono text-slate-400 hover:text-slate-200 transition"
                                >
                                  <FileCode className="w-3 h-3" />
                                  <span>{showDrafts[msg.id] ? 'Hide Raw Pre-Audit Draft' : 'View Raw Pre-Audit Draft'}</span>
                                </button>
                                {showDrafts[msg.id] && (
                                  <div className="mt-2 p-2.5 rounded bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300 max-h-48 overflow-y-auto whitespace-pre-wrap">
                                    <div className="text-[10px] text-amber-400 font-semibold mb-1 uppercase tracking-wider">
                                      Initial Draft (Before Skeptic Audit):
                                    </div>
                                    {msg.audit.draft}
                                  </div>
                                )}
                              </div>
                            )}

                            {/* Checked Sources List */}
                            {(msg.sources && msg.sources.length > 0) && (
                              <div className="pt-1.5 border-t border-slate-800">
                                <div className="flex items-center gap-1 text-[10px] font-mono text-slate-400 mb-1">
                                  <BookOpen className="w-3 h-3" />
                                  <span>Retrieved References ({msg.sources.length}):</span>
                                </div>
                                <div className="flex flex-wrap gap-1">
                                  {msg.sources.map((src, idx) => (
                                    <span
                                      key={idx}
                                      className="text-[10px] font-mono bg-slate-800/80 text-slate-300 px-2 py-0.5 rounded border border-slate-700/60"
                                    >
                                      {src}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Main Assistant Content */}
                    <MarkdownViewer content={msg.content} />

                    {/* Footer Meta Badge */}
                    <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[10px] font-mono text-slate-500">
                      <div className="flex items-center gap-2">
                        <span className="flex items-center gap-1 text-slate-400">
                          <FileCheck2 className="w-3 h-3 text-slate-400" /> Hybrid RAG (Dense + BM25 RRF)
                        </span>
                      </div>
                      {msg.sources && (
                        <span>{msg.sources.length} sources consulted</span>
                      )}
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
