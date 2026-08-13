import React, { useState } from 'react';
import { Search, Network, Loader2, Sparkles, BookOpenCheck } from 'lucide-react';
import { ForceGraph } from './ForceGraph';
import type { GraphNode, GraphEdge } from './ForceGraph';
import { MarkdownViewer } from './MarkdownViewer';

interface ConceptExplorerProps {
  onGenerateGraph: (topic: string) => Promise<{ nodes: GraphNode[]; edges: GraphEdge[] } | null>;
  onExplainNode: (topicLabel: string, coreTopic: string) => Promise<string | null>;
}

const PRESET_EXPLORE_TOPICS = [
  'Kakeya Conjecture',
  'Green-Tao Theorem',
  'Navier-Stokes Blowup',
  'Compressed Sensing',
  'Erdős Discrepancy'
];

export const ConceptExplorer: React.FC<ConceptExplorerProps> = ({
  onGenerateGraph,
  onExplainNode
}) => {
  const [topic, setTopic] = useState('');
  const [activeCoreTopic, setActiveCoreTopic] = useState('');
  const [graphData, setGraphData] = useState<{ nodes: GraphNode[]; edges: GraphEdge[] } | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [isGeneratingGraph, setIsGeneratingGraph] = useState(false);
  const [isGeneratingExplain, setIsGeneratingExplain] = useState(false);

  const handleExplore = async (exploreTopic: string) => {
    if (!exploreTopic.trim() || isGeneratingGraph) return;
    const queryTopic = exploreTopic.trim();
    setIsGeneratingGraph(true);
    setActiveCoreTopic(queryTopic);
    setSelectedNodeId(null);
    setExplanation(null);

    const result = await onGenerateGraph(queryTopic);
    setGraphData(result);
    setIsGeneratingGraph(false);
  };

  const handleSelectNode = async (nodeId: string) => {
    if (!graphData || nodeId === selectedNodeId) return;
    setSelectedNodeId(nodeId);

    const targetNode = graphData.nodes.find(n => n.id === nodeId);
    if (!targetNode) return;

    setIsGeneratingExplain(true);
    setExplanation(null);

    const result = await onExplainNode(targetNode.label, activeCoreTopic);
    setExplanation(result);
    setIsGeneratingExplain(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      
      {/* Search Header */}
      <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
            <Network className="w-5 h-5 text-slate-300" />
            <span>Mathematical Concept Explorer</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Map out conceptual relationships and explore Terence Tao's work on mathematical fields.
          </p>
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleExplore(topic);
          }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a mathematical topic (e.g., Kakeya Conjecture)..."
              className="w-full bg-slate-900 border border-slate-800 focus:border-slate-600 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition font-sans"
            />
          </div>
          <button
            type="submit"
            disabled={!topic.trim() || isGeneratingGraph}
            className="flex items-center justify-center gap-2 bg-slate-100 hover:bg-white disabled:opacity-40 text-slate-900 font-semibold px-6 py-2.5 rounded-xl text-sm transition shadow-sm"
          >
            {isGeneratingGraph ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-slate-900" />
                <span>Mapping...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-slate-900" />
                <span>Explore Map</span>
              </>
            )}
          </button>
        </form>

        {/* Preset Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className="text-xs font-mono text-slate-500">Presets:</span>
          {PRESET_EXPLORE_TOPICS.map((preset, idx) => (
            <button
              key={idx}
              onClick={() => {
                setTopic(preset);
                handleExplore(preset);
              }}
              className="px-3 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 hover:text-slate-100 transition font-mono"
            >
              {preset}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      {graphData ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Force Graph (Takes 2 columns) */}
          <div className="lg:col-span-2 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-200 font-mono">
                Knowledge Graph: {activeCoreTopic}
              </h3>
              <span className="text-xs text-slate-400 font-mono">
                {graphData.nodes.length} concepts • {graphData.edges.length} relationships
              </span>
            </div>

            <ForceGraph
              nodes={graphData.nodes}
              edges={graphData.edges}
              selectedNodeId={selectedNodeId}
              onSelectNode={handleSelectNode}
            />
          </div>

          {/* Side Panel: Explanation Drawer */}
          <div className="bg-[#0E131F] border border-slate-800 rounded-2xl p-5 flex flex-col h-[560px]">
            <div className="flex items-center gap-2 pb-3 mb-3 border-b border-slate-800">
              <BookOpenCheck className="w-4 h-4 text-slate-400" />
              <h3 className="text-sm font-semibold text-slate-100">Topic Explanation</h3>
            </div>

            <div className="flex-1 overflow-y-auto pr-1">
              {selectedNodeId ? (
                <div>
                  <div className="mb-3">
                    <span className="text-xs font-mono text-slate-200 bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
                      {graphData.nodes.find(n => n.id === selectedNodeId)?.label}
                    </span>
                  </div>

                  {isGeneratingExplain ? (
                    <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                      <Loader2 className="w-6 h-6 text-slate-400 animate-spin" />
                      <span className="text-xs font-mono text-slate-400">
                        Synthesizing mathematical explanation...
                      </span>
                    </div>
                  ) : explanation ? (
                    <MarkdownViewer content={explanation} />
                  ) : (
                    <p className="text-xs text-slate-400">No explanation generated.</p>
                  )}
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500 space-y-2">
                  <Network className="w-8 h-8 opacity-40 text-slate-400" />
                  <p className="text-xs leading-relaxed">
                    Select any concept node in the graph to view detailed mathematical analysis & RAG references.
                  </p>
                </div>
              )}
            </div>
          </div>

        </div>
      ) : (
        <div className="bg-[#0E131F]/50 border border-slate-800/80 rounded-2xl p-16 text-center space-y-3">
          <Network className="w-10 h-10 text-slate-500 mx-auto" />
          <h3 className="text-base font-semibold text-slate-300">Ready to Explore</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Type a topic above or pick a preset to construct a concept graph.
          </p>
        </div>
      )}

    </div>
  );
};
