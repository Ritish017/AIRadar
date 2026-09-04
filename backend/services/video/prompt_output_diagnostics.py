"""
Prompt-vs-Output Diagnostics (V3.3):
Compares compiled PROMPT INTENT against ACTUAL VIDEO forensic observations.
Pinpoints exactly where external generation models deviated from directorial instructions.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class IntentVsOutputMismatch(BaseModel):
    mismatch_type: str  # SUBJECT_ABSENT, ACTION_ABSENT, CAMERA_ACTION_MISMATCH, CONTINUITY_VIOLATION, TIMING_MISMATCH
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    prompt_intent: str
    observed_video_output: str
    failure_mode_code: str
    actionable_remediation: str


class DiagnosticInspectionReport(BaseModel):
    inspection_id: str
    total_mismatches: int
    intent_fidelity_score: float = Field(ge=0.0, le=100.0)
    mismatches: List[IntentVsOutputMismatch]
    primary_failure_driver: str
    recommended_evolution_strategy: str


class PromptOutputDiagnostics:
    """
    Automated directorial comparison between specification and execution.
    """

    def diagnose_discrepancies(
        self,
        prompt_shots: List[Dict[str, Any]],
        forensic_failures: List[Dict[str, Any]],
        extracted_metadata: Dict[str, Any]
    ) -> DiagnosticInspectionReport:
        mismatches = []
        fail_codes = {f.get("id") or f.get("failure_code"): f for f in forensic_failures}

        # 1. Camera Action Mismatch
        if "FAIL_STATIC_MOTION" in fail_codes:
            mismatches.append(
                IntentVsOutputMismatch(
                    mismatch_type="CAMERA_ACTION_MISMATCH",
                    severity="HIGH",
                    prompt_intent="Camera executes rapid push-in or tracking move",
                    observed_video_output="Camera remained static with zero optical flow across frame sequence",
                    failure_mode_code="CAMERA_STATIC_FREEZE",
                    actionable_remediation="Reduce prompt subject clutter and explicitly specify primary directional camera axis."
                )
            )

        # 2. Timing / Aspect Ratio Mismatch
        if "FAIL_WRONG_ASPECT_RATIO" in fail_codes:
            mismatches.append(
                IntentVsOutputMismatch(
                    mismatch_type="TIMING_MISMATCH",
                    severity="HIGH",
                    prompt_intent="Vertical 9:16 aspect ratio (1080x1920) for Instagram Reel",
                    observed_video_output=f"Observed {extracted_metadata.get('width', 1920)}x{extracted_metadata.get('height', 1080)} landscape output",
                    failure_mode_code="ASPECT_RATIO_COLLISION",
                    actionable_remediation="Enforce output_format flag and re-render composition."
                )
            )

        # 3. Continuity Violation
        if "FAIL_CHARACTER_DRIFT" in fail_codes:
            mismatches.append(
                IntentVsOutputMismatch(
                    mismatch_type="CONTINUITY_VIOLATION",
                    severity="CRITICAL",
                    prompt_intent="Maintain consistent character appearance and attire across shots",
                    observed_video_output="Facial structure and clothing shifted significantly between shot intervals",
                    failure_mode_code="CHARACTER_FACE_DRIFT",
                    actionable_remediation="Inject persistent Character Bible reference token and constrain camera trajectory."
                )
            )

        # 4. Action / Subject Absent
        if "FAIL_NARRATION_MISMATCH" in fail_codes:
            mismatches.append(
                IntentVsOutputMismatch(
                    mismatch_type="ACTION_ABSENT",
                    severity="CRITICAL",
                    prompt_intent="Show concrete empirical metric and benchmark acceleration",
                    observed_video_output="Generic abstract visuals rendered without clear data grounding",
                    failure_mode_code="VISUAL_NARRATION_DISSONANCE",
                    actionable_remediation="Route metric visualization to Remotion rather than generative diffusion models."
                )
            )

        fidelity_penalty = len(mismatches) * 22.0
        fidelity_score = max(0.0, 100.0 - fidelity_penalty)

        primary_driver = mismatches[0].mismatch_type if mismatches else "NO_SIGNIFICANT_MISMATCH"
        strategy = (
            "Targeted prompt parameter mutation" if mismatches else "Prompt specification executed with high fidelity."
        )

        return DiagnosticInspectionReport(
            inspection_id=f"diag_{extracted_metadata.get('container_format', 'mp4')}",
            total_mismatches=len(mismatches),
            intent_fidelity_score=round(fidelity_score, 1),
            mismatches=mismatches,
            primary_failure_driver=primary_driver,
            recommended_evolution_strategy=strategy
        )


prompt_output_diagnostics = PromptOutputDiagnostics()
