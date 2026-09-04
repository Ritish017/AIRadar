"""
Video Failure Classifier (V3.3):
Hierarchical taxonomy classifier for AI video generation and editing failures across
Generation, Continuity, Story, Technical, and Creative domains.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ClassifiedVideoFailure(BaseModel):
    failure_code: str
    category: str  # Generation, Continuity, Story, Technical, Creative
    title: str
    severity: str  # Critical, High, Medium, Low
    affected_scenes: List[int] = Field(default_factory=list)
    diagnostic_evidence: str
    targeted_mutation_operator: str


class FailureTaxonomyReport(BaseModel):
    total_failures: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    category_breakdown: Dict[str, int]
    classified_failures: List[ClassifiedVideoFailure]
    highest_priority_operator: str


class VideoFailureClassifier:
    """
    Classifies raw forensic alerts into structured taxonomy buckets with targeted prompt mutations.
    """

    TAXONOMY_MAP = {
        # Generation failures
        "FAIL_STATIC_MOTION": ("Generation", "Static Optical Flow (Motion Failure)", "High", "add_temporal_camera_vectors"),
        "FAIL_TEMPORAL_STUTTER": ("Generation", "Temporal Frame Recurrence", "High", "reduce_action_density"),
        "FAIL_FACE_DRIFT": ("Generation", "Facial Geometry Distortion", "Critical", "inject_character_anchor"),
        "FAIL_ANATOMY_GLITCH": ("Generation", "Malformed Anatomy Artifact", "Critical", "constrain_negative_prompts"),
        "FAIL_TEXTURE_INSTABILITY": ("Generation", "Texture Boiling / Flickering", "Medium", "lock_lighting_parameters"),

        # Continuity failures
        "FAIL_CHARACTER_DRIFT": ("Continuity", "Cross-Shot Character Inconsistency", "Critical", "inject_character_anchor"),
        "FAIL_ENVIRONMENT_SHIFT": ("Continuity", "Unplanned Location Jump", "High", "lock_environment_landmarks"),
        "FAIL_LIGHTING_MISMATCH": ("Continuity", "Color Temperature Jump", "Medium", "enforce_color_palette_lock"),

        # Story failures
        "FAIL_RAPID_PACING": ("Story", "Excessive Shot Frequency", "Medium", "extend_shot_holds"),
        "FAIL_NARRATION_MISMATCH": ("Story", "Visual-Narration Dissonance", "Critical", "align_visual_concept_to_claim"),
        "FAIL_WEAK_HOOK": ("Story", "Sub-threshold 2-Second Retention Hook", "High", "recompile_hook_interrupt"),

        # Technical failures
        "FAIL_WRONG_ASPECT_RATIO": ("Technical", "Platform Dimension Mismatch", "High", "recompile_composition_aspect_ratio"),
        "FAIL_MISSING_AUDIO": ("Technical", "Absent Audio Stream", "Critical", "attach_multitrack_audio_manifest"),
        "FAIL_SUBTITLE_OCCLUSION": ("Technical", "Platform UI Subtitle Collision", "High", "adjust_safe_zone_margin"),

        # Creative failures
        "FAIL_CLICHE_DETECTED": ("Creative", "Repetitive AI Generation Trope", "Medium", "replace_cliches_with_grounded_metaphors"),
        "FAIL_LOW_NOVELTY": ("Creative", "Generic Stock Visual Pattern", "Medium", "inject_specific_technical_artifacts")
    }

    def classify_forensic_failures(
        self,
        raw_failures: List[Dict[str, Any]]
    ) -> FailureTaxonomyReport:
        classified = []
        cat_counts = {"Generation": 0, "Continuity": 0, "Story": 0, "Technical": 0, "Creative": 0}
        crit, high, med, low = 0, 0, 0, 0

        for rf in raw_failures:
            f_id = rf.get("id", "FAIL_UNKNOWN")
            tax_entry = self.TAXONOMY_MAP.get(f_id)

            if tax_entry:
                cat, title, sev, op = tax_entry
            else:
                cat = rf.get("category", "Generation")
                title = rf.get("description", "Unclassified video generation anomaly")
                sev = rf.get("severity", "Medium")
                op = "refine_prompt_instructions"

            if sev == "Critical":
                crit += 1
            elif sev == "High":
                high += 1
            elif sev == "Medium":
                med += 1
            else:
                low += 1

            cat_counts[cat] = cat_counts.get(cat, 0) + 1

            classified.append(
                ClassifiedVideoFailure(
                    failure_code=f_id,
                    category=cat,
                    title=title,
                    severity=sev,
                    affected_scenes=rf.get("affected_scenes", [1]),
                    diagnostic_evidence=rf.get("description", ""),
                    targeted_mutation_operator=op
                )
            )

        # Select highest priority operator
        priority_op = "maintain_current_spec"
        if classified:
            # Sort by severity priority: Critical -> High -> Medium -> Low
            sev_rank = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
            sorted_fails = sorted(classified, key=lambda f: sev_rank.get(f.severity, 0), reverse=True)
            priority_op = sorted_fails[0].targeted_mutation_operator

        return FailureTaxonomyReport(
            total_failures=len(classified),
            critical_count=crit,
            high_count=high,
            medium_count=med,
            low_count=low,
            category_breakdown=cat_counts,
            classified_failures=classified,
            highest_priority_operator=priority_op
        )


video_failure_classifier = VideoFailureClassifier()
