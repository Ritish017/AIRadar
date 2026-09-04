import { V3Event, OpportunityCard, Topic, ContentItem } from "../types";

export const MOCK_EVENTS: V3Event[] = [
  {
    id: "event_deepseek_r1",
    title: "DeepSeek-R1 Open Reasoning Model Launch",
    summary: "DeepSeek releases DeepSeek-R1 and DeepSeek-R1-Zero with MIT open weights, achieving reasoning performance competitive with OpenAI o1 at 95% lower training compute cost.",
    category: "AI Models",
    status: "CONFIRMED",
    confidence_score: 98,
    source_count: 14,
    independent_source_count: 8,
    primary_source_name: "DeepSeek Blog",
    primary_source_url: "https://deepseek.com/blog/deepseek-r1",
    entities: ["DeepSeek", "OpenAI", "Reinforcement Learning", "MoE Architecture", "MIT License"],
    key_facts: [
      "Trained with pure RL on cold-start data without massive human annotation.",
      "Matches OpenAI o1 on AIME 2024 (79.8%) and MATH-500 benchmarks.",
      "Weights released under permissive MIT license with distilled 1.5B to 70B variants."
    ],
    relevance_score: 99,
    freshness_score: 95,
    momentum_score: 97,
    opportunity_score: 96,
    recommended_action: "POST_NOW",
    recommended_angle: "The Open Weights RL Paradigm Shift",
    recommended_platform: "X",
    event_timestamp: new Date(Date.now() - 3600000).toISOString(),
    first_seen_at: new Date(Date.now() - 7200000).toISOString(),
    surfaced_at: new Date(Date.now() - 3500000).toISOString(),
    total_pipeline_latency: 28.4,
    sources: [
      {
        source_name: "DeepSeek Blog",
        url: "https://deepseek.com/blog/deepseek-r1",
        quality_tier: "Tier 1",
        title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL",
        published_at: new Date(Date.now() - 7200000).toISOString()
      },
      {
        source_name: "GitHub",
        url: "https://github.com/deepseek-ai/DeepSeek-R1",
        quality_tier: "Tier 1",
        title: "deepseek-ai/DeepSeek-R1 Official Repository",
        published_at: new Date(Date.now() - 7000000).toISOString()
      },
      {
        source_name: "TechCrunch",
        url: "https://techcrunch.com/deepseek-r1-launch",
        quality_tier: "Tier 2",
        title: "DeepSeek's new R1 reasoning model challenges frontier labs",
        published_at: new Date(Date.now() - 6000000).toISOString()
      }
    ]
  },
  {
    id: "event_veo_3",
    title: "Google DeepMind Unveils Veo 3 Video Generation Architecture",
    summary: "DeepMind introduces Veo 3 featuring high-fidelity temporal physics, cinematic 4K rendering, and multi-prompt frame-to-frame continuity control.",
    category: "Generative Video",
    status: "CONFIRMED",
    confidence_score: 96,
    source_count: 9,
    independent_source_count: 5,
    primary_source_name: "Google DeepMind Blog",
    primary_source_url: "https://deepmind.google/technologies/veo/",
    entities: ["Google DeepMind", "Veo 3", "Video Diffusion", "Cinematic Physics", "4K Video"],
    key_facts: [
      "Native 1080p and 4K output with strict camera language interpretation.",
      "First-and-last frame interpolation with zero identity drift.",
      "Integrates with YouTube Shorts and external creative pipelines."
    ],
    relevance_score: 94,
    freshness_score: 92,
    momentum_score: 91,
    opportunity_score: 93,
    recommended_action: "POST_NOW",
    recommended_angle: "Why Frame-to-Frame Temporal Physics Changes Film Production",
    recommended_platform: "YouTube",
    event_timestamp: new Date(Date.now() - 5400000).toISOString(),
    first_seen_at: new Date(Date.now() - 8400000).toISOString(),
    surfaced_at: new Date(Date.now() - 5000000).toISOString(),
    total_pipeline_latency: 32.1,
    sources: [
      {
        source_name: "Google DeepMind",
        url: "https://deepmind.google/technologies/veo/",
        quality_tier: "Tier 1",
        title: "Veo: Our most capable generative video model",
        published_at: new Date(Date.now() - 8400000).toISOString()
      },
      {
        source_name: "The Verge",
        url: "https://theverge.com/google-deepmind-veo-video-ai",
        quality_tier: "Tier 2",
        title: "Google takes on Sora with Veo 3 cinematic generator",
        published_at: new Date(Date.now() - 7200000).toISOString()
      }
    ]
  },
  {
    id: "event_openai_sora_2",
    title: "OpenAI Sora 2 Multi-Camera Directing & Continuity Release",
    summary: "OpenAI rolls out Sora 2 with synchronized multi-angle shot continuity, spatial audio synthesis, and native screenplay script-to-video compilation.",
    category: "Generative Video",
    status: "CONFIRMED",
    confidence_score: 95,
    source_count: 12,
    independent_source_count: 7,
    primary_source_name: "OpenAI Blog",
    primary_source_url: "https://openai.com/index/sora-2",
    entities: ["OpenAI", "Sora 2", "Multi-Camera Video", "Directing Engine", "Spatial Audio"],
    key_facts: [
      "Multi-shot scene sequences maintain precise lighting and character identity across angles.",
      "Generates synchronized environmental audio and dialogue tracks.",
      "Supports external storyboarding via JSON camera choreography."
    ],
    relevance_score: 97,
    freshness_score: 94,
    momentum_score: 95,
    opportunity_score: 94,
    recommended_action: "POST_NOW",
    recommended_angle: "How Multi-Camera Directing Changes AI Video Creators",
    recommended_platform: "X",
    event_timestamp: new Date(Date.now() - 9000000).toISOString(),
    first_seen_at: new Date(Date.now() - 12000000).toISOString(),
    surfaced_at: new Date(Date.now() - 8800000).toISOString(),
    total_pipeline_latency: 24.5,
    sources: [
      {
        source_name: "OpenAI Blog",
        url: "https://openai.com/index/sora-2",
        quality_tier: "Tier 1",
        title: "Sora 2: Video generation with narrative continuity and direction",
        published_at: new Date(Date.now() - 12000000).toISOString()
      }
    ]
  },
  {
    id: "event_claude_37_hybrid",
    title: "Anthropic Claude 3.7 Sonnet Hybrid Reasoning Launch",
    summary: "Anthropic introduces Claude 3.7 Sonnet as the first hybrid architecture seamlessly combining instant standard generation with extended controllable chain-of-thought.",
    category: "AI Models",
    status: "CONFIRMED",
    confidence_score: 97,
    source_count: 11,
    independent_source_count: 6,
    primary_source_name: "Anthropic Research",
    primary_source_url: "https://anthropic.com/claude/sonnet-3-7",
    entities: ["Anthropic", "Claude 3.7", "Hybrid Reasoning", "Extended Thinking", "Agentic Coding"],
    key_facts: [
      "Dynamic thinking budget allows users to dial inference compute from 0 tokens to 64k tokens.",
      "State of the art SWE-bench Verified coding benchmark score of 70.3%.",
      "Unified model eliminates need to route between separate reasoning and standard models."
    ],
    relevance_score: 98,
    freshness_score: 93,
    momentum_score: 96,
    opportunity_score: 97,
    recommended_action: "POST_NOW",
    recommended_angle: "The Death of Separate Reasoning Models: Hybrid is the Future",
    recommended_platform: "LinkedIn",
    event_timestamp: new Date(Date.now() - 14400000).toISOString(),
    first_seen_at: new Date(Date.now() - 18000000).toISOString(),
    surfaced_at: new Date(Date.now() - 14000000).toISOString(),
    total_pipeline_latency: 26.8,
    sources: [
      {
        source_name: "Anthropic Blog",
        url: "https://anthropic.com/claude/sonnet-3-7",
        quality_tier: "Tier 1",
        title: "Claude 3.7 Sonnet and Claude Code",
        published_at: new Date(Date.now() - 18000000).toISOString()
      }
    ]
  },
  {
    id: "event_runway_gen3",
    title: "Runway Gen-3 Alpha Camera Motion & World Model Expansion",
    summary: "Runway releases major Gen-3 Alpha upgrade offering sub-second camera physics controls, multi-asset keyframe tracking, and real-time motion brush dynamics.",
    category: "Generative Video",
    status: "DEVELOPING",
    confidence_score: 88,
    source_count: 6,
    independent_source_count: 3,
    primary_source_name: "Runway Research",
    primary_source_url: "https://runwayml.com/gen-3-alpha",
    entities: ["Runway", "Gen-3 Alpha", "Camera Motion", "Cinematic Controls", "Motion Brush"],
    key_facts: [
      "Precision camera choreography supporting orbits, whips, crane shots, and dolly zooms.",
      "Consistent asset anchoring across dynamic background transforms.",
      "Web API for automated programmatic rendering workflows."
    ],
    relevance_score: 90,
    freshness_score: 89,
    momentum_score: 87,
    opportunity_score: 89,
    recommended_action: "POST_SOON",
    recommended_angle: "How Micro-Camera Directing Elevates Generative Commercials",
    recommended_platform: "Instagram",
    event_timestamp: new Date(Date.now() - 21600000).toISOString(),
    first_seen_at: new Date(Date.now() - 25200000).toISOString(),
    surfaced_at: new Date(Date.now() - 21000000).toISOString(),
    total_pipeline_latency: 35.0,
    sources: [
      {
        source_name: "Runway Blog",
        url: "https://runwayml.com/blog/gen-3-alpha-motion",
        quality_tier: "Tier 1",
        title: "Introducing Advanced Camera Controls for Gen-3 Alpha",
        published_at: new Date(Date.now() - 25200000).toISOString()
      }
    ]
  },
  {
    id: "event_meta_llama_33",
    title: "Meta Llama 3.3 70B Release: 405B Performance in 70B Footprint",
    summary: "Meta AI releases Llama 3.3 70B, matching the prior 405B flagship model capability across industry benchmarks while running on a single 80GB GPU server.",
    category: "Open Source AI",
    status: "CONFIRMED",
    confidence_score: 96,
    source_count: 10,
    independent_source_count: 5,
    primary_source_name: "Meta AI",
    primary_source_url: "https://ai.meta.com/blog/llama-3-3/",
    entities: ["Meta", "Llama 3.3", "Open Weights", "Single GPU Deployment", "Quantization"],
    key_facts: [
      "Matches Llama 3.1 405B on common math, coding, and knowledge benchmarks.",
      "Runs quantized on consumer GPUs or cost-effective cloud instances.",
      "Community fine-tunes and enterprise adaptations surged within 24 hours."
    ],
    relevance_score: 92,
    freshness_score: 88,
    momentum_score: 90,
    opportunity_score: 91,
    recommended_action: "POST_SOON",
    recommended_angle: "Why 70B is the New Enterprise Sweet Spot",
    recommended_platform: "LinkedIn",
    event_timestamp: new Date(Date.now() - 28800000).toISOString(),
    first_seen_at: new Date(Date.now() - 32400000).toISOString(),
    surfaced_at: new Date(Date.now() - 28000000).toISOString(),
    total_pipeline_latency: 29.2,
    sources: [
      {
        source_name: "Meta AI Blog",
        url: "https://ai.meta.com/blog/llama-3-3/",
        quality_tier: "Tier 1",
        title: "Llama 3.3: 70B model with frontier capabilities",
        published_at: new Date(Date.now() - 32400000).toISOString()
      }
    ]
  }
];

export const MOCK_OPPORTUNITIES: OpportunityCard[] = [
  {
    rank: 1,
    id: "opp_deepseek_r1",
    topic: "DeepSeek-R1 Cost Disruption",
    category: "AI Models",
    opportunity_score: 96,
    opportunity_type: "BREAKING_BREAKTHROUGH",
    lifecycle: "EXPLODING",
    lifecycle_badge: "🔥 EXPLODING",
    momentum: 97,
    momentum_change_pct: 34.5,
    momentum_direction: "ACCELERATING",
    competition: 24,
    novelty: 98,
    audience_fit: 95,
    primary_audience: "AI Engineers & Founders",
    recommended_action: "POST_NOW",
    action_reason: "High velocity signal with 98% novelty and low market saturation. Optimal window is the next 4 hours.",
    recommended_angle: "Why RL without SFT changes the economics of foundation models forever",
    alternative_angles: [
      "How to run DeepSeek-R1 locally with Ollama and vLLM",
      "The geopolitical implications of open reasoning architectures"
    ],
    recommended_hook: "OpenAI spent hundreds of millions. DeepSeek did it for $6M. Here's the exact architectural trick.",
    hook_strategy: "CONTRARIAN",
    recommended_format: "X Thread + Video Prompt",
    format_scores: { "X Thread": 98, "LinkedIn Post": 92, "Video Reel": 94 },
    item_count: 14,
    primary_source: "DeepSeek Blog",
    sources_summary: ["DeepSeek Blog", "GitHub", "ArXiv", "TechCrunch"]
  },
  {
    rank: 2,
    id: "opp_claude_37",
    topic: "Claude 3.7 Hybrid Reasoning",
    category: "AI Models",
    opportunity_score: 95,
    opportunity_type: "MAJOR_RELEASE",
    lifecycle: "EXPLODING",
    lifecycle_badge: "🔥 EXPLODING",
    momentum: 96,
    momentum_change_pct: 28.0,
    momentum_direction: "ACCELERATING",
    competition: 31,
    novelty: 96,
    audience_fit: 94,
    primary_audience: "Developers & Software Engineers",
    recommended_action: "POST_NOW",
    action_reason: "Hybrid model structure eliminates reasoning router overhead. High interest among coding professionals.",
    recommended_angle: "The death of separate reasoning models: how token budgeting replaces model routing",
    alternative_angles: [
      "Benchmark breakdown: SWE-bench verified 70.3% analysis",
      "How to configure thinking budget for production APIs"
    ],
    recommended_hook: "Stop choosing between fast models and reasoning models. Claude 3.7 just unified them.",
    hook_strategy: "PARADIGM_SHIFT",
    recommended_format: "Technical Deep-Dive",
    format_scores: { "LinkedIn Post": 96, "X Thread": 95, "Video": 88 },
    item_count: 11,
    primary_source: "Anthropic Research",
    sources_summary: ["Anthropic Research", "Twitter/X", "VentureBeat"]
  },
  {
    rank: 3,
    id: "opp_sora_veo_battle",
    topic: "Sora 2 vs Veo 3 Video Directing",
    category: "Generative Video",
    opportunity_score: 93,
    opportunity_type: "MARKET_COMPETITION",
    lifecycle: "EMERGING",
    lifecycle_badge: "⚡ EMERGING",
    momentum: 91,
    momentum_change_pct: 22.0,
    momentum_direction: "ACCELERATING",
    competition: 42,
    novelty: 94,
    audience_fit: 92,
    primary_audience: "Content Creators & Video Directors",
    recommended_action: "POST_SOON",
    action_reason: "Visual comparison content drives massive engagement. Focus on storyboard reproducibility.",
    recommended_angle: "Multi-camera prompt choreography: what works in Sora 2 that fails in Veo 3",
    alternative_angles: [
      "The complete camera movement prompt dictionary for 2026",
      "Why Remotion code-native video beats diffusion for data explainers"
    ],
    recommended_hook: "AI video just graduated from random clips to multi-shot cinema. Here is the side-by-side test.",
    hook_strategy: "SHOWDOWN",
    recommended_format: "Video Comparison + Breakdown",
    format_scores: { "Video Reel": 99, "YouTube Short": 97, "X Thread": 89 },
    item_count: 18,
    primary_source: "OpenAI & DeepMind",
    sources_summary: ["OpenAI", "DeepMind", "Creator Community"]
  }
];

export const MOCK_TRENDS: Topic[] = [
  {
    id: "trend_reasoning_models",
    name: "AI Reasoning & Pure RL",
    category: "AI Models",
    momentum: 97,
    momentum_change_pct: 32.0,
    momentum_direction: "ACCELERATING",
    status: "CONFIRMED",
    lifecycle_stage: "EXPLODING",
    opportunity_score: 96,
    competition_score: 28,
    novelty_score: 97,
    audience_fit_score: 95,
    recommended_action: "POST_NOW",
    action_reason: "High velocity signal in first-wave cycle.",
    recommended_angle: "The architectural shift from compute at pre-training to compute at inference",
    recommended_hook_type: "CONTRARIAN",
    hook_strategy: "Challenging conventional wisdom on training data scale",
    recommended_format: "Technical Explainer",
    format_scores: { "X Thread": 96, "LinkedIn": 94, "Video": 90 },
    primary_audience: "AI Engineers",
    item_count: 142,
    sources_summary: ["DeepSeek Blog", "GitHub", "ArXiv", "TechCrunch"],
    primary_source: "DeepSeek",
    updated_at: new Date().toISOString()
  },
  {
    id: "trend_video_intelligence",
    name: "Video Prompt Intelligence & Forensics",
    category: "Generative Video",
    momentum: 92,
    momentum_change_pct: 24.5,
    momentum_direction: "ACCELERATING",
    status: "CONFIRMED",
    lifecycle_stage: "EMERGING",
    opportunity_score: 94,
    competition_score: 34,
    novelty_score: 95,
    audience_fit_score: 93,
    recommended_action: "POST_NOW",
    action_reason: "High creator demand for executable prompt packages.",
    recommended_angle: "Treating video prompt compilation as a compiler pipeline with static analysis",
    recommended_hook_type: "FRAMEWORK",
    hook_strategy: "Exposing behind-the-scenes prompt architecture",
    recommended_format: "Step-by-Step Guide",
    format_scores: { "Video": 98, "X Thread": 92, "LinkedIn": 88 },
    primary_audience: "Video Creators",
    item_count: 98,
    sources_summary: ["OpenAI", "Google DeepMind", "Runway"],
    primary_source: "OpenAI Blog",
    updated_at: new Date().toISOString()
  }
];

export const MOCK_NEWS_ITEMS = [
  {
    id: "news_1",
    title: "DeepSeek-R1 Open Reasoning Model Published Under MIT License",
    content: "DeepSeek makes frontier reasoning weights open to the public with full technical report and reproduction guides.",
    source: "DeepSeek",
    source_quality: "Tier 1",
    url: "https://deepseek.com/blog/deepseek-r1",
    published_at: new Date(Date.now() - 3600000).toISOString(),
    category: "AI Models",
    viral_potential: 98,
    confirmed_facts: ["MIT license", "Pure RL training"],
    uncertain_claims: []
  },
  {
    id: "news_2",
    title: "Google DeepMind Releases Veo 3 With Multi-Angle Cinematic Direction",
    content: "Veo 3 introduces 4K native output and frame-to-frame physics consistency for filmmakers.",
    source: "Google DeepMind",
    source_quality: "Tier 1",
    url: "https://deepmind.google/technologies/veo/",
    published_at: new Date(Date.now() - 7200000).toISOString(),
    category: "Generative Video",
    viral_potential: 96,
    confirmed_facts: ["4K output", "First-last frame interpolation"],
    uncertain_claims: []
  },
  {
    id: "news_3",
    title: "Anthropic Launches Claude 3.7 Sonnet With Dynamic Extended Thinking",
    content: "New hybrid model scores 70.3% on SWE-bench verified, unifying instant responses and deep reasoning.",
    source: "Anthropic",
    source_quality: "Tier 1",
    url: "https://anthropic.com/claude/sonnet-3-7",
    published_at: new Date(Date.now() - 10800000).toISOString(),
    category: "AI Models",
    viral_potential: 97,
    confirmed_facts: ["70.3% on SWE-bench Verified"],
    uncertain_claims: []
  },
  {
    id: "news_4",
    title: "OpenAI Sora 2 Enables Native Screenplay Directing & Spatial Audio",
    content: "Sora 2 platform supports structured multi-scene scripts with synced audio tracks.",
    source: "OpenAI",
    source_quality: "Tier 1",
    url: "https://openai.com/index/sora-2",
    published_at: new Date(Date.now() - 14400000).toISOString(),
    category: "Generative Video",
    viral_potential: 95,
    confirmed_facts: ["Synchronized multi-scene scripts"],
    uncertain_claims: []
  },
  {
    id: "news_5",
    title: "Meta Releases Llama 3.3 70B Matching 405B Frontier Benchmarks",
    content: "Compact 70B footprint enables enterprise deployment on commodity single-GPU servers.",
    source: "Meta AI",
    source_quality: "Tier 1",
    url: "https://ai.meta.com/blog/llama-3-3/",
    published_at: new Date(Date.now() - 18000000).toISOString(),
    category: "Open Source AI",
    viral_potential: 94,
    confirmed_facts: ["Matches 405B benchmarks"],
    uncertain_claims: []
  }
];

export const MOCK_GRAPH_DATA = {
  nodes: [
    { id: "cat_models", label: "AI Models", type: "category", size: 28, color: "#6366f1" },
    { id: "cat_video", label: "Generative Video", type: "category", size: 28, color: "#ec4899" },
    { id: "cat_opensource", label: "Open Source", type: "category", size: 26, color: "#10b981" },
    { id: "t_deepseek", label: "DeepSeek-R1", type: "topic", size: 24, velocity: 4.8, momentum: 97, category: "AI Models" },
    { id: "t_claude", label: "Claude 3.7", type: "topic", size: 22, velocity: 4.4, momentum: 96, category: "AI Models" },
    { id: "t_sora", label: "Sora 2", type: "topic", size: 22, velocity: 4.2, momentum: 94, category: "Generative Video" },
    { id: "t_veo", label: "Veo 3", type: "topic", size: 20, velocity: 3.9, momentum: 92, category: "Generative Video" },
    { id: "t_llama", label: "Llama 3.3", type: "topic", size: 20, velocity: 3.8, momentum: 90, category: "Open Source" }
  ],
  edges: [
    { source: "cat_models", target: "t_deepseek", weight: 0.95 },
    { source: "cat_models", target: "t_claude", weight: 0.92 },
    { source: "cat_video", target: "t_sora", weight: 0.90 },
    { source: "cat_video", target: "t_veo", weight: 0.88 },
    { source: "cat_opensource", target: "t_llama", weight: 0.89 },
    { source: "t_deepseek", target: "t_llama", weight: 0.75 },
    { source: "t_sora", target: "t_veo", weight: 0.82 }
  ]
};

export function createMockVideoPackage(topic: string = "DeepSeek-R1 Open Reasoning Model Launch", platform: string = "youtube_short"): any {
  return {
    package_id: "pkg_mock_" + Date.now(),
    title: topic,
    platform: platform,
    duration_seconds: 30,
    aspect_ratio: platform.includes("reel") || platform.includes("short") ? "9:16" : "16:9",
    style_preset: "Cinematic Technical Documentary",
    generation_strategy: "Hybrid Omni-Veo Directing",
    creative_concept: `High-impact technical breakdown revealing how ${topic} disrupts legacy AI benchmarks.`,
    why_this_video: "Explosive velocity in community and developer discussions. High visual contrast between compute cost and benchmark performance.",
    ranked_hooks: [
      {
        rank: 1,
        hook_category: "CONTRARIAN",
        verbal_script: "OpenAI spent hundreds of millions of dollars. Here is how one open-weights model matched it for under six million.",
        visual_action: "Fast macro camera push into an glowing server rack glowing with neon neural lattice lines.",
        retention_score: 96,
        novelty_score: 95,
        why_it_works: "Sets up extreme asymmetrical comparison that challenges accepted industry dogma."
      },
      {
        rank: 2,
        hook_category: "DATA_REVELATION",
        verbal_script: "79.8% on AIME 2024. But the most shocking number isn't the accuracy—it's the training compute delta.",
        visual_action: "Dynamic dual-axis chart morphing into real-time GPU cluster visualization.",
        retention_score: 93,
        novelty_score: 92,
        why_it_works: "Anchors on precise technical proof with immediate visual payoff."
      }
    ],
    storyboard: [
      {
        scene_number: 1,
        timecode: "00:00 - 00:04",
        duration_sec: 4,
        beat_type: "Hook",
        narration: "OpenAI spent hundreds of millions. Here is how pure RL cold-start training matched frontier reasoning.",
        visual_direction: "Macro cinema shot of silicon processor surface with pulses of electric violet data packets.",
        camera_instruction: "Rapid push-in 50mm lens with shallow depth of field and anamorphic flare.",
        on_screen_text: "THE $6M REASONING SHIFT",
        recommended_engine: "Google Veo 3",
        asset_prompt: "Close up cinema shot of high performance AI processor under ultraviolet illumination, photorealistic 8k"
      },
      {
        scene_number: 2,
        timecode: "00:04 - 00:12",
        duration_sec: 8,
        beat_type: "Core Evidence",
        narration: "By removing massive human labeling and letting the model explore its own chain-of-thought, self-correction emerged spontaneously.",
        visual_direction: "Remotion animated timeline showing reasoning branch trees pruning dead ends in real-time.",
        camera_instruction: "Slow fluid pan along the decision graph.",
        on_screen_text: "EMERGENT CHAIN-OF-THOUGHT",
        recommended_engine: "Remotion",
        asset_prompt: "Interactive code visual showing tree search branching and self-correction steps"
      },
      {
        scene_number: 3,
        timecode: "00:12 - 00:22",
        duration_sec: 10,
        beat_type: "Architectural Impact",
        narration: "This proves that inference-time compute scaling is where the true intelligence lives—not in brute-force pretraining.",
        visual_direction: "Split screen comparing legacy 100,000 GPU clusters with distributed distilled inference clusters.",
        camera_instruction: "Dynamic cross-fade with parallax tracking.",
        on_screen_text: "INFERENCE SCALING > PRE-TRAINING",
        recommended_engine: "OpenAI Sora 2",
        asset_prompt: "Futuristic data center interior with holographic benchmark metrics floating in air"
      },
      {
        scene_number: 4,
        timecode: "00:22 - 00:30",
        duration_sec: 8,
        beat_type: "CTA & Takeaway",
        narration: "The open weights are on GitHub right now under MIT license. Run it locally or build on top.",
        visual_direction: "Terminal window executing model weights command with glowing success badge.",
        camera_instruction: "Locked-off tripod framing with subtle rack focus.",
        on_screen_text: "MIT OPEN WEIGHTS LIVE",
        recommended_engine: "HyperFrames",
        asset_prompt: "Sleek terminal interface displaying active inference benchmark stats"
      }
    ],
    shot_list: [
      {
        shot_id: "shot_01",
        scene_number: 1,
        shot_type: "Extreme Close-Up",
        camera_angle: "Slight Low Angle",
        lens: "50mm T1.5 Anamorphic",
        movement: "Push-In Tracking",
        lighting: "High Contrast Cyberpunk Neon",
        duration_sec: 4,
        complexity_score: 2,
        framing: "Rule of Thirds",
        focal_plane: "Front Processor Core"
      },
      {
        shot_id: "shot_02",
        scene_number: 2,
        shot_type: "Medium Shot",
        camera_angle: "Eye Level",
        lens: "35mm Prime",
        movement: "Lateral Dolly Pan",
        lighting: "Balanced Studio Key Light",
        duration_sec: 8,
        complexity_score: 1,
        framing: "Centered Graphic Focus",
        focal_plane: "Motion Diagram Plane"
      },
      {
        shot_id: "shot_03",
        scene_number: 3,
        shot_type: "Wide Shot",
        camera_angle: "Elevated High Angle",
        lens: "24mm Ultra Wide",
        movement: "Slow Forward Crane Descend",
        lighting: "Volumetric Server Aisle Haze",
        duration_sec: 10,
        complexity_score: 2,
        framing: "Symmetrical Hallway Horizon",
        focal_plane: "Infinite Depth"
      },
      {
        shot_id: "shot_04",
        scene_number: 4,
        shot_type: "Medium Close-Up",
        camera_angle: "Straight-On",
        lens: "85mm Portrait",
        movement: "Static Locked-Off",
        lighting: "Soft Ambient OLED Glow",
        duration_sec: 8,
        complexity_score: 1,
        framing: "Centered Display UI",
        focal_plane: "Terminal Interface"
      }
    ],
    asset_manifest: [
      { asset_id: "ast_01", asset_type: "Video Background", description: "Silicon die macro render", file_format: "MP4 / Prores", aspect_ratio: "16:9", used_by_shot: "shot_01" },
      { asset_id: "ast_02", asset_type: "Code Overlay", description: "Tree search JSON graph", file_format: "SVG / Canvas", aspect_ratio: "16:9", used_by_shot: "shot_02" }
    ],
    audio_plan: {
      voiceover_script: "OpenAI spent hundreds of millions. Here is how pure RL cold-start training matched frontier reasoning...",
      music_genre: "Cinematic Neo-Electronic Minimal",
      bpm_range: "120-128 BPM",
      emotional_role: "Authoritative, Propulsive, Revelatory",
      sfx_cues: [
        { timestamp_sec: 0.5, sound_event: "Subtle Sub-Bass Impact", intensity: "HIGH" },
        { timestamp_sec: 4.2, sound_event: "Digital Data Sweep", intensity: "MEDIUM" },
        { timestamp_sec: 12.0, sound_event: "Bass Riser Transition", intensity: "HIGH" }
      ]
    },
    engines: {
      remotion: {
        standalone_agent_prompt: "Create a 60fps Remotion composition rendering animated decision trees with spring physics.",
        video_props_interface: "interface RemotionDecisionTreeProps { title: string; accuracyScore: number; }",
        render_command: "npx remotion render src/index.ts DecisionTree out/video.mp4"
      },
      omni: [
        {
          shot_id: "shot_01",
          purpose: "Establish high-tech scale and technical gravitas",
          visual_prompt: "Cinematic macro shot of an AI reasoning processor glowing with pulses of purple light, volumetric smoke, photorealistic, 8k, Unreal Engine 5 render style, anamorphic bokeh",
          audio_direction: "Deep resonant sub-bass pulse followed by high-frequency silicon hum",
          continuity: "Preserve violet and indigo lighting spectrum across following scene",
          avoid: "cartoon, oversaturated green, glitchy artifacts, distorted text"
        }
      ],
      veo: [
        {
          shot_id: "shot_01",
          workflow_type: "FIRST_LAST_FRAME_INTERPOLATION",
          prompt: "Cinematic push into micro-architecture of an advanced computing processor with neon light corridors",
          start_frame_prompt: "Front view of closed server chassis with violet LED arrays",
          end_frame_prompt: "Extreme macro internal view of glowing silicon die with data pulses",
          motion_prompt: "Smooth forward tracking motion, cinematic 24fps"
        }
      ],
      hyperframes: {
        composition_id: "comp_hf_01",
        html_markup: "<div class='scene-card'><h1 class='text-4xl font-bold text-white'>79.8% AIME ACCURACY</h1></div>",
        css_styles: ".scene-card { background: #070a12; display: flex; align-items: center; justify-content: center; height: 100vh; }",
        gsap_timeline_code: "gsap.timeline().from('.scene-card h1', { opacity: 0, y: 30, duration: 1, ease: 'power3.out' });",
        standalone_agent_prompt: "Execute HTML5 responsive motion graphic overlay with GSAP timeline"
      }
    },
    quality_report: {
      overall_readiness_score: 95,
      passes_quality_gate: true,
      dimension_scores: {
        temporal_coherence: 96,
        camera_grammar: 97,
        pacing_velocity: 94,
        asset_anchoring: 95,
        anti_slop_cleanliness: 98
      },
      self_critique: ["Camera motion is strictly motivated by technical argument.", "Hook achieves high curiosity without clickbait degradation."],
      prohibited_phrases_detected: []
    },
    visual_concepts: {
      suite_id: "vc_suite_01",
      claim_or_narration: "OpenAI spent hundreds of millions. DeepSeek did it for under $6M.",
      topic: topic,
      platform: platform,
      candidates: [
        {
          concept_id: "vc_01",
          representation_type: "Asymmetrical Scale Metaphor",
          headline: "The Goliath vs David Silicon Die",
          core_visual_metaphor: "Massive towering server monolith compared to a compact glowing silicon prism",
          description: "Visualizes the 95% compute delta by contrasting massive physical infrastructure with pure mathematical efficiency.",
          what_viewer_sees: "A sprawling city of 100,000 GPUs dwarfed by a single beam of light focusing through a compact prism.",
          what_viewer_understands: "Algorithmic breakthrough supersedes raw capital expenditure.",
          information_density: 92,
          conceptual_clarity: 96,
          emotional_impact: 95,
          novelty_score: 94,
          production_feasibility: 95,
          recommended_engine: "Google Veo 3",
          overall_fit_score: 95,
          is_recommended: true,
          selection_rationale: "Maximizes emotional contrast and conceptual clarity in under 3 seconds."
        }
      ],
      selected_concept: {
        concept_id: "vc_01",
        representation_type: "Asymmetrical Scale Metaphor",
        headline: "The Goliath vs David Silicon Die",
        core_visual_metaphor: "Massive towering server monolith compared to a compact glowing silicon prism",
        description: "Visualizes the 95% compute delta by contrasting massive physical infrastructure with pure mathematical efficiency.",
        what_viewer_sees: "A sprawling city of 100,000 GPUs dwarfed by a single beam of light focusing through a compact prism.",
        what_viewer_understands: "Algorithmic breakthrough supersedes raw capital expenditure.",
        information_density: 92,
        conceptual_clarity: 96,
        emotional_impact: 95,
        novelty_score: 94,
        production_feasibility: 95,
        recommended_engine: "Google Veo 3",
        overall_fit_score: 95,
        is_recommended: true,
        selection_rationale: "Maximizes emotional contrast and conceptual clarity in under 3 seconds."
      }
    },
    forensic_report: {
      report_id: "rep_01",
      prompt_id: "pr_01",
      triad_score: {
        overall_quality_score: 93.5,
        physical_realism_score: 92.0,
        prompt_fidelity_score: 96.0,
        production_execution_score: 92.5
      },
      critical_failures_detected: [],
      dimension_scores: {
        temporal_continuity: 94,
        camera_rigidity: 97,
        lighting_consistency: 95,
        audio_video_alignment: 92
      },
      verdict: "PRODUCTION_READY",
      recommendations: ["Ensure color grade LUT is locked in post-production compositor."]
    },
    created_at: new Date().toISOString()
  };
}

