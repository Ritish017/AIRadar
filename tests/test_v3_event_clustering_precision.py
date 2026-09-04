"""
V3.1 Event Clustering Precision & Robustness Benchmark Test Suite.
Evaluates heterogeneous real-world sources against:
- 10-source, 20-source, and 50-source realistic fixtures.
- True merges across official blogs, arXiv, GitHub, news, and social channels.
- False merge prevention on shared company entities (e.g. DeepSeek-R1 vs Janus-Pro; o3-mini vs Operator).
- False split prevention on multi-angle coverage (academic paper vs news headline vs dev repo).
- Duplicate and parameterized URL deduplication (?utm_source=..., trailing slashes).
- Syndicated article detection across different news domains.
- Unrelated articles sharing generic AI keywords ("reasoning", "benchmarks", "models").
- Contradictory benchmark claim handling (triggering conflict detection).
- Resurfaced stale articles (>48h / stale timeline).

Calculates and reports:
- Pairwise Precision
- Pairwise Recall
- False Merge Rate
- False Split Rate
- Cluster Purity
"""

import pytest
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from backend.db.session import init_db, AsyncSessionLocal
from backend.services.events.event_engine import event_engine
from backend.db.models import Event, EventSource, EventObservation

async def reset_db():
    """Wipe events table before each test to prevent test state cross-contamination."""
    await init_db()
    async with AsyncSessionLocal() as db:
        await db.execute(delete(EventSource))
        await db.execute(delete(EventObservation))
        await db.execute(delete(Event))
        await db.commit()


def compute_clustering_metrics(items: List[Dict[str, Any]], clustered_events: List[Event], db_sources: List[EventSource]) -> Dict[str, float]:
    """
    Computes pairwise precision, recall, false merge rate, false split rate, and cluster purity.
    Uses ground_truth_id on each item.
    """
    # Map item url/title to cluster event id
    item_to_cluster = {}
    for ev in clustered_events:
        sources = getattr(ev, "sources", None) or []
        for s in sources:
            norm_url = event_engine.normalize_url(s.url)
            if norm_url:
                item_to_cluster[norm_url] = ev.id
            if s.title:
                item_to_cluster[s.title.strip().lower()] = ev.id
            if s.url:
                item_to_cluster[s.url] = ev.id
        # Also map canonical title and primary URL
        if ev.canonical_title:
            item_to_cluster[ev.canonical_title.strip().lower()] = ev.id
        if ev.primary_source_url:
            norm_primary = event_engine.normalize_url(ev.primary_source_url)
            if norm_primary:
                item_to_cluster[norm_primary] = ev.id

    # Resolve cluster for each original test item
    assignments = []
    for idx, it in enumerate(items):
        norm_url = event_engine.normalize_url(it.get("url", ""))
        title_lower = (it.get("title") or "").strip().lower()
        cid = item_to_cluster.get(norm_url) or item_to_cluster.get(title_lower) or item_to_cluster.get(it.get("url", ""))
        # Fallback: check matching title or high similarity in clustered events
        if not cid:
            for ev in clustered_events:
                if (ev.canonical_title or "").strip().lower() == title_lower or event_engine.compute_title_similarity(ev.canonical_title, it.get("title", "")) >= 0.70:
                    cid = ev.id
                    break
        assignments.append((it["ground_truth_id"], cid or f"singleton_{idx}"))

    print(f"DEBUG ASSIGNMENTS ({len(assignments)} items):")
    for gt, cl in assignments:
        print(f"  GT: {gt} -> Cluster: {cl[:8] if cl else None}")


    n = len(assignments)
    tp = 0  # same ground truth, same cluster
    fp = 0  # different ground truth, same cluster (false merge)
    fn = 0  # same ground truth, different cluster (false split)
    tn = 0  # different ground truth, different cluster

    for i in range(n):
        gt_i, cl_i = assignments[i]
        for j in range(i + 1, n):
            gt_j, cl_j = assignments[j]
            same_gt = (gt_i == gt_j)
            same_cl = (cl_i == cl_j)

            if same_gt and same_cl:
                tp += 1
            elif not same_gt and same_cl:
                fp += 1
            elif same_gt and not same_cl:
                fn += 1
            else:
                tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    false_merge_rate = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    false_split_rate = fn / (tp + fn) if (tp + fn) > 0 else 0.0

    # Cluster Purity
    from collections import Counter
    cluster_groups = {}
    for gt_id, cl_id in assignments:
        cluster_groups.setdefault(cl_id, []).append(gt_id)

    total_correct = sum(Counter(gt_list).most_common(1)[0][1] for gt_list in cluster_groups.values())
    purity = total_correct / n if n > 0 else 1.0

    return {
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "false_merge_rate": round(false_merge_rate * 100, 2),
        "false_split_rate": round(false_split_rate * 100, 2),
        "cluster_purity": round(purity * 100, 2),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "num_items": n,
        "num_clusters": len(clustered_events)
    }


# =========================================================================
# 10-SOURCE FIXTURE
# =========================================================================
FIXTURE_10_SOURCES: List[Dict[str, Any]] = [
    # True Event A: DeepSeek-R1 Release
    {
        "ground_truth_id": "event_deepseek_r1",
        "title": "DeepSeek-R1: Open-Source Reasoning Model Released",
        "content": "DeepSeek announces DeepSeek-R1 reasoning model trained via large-scale reinforcement learning.",
        "url": "https://deepseek.com/blog/deepseek-r1",
        "source": "DeepSeek Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=2)
    },
    {
        "ground_truth_id": "event_deepseek_r1",
        "title": "DeepSeek's new R1 reasoning model challenges OpenAI o1 at fraction of cost",
        "content": "Chinese AI lab DeepSeek released DeepSeek-R1 open weights with 671B parameters and MoE architecture.",
        "url": "https://techcrunch.com/2025/01/20/deepseek-r1-launch",
        "source": "TechCrunch",
        "source_type": "news",
        "source_quality": "Tier 2",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=45)
    },
    {
        "ground_truth_id": "event_deepseek_r1",
        "title": "deepseek-ai/DeepSeek-R1: Official inference code and model checkpoints",
        "content": "GitHub repository for DeepSeek-R1 inference engines, quantization scripts, and SGLang configs.",
        "url": "https://github.com/deepseek-ai/DeepSeek-R1",
        "source": "GitHub",
        "source_type": "code",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=30)
    },
    {
        "ground_truth_id": "event_deepseek_r1",
        "title": "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
        "content": "Research paper explaining cold-start data, multi-stage RL training, and distillation to smaller dense models.",
        "url": "https://arxiv.org/abs/2501.12948",
        "source": "arXiv",
        "source_type": "academic",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=15)
    },
    # Duplicate URL with tracking parameters of Event A
    {
        "ground_truth_id": "event_deepseek_r1",
        "title": "DeepSeek-R1: Open-Source Reasoning Model Released",
        "content": "DeepSeek announces DeepSeek-R1 reasoning model trained via large-scale reinforcement learning.",
        "url": "https://deepseek.com/blog/deepseek-r1?utm_source=twitter&utm_medium=social",
        "source": "DeepSeek Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=2)
    },

    # True Event B: DeepSeek Janus-Pro Multimodal (FALSE MERGE TRAP: shares DeepSeek entity!)
    {
        "ground_truth_id": "event_deepseek_janus",
        "title": "DeepSeek releases Janus-Pro multimodal model for visual understanding and generation",
        "content": "DeepSeek unveils Janus-Pro 7B and 1B models unifying multimodal comprehension and visual synthesis.",
        "url": "https://deepseek.com/blog/janus-pro",
        "source": "DeepSeek Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=4)
    },
    {
        "ground_truth_id": "event_deepseek_janus",
        "title": "Janus-Pro open-source vision weights now live on Hugging Face",
        "content": "Community tests DeepSeek Janus-Pro unified multimodal model against SDXL and Flux.",
        "url": "https://huggingface.co/deepseek-ai/Janus-Pro-7B",
        "source": "Hugging Face",
        "source_type": "community",
        "source_quality": "Tier 2",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=3, minutes=30)
    },

    # True Event C: OpenAI o3-mini Launch
    {
        "ground_truth_id": "event_openai_o3_mini",
        "title": "Introducing o3-mini: our newest small reasoning model for STEM and coding",
        "content": "OpenAI releases o3-mini featuring adjustable reasoning effort levels across ChatGPT and API.",
        "url": "https://openai.com/index/o3-mini",
        "source": "OpenAI Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=5)
    },
    {
        "ground_truth_id": "event_openai_o3_mini",
        "title": "OpenAI launches o3-mini reasoning model in ChatGPT free tier",
        "content": "The Verge reports on OpenAI rollout of o3-mini reasoning model to all users including free tier.",
        "url": "https://theverge.com/2025/1/31/openai-o3-mini-reasoning-model",
        "source": "The Verge",
        "source_type": "news",
        "source_quality": "Tier 2",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=4, minutes=45)
    },

    # True Event D: Unrelated academic paper sharing generic keywords ('reasoning', 'benchmarks', 'models')
    {
        "ground_truth_id": "event_stanford_reasoning_survey",
        "title": "Evaluating Emergent Reasoning Behaviors Across Frontier Open Weights LLMs",
        "content": "Stanford researchers conduct comprehensive benchmark survey evaluating mathematical proof and reasoning.",
        "url": "https://arxiv.org/abs/2501.99881",
        "source": "arXiv",
        "source_type": "academic",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=6)
    }
]


# =========================================================================
# 20-SOURCE FIXTURE (Expands 10-Source with Contradictions, Syndication, Follow-ups)
# =========================================================================
FIXTURE_20_SOURCES: List[Dict[str, Any]] = FIXTURE_10_SOURCES + [
    # True Event E: Claude 3.7 Sonnet & Hybrid Reasoning Launch
    {
        "ground_truth_id": "event_claude_37_sonnet",
        "title": "Anthropic introduces Claude 3.7 Sonnet with hybrid reasoning and Claude Code CLI",
        "content": "Anthropic announces Claude 3.7 Sonnet combining instantaneous responses with extended thinking tokens.",
        "url": "https://anthropic.com/news/claude-3-7-sonnet",
        "source": "Anthropic Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=8)
    },
    {
        "ground_truth_id": "event_claude_37_sonnet",
        "title": "Claude 3.7 Sonnet achieves 70.3% on SWE-bench Verified setting new coding frontier",
        "content": "Official benchmark scores show Claude 3.7 Sonnet reaching 70.3% on real-world SWE-bench software engineering tasks.",
        "url": "https://techcrunch.com/2025/02/24/claude-3-7-sonnet-swe-bench",
        "source": "TechCrunch",
        "source_type": "news",
        "source_quality": "Tier 2",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=7, minutes=30)
    },
    # Conflicting Claim / Contradiction on Claude 3.7 benchmark (Must merge + detect contradiction)
    {
        "ground_truth_id": "event_claude_37_sonnet",
        "title": "Independent audit disputes Claude 3.7 Sonnet SWE-bench score: reproduces only 62.1%",
        "content": "Independent researchers dispute Anthropic claims after reproducing Claude 3.7 Sonnet on SWE-bench Verified with pass@1 yielding 62.1%.",
        "url": "https://twitter.com/ai_evals/status/1892837191",
        "source": "X",
        "source_type": "social",
        "source_quality": "Tier 3",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=6, minutes=50)
    },
    # Follow-up update 4 hours later
    {
        "ground_truth_id": "event_claude_37_sonnet",
        "title": "Anthropic clarifies Claude 3.7 Sonnet SWE-bench evaluation methodology and reasoning budget",
        "content": "Anthropic updates documentation explaining 64k extended thinking budget used for 70.3% SWE-bench result.",
        "url": "https://anthropic.com/news/claude-3-7-swe-bench-methodology",
        "source": "Anthropic Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=5, minutes=10)
    },

    # True Event F: vLLM V1 Engine Redesign
    {
        "ground_truth_id": "event_vllm_v1",
        "title": "vLLM V1: A High-Throughput Architecture Overhaul for LLM Serving",
        "content": "vLLM project announces complete V1 core rewrite delivering 3x higher throughput with zero-overhead scheduling.",
        "url": "https://blog.vllm.ai/2025/01/27/v1-alpha-release.html",
        "source": "vLLM Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=10)
    },
    {
        "ground_truth_id": "event_vllm_v1",
        "title": "vllm-project/vllm: V1 release candidate merged into main branch",
        "content": "GitHub pull request details architectural changes, prefix caching enhancements, and torch.compile integrations.",
        "url": "https://github.com/vllm-project/vllm/releases/tag/v1.0.0",
        "source": "GitHub",
        "source_type": "code",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=9, minutes=30)
    },

    # True Event G: Market Impact of DeepSeek on Chip Stocks (Syndicated News Test)
    {
        "ground_truth_id": "event_deepseek_chip_stocks",
        "title": "NVIDIA and global chipmakers tumble following DeepSeek AI efficiency shock",
        "content": "Semiconductor stocks drop sharply as investors assess whether algorithmic efficiency reduces GPU capital expenditure demand.",
        "url": "https://bloomberg.com/news/articles/2025-01-27/nvidia-chip-stocks-deepseek-drop",
        "source": "Bloomberg",
        "source_type": "news",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=12)
    },
    {
        "ground_truth_id": "event_deepseek_chip_stocks",
        "title": "NVIDIA and global chipmakers tumble following DeepSeek AI efficiency shock",
        "content": "Semiconductor stocks drop sharply as investors assess whether algorithmic efficiency reduces GPU capital expenditure demand.",
        "url": "https://finance.yahoo.com/news/nvidia-chipmakers-tumble-deepseek-shock",
        "source": "Yahoo Finance",
        "source_type": "news",
        "source_quality": "Tier 2",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=11, minutes=50)
    },

    # True Event H: Resurfaced Old Stale Event (> 48 hours old)
    {
        "ground_truth_id": "event_stale_gpt4o_audio",
        "title": "OpenAI releases Advanced Voice Mode in GPT-4o for ChatGPT Plus users",
        "content": "Archived release from months ago discussing realistic audio conversations with low latency.",
        "url": "https://openai.com/index/gpt-4o-advanced-voice-archived",
        "source": "OpenAI Archive",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(days=25)  # 25 days old!
    },

    # True Event I: OpenAI Operator Autonomous Agent (FALSE MERGE TRAP with o3-mini: shares OpenAI!)
    {
        "ground_truth_id": "event_openai_operator",
        "title": "OpenAI introduces Operator computer-using autonomous agent preview",
        "content": "OpenAI launches Operator research preview capable of executing web browsing, form completion, and travel booking.",
        "url": "https://openai.com/index/introducing-operator",
        "source": "OpenAI Blog",
        "source_type": "official",
        "source_quality": "Tier 1",
        "published_at": datetime.now(timezone.utc) - timedelta(hours=14)
    }
]


# =========================================================================
# 50-SOURCE FIXTURE (Massive Heterogeneous Real-World Production Load)
# =========================================================================
def generate_50_source_fixture() -> List[Dict[str, Any]]:
    items = list(FIXTURE_20_SOURCES)

    additional_events = [
        # Event J: Google Gemini 2.0 Flash
        ("event_gemini_2_flash", "Google DeepMind releases Gemini 2.0 Flash with native multimodality", "Google DeepMind", "Tier 1", "official", "https://blog.google/technology/ai/gemini-2-0-flash"),
        ("event_gemini_2_flash", "Gemini 2.0 Flash is now available in Google AI Studio and Vertex AI", "TechCrunch", "Tier 2", "news", "https://techcrunch.com/2024/12/11/gemini-2-flash-developer-access"),
        ("event_gemini_2_flash", "Testing Gemini 2.0 Flash real-time multimodal audio and visual streaming API", "Reddit", "Tier 3", "community", "https://reddit.com/r/Bard/comments/gemini_2_flash_stream"),

        # Event K: Gemma 2 2B (Google False Merge Trap with Gemini 2!)
        ("event_google_gemma_2", "Google releases Gemma 2 2B open model for on-device applications", "Google Developers", "Tier 1", "official", "https://developers.googleblog.com/gemma-2-2b"),
        ("event_google_gemma_2", "google/gemma-2-2b: Open weight checkpoints available on Hugging Face", "Hugging Face", "Tier 2", "code", "https://huggingface.co/google/gemma-2-2b"),

        # Event L: Meta Llama 3.3 70B
        ("event_llama_33_70b", "Meta AI launches Llama 3.3 70B with 405B capabilities at 70B cost", "Meta AI", "Tier 1", "official", "https://ai.meta.com/blog/llama-3-3-70b"),
        ("event_llama_33_70b", "Llama 3.3 70B open weights download hits 500k in first 48 hours", "VentureBeat", "Tier 2", "news", "https://venturebeat.com/ai/llama-3-3-hits-500k-downloads"),
        ("event_llama_33_70b", "llama.cpp adds quantized GGUF support for Meta Llama 3.3 70B instruct", "GitHub", "Tier 2", "code", "https://github.com/ggerganov/llama.cpp/releases/tag/b4210"),

        # Event M: Cursor Agent Mode
        ("event_cursor_agent_mode", "Cursor introduces Agent Mode for autonomous codebase edits and terminal execution", "Cursor Forum", "Tier 1", "official", "https://forum.cursor.com/t/agent-mode-launch"),
        ("event_cursor_agent_mode", "How Cursor's new agent mode writes, debugs, and runs code autonomously", "YouTube Tech Review", "Tier 3", "media", "https://youtube.com/watch?v=cursor_agent_demo"),

        # Event N: SWE-bench Verified Leap
        ("event_swebench_verified", "Princeton NLP releases SWE-bench Verified benchmark dataset", "Princeton NLP", "Tier 1", "academic", "https://arxiv.org/abs/2408.15242"),
        ("event_swebench_verified", "swe-bench/SWE-bench-verified official repository and human validation guidelines", "GitHub", "Tier 1", "code", "https://github.com/swe-bench/SWE-bench-verified"),

        # Event O: Manus AI Autonomous Agent
        ("event_manus_agent", "Manus AI unveils general agent capable of cross-application workflows", "Manus Site", "Tier 1", "official", "https://manus.im/launch"),
        ("event_manus_agent", "Manus autonomous agent demo goes viral demonstrating full browser automation", "X", "Tier 3", "social", "https://x.com/manus_ai/status/1897261524"),
        ("event_manus_agent", "Hacker News discussion: Is Manus truly autonomous or scripted demo?", "Hacker News", "Tier 2", "community", "https://news.ycombinator.com/item?id=43291823"),

        # Event P: Qwen 2.5 Coder 32B
        ("event_qwen_25_coder", "Alibaba releases Qwen 2.5-Coder 32B matching GPT-4o on coding benchmarks", "Alibaba Cloud", "Tier 1", "official", "https://qwenlm.github.io/blog/qwen2.5-coder"),
        ("event_qwen_25_coder", "Qwen/Qwen2.5-Coder-32B-Instruct checkpoints released on Hugging Face", "Hugging Face", "Tier 1", "code", "https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct"),

        # Event Q: Qwen 2.5 Math (Qwen False Merge Trap with Qwen Coder!)
        ("event_qwen_25_math", "Alibaba releases Qwen 2.5-Math specialized for mathematical reasoning and Olympiad proofs", "Alibaba Cloud", "Tier 1", "official", "https://qwenlm.github.io/blog/qwen2.5-math"),

        # Event R: NVIDIA Blackwell GB200 NVL72 Shipments
        ("event_nvidia_blackwell_gb200", "NVIDIA begins volume shipments of Blackwell GB200 NVL72 systems to hyperscalers", "NVIDIA Newsroom", "Tier 1", "official", "https://nvidianews.nvidia.com/news/blackwell-gb200-shipments"),
        ("event_nvidia_blackwell_gb200", "Microsoft Azure and AWS deploy first liquid-cooled NVIDIA Blackwell racks", "Reuters", "Tier 1", "news", "https://reuters.com/technology/azure-aws-deploy-blackwell-2025-01-22"),

        # Event S: Mistral Le Chat Reasoning Upgrade
        ("event_mistral_le_chat", "Mistral upgrades Le Chat with web search, canvas, and code execution capabilities", "Mistral AI", "Tier 1", "official", "https://mistral.ai/news/le-chat-update"),
        ("event_mistral_le_chat", "Mistral Le Chat takes on ChatGPT with free reasoning, canvas, and document analysis", "The Verge", "Tier 2", "news", "https://theverge.com/2025/2/6/mistral-le-chat-canvas-reasoning"),

        # Event T: SGLang Fast Serving Engine
        ("event_sglang_serving", "SGLang introduces RadixAttention and fast structured decoding for frontier models", "SGLang Team", "Tier 1", "academic", "https://arxiv.org/abs/2312.07104"),
        ("event_sglang_serving", "sgl-project/sglang v0.4 release accelerates DeepSeek-R1 inference by 4x", "GitHub", "Tier 1", "code", "https://github.com/sgl-project/sglang/releases/tag/v0.4.0"),

        # Additional Syndications & URL variations
        ("event_llama_33_70b", "Meta AI launches Llama 3.3 70B with 405B capabilities at 70B cost", "Meta Syndicated", "Tier 2", "news", "https://ai.meta.com/blog/llama-3-3-70b?utm_source=rss&utm_medium=feed"),
        ("event_nvidia_blackwell_gb200", "NVIDIA begins volume shipments of Blackwell GB200 NVL72 systems to hyperscalers", "Yahoo Tech", "Tier 2", "news", "https://finance.yahoo.com/news/nvidia-begins-volume-shipments-blackwell"),
        ("event_openai_operator", "OpenAI Operator browser agent: What developers need to know", "Ars Technica", "Tier 2", "news", "https://arstechnica.com/ai/2025/01/openai-operator-autonomous-agent"),
        ("event_manus_agent", "Manus AI agent benchmark validation: tests against WebArena and GAIA", "AgentBench Labs", "Tier 2", "academic", "https://agentbench.org/evals/manus-validation"),
        ("event_cursor_agent_mode", "Cursor Agent Mode benchmark: evaluating SWE-bench performance on local workspaces", "DevTools Review", "Tier 2", "news", "https://devtoolsreview.com/cursor-agent-benchmark"),
        ("event_qwen_25_coder", "Qwen 2.5-Coder benchmarked against Claude 3.5 Sonnet on HumanEval and SWE-bench", "AIEval Blog", "Tier 2", "academic", "https://aieval.dev/qwen-25-coder-vs-claude")
    ]

    base_time = datetime.now(timezone.utc) - timedelta(hours=18)
    for idx, (gt_id, title, src, tier, stype, url) in enumerate(additional_events):
        items.append({
            "ground_truth_id": gt_id,
            "title": title,
            "content": f"{title}. Detailed technical breakdown and community reactions to {title}.",
            "url": url,
            "source": src,
            "source_type": stype,
            "source_quality": tier,
            "published_at": base_time + timedelta(minutes=idx * 25)
        })

    return items


# =========================================================================
# TEST SUITE
# =========================================================================

@pytest.mark.asyncio
async def test_clustering_precision_10_sources():
    """
    Evaluates clustering precision, recall, and purity across 10 heterogeneous sources.
    Asserts zero false merges across distinct models (DeepSeek-R1 vs Janus-Pro; o3-mini vs unrelated paper).
    """
    await reset_db()
    async with AsyncSessionLocal() as db:
        events = await event_engine.cluster_items_into_events(FIXTURE_10_SOURCES, db)
        
        # Verify events returned
        assert len(events) >= 4, f"Expected at least 4 canonical events, got {len(events)}"

        metrics = compute_clustering_metrics(FIXTURE_10_SOURCES, events, [])
        print("\n--- 10-SOURCE CLUSTERING METRICS ---")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

        # Assertions
        assert metrics["false_merge_rate"] == 0.0, f"False merge detected! Rate: {metrics['false_merge_rate']}%"
        assert metrics["precision"] >= 95.0, f"Precision {metrics['precision']}% fell below 95%"
        assert metrics["cluster_purity"] >= 90.0, f"Purity {metrics['cluster_purity']}% fell below 90%"


@pytest.mark.asyncio
async def test_clustering_precision_20_sources_with_contradictions():
    """
    Evaluates 20 sources with duplicate URLs, syndicated news, and conflicting claims.
    Verifies that conflicting reports merge into the same canonical event while triggering contradiction detection.
    """
    await reset_db()
    async with AsyncSessionLocal() as db:
        events = await event_engine.cluster_items_into_events(FIXTURE_20_SOURCES, db)
        
        metrics = compute_clustering_metrics(FIXTURE_20_SOURCES, events, [])
        print("\n--- 20-SOURCE CLUSTERING METRICS ---")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

        claude_event = next((e for e in events if "claude" in e.canonical_title.lower() or "3.7" in e.canonical_title.lower()), None)
        assert claude_event is not None, "Claude 3.7 canonical event was not found"
        assert claude_event.status == "DEVELOPING", f"Expected DEVELOPING due to contradiction, got {claude_event.status}"
        assert "[CONFLICT DETECTED" in (claude_event.summary or ""), "Contradiction conflict banner missing from summary"
        assert claude_event.recommended_action == "WAIT", f"Expected WAIT action on conflicted event, got {claude_event.recommended_action}"

        # Assert metrics
        assert metrics["false_merge_rate"] <= 5.0, f"False merge rate {metrics['false_merge_rate']}% too high"
        assert metrics["precision"] >= 90.0, f"Precision {metrics['precision']}% fell below 90%"
        assert metrics["cluster_purity"] >= 88.0, f"Cluster purity {metrics['cluster_purity']}% fell below 88%"


@pytest.mark.asyncio
async def test_clustering_precision_50_sources_production_stress():
    """
    Production load test with 50 realistic heterogeneous sources across 15+ frontier AI events.
    Verifies precision, recall, false merge rate, false split rate, and cluster purity.
    """
    await reset_db()
    items_50 = generate_50_source_fixture()
    assert len(items_50) >= 50, f"Expected 50 items, got {len(items_50)}"

    async with AsyncSessionLocal() as db:
        events = await event_engine.cluster_items_into_events(items_50, db)
        metrics = compute_clustering_metrics(items_50, events, [])
        
        print("\n--- 50-SOURCE PRODUCTION STRESS CLUSTERING METRICS ---")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

        # Strict validation requirements
        assert metrics["precision"] >= 88.0, f"Precision {metrics['precision']}% fell below 88%"
        assert metrics["recall"] >= 80.0, f"Recall {metrics['recall']}% fell below 80%"
        assert metrics["false_merge_rate"] <= 6.0, f"False merge rate {metrics['false_merge_rate']}% exceeded 6%"
        assert metrics["cluster_purity"] >= 85.0, f"Cluster purity {metrics['cluster_purity']}% fell below 85%"
