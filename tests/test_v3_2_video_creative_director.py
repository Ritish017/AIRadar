import pytest
import asyncio
from backend.services.video.video_orchestrator import video_generation_service
from backend.services.video.model_capabilities import model_capability_registry
from backend.services.video.video_quality_evaluator import video_quality_evaluator
from backend.services.video.storyboard_engine import storyboard_engine
from backend.services.video.prompt_memory import prompt_memory_service
from backend.services.video.remotion_prompt_compiler import remotion_prompt_compiler
from backend.services.video.omni_prompt_compiler import omni_prompt_compiler
from backend.services.video.veo_prompt_compiler import veo_prompt_compiler
from backend.services.video.hyperframes_prompt_compiler import hyperframes_prompt_compiler
from backend.services.video.hybrid_planner import hybrid_planner

@pytest.mark.asyncio
async def test_golden_1_ai_model_launch_hybrid():
    """Golden Test 1: AI model launch -> Omni + Remotion hybrid workflow."""
    pkg = await video_generation_service.generate_video_package(
        title="OpenAI Announces GPT-5 Orion with Autonomous Tool Loops",
        topic="GPT-5 Orion Model Launch",
        angle="Autonomous multi-agent execution and enterprise pricing",
        platform="instagram_reel",
        duration_seconds=30,
        aspect_ratio="9:16",
        style_preset="TECH_DOCUMENTARY",
        strategy="HYBRID",
        key_claims=["Autonomous multi-step tool execution", "4x lower token latency", "Enterprise data isolation"],
        metrics={"Latency": "22ms/tok", "Accuracy": "86.4%", "Cost": "-40%"},
        sources=[{"name": "OpenAI Blog", "url": "https://openai.com/index/gpt-5-orion"}]
    )

    assert pkg.generation_strategy in ("HYBRID", "AUTO")
    assert pkg.hybrid_assembly is not None
    assert len(pkg.hybrid_assembly.layer_order) >= 4
    # Omni base layer + Remotion HUD / Overlays
    assert any("Omni" in layer or "Photoreal" in layer for layer in pkg.hybrid_assembly.layer_order)
    assert any("Remotion" in layer or "SVG" in layer for layer in pkg.hybrid_assembly.layer_order)
    assert pkg.engines.omni is not None and len(pkg.engines.omni) >= 1
    assert pkg.engines.remotion is not None
    assert pkg.quality_report.passes_quality_gate is True
    assert pkg.quality_report.overall_readiness_score >= 85.0

@pytest.mark.asyncio
async def test_golden_2_ai_benchmark_comparison_remotion():
    """Golden Test 2: AI benchmark comparison -> Remotion-heavy programmatic charts & springs."""
    pkg = await video_generation_service.generate_video_package(
        title="SWE-bench Verified Leaderboard: Claude 3.7 vs OpenAI Orion",
        topic="Frontier Benchmark Comparison",
        angle="Empirical code generation resolution delta across 500 tasks",
        platform="x",
        duration_seconds=30,
        aspect_ratio="16:9",
        style_preset="EDITORIAL_NEWS",
        strategy="REMOTION",
        key_claims=["Claude 3.7 scores 70.3% resolution", "Orion scores 71.1% on verified subset"],
        metrics={"Claude 3.7": "70.3%", "Orion": "71.1%", "Margin": "+0.8%"},
        sources=[{"name": "SWE-bench Verified", "url": "https://swebench.com"}]
    )

    assert pkg.generation_strategy == "REMOTION"
    assert pkg.engines.remotion is not None
    remotion = pkg.engines.remotion
    assert "useCurrentFrame" in remotion.standalone_agent_prompt
    assert "spring(" in remotion.standalone_agent_prompt
    assert "interpolate(" in remotion.standalone_agent_prompt
    assert "VideoProps" in remotion.video_props_interface
    # Asset manifest contains metrics / charts
    assert len(pkg.asset_manifest) >= 3

@pytest.mark.asyncio
async def test_golden_3_cinematic_ai_future_scenario():
    """Golden Test 3: Cinematic AI future scenario -> Omni/Veo-heavy photorealistic atmosphere."""
    pkg = await video_generation_service.generate_video_package(
        title="The 2030 Autonomous Datacenter: Subsea Micro-Clusters",
        topic="Autonomous AI Infrastructure Scenario",
        angle="Self-repairing submerged compute grids powered by geothermal currents",
        platform="youtube_short",
        duration_seconds=60,
        aspect_ratio="9:16",
        style_preset="CINEMATIC_AI",
        strategy="OMNI",
        key_claims=["Subsea pods eliminate 98% cooling energy", "Robotic manipulator arm repairs GPU blades"],
        metrics={"PUE": "1.02", "CoolingEnergy": "-98%"},
        sources=[{"name": "IEEE Spectrum", "url": "https://spectrum.ieee.org"}]
    )

    assert pkg.engines.omni is not None and len(pkg.engines.omni) >= 4
    for omni_shot in pkg.engines.omni:
        assert "SHOT-" in omni_shot.shot_id
        assert len(omni_shot.visual_prompt) > 80
        assert "35mm anamorphic" in omni_shot.visual_prompt.lower() or "lighting" in omni_shot.visual_prompt.lower()
        assert len(omni_shot.avoid) > 10
        assert len(omni_shot.continuity) > 10

@pytest.mark.asyncio
async def test_golden_4_technical_html_interface_hyperframes():
    """Golden Test 4: Technical HTML interface -> HyperFrames deterministic paused GSAP."""
    pkg = await video_generation_service.generate_video_package(
        title="Next-Gen Linux Kernel Telemetry with eBPF Model Monitoring",
        topic="Kernel Level AI Telemetry",
        angle="Real-time kernel memory tracing for 100k distributed token streams",
        platform="instagram_reel",
        duration_seconds=15,
        aspect_ratio="9:16",
        style_preset="FUTURISTIC_INTERFACE",
        strategy="HYPERFRAMES",
        key_claims=["Zero-overhead kernel probes", "Sub-microsecond token packet inspection"],
        metrics={"Overhead": "<0.01%", "Throughput": "100k req/s"}
    )

    assert pkg.engines.hyperframes is not None
    hf = pkg.engines.hyperframes
    assert "class=\"hyperframe-container\"" in hf.html_markup
    assert "gsap.timeline({ paused: true })" in hf.gsap_timeline_code
    assert "window.__timelines" in hf.gsap_timeline_code
    assert "window.renderFrame" in hf.gsap_timeline_code
    assert "DO NOT use setTimeout" in hf.standalone_agent_prompt

@pytest.mark.asyncio
async def test_golden_5_research_paper_explainer():
    """Golden Test 5: Research paper explainer -> Omni + Remotion hybrid structure."""
    pkg = await video_generation_service.generate_video_package(
        title="Attention Is Not All You Need: Linear Recurrence Breakthrough",
        topic="Transformer Architecture Evolution",
        angle="Sub-quadratic linear attention mechanisms match full attention at 1M context",
        platform="youtube_short",
        duration_seconds=60,
        aspect_ratio="9:16",
        style_preset="TECH_DOCUMENTARY",
        strategy="AUTO",
        key_claims=["O(N) memory complexity", "Matches standard Transformer perplexity at 128k"],
        metrics={"Context": "1,048,576 tokens", "Complexity": "O(N)"},
        sources=[{"name": "arXiv 2609.12345", "url": "https://arxiv.org/abs/2609.12345"}]
    )

    assert len(pkg.storyboard) >= 4
    # Check that both Remotion diagrams and Omni documentary footage exist in shot list
    engines_used = {s.engine for s in pkg.shot_list}
    assert "REMOTION" in engines_used or "OMNI" in engines_used
    assert pkg.quality_report.overall_readiness_score >= 85.0

@pytest.mark.asyncio
async def test_golden_6_character_dialogue_with_character_bible():
    """Golden Test 6: Character dialogue -> Omni/Veo with consistent Character Bible."""
    pkg = await video_generation_service.generate_video_package(
        title="Debating AGI Timeline: Senior Research Director vs Infrastructure Lead",
        topic="AGI Horizon Debate",
        angle="Compute power limits vs algorithmic efficiency breakthroughs",
        platform="instagram_reel",
        duration_seconds=30,
        aspect_ratio="9:16",
        style_preset="ANIMATED_CHARACTER",
        strategy="AUTO",
        has_characters=True,
        character_name="Dr. Elena Vance (Lead AI Architect)",
        key_claims=["Energy grid constraint in 2028", "Algorithmic compression advances 10x yearly"]
    )

    # Character Bible must be injected into all cinematic prompts and continuity locks
    assert any("Dr. Elena Vance" in s.continuity_requirements or "Dr. Elena Vance" in s.exact_model_prompt for s in pkg.shot_list)
    assert any("character" in a.asset_type for a in pkg.asset_manifest)

@pytest.mark.asyncio
async def test_golden_7_instagram_reel_shot_count():
    """Golden Test 7: 30-second Instagram Reel -> 7 to 10 shots depending on rapid visual pacing."""
    pkg = await video_generation_service.generate_video_package(
        title="DeepSeek V3 Architecture Deep Dive in 30 Seconds",
        topic="DeepSeek Architecture",
        angle="DualPipe scheduling and Multi-Head Latent Attention explained",
        platform="instagram_reel",
        duration_seconds=30,
        aspect_ratio="9:16",
        style_preset="TECH_DOCUMENTARY",
        strategy="AUTO",
        key_claims=["DualPipe hides communication overhead", "MLA compresses KV-cache by 93%"]
    )

    # 30-second reel must generate 7 to 10 shots for high retention pacing
    assert 7 <= len(pkg.shot_list) <= 10
    total_shot_dur = sum(s.duration_sec for s in pkg.shot_list)
    assert abs(total_shot_dur - 30.0) < 1.0

@pytest.mark.asyncio
async def test_golden_8_youtube_short_retention_arc():
    """Golden Test 8: 60-second YouTube Short -> structured retention arc and 3 ranked hooks."""
    pkg = await video_generation_service.generate_video_package(
        title="How Ilya Sutskever's Safe Superintelligence Raised $1 Billion",
        topic="SSI Funding & Mission",
        angle="The pure-play superintelligence research thesis without commercial distraction",
        platform="youtube_short",
        duration_seconds=60,
        aspect_ratio="9:16",
        style_preset="TECH_DOCUMENTARY",
        strategy="AUTO",
        key_claims=["Zero consumer product division", "Straight run to safe superintelligence"]
    )

    assert len(pkg.ranked_hooks) == 3
    # Verify retention scores are ranked
    assert pkg.ranked_hooks[0].retention_score >= pkg.ranked_hooks[1].retention_score
    assert len(pkg.storyboard) >= 5
    # Payoff and escalating stakes
    assert any("payoff" in s.narrative_purpose.lower() or "conclusion" in s.narrative_purpose.lower() or "cta" in s.narrative_purpose.lower() for s in pkg.storyboard)

@pytest.mark.asyncio
async def test_golden_9_youtube_long_form_multi_scene():
    """Golden Test 9: 3-minute YouTube explainer (180s) -> multi-scene chapter architecture."""
    pkg = await video_generation_service.generate_video_package(
        title="Complete Guide to Local AI: Run 70B Models on a Consumer Mac Studio",
        topic="Local Model Deployment",
        angle="Quantization, unified memory bandwidth, and llama.cpp optimization",
        platform="youtube_long",
        duration_seconds=180,
        aspect_ratio="16:9",
        style_preset="TECH_DOCUMENTARY",
        strategy="AUTO",
        key_claims=["Metal unified memory eliminates PCI-e bottlenecks", "EXL2 4-bit quantization retains 98% quality"]
    )

    assert pkg.duration_seconds == 180
    assert pkg.aspect_ratio == "16:9"
    # Long form must feature multi-scene chapters
    assert len(pkg.storyboard) >= 6
    assert len(pkg.shot_list) >= 12
    assert len(pkg.asset_manifest) >= 6

@pytest.mark.asyncio
async def test_golden_10_breaking_ai_news_source_grounded():
    """Golden Test 10: Breaking AI news -> source-grounded visuals and rapid production readiness."""
    pkg = await video_generation_service.generate_video_package(
        title="NVIDIA Announces Blackwell Ultra with 288GB HBM3e Memory",
        topic="NVIDIA Hardware Launch",
        angle="Memory bandwidth leap enabling single-node FP4 inference for trillion-parameter models",
        platform="x",
        duration_seconds=30,
        aspect_ratio="16:9",
        style_preset="EDITORIAL_NEWS",
        strategy="AUTO",
        key_claims=["288GB HBM3e per GPU", "14TB/s aggregate bandwidth", "Shipping Q4 2026"],
        metrics={"Memory": "288GB", "Bandwidth": "14TB/s"},
        sources=[{"name": "NVIDIA Newsroom", "url": "https://nvidianews.nvidia.com"}]
    )

    # Source cards or verified attribution must be present
    assert any("NVIDIA" in s.on_screen_text or "SOURCE" in s.on_screen_text for s in pkg.storyboard)
    assert pkg.quality_report.passes_quality_gate is True
    assert pkg.quality_report.dimension_scores["factual_integrity"] >= 90.0

def test_model_capabilities_validation_and_rejection():
    """Verify official model capability registry and rejection of unsupported features."""
    # Remotion checks
    valid, reason = model_capability_registry.validate_capability("Remotion", "text_to_video")
    assert valid is False
    assert "generative text-to-video" in reason

    valid, _ = model_capability_registry.validate_capability("Remotion", "charts")
    assert valid is True

    valid, _ = model_capability_registry.validate_capability("Remotion", "timelines")
    assert valid is True

    # Veo checks
    valid, _ = model_capability_registry.validate_capability("Veo", "first_last_frame")
    assert valid is True

    valid, _ = model_capability_registry.validate_capability("Veo", "audio")
    assert valid is True

    valid, reason = model_capability_registry.validate_capability("Veo", "code_rendering")
    assert valid is False

    # Omni checks
    valid, _ = model_capability_registry.validate_capability("Gemini Omni Flash", "image_to_video")
    assert valid is True

    valid, _ = model_capability_registry.validate_capability("Gemini Omni Flash", "cinematic")
    assert valid is True

    # HyperFrames checks
    valid, _ = model_capability_registry.validate_capability("HyperFrames", "gsap")
    assert valid is True

    valid, reason = model_capability_registry.validate_capability("HyperFrames", "wall_clock_animation")
    assert valid is False

def test_quality_gate_prohibited_phrases_detection():
    """Verify rejection of generic fluff words ('make it cinematic', 'make it viral') without parameters."""
    bad_shots = [
        {
            "shot_id": "SHOT-01",
            "exact_model_prompt": "Make it cinematic and make it viral with dynamic visuals and cool animations.",
            "camera_movement": "fast zoom",
            "subject_action": "looking at screen"
        }
    ]
    report = video_quality_evaluator.evaluate(
        shots=bad_shots,
        storyboard=[],
        assets=[],
        audio_plan={"music_genre": "Synthwave", "sfx_cues": []},
        platform="x",
        duration_sec=30
    )
    # Prohibited fluff words must be detected
    assert len(report.prohibited_phrases_detected) >= 2
    assert "make it cinematic" in report.prohibited_phrases_detected
    assert "make it viral" in report.prohibited_phrases_detected
    assert report.passes_quality_gate is False

def test_veo_first_last_frame_workflow_spec():
    """Verify Veo compiler produces start frame, end frame, and transition motion prompt."""
    spec = veo_prompt_compiler.compile_first_last_frame_shot(
        shot_id="SHOT-03",
        purpose="Datacenter rack transforms into microscopic silicon wafer",
        start_frame_description="Towering server rack glowing with blue fiber optic cables in a misty cold-aisle containment pod",
        end_frame_description="Extreme macro view of a 3nm silicon die with intricate conductive copper interconnects",
        motion_description="Continuous seamless zoom-in through the server chassis directly penetrating the silicon heat spreader",
        aspect_ratio="16:9"
    )

    assert spec.workflow_type == "FIRST_LAST_FRAME"
    assert "START FRAME PROMPT:" in spec.prompt
    assert "END FRAME PROMPT:" in spec.prompt
    assert "VIDEO TRANSITION PROMPT:" in spec.prompt
    assert spec.start_frame_prompt is not None
    assert spec.end_frame_prompt is not None
    assert spec.motion_prompt is not None

def test_prompt_memory_and_19_templates():
    """Verify prompt memory stores 19 reusable templates and logs performance ratings."""
    templates = prompt_memory_service.list_templates()
    assert len(templates) == 19
    template_names = [t.name if hasattr(t, "name") else t["name"] for t in templates]
    assert "Cinematic Documentary" in template_names
    assert "Breaking News" in template_names
    assert "Benchmark Breakdown" in template_names
    assert "Technical Deep Dive" in template_names

    # Record rating
    res = prompt_memory_service.rate_prompt(
        prompt_id="test_prompt_001",
        rating=98.5,
        feedback="Flawless camera speed and crisp Remotion layout",
        failure_mode=None
    )
    assert res["status"] == "recorded"
    assert res["prompt_id"] == "test_prompt_001"

def test_export_formats_generator():
    """Verify video orchestrator exports all 7 required production formats."""
    sample_pkg = {
        "package_id": "pkg_test_123",
        "title": "Quantum AI Hardware",
        "platform": "instagram_reel",
        "duration_seconds": 30,
        "storyboard": [
            {"scene_number": 1, "start_time_sec": 0, "end_time_sec": 3, "visual_objective": "Cryogenic diluter", "voiceover_text": "Quantum compute is here."}
        ],
        "shot_list": [
            {"shot_id": "SHOT-01", "engine": "OMNI", "exact_model_prompt": "35mm anamorphic camera dollying toward dilution refrigerator", "copyable_prompt": "35mm anamorphic..."}
        ],
        "asset_manifest": [
            {"asset_id": "ASSET-001", "asset_type": "generated_image", "description": "Cryostat"}
        ],
        "audio_plan": {
            "voiceover_script": "Quantum compute is here.",
            "music_genre": "Dark Cyberpunk Ambient",
            "bpm_range": "110-120",
            "emotional_role": "High stakes urgency",
            "sfx_cues": [{"timestamp_sec": 0.5, "sound_event": "Hydraulic hiss", "intensity": "High"}]
        },
        "engines": {
            "remotion": {"standalone_agent_prompt": "You are a Remotion engineer..."},
            "omni": [{"shot_id": "SHOT-01", "visual_prompt": "35mm anamorphic...", "avoid": "glitches"}],
            "veo": [{"shot_id": "SHOT-01", "prompt": "Cinematography: dolly in..."}],
            "hyperframes": {"standalone_agent_prompt": "You are a HyperFrames engineer..."}
        },
        "quality_report": {"overall_readiness_score": 96.0}
    }

    formats = [
        "video_package.json",
        "video_storyboard.md",
        "remotion_prompt.md",
        "omni_prompts.md",
        "veo_prompts.md",
        "hyperframes_prompt.md",
        "shot_list.md"
    ]
    for fmt in formats:
        exported = video_generation_service.export_package(sample_pkg, fmt)
        assert len(exported) > 30, f"Export format {fmt} returned empty or too small"
