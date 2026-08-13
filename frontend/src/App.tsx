import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ChatWorkspace } from './components/ChatWorkspace';
import type { ChatMessage } from './components/ChatWorkspace';
import { MemoryMatrix } from './components/MemoryMatrix';
import { ConceptExplorer } from './components/ConceptExplorer';
import type { GraphNode, GraphEdge } from './components/ForceGraph';


interface SystemStatus {
  status: string;
  chroma_items: number;
  model: string;
}

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

export function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'memory' | 'explore'>('chat');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [memoryData, setMemoryData] = useState<MemoryData | null>(null);

  // Fetch health check & system status
  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setSystemStatus(data);
      }
    } catch {
      // Ignore if backend is coming up
    }
  };

  // Fetch long term memory
  const fetchMemory = async () => {
    try {
      const res = await fetch('/api/memory');
      if (res.ok) {
        const data = await res.json();
        setMemoryData(data);
      }
    } catch (err) {
      console.error('Failed to fetch memory:', err);
    }
  };

  useEffect(() => {
    fetchHealth();
    fetchMemory();
  }, []);

  const handleNewChat = () => {
    setMessages([]);
  };

  const handleClearMemory = async () => {
    if (!confirm('Are you sure you want to clear long-term memory?')) return;
    try {
      const res = await fetch('/api/memory/clear', { method: 'POST' });
      if (res.ok) {
        await fetchMemory();
        alert('Memory cleared successfully.');
      }
    } catch (err) {
      alert('Failed to clear memory: ' + err);
    }
  };

  const handleSendMessage = async (userText: string) => {
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userText
    };

    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const historyPayload = newMessages.map(m => ({
        role: m.role,
        content: m.content
      }));

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userText,
          history: historyPayload
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || 'Failed to communicate with Terence Tao AI');
      }

      const data = await res.json();

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        sources: data.sources
      };

      setMessages([...newMessages, assistantMsg]);
      await fetchMemory();
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `**Error calling AI backend:** ${err.message || String(err)}`
      };
      setMessages([...newMessages, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateGraph = async (topic: string): Promise<{ nodes: GraphNode[]; edges: GraphEdge[] } | null> => {
    try {
      const res = await fetch('/api/explore/graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      if (!res.ok) throw new Error('Graph generation failed');
      const data = await res.json();
      return data.graph || null;
    } catch (err) {
      console.error('Error generating graph:', err);
      return null;
    }
  };

  const handleExplainNode = async (topicLabel: string, coreTopic: string): Promise<string | null> => {
    try {
      const res = await fetch('/api/explore/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic_label: topicLabel, core_topic: coreTopic })
      });
      if (!res.ok) throw new Error('Node explanation failed');
      const data = await res.json();
      return data.explanation || null;
    } catch (err) {
      console.error('Error explaining node:', err);
      return 'Failed to generate explanation for this topic.';
    }
  };

  return (
    <div className="h-screen bg-[#0B0F17] text-slate-100 flex flex-col font-sans overflow-hidden">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onNewChat={handleNewChat}
        onClearMemory={handleClearMemory}
        systemStatus={systemStatus}
      />

      <main className="flex-1 flex flex-col min-h-0 overflow-auto">
        {activeTab === 'chat' && (
          <ChatWorkspace
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
        )}

        {activeTab === 'memory' && (
          <MemoryMatrix
            memoryData={memoryData}
            onRefresh={fetchMemory}
          />
        )}

        {activeTab === 'explore' && (
          <ConceptExplorer
            onGenerateGraph={handleGenerateGraph}
            onExplainNode={handleExplainNode}
          />
        )}
      </main>
    </div>

  );
}

export default App;
