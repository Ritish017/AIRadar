import React, { useState, useEffect } from "react";
import { Search, X, Zap, Globe, TrendingUp, ArrowUpRight } from "lucide-react";
import { MOCK_EVENTS, MOCK_NEWS_ITEMS, MOCK_TRENDS } from "../lib/mockData";

interface GlobalSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectResult?: (type: string, item: any) => void;
}

export const GlobalSearchModal: React.FC<GlobalSearchModalProps> = ({
  isOpen,
  onClose,
  onSelectResult
}) => {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<any>({ events: [], news: [], trends: [] });
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (!query || query.length < 2) {
      setResults({ events: [], news: [], trends: [] });
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        if (res.ok) {
          const text = await res.text();
          if (!text.trim().startsWith("<")) {
            const data = JSON.parse(text);
            if (data.results) {
              setResults(data.results);
              return;
            }
          }
        }
        const q = query.toLowerCase();
        setResults({
          events: MOCK_EVENTS.filter(e => e.title.toLowerCase().includes(q) || e.summary.toLowerCase().includes(q)),
          news: MOCK_NEWS_ITEMS.filter(n => n.title.toLowerCase().includes(q) || n.content.toLowerCase().includes(q)),
          trends: MOCK_TRENDS.filter(t => t.name.toLowerCase().includes(q) || t.category.toLowerCase().includes(q))
        });
      } catch (err) {
        console.warn("Backend search unavailable, searching offline intelligence:", err);
        const q = query.toLowerCase();
        setResults({
          events: MOCK_EVENTS.filter(e => e.title.toLowerCase().includes(q) || e.summary.toLowerCase().includes(q)),
          news: MOCK_NEWS_ITEMS.filter(n => n.title.toLowerCase().includes(q) || n.content.toLowerCase().includes(q)),
          trends: MOCK_TRENDS.filter(t => t.name.toLowerCase().includes(q) || t.category.toLowerCase().includes(q))
        });
      } finally {
        setLoading(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-[#090d16] border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col">
        {/* Search Input */}
        <div className="p-4 border-b border-slate-800 flex items-center gap-3 bg-[#0d121f]">
          <Search className="w-5 h-5 text-slate-400" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search events, news, or trends (e.g., DeepSeek, Claude, Llama)..."
            className="flex-1 bg-transparent text-sm text-white placeholder-slate-500 focus:outline-none"
          />
          <button onClick={onClose} className="p-1 rounded text-slate-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results */}
        <div className="max-h-[60vh] overflow-y-auto p-4 space-y-4 text-xs">
          {loading && (
            <p className="text-center py-6 text-slate-500 font-mono">Searching intelligence graph...</p>
          )}

          {/* Events */}
          {results.events && results.events.length > 0 && (
            <div className="space-y-2">
              <span className="font-mono text-slate-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <Zap className="w-3 h-3 text-amber-400" /> Canonical Events ({results.events.length})
              </span>
              {results.events.map((ev: any) => (
                <div
                  key={ev.id}
                  onClick={() => { onSelectResult && onSelectResult("event", ev); onClose(); }}
                  className="p-2.5 rounded-lg bg-[#0e1322] hover:bg-slate-800/60 border border-slate-800 cursor-pointer flex items-center justify-between"
                >
                  <div>
                    <div className="font-bold text-white text-xs">{ev.title}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{ev.category} • Status: {ev.status}</div>
                  </div>
                  <ArrowUpRight className="w-3.5 h-3.5 text-slate-500" />
                </div>
              ))}
            </div>
          )}

          {/* News */}
          {results.news && results.news.length > 0 && (
            <div className="space-y-2">
              <span className="font-mono text-slate-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <Globe className="w-3 h-3 text-sky-400" /> Global News ({results.news.length})
              </span>
              {results.news.map((item: any) => (
                <div
                  key={item.id}
                  onClick={() => { onSelectResult && onSelectResult("news", item); onClose(); }}
                  className="p-2.5 rounded-lg bg-[#0e1322] hover:bg-slate-800/60 border border-slate-800 cursor-pointer flex items-center justify-between"
                >
                  <div>
                    <div className="font-bold text-white text-xs">{item.title}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{item.source} • {item.source_quality}</div>
                  </div>
                  <ArrowUpRight className="w-3.5 h-3.5 text-slate-500" />
                </div>
              ))}
            </div>
          )}

          {/* Trends */}
          {results.trends && results.trends.length > 0 && (
            <div className="space-y-2">
              <span className="font-mono text-slate-500 text-[10px] uppercase font-bold flex items-center gap-1">
                <TrendingUp className="w-3 h-3 text-violet-400" /> Trends ({results.trends.length})
              </span>
              {results.trends.map((tr: any) => (
                <div
                  key={tr.id}
                  onClick={() => { onSelectResult && onSelectResult("trend", tr); onClose(); }}
                  className="p-2.5 rounded-lg bg-[#0e1322] hover:bg-slate-800/60 border border-slate-800 cursor-pointer flex items-center justify-between"
                >
                  <div>
                    <div className="font-bold text-white text-xs">{tr.name}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{tr.category} • Momentum: {tr.momentum}</div>
                  </div>
                  <ArrowUpRight className="w-3.5 h-3.5 text-slate-500" />
                </div>
              ))}
            </div>
          )}

          {!loading && query.length >= 2 && results.events.length === 0 && results.news.length === 0 && results.trends.length === 0 && (
            <p className="text-center py-8 text-slate-500">No results found for "{query}".</p>
          )}
        </div>
      </div>
    </div>
  );
};
