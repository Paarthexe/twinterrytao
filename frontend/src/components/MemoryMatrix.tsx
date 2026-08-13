import React from 'react';
import { Brain, HelpCircle, UserCheck, Clock, Calendar, Sparkles } from 'lucide-react';

interface MemoryData {
  discussed_topics: string[];
  user_questions: Array<{ date: string; question: string }>;
  user_facts: string[];
  last_updated: string | null;
  stats: {
    topics_count: number;
    questions_count: number;
    facts_count: number;
  };
}

interface MemoryMatrixProps {
  memoryData: MemoryData | null;
  onRefresh: () => void;
}

export const MemoryMatrix: React.FC<MemoryMatrixProps> = ({ memoryData }) => {
  if (!memoryData) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 font-mono text-sm">
        Loading memory matrix...
      </div>
    );
  }

  const formatDate = (isoString: string) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      
      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
          <div className="w-11 h-11 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">
              {memoryData.stats.topics_count}
            </div>
            <div className="text-xs text-slate-400 font-medium">Mathematical Topics Registered</div>
          </div>
        </div>

        <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
          <div className="w-11 h-11 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200">
            <HelpCircle className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">
              {memoryData.stats.questions_count}
            </div>
            <div className="text-xs text-slate-400 font-medium">Notable Questions Asked</div>
          </div>
        </div>

        <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5 flex items-center gap-4 shadow-sm">
          <div className="w-11 h-11 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200">
            <UserCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100 font-mono">
              {memoryData.stats.facts_count}
            </div>
            <div className="text-xs text-slate-400 font-medium">Learned Profile Facts</div>
          </div>
        </div>

      </div>

      {/* Main Grid: Topics & Facts Left, Timeline Right */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Column: Topics & Facts */}
        <div className="space-y-6">
          
          {/* Topics Card */}
          <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-4 h-4 text-slate-400" />
              <h3 className="text-sm font-semibold text-slate-100 tracking-tight">Explored Math Topics</h3>
            </div>

            {memoryData.discussed_topics.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {memoryData.discussed_topics.map((topic, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 border border-slate-800 text-slate-300 font-mono"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic bg-slate-900/40 p-4 rounded-xl border border-slate-800/60">
                No mathematical topics registered in long-term memory yet.
              </p>
            )}
          </div>

          {/* User Profile Facts Card */}
          <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-4">
              <UserCheck className="w-4 h-4 text-slate-400" />
              <h3 className="text-sm font-semibold text-slate-100 tracking-tight">User Facts Profile</h3>
            </div>

            {memoryData.user_facts.length > 0 ? (
              <div className="space-y-2">
                {memoryData.user_facts.map((fact, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed"
                  >
                    • {fact}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic bg-slate-900/40 p-4 rounded-xl border border-slate-800/60">
                No personal mathematical facts or background learned from conversation history yet.
              </p>
            )}
          </div>

        </div>

        {/* Right Column: Questions Timeline */}
        <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-slate-400" />
              <h3 className="text-sm font-semibold text-slate-100 tracking-tight">Stored Questions Timeline</h3>
            </div>
            {memoryData.last_updated && (
              <span className="text-[10px] font-mono text-slate-500">
                Sync: {formatDate(memoryData.last_updated)}
              </span>
            )}
          </div>

          {memoryData.user_questions.length > 0 ? (
            <div className="space-y-3 overflow-y-auto max-h-[500px] pr-2">
              {[...memoryData.user_questions].reverse().map((item, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/90 text-xs space-y-1">
                  <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-400">
                    <Calendar className="w-3 h-3 text-slate-500" />
                    <span>{formatDate(item.date)}</span>
                  </div>
                  <p className="text-slate-200 leading-relaxed">{item.question}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-500 italic bg-slate-900/40 p-4 rounded-xl border border-slate-800/60">
              No question timeline logged yet. Start chatting to build your persistent memory record!
            </p>
          )}
        </div>

      </div>

    </div>
  );
};
