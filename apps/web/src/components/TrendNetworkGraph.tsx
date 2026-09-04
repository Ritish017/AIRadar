import React, { useState, useEffect, useRef } from "react";
import { Share2, ZoomIn, ZoomOut, RefreshCw, Layers, Sparkles } from "lucide-react";
import { TrendGraphData } from "../types";
import { MOCK_GRAPH_DATA } from "../lib/mockData";

interface TrendNetworkGraphProps {
  onSelectTrendNode?: (trendName: string) => void;
}

export const TrendNetworkGraph: React.FC<TrendNetworkGraphProps> = ({
  onSelectTrendNode
}) => {
  const [graphData, setGraphData] = useState<TrendGraphData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedNode, setSelectedNode] = useState<any | null>(null);
  const [scale, setScale] = useState<number>(1);
  const svgRef = useRef<SVGSVGElement>(null);

  const fetchGraph = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/trends/graph?topic_limit=18&event_limit=12");
      if (res.ok) {
        const text = await res.text();
        if (!text.trim().startsWith("<")) {
          const data = JSON.parse(text);
          if (data && data.nodes && data.nodes.length > 0) {
            setGraphData(data);
            return;
          }
        }
      }
      setGraphData(MOCK_GRAPH_DATA as any);
    } catch (err) {
      console.warn("Backend trend graph unavailable, using verified mock graph data:", err);
      setGraphData(MOCK_GRAPH_DATA as any);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  // Compute radial/clustered positions for nodes in SVG canvas (800x500 viewport)
  const computeNodePositions = (nodes: any[]) => {
    const width = 800;
    const height = 500;
    const centerX = width / 2;
    const centerY = height / 2;

    const positioned = [...nodes];
    const catNodes = positioned.filter(n => n.type === "category");
    const trendNodes = positioned.filter(n => n.type === "trend");
    const eventNodes = positioned.filter(n => n.type === "event");

    // Position categories in inner circle
    catNodes.forEach((node, i) => {
      const angle = (i / Math.max(1, catNodes.length)) * 2 * Math.PI;
      node.x = centerX + Math.cos(angle) * 110;
      node.y = centerY + Math.sin(angle) * 100;
    });

    // Position trends in middle ring
    trendNodes.forEach((node, i) => {
      const angle = (i / Math.max(1, trendNodes.length)) * 2 * Math.PI + 0.2;
      node.x = centerX + Math.cos(angle) * 230;
      node.y = centerY + Math.sin(angle) * 190;
    });

    // Position events in outer orbit
    eventNodes.forEach((node, i) => {
      const angle = (i / Math.max(1, eventNodes.length)) * 2 * Math.PI + 0.4;
      node.x = centerX + Math.cos(angle) * 330;
      node.y = centerY + Math.sin(angle) * 230;
    });

    return positioned;
  };

  const positionedNodes = graphData ? computeNodePositions(graphData.nodes) : [];
  const nodeMap = new Map(positionedNodes.map(n => [n.id, n]));

  return (
    <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Share2 className="w-4 h-4 text-violet-400" />
            Interactive Trend & Event Relationship Graph
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Semantic network clusters connecting active AI trends, breaking developments, and domain hubs.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setScale(s => Math.min(1.5, s + 0.1))}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
            title="Zoom In"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setScale(s => Math.max(0.7, s - 0.1))}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
            title="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={fetchGraph}
            className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
            title="Recompute Network"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-violet-400" : ""}`} />
          </button>
        </div>
      </div>

      {/* SVG Network Canvas */}
      <div className="relative w-full h-[480px] bg-[#070a12] border border-slate-800/80 rounded-lg overflow-hidden flex items-center justify-center">
        {loading && !graphData ? (
          <div className="flex flex-col items-center gap-2">
            <RefreshCw className="w-6 h-6 text-violet-400 animate-spin" />
            <span className="text-xs text-slate-400 font-mono">Mapping semantic relationship graph...</span>
          </div>
        ) : (
          <svg
            ref={svgRef}
            viewBox="0 0 800 500"
            className="w-full h-full cursor-grab active:cursor-grabbing select-none"
            style={{ transform: `scale(${scale})`, transition: "transform 0.15s ease" }}
          >
            <defs>
              <linearGradient id="linkGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.25" />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.1" />
              </linearGradient>
            </defs>

            {/* Links / Edges */}
            {graphData?.links.map((link, i) => {
              const sourceNode = nodeMap.get(link.source);
              const targetNode = nodeMap.get(link.target);
              if (!sourceNode || !targetNode) return null;

              return (
                <line
                  key={i}
                  x1={sourceNode.x}
                  y1={sourceNode.y}
                  x2={targetNode.x}
                  y2={targetNode.y}
                  stroke="url(#linkGradient)"
                  strokeWidth={link.value || 1.5}
                  strokeDasharray={link.type === "event_trend_link" ? "3,3" : "none"}
                />
              );
            })}

            {/* Nodes */}
            {positionedNodes.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              const radius = node.type === "category" ? 18 : node.type === "trend" ? 14 : 10;

              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  onClick={() => setSelectedNode(node)}
                  className="cursor-pointer group"
                >
                  {/* Glow circle if selected */}
                  {isSelected && (
                    <circle
                      r={radius + 8}
                      fill="none"
                      stroke={node.color}
                      strokeWidth="2"
                      className="animate-pulse opacity-80"
                    />
                  )}

                  {/* Core Node Circle */}
                  <circle
                    r={radius}
                    fill={node.color}
                    fillOpacity={node.type === "category" ? 0.85 : 0.7}
                    stroke="#ffffff"
                    strokeWidth={isSelected ? 2 : 1}
                    className="transition hover:scale-110"
                  />

                  {/* Node Label */}
                  <text
                    y={radius + 12}
                    textAnchor="middle"
                    fill={isSelected ? "#ffffff" : "#94a3b8"}
                    fontSize={node.type === "category" ? "11px" : "9px"}
                    fontWeight={node.type === "category" ? "bold" : "normal"}
                    fontFamily="Inter, sans-serif"
                    className="pointer-events-none drop-shadow"
                  >
                    {node.name.length > 20 ? node.name.slice(0, 18) + ".." : node.name}
                  </text>
                </g>
              );
            })}
          </svg>
        )}

        {/* Selected Node Inspector Drawer */}
        {selectedNode && (
          <div className="absolute bottom-3 right-3 bg-[#0d121f]/95 border border-slate-700 p-3.5 rounded-lg max-w-xs text-xs backdrop-blur shadow-xl space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-mono text-[10px] text-slate-400 uppercase font-semibold">
                {selectedNode.type} Node
              </span>
              <button 
                onClick={() => setSelectedNode(null)} 
                className="text-slate-500 hover:text-white text-xs"
              >
                ✕
              </button>
            </div>

            <div className="font-bold text-white text-sm leading-tight">
              {selectedNode.full_title || selectedNode.name}
            </div>

            {selectedNode.momentum && (
              <div className="flex items-center justify-between text-slate-300 font-mono text-[11px]">
                <span>Momentum:</span>
                <span className="font-bold text-amber-400">{selectedNode.momentum}/100</span>
              </div>
            )}

            {selectedNode.lifecycle && (
              <div className="flex items-center justify-between text-slate-300 font-mono text-[11px]">
                <span>Stage:</span>
                <span className="font-bold text-sky-400">{selectedNode.lifecycle}</span>
              </div>
            )}

            <button
              onClick={() => onSelectTrendNode && onSelectTrendNode(selectedNode.name)}
              className="w-full bg-violet-600 hover:bg-violet-500 text-white font-semibold py-1.5 rounded transition text-xs flex items-center justify-center gap-1 mt-1"
            >
              <Sparkles className="w-3 h-3" />
              <span>Explore Content Opportunities</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
