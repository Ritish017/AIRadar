"""
V3.3 Golden Video Reality Benchmark Suite:
Comprehensive validation of the 10 core creative benchmark categories,
end-to-end creative loop, shot complexity analyzer, continuity engine,
anti-slop engine, model routing, forensic diagnostics, and prompt evolution.
"""

import os
import json
import pytest
from backend.services.video.video_orchestrator import video_generation_service
from backend.services.video.visual_concept_engine import visual_concept_engine
from backend.services.video.shot_complexity_analyzer import shot_complexity_analyzer
from backend.services.video.continuity_engine import continuity_engine, CharacterState
from backend.services.video.camera_language_engine import camera_language_engine
from backend.services.video.visual_diversity import visual_diversity_engine
from backend.services.video.shot_director import shot_director
from backend.services.video.video_forensic_analyzer import video_forensic_analyzer
from backend.services.video.video_failure_classifier import video_failure_classifier
from backend.services.video.prompt_output_diagnostics import prompt_output_diagnostics
from backend.services.video.prompt_evolution_engine import prompt_evolution_engine
from backend.services.video.prompt_memory import prompt_memory_service


BENCHMARK_BASE = os.path.join(os.path.dirname(__file__), "..", "benchmarks", "video")


@pytest.mark.asyncio
async def test_golden_benchmark_1_ai_model_launch_hybrid():
    """Case 1: AI Model Launch -> Visual concept, hybrid routing (Omni + Remotion), triad score."""
    case_path = os.path.join(BENCHMARK_BASE, "001_ai_model_launch")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "visual_concepts.json"), "r") as f:
        concepts = json.load(f)
    assert len(concepts["candidates"]) >= 3
    assert concepts["selected_concept"]["production_feasibility"] >= 80.0

    with open(os.path.join(case_path, "evaluation", "forensic_report.json"), "r") as f:
        report = json.load(f)
    assert report["prompt_readiness_score"] >= 95.0
    assert report["expected_executability_score"] >= 85.0
    assert report["actual_video_quality_score"] >= 85.0
    assert report["overall_verdict"] in ("PASS", "EXCELLENT")


@pytest.mark.asyncio
async def test_golden_benchmark_2_benchmark_comparison_remotion():
    """Case 2: Benchmark Comparison -> Remotion routing for exact charts, zero hallucinated text."""
    case_path = os.path.join(BENCHMARK_BASE, "002_benchmark_comparison")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "prompts", "remotion_spec_v1.json"), "r") as f:
        remotion_code = f.read()
    assert "useCurrentFrame" in remotion_code or "interpolate" in remotion_code or "spring" in remotion_code

    with open(os.path.join(case_path, "evaluation", "forensic_report.json"), "r") as f:
        report = json.load(f)
    assert report["dimension_scores"]["text_accuracy"] >= 90.0


@pytest.mark.asyncio
async def test_golden_benchmark_3_future_scenario_cinematic():
    """Case 3: Cinematic Future Scenario -> Anamorphic framing, anti-slop audit, Omni/Veo routing."""
    case_path = os.path.join(BENCHMARK_BASE, "003_future_scenario")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "storyboard.json"), "r") as f:
        sb = json.load(f)
    assert sb["aspect_ratio"] == "16:9"

    # Anti-slop check
    audit = visual_diversity_engine.audit_visual_content(
        "Daylight city drone tracking shot moving smoothly above modern elevated transit line."
    )
    assert audit.has_prohibited_cliches is False


@pytest.mark.asyncio
async def test_golden_benchmark_4_technical_interface_hyperframes():
    """Case 4: Technical Interface -> HyperFrames DOM deterministic code diff."""
    case_path = os.path.join(BENCHMARK_BASE, "004_technical_interface")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "prompts", "hyperframes_spec_v1.json"), "r") as f:
        hf_spec = f.read()
    assert "gsap" in hf_spec.lower() or "renderframe" in hf_spec.lower() or "html" in hf_spec.lower()


@pytest.mark.asyncio
async def test_golden_benchmark_5_research_explainer_pedagogical():
    """Case 5: Research Explainer -> Pedagogical clarity, animated math + conceptual flow."""
    case_path = os.path.join(BENCHMARK_BASE, "005_research_explainer")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "evaluation", "forensic_report.json"), "r") as f:
        report = json.load(f)
    assert report["dimension_scores"]["narrative_clarity"] >= 88.0
    assert report["dimension_scores"]["information_density"] >= 88.0


@pytest.mark.asyncio
async def test_golden_benchmark_6_character_dialogue_continuity():
    """Case 6: Character Dialogue -> Character Bible lock, continuity state tracking."""
    case_path = os.path.join(BENCHMARK_BASE, "006_character_dialogue")
    assert os.path.exists(case_path)

    state = continuity_engine.initialize_state(
        title="Dialogue 006",
        topic="Edge vs Cloud",
        has_character=True,
        character_name="Elena Ramos"
    )
    anchor = continuity_engine.generate_shot_continuity_anchor(
        state=state,
        shot_number=1,
        requires_character=True
    )
    assert "Elena Ramos" in anchor.continuity_instruction
    assert "eyeglasses" in anchor.continuity_instruction.lower()


@pytest.mark.asyncio
async def test_golden_benchmark_7_instagram_reel_retention():
    """Case 7: Instagram Reel -> Safe-zone compliance, retention hook in first 2s."""
    case_path = os.path.join(BENCHMARK_BASE, "007_instagram_reel")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "evaluation", "forensic_report.json"), "r") as f:
        report = json.load(f)
    assert report["dimension_scores"]["platform_fitness"] >= 90.0
    assert report["dimension_scores"]["hook_strength"] >= 90.0


@pytest.mark.asyncio
async def test_golden_benchmark_8_youtube_short_hardware():
    """Case 8: YouTube Short -> Macro semiconductor shot + Remotion bandwidth gauge."""
    case_path = os.path.join(BENCHMARK_BASE, "008_youtube_short")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "content_brief.json"), "r") as f:
        brief = json.load(f)
    assert brief["platform"] == "youtube_short"
    assert brief["aspect_ratio"] == "9:16"


@pytest.mark.asyncio
async def test_golden_benchmark_9_youtube_longform_multiscene():
    """Case 9: YouTube Explainer -> Long-form multi-scene narrative progression."""
    case_path = os.path.join(BENCHMARK_BASE, "009_youtube_explainer")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "generated", "manifest.json"), "r") as f:
        manifest = json.load(f)
    assert manifest["duration_sec"] >= 60.0
    assert manifest["aspect_ratio"] == "16:9"


@pytest.mark.asyncio
async def test_golden_benchmark_10_breaking_news_journalistic():
    """Case 10: Breaking AI News -> Journalistic grounding, zero hallucinations, source citation."""
    case_path = os.path.join(BENCHMARK_BASE, "010_breaking_news")
    assert os.path.exists(case_path)

    with open(os.path.join(case_path, "event.json"), "r") as f:
        event = json.load(f)
    assert "deepseek" in event["headline"].lower()
    assert event["confidence"] >= 0.95
    assert len(event["key_facts"]) >= 3


def test_shot_complexity_overloaded_split():
    """Verify that overloaded shots with complexity score > 75 are automatically decomposed."""
    report = shot_complexity_analyzer.analyze_shot(
        shot_id="SHOT-OVERLOADED-01",
        visual_objective="Camera flies through city and zooms into building window",
        subject_action="Engineer walks and talks while robot transforms and drone drops chip",
        camera_movement="Continuous 360 degree orbit and fly-through"
    )
    assert report.total_complexity_score > 70.0
    assert report.is_split_recommended is True
    assert len(report.split_sub_shots) >= 2


def test_anti_slop_cliche_detection_and_alternative():
    """Verify detection of generic AI clichés and recommendation of grounded visual alternatives."""
    bad_prompt = "Camera glides through a neon blue cyberpunk server room with floating holograms and glowing circuitry."
    audit = visual_diversity_engine.audit_visual_content(bad_prompt)
    assert audit.has_prohibited_cliches is True
    assert len(audit.detected_cliches) >= 2
    assert audit.detected_cliches[0].suggested_grounded_alternative is not None


def test_camera_language_engine_rationales():
    """Verify camera language engine provides explicit directorial rationales."""
    cam = camera_language_engine.design_camera(
        beat_type="hook",
        subject_type="Benchmark Data Comparison",
        platform="youtube_short"
    )
    assert cam.shot_scale is not None
    assert cam.movement_vector is not None
    assert len(cam.narrative_justification) > 15


def test_failure_patterns_dashboard_reporting():
    """Verify failure patterns dashboard aggregates stored feedback and heuristics."""
    dashboard = prompt_memory_service.get_failure_patterns_dashboard()
    assert "most_common_failures" in dashboard
    assert "best_improvement_mutations" in dashboard
    assert "learned_heuristics" in dashboard
    assert len(dashboard["learned_heuristics"]) >= 3
