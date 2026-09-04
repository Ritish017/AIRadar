"""
Prompt Evolution Engine (V3.3):
Closes the creative intelligence loop by mutating video prompts based on empirical forensic failures.
Executes targeted mutations across prompt versions (V1 -> V2 -> V3) while preserving successful elements.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid
import re


class MutationRecord(BaseModel):
    operator: str
    target_shot_or_section: str
    rationale: str
    original_snippet: str
    mutated_snippet: str
    expected_quality_delta: float


class PromptEvolutionLineage(BaseModel):
    evolution_id: str
    parent_version: str  # e.g. "V1"
    new_version: str  # e.g. "V2"
    primary_failure_addressed: str
    mutations_applied: List[MutationRecord]
    evolved_prompt_text: str
    expected_executability_score: float
    predicted_quality_score: float
    lineage_notes: str


class PromptEvolutionEngine:
    """
    Applies targeted prompt mutations based on diagnosed failures.
    """

    def evolve_prompt(
        self,
        current_version_label: str,
        original_prompt_text: str,
        detected_failures: List[Dict[str, Any]],
        target_model: str = "AUTO",
        human_critique: Optional[str] = None
    ) -> PromptEvolutionLineage:
        next_ver = f"V{int(current_version_label.replace('V', '')) + 1}" if current_version_label.startswith("V") else "V2"
        mutations = []
        evolved_text = original_prompt_text
        primary_failure = "General quality refinement"

        # 1. Address Static Camera / Motion Failure
        if any(f.get("id") == "FAIL_STATIC_MOTION" or "static" in str(f).lower() for f in detected_failures):
            primary_failure = "Static Optical Flow / Frozen Camera"
            orig_snippet = "Camera: Rapid push-in"
            mut_snippet = "Camera: Continuous motorized dolly push-in along primary Z-axis at 0.8 meters/second, locked orthogonal tracking."
            evolved_text = evolved_text.replace("Camera: Rapid push-in", mut_snippet)
            if mut_snippet not in evolved_text:
                evolved_text += f"\n\n[MUTATION - CAMERA VECTOR]: {mut_snippet}"
            mutations.append(
                MutationRecord(
                    operator="add_temporal_camera_vectors",
                    target_shot_or_section="Camera trajectory",
                    rationale="Forces generative video diffusion models to compute linear optical flow across frames.",
                    original_snippet=orig_snippet,
                    mutated_snippet=mut_snippet,
                    expected_quality_delta=14.0
                )
            )

        # 2. Address Character Face Drift
        if any(f.get("id") == "FAIL_CHARACTER_DRIFT" or "character" in str(f).lower() for f in detected_failures):
            primary_failure = "Cross-Shot Character Identity Drift"
            orig_snippet = "Maintain consistent subject appearance"
            mut_snippet = "STRICT IDENTITY ANCHOR: [REF-CHAR-01] Maintain immutable facial bone structure, dark acetate eyeglasses, and charcoal blazer. Zero cosmetic changes."
            evolved_text += f"\n\n[MUTATION - IDENTITY LOCK]: {mut_snippet}"
            mutations.append(
                MutationRecord(
                    operator="strengthen_character_anchor",
                    target_shot_or_section="Character Continuity",
                    rationale="Locks subject identity with reference asset token, preventing generative facial drift.",
                    original_snippet=orig_snippet,
                    mutated_snippet=mut_snippet,
                    expected_quality_delta=18.0
                )
            )

        # 3. Address Platform UI Subtitle Occlusion
        if any(f.get("id") == "FAIL_SUBTITLE_OCCLUSION" or "subtitle" in str(f).lower() for f in detected_failures):
            primary_failure = "Subtitle Occlusion by Native UI"
            orig_snippet = "Captions positioned at bottom"
            mut_snippet = "REMOTION SAFE ZONE: Elevate caption container translateY: -140px, ensuring text remains inside platform safe boundaries above TikTok/Reels description overlay."
            evolved_text += f"\n\n[MUTATION - SAFE ZONE ADJUSTMENT]: {mut_snippet}"
            mutations.append(
                MutationRecord(
                    operator="adjust_safe_zone_margin",
                    target_shot_or_section="Caption Positioning",
                    rationale="Prevents on-screen text from being occluded by native platform interaction buttons.",
                    original_snippet=orig_snippet,
                    mutated_snippet=mut_snippet,
                    expected_quality_delta=12.0
                )
            )

        # 4. Address Excessive Shot Complexity / Splitting
        if any(f.get("id") == "FAIL_RAPID_PACING" or "pacing" in str(f).lower() for f in detected_failures):
            primary_failure = "Excessive Shot Complexity"
            orig_snippet = "Rapid transitions"
            mut_snippet = "PACING DECOMPOSITION: Split multi-action beats into discrete 3.0s holds. Isolate establishing shot from macro detail."
            evolved_text += f"\n\n[MUTATION - SHOT SPLIT]: {mut_snippet}"
            mutations.append(
                MutationRecord(
                    operator="split_overloaded_shot",
                    target_shot_or_section="Timeline Pacing",
                    rationale="Eliminates cognitive overload by giving each distinct idea its own clear shot hold.",
                    original_snippet=orig_snippet,
                    mutated_snippet=mut_snippet,
                    expected_quality_delta=11.0
                )
            )

        # 5. Integrate Human Feedback if provided
        if human_critique:
            mutations.append(
                MutationRecord(
                    operator="human_editorial_refinement",
                    target_shot_or_section="Creator Directorial Notes",
                    rationale=f"Incorporating direct user feedback: '{human_critique}'",
                    original_snippet="Standard AI directorial assumptions",
                    mutated_snippet=f"USER DIRECTIVE: {human_critique}",
                    expected_quality_delta=15.0
                )
            )
            evolved_text += f"\n\n[MUTATION - CREATOR DIRECTIVE]: {human_critique}"

        # Default mutation if no specific failures detected
        if not mutations:
            mut_snippet = "PRECISION REFINEMENT: Heighten commercial lighting contrast and clarify key subject action."
            evolved_text += f"\n\n[MUTATION - POLISH]: {mut_snippet}"
            mutations.append(
                MutationRecord(
                    operator="clarify_subject_action",
                    target_shot_or_section="Visual Prompt Polish",
                    rationale="Increases visual specificity and eliminates ambiguity for diffusion generators.",
                    original_snippet="Standard prompt description",
                    mutated_snippet=mut_snippet,
                    expected_quality_delta=6.0
                )
            )

        total_predicted_gain = sum(m.expected_quality_delta for m in mutations)
        predicted_score = min(98.5, round(72.0 + total_predicted_gain, 1))

        return PromptEvolutionLineage(
            evolution_id=f"evo_{uuid.uuid4().hex[:8]}",
            parent_version=current_version_label,
            new_version=next_ver,
            primary_failure_addressed=primary_failure,
            mutations_applied=mutations,
            evolved_prompt_text=evolved_text,
            expected_executability_score=95.0,
            predicted_quality_score=predicted_score,
            lineage_notes=(
                f"Evolved from {current_version_label} to {next_ver} by applying {len(mutations)} targeted mutation operators. "
                f"Predicted quality gain: +{total_predicted_gain:.1f} points."
            )
        )


prompt_evolution_engine = PromptEvolutionEngine()
