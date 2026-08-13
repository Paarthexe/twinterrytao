import React, { useState, useRef, useEffect } from 'react';

export interface GraphNode {
  id: string;
  label: string;
  description?: string;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
}

export interface GraphEdge {
  source: string;
  target: string;
  label?: string;
  from?: string;
  to?: string;
}

interface ForceGraphProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNodeId: string | null;
  onSelectNode: (nodeId: string) => void;
}

export const ForceGraph: React.FC<ForceGraphProps> = ({
  nodes,
  edges,
  selectedNodeId,
  onSelectNode
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [nodePositions, setNodePositions] = useState<Record<string, { x: number; y: number }>>({});
  const [draggingNode, setDraggingNode] = useState<string | null>(null);

  // Initialize node layout positions in a circle/force layout simulation
  useEffect(() => {
    if (!nodes || nodes.length === 0) return;

    const width = 650;
    const height = 450;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    const initialPos: Record<string, { x: number; y: number }> = {};
    
    nodes.forEach((node, index) => {
      if (index === 0) {
        // Central node
        initialPos[node.id] = { x: centerX, y: centerY };
      } else {
        const angle = ((index - 1) / (nodes.length - 1)) * 2 * Math.PI;
        initialPos[node.id] = {
          x: centerX + radius * Math.cos(angle),
          y: centerY + radius * Math.sin(angle)
        };
      }
    });

    setNodePositions(initialPos);
  }, [nodes]);

  const handleMouseDown = (nodeId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setDraggingNode(nodeId);
    onSelectNode(nodeId);
  };

  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!draggingNode || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setNodePositions(prev => ({
      ...prev,
      [draggingNode]: { x, y }
    }));
  };

  const handleMouseUp = () => {
    setDraggingNode(null);
  };

  const getEdgeEndpoints = (edge: GraphEdge) => {
    const sId = edge.source || edge.from || '';
    const tId = edge.target || edge.to || '';
    const sourcePos = nodePositions[sId];
    const targetPos = nodePositions[tId];
    return { sourcePos, targetPos, sId, tId };
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-[520px] bg-[#090D15] rounded-2xl border border-slate-800 overflow-hidden shadow-inner flex items-center justify-center select-none"
    >
      <svg
        className="w-full h-full cursor-crosshair"
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="8"
            markerHeight="6"
            refX="22"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#334155" />
          </marker>
          <marker
            id="arrowhead-active"
            markerWidth="8"
            markerHeight="6"
            refX="22"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 8 3, 0 6" fill="#64748B" />
          </marker>
        </defs>

        {/* Render Edges */}
        {edges.map((edge, idx) => {
          const { sourcePos, targetPos, sId, tId } = getEdgeEndpoints(edge);
          if (!sourcePos || !targetPos) return null;

          const isConnectedToSelected = selectedNodeId && (sId === selectedNodeId || tId === selectedNodeId);
          const midX = (sourcePos.x + targetPos.x) / 2;
          const midY = (sourcePos.y + targetPos.y) / 2;

          return (
            <g key={idx}>
              <line
                x1={sourcePos.x}
                y1={sourcePos.y}
                x2={targetPos.x}
                y2={targetPos.y}
                stroke={isConnectedToSelected ? '#64748B' : '#1E293B'}
                strokeWidth={isConnectedToSelected ? 1.5 : 1}
                strokeDasharray={isConnectedToSelected ? 'none' : '4 4'}
                markerEnd={isConnectedToSelected ? 'url(#arrowhead-active)' : 'url(#arrowhead)'}
                className="transition-colors duration-200"
              />
              {edge.label && (
                <text
                  x={midX}
                  y={midY - 5}
                  fill={isConnectedToSelected ? '#94A3B8' : '#475569'}
                  fontSize="10"
                  fontFamily="monospace"
                  textAnchor="middle"
                >
                  {edge.label}
                </text>
              )}
            </g>
          );
        })}

        {/* Render Nodes */}
        {nodes.map((node) => {
          const pos = nodePositions[node.id];
          if (!pos) return null;

          const isSelected = node.id === selectedNodeId;

          return (
            <g
              key={node.id}
              transform={`translate(${pos.x}, ${pos.y})`}
              onMouseDown={(e) => handleMouseDown(node.id, e)}
              className="cursor-grab active:cursor-grabbing group"
            >
              {/* Highlight border on selected node */}
              {isSelected && (
                <rect
                  x="-74"
                  y="-21"
                  width="148"
                  height="42"
                  rx="11"
                  fill="none"
                  stroke="#64748B"
                  strokeWidth="1.5"
                />
              )}

              {/* Node Pill Shape */}
              <rect
                x="-70"
                y="-18"
                width="140"
                height="36"
                rx="10"
                fill={isSelected ? '#1E293B' : '#0F172A'}
                stroke={isSelected ? '#94A3B8' : '#334155'}
                strokeWidth="1"
                className="transition-all duration-200 group-hover:stroke-slate-400"
              />

              {/* Node Label Text */}
              <text
                x="0"
                y="3"
                fill={isSelected ? '#F8FAFC' : '#CBD5E1'}
                fontSize="11"
                fontWeight={isSelected ? '600' : '400'}
                fontFamily="sans-serif"
                textAnchor="middle"
                className="pointer-events-none"
              >
                {node.label.length > 18 ? node.label.substring(0, 16) + '...' : node.label}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="absolute bottom-3 left-3 text-[10px] font-mono text-slate-500 bg-slate-900/90 px-2.5 py-1 rounded border border-slate-800 pointer-events-none">
        Click node to inspect explanation • Drag to arrange
      </div>
    </div>
  );
};
