"""
V3.3 Synthetic Forensic Tests:
Tests forensic analyzer, failure classification, and prompt evolution
against deterministic synthetic video conditions A through F.
Validates analyzer behavior and strict triad score separation.
"""

import pytest
from backend.services.video.video_forensic_analyzer import video_forensic_analyzer
from backend.services.video.video_failure_classifier import video_failure_classifier
from backend.services.video.prompt_evolution_engine import prompt_evolution_engine
from backend.services.video.prompt_output_diagnostics import prompt_output_diagnostics


def test_synthetic_video_a_static_freeze():
    """TEST VIDEO A: Static frozen video -> low motion score, FAIL_STATIC_MOTION, targeted camera vector evolution."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_a_static.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 30.0, "quality_report": {"overall_readiness_score": 97.0}},
        synthetic_properties={"is_static_freeze": True, "static_motion": True}
    )

    # Decoupled scores: Prompt readiness is 97, but motion is degraded
    assert report.prompt_readiness_score == 97.0
    assert report.dimension_scores["motion_quality"] < 50.0
    assert report.dimension_scores["motion_quality"] == 38.0

    # Failure detected
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_STATIC_MOTION" in fail_ids

    # Taxonomy classification
    tax = video_failure_classifier.classify_forensic_failures(report.detected_failures)
    assert any(cf.failure_code == "FAIL_STATIC_MOTION" for cf in tax.classified_failures)
    assert tax.highest_priority_operator == "add_temporal_camera_vectors"

    # Prompt evolution mutates camera trajectory
    evo = prompt_evolution_engine.evolve_prompt(
        current_version_label="V1",
        original_prompt_text="Camera: Rapid push-in towards the central node.",
        detected_failures=report.detected_failures
    )
    assert evo.parent_version == "V1"
    assert evo.new_version == "V2"
    assert any(m.operator == "add_temporal_camera_vectors" for m in evo.mutations_applied)
    assert "dolly push-in" in evo.evolved_prompt_text.lower()


def test_synthetic_video_b_rapid_scene_changes():
    """TEST VIDEO B: Rapid scene changes -> pacing warning, FAIL_RAPID_PACING, shot splitting evolution."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_b_rapid.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 20.0, "quality_report": {"overall_readiness_score": 95.0}},
        synthetic_properties={"excessive_rapid_cuts": True, "scene_cut_count": 18, "duration_sec": 20.0}
    )

    assert report.dimension_scores["pacing"] < 60.0
    assert report.dimension_scores["pacing"] == 52.0
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_RAPID_PACING" in fail_ids

    tax = video_failure_classifier.classify_forensic_failures(report.detected_failures)
    assert any(cf.failure_code == "FAIL_RAPID_PACING" for cf in tax.classified_failures)
    assert any(cf.category == "Story" for cf in tax.classified_failures)

    evo = prompt_evolution_engine.evolve_prompt(
        current_version_label="V1",
        original_prompt_text="Scene sequence with rapid transitions between 18 locations.",
        detected_failures=report.detected_failures
    )
    assert any(m.operator == "split_overloaded_shot" for m in evo.mutations_applied)


def test_synthetic_video_c_repeated_identical_frames():
    """TEST VIDEO C: Repeated identical frames -> temporal stutter warning, FAIL_TEMPORAL_STUTTER."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_c_stutter.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 30.0},
        synthetic_properties={"repeated_frames": True, "temporal_stutter": True}
    )

    assert report.dimension_scores["temporal_consistency"] < 60.0
    assert report.dimension_scores["temporal_consistency"] == 44.0
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_TEMPORAL_STUTTER" in fail_ids

    tax = video_failure_classifier.classify_forensic_failures(report.detected_failures)
    assert any(cf.failure_code == "FAIL_TEMPORAL_STUTTER" for cf in tax.classified_failures)
    assert tax.classified_failures[0].category == "Generation"


def test_synthetic_video_d_wrong_resolution():
    """TEST VIDEO D: Wrong resolution (16:9 for Instagram Reel) -> FAIL_WRONG_ASPECT_RATIO, platform fitness fail."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_d_res.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 30.0},
        synthetic_properties={
            "wrong_resolution": True,
            "width": 1920,
            "height": 1080,
            "target_platform": "instagram_reel"
        }
    )

    assert report.dimension_scores["platform_fitness"] < 60.0
    assert report.dimension_scores["platform_fitness"] == 48.0
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_WRONG_ASPECT_RATIO" in fail_ids


def test_synthetic_video_e_missing_audio():
    """TEST VIDEO E: Missing audio track -> critical FAIL_MISSING_AUDIO, audio_quality < 30."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_e_no_audio.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 30.0},
        synthetic_properties={"missing_audio": True, "has_audio": False}
    )

    assert report.dimension_scores["audio_quality"] <= 30.0
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_MISSING_AUDIO" in fail_ids

    tax = video_failure_classifier.classify_forensic_failures(report.detected_failures)
    assert any(cf.failure_code == "FAIL_MISSING_AUDIO" and cf.severity == "Critical" for cf in tax.classified_failures)


def test_synthetic_video_f_subtitle_safe_zone_overlap():
    """TEST VIDEO F: Subtitles in dead-zone -> typography FAIL_SUBTITLE_OCCLUSION, safe-zone elevation evolution."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_f_subtitles.mp4",
        prompt_spec={"aspect_ratio": "9:16", "duration_seconds": 30.0},
        synthetic_properties={"subtitle_overlap_safe_zone": True}
    )

    assert report.dimension_scores["typography_quality"] < 65.0
    fail_ids = [f["id"] for f in report.detected_failures]
    assert "FAIL_SUBTITLE_OCCLUSION" in fail_ids

    evo = prompt_evolution_engine.evolve_prompt(
        current_version_label="V1",
        original_prompt_text="Captions positioned at bottom edge of screen.",
        detected_failures=report.detected_failures
    )
    assert any(m.operator == "adjust_safe_zone_margin" for m in evo.mutations_applied)
    assert "translatey" in evo.evolved_prompt_text.lower()


def test_triad_score_separation_contract():
    """Verify that Prompt Readiness (specification) NEVER masquerades as Actual Video Quality."""
    report = video_forensic_analyzer.analyze_video(
        video_path_or_id="synthetic_test_mixed.mp4",
        prompt_spec={"quality_report": {"overall_readiness_score": 98.0}, "aspect_ratio": "9:16", "duration_seconds": 30.0},
        synthetic_properties={"is_static_freeze": True, "missing_audio": True}
    )

    # Prompt specification was 98.0
    assert report.prompt_readiness_score == 98.0
    # Expected executability is high
    assert report.expected_executability_score >= 80.0
    # Actual video quality is heavily penalized due to freeze + missing audio
    assert report.actual_video_quality_score < 80.0
    assert report.overall_verdict in ("WARN", "FAIL")
    # Crucial assertion: prompt score != video quality
    assert report.prompt_readiness_score != report.actual_video_quality_score
