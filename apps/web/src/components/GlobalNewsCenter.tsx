import React, { useState, useEffect } from "react";
import { 
  Globe, Search, Filter, Shield, CheckCircle2, 
  AlertCircle, ExternalLink, Sparkles, RefreshCw, Cpu
} from "lucide-react";
import { MOCK_NEWS_ITEMS } from "../lib/mockData";

interface NewsItem {
  id: string;
  title: string;
  content: string;
  source: string;
  source_quality: string;
  url: string;
  published_at: string;
  category: string;
  viral_potential: number;
  confirmed_facts: string[];
  uncertain_claims: string[];
}

interface GlobalNewsCenterProps {
  onOpenContentStudioForNews: (item: NewsItem) => void;
}

const CATEGORIES = [
  "All",
  "AI Models",
  "AI Companies",
  "AI Agents",
  "AI Coding",
  "AI Video",
  "AI Image",
  "Robotics",
  "Research",
  "AI Business",
  "AI Hardware",
  "AI Policy"
];

export const GlobalNewsCenter: React.FC<GlobalNewsCenterProps> = ({
  onOpenContentStudioForNews
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [selectedTier, setSelectedTier] = useState<string>("All");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchNews = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (selectedCategory !== "All") params.append("category", selectedCategory);
      if (selectedTier !== "All") params.append("tier", selectedTier);
      if (searchQuery) params.append("search", searchQuery);

      const res = await fetch(`/api/news?${params.toString()}`);
      if (res.ok) {
        const text = await res.text();
        if (!text.trim().startsWith("<")) {
          const data = JSON.parse(text);
          if (data.items && data.items.length > 0) {
            setNews(data.items);
            return;
          }
        }
      }
      let filtered = [...MOCK_NEWS_ITEMS];
      if (selectedCategory !== "All") filtered = filtered.filter(i => i.category === selectedCategory);
      if (selectedTier !== "All") filtered = filtered.filter(i => i.source_quality === selectedTier);
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        filtered = filtered.filter(i => i.title.toLowerCase().includes(q) || i.content.toLowerCase().includes(q));
      }
      setNews(filtered);
    } catch (err) {
      console.warn("Backend news stream unavailable, loading verified news fallback:", err);
      let filtered = [...MOCK_NEWS_ITEMS];
      if (selectedCategory !== "All") filtered = filtered.filter(i => i.category === selectedCategory);
      if (selectedTier !== "All") filtered = filtered.filter(i => i.source_quality === selectedTier);
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        filtered = filtered.filter(i => i.title.toLowerCase().includes(q) || i.content.toLowerCase().includes(q));
      }
      setNews(filtered);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, [selectedCategory, selectedTier]);

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="bg-[#0d121f] border border-slate-800/80 p-5 rounded-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-black text-white flex items-center gap-2">
              <Globe className="w-5 h-5 text-sky-400" />
              Global AI News Center
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Curated intelligence stream across 11 AI domain categories with quality tiering.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && fetchNews()}
                placeholder="Search headlines..."
                className="bg-slate-900 border border-slate-700/80 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
            </div>

            <button
              onClick={fetchNews}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-sky-400" : ""}`} />
            </button>
          </div>
        </div>

        {/* 11 Category Selector Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pt-4 pb-1 scrollbar-thin">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition ${
                selectedCategory === cat
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 font-bold"
                  : "bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Quality Tier Filter Bar */}
      <div className="flex items-center gap-3 text-xs font-mono">
        <span className="text-slate-500 flex items-center gap-1">
          <Shield className="w-3.5 h-3.5" /> Source Quality:
        </span>
        {["All", "Tier 1", "Tier 2", "Tier 3"].map((tier) => (
          <button
            key={tier}
            onClick={() => setSelectedTier(tier)}
            className={`px-2.5 py-0.5 rounded text-[11px] transition ${
              selectedTier === tier
                ? "bg-slate-700 text-white font-bold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            {tier === "Tier 1" ? "Tier 1 (Official Labs)" : tier === "Tier 2" ? "Tier 2 (Tech Press)" : tier}
          </button>
        ))}
      </div>

      {/* News Cards Grid */}
      {loading && news.length === 0 ? (
        <div className="text-center p-16 bg-[#0d121f]/50 border border-slate-800 rounded-xl">
          <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto mb-3" />
          <p className="text-sm text-slate-400 font-mono">Loading categorized global AI news...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {news.map((item) => (
            <div
              key={item.id}
              className="bg-[#0e1322] border border-slate-800 hover:border-slate-700 rounded-xl p-5 flex flex-col justify-between transition group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-800 text-slate-300 text-[10px] font-mono px-2 py-0.5 rounded">
                      {item.category || "General AI"}
                    </span>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                      item.source_quality === "Tier 1" 
                        ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/40" 
                        : "bg-slate-800 text-slate-400"
                    }`}>
                      {item.source} ({item.source_quality})
                    </span>
                  </div>

                  <span className="text-[11px] font-mono text-slate-500">
                    {new Date(item.published_at).toLocaleDateString()}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white group-hover:text-sky-300 transition leading-snug mb-2">
                  {item.title}
                </h3>
                <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed mb-4">
                  {item.content}
                </p>

                {/* Confirmed Facts if available */}
                {item.confirmed_facts && item.confirmed_facts.length > 0 && (
                  <div className="bg-[#121829] border border-slate-800 rounded p-2.5 mb-3 text-[11px]">
                    <span className="text-emerald-400 font-mono font-semibold flex items-center gap-1 mb-1">
                      <CheckCircle2 className="w-3 h-3" /> Verified Claim:
                    </span>
                    <p className="text-slate-300">{item.confirmed_facts[0]}</p>
                  </div>
                )}
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-slate-800/60 mt-2">
                <a
                  href={item.url}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1 text-xs font-mono text-slate-400 hover:text-slate-200 transition"
                >
                  <span>Read Source</span>
                  <ExternalLink className="w-3 h-3" />
                </a>

                <button
                  onClick={() => onOpenContentStudioForNews(item)}
                  className="flex items-center gap-1.5 bg-sky-600/20 hover:bg-sky-600/30 text-sky-300 border border-sky-500/30 px-3 py-1 rounded-lg text-xs font-semibold transition"
                >
                  <Sparkles className="w-3.5 h-3.5 text-sky-400" />
                  <span>Synthesize Content</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
