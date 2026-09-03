from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from backend.providers.base import BaseProvider

class MockProvider(BaseProvider):
    """
    Supplies realistic, verified high-signal viral AI items for Demo Mode.
    Always clearly marked with DEMO DATA attributes.
    """

    def __init__(self):
        super().__init__(name="Mock AI Feeds", source_type="demo")

    async def fetch_items(self) -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc)

        mock_stories = [
            {
                "title": "OpenAI releases new reasoning model with native computer use",
                "content": "OpenAI has officially launched a new lightweight reasoning architecture with native mouse, keyboard, and terminal control. Benchmarks demonstrate an 84.6% success rate on SWE-bench Verified while reducing latency by 42% compared to previous frontier models. Public API rollout begins today for tier 3 developers.",
                "url": "https://openai.com/index/announcing-reasoning-computer-use",
                "source": "OpenAI",
                "source_type": "x",
                "author": "OpenAI",
                "author_handle": "@OpenAI",
                "author_url": "https://x.com/OpenAI",
                "published_at": now - timedelta(minutes=45),
                "views": 2400000,
                "likes": 31200,
                "reposts": 5800,
                "replies": 1240,
                "quotes": 890,
                "topic": "Models",
                "content_type": "release",
                "hook_type": "breaking_news",
                "hashtags": ["#OpenAI", "#ArtificialIntelligence", "#SWEbench"]
            },
            {
                "title": "DeepSeek-V3 open-source model outperforms 70B competitors on coding",
                "content": "A newly released open-weights mixture-of-experts model has taken top spots across HumanEval, LiveCodeBench, and AIME math tests. The full 671B model requires only 37B activated parameters during inference, allowing multi-GPU local hosting with FP8 quantization. Hugging Face weights and repository live now.",
                "url": "https://github.com/deepseek-ai/DeepSeek-V3",
                "source": "GitHub",
                "source_type": "github",
                "author": "deepseek-ai",
                "author_handle": "deepseek-ai",
                "author_url": "https://github.com/deepseek-ai",
                "published_at": now - timedelta(hours=2, minutes=15),
                "views": 1200000,
                "likes": 18400,
                "reposts": 3900,
                "replies": 780,
                "quotes": 410,
                "topic": "Open Source",
                "content_type": "benchmark",
                "hook_type": "milestone",
                "hashtags": ["#OpenSourceAI", "#LLMs", "#DeepSeek"]
            },
            {
                "title": "Anthropic reveals MCP (Model Context Protocol) 2.0 with async streaming tools",
                "content": "Anthropic today expanded the open Model Context Protocol specification with bidirectional WebSocket streaming, local security sandboxing, and standardized client session states. Over 40 enterprise developer tooling platforms announced zero-day integration.",
                "url": "https://anthropic.com/news/model-context-protocol-2",
                "source": "Anthropic",
                "source_type": "rss",
                "author": "Anthropic",
                "author_handle": "@AnthropicAI",
                "author_url": "https://x.com/AnthropicAI",
                "published_at": now - timedelta(hours=4),
                "views": 840000,
                "likes": 14200,
                "reposts": 2800,
                "replies": 620,
                "quotes": 310,
                "topic": "Agents",
                "content_type": "tool",
                "hook_type": "curiosity",
                "hashtags": ["#Anthropic", "#MCP", "#AIAgents"]
            },
            {
                "title": "SWE-agent benchmark results shake up autonomous software engineering rankings",
                "content": "The latest SWE-bench evaluation shows an autonomous agent team architecture solving 68.3% of real GitHub issues without human intervention. Researchers leveraged dynamic test execution with self-repair loops rather than single-shot prompt generation.",
                "url": "https://arxiv.org/abs/2410.12345",
                "source": "arXiv",
                "source_type": "research",
                "author": "Princeton NLP",
                "author_handle": "@PrincetonNLP",
                "author_url": "https://x.com/PrincetonNLP",
                "published_at": now - timedelta(hours=6, minutes=30),
                "views": 620000,
                "likes": 9800,
                "reposts": 1950,
                "replies": 430,
                "quotes": 240,
                "topic": "Coding",
                "content_type": "research",
                "hook_type": "milestone",
                "hashtags": ["#SWEbench", "#CodingAgents", "#MachineLearning"]
            },
            {
                "title": "Google DeepMind unveils Gemini Robotics foundation model for dual-arm manipulation",
                "content": "DeepMind published research demonstrating real-time sub-100ms visual-motor policy execution directly conditioned on multimodal Gemini embeddings. The system learned 40 novel manipulation tasks in zero-shot transfer from simulated teleoperation.",
                "url": "https://deepmind.google/discover/blog/gemini-robotics-foundation",
                "source": "Google DeepMind",
                "source_type": "news",
                "author": "DeepMind",
                "author_handle": "@GoogleDeepMind",
                "author_url": "https://x.com/GoogleDeepMind",
                "published_at": now - timedelta(hours=10),
                "views": 950000,
                "likes": 16500,
                "reposts": 3100,
                "replies": 510,
                "quotes": 280,
                "topic": "Robotics",
                "content_type": "release",
                "hook_type": "curiosity",
                "hashtags": ["#DeepMind", "#Robotics", "#Gemini"]
            },
            {
                "title": "Meta opens weights for Llama 3.3 70B instruction-tuned model with 128k context",
                "content": "Meta has made Llama 3.3 70B available under its community license. Fine-tuned with enhanced synthetic reasoning datasets, it matches Llama 3.1 405B performance on standard instruction following while fitting comfortably onto a single quad-GPU workstation.",
                "url": "https://ai.meta.com/blog/llama-3-3-open-source/",
                "source": "Meta AI",
                "source_type": "rss",
                "author": "Meta AI",
                "author_handle": "@MetaAI",
                "author_url": "https://x.com/MetaAI",
                "published_at": now - timedelta(hours=14),
                "views": 1800000,
                "likes": 25100,
                "reposts": 4900,
                "replies": 940,
                "quotes": 520,
                "topic": "Models",
                "content_type": "release",
                "hook_type": "milestone",
                "hashtags": ["#Llama3", "#MetaAI", "#OpenSource"]
            },
            {
                "title": "Figure AI showcases autonomous humanoid fleet operating in commercial warehouse",
                "content": "Figure 02 humanoids achieved 99.2% uptime across a 72-hour continuous sorting and material handling pilot. Powered by on-device neural vision policies running at 200Hz, the robots adjust to dynamic human workers without safety stoppages.",
                "url": "https://x.com/Figure_robot/status/1850123456789",
                "source": "X",
                "source_type": "x",
                "author": "Brett Adcock",
                "author_handle": "@adcock_brett",
                "author_url": "https://x.com/adcock_brett",
                "published_at": now - timedelta(hours=18),
                "views": 3100000,
                "likes": 42000,
                "reposts": 7200,
                "replies": 1850,
                "quotes": 980,
                "topic": "Robotics",
                "content_type": "news",
                "hook_type": "contrarian",
                "hashtags": ["#Humanoids", "#FigureAI", "#Robotics"]
            },
            {
                "title": "NVIDIA introduces Cosmos physical AI world foundation models for robotics and AVs",
                "content": "NVIDIA Cosmos world foundation models allow developers to simulate physical environments and generate photorealistic physics-accurate training trajectories for robots and autonomous vehicles. Pre-trained checkpoints released on Hugging Face.",
                "url": "https://blogs.nvidia.com/blog/cosmos-physical-ai-world-models/",
                "source": "NVIDIA",
                "source_type": "news",
                "author": "NVIDIA AI",
                "author_handle": "@NVIDIAAI",
                "author_url": "https://x.com/NVIDIAAI",
                "published_at": now - timedelta(hours=22),
                "views": 1100000,
                "likes": 15800,
                "reposts": 2900,
                "replies": 410,
                "quotes": 310,
                "topic": "AI Tools",
                "content_type": "tool",
                "hook_type": "announcement",
                "hashtags": ["#NVIDIA", "#Cosmos", "#PhysicalAI"]
            }
        ]

        # Tag items with DEMO metadata
        for item in mock_stories:
            item["is_demo"] = True

        return mock_stories

mock_provider = MockProvider()
