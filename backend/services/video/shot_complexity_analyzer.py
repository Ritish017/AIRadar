"""
Shot Complexity Analyzer (V3.3):
Evaluates narrative and visual density of video shots across 10 physical and cinematographic dimensions.
When a shot attempts too many simultaneous actions, it triggers an intelligent shot splitter
to prevent model hallucination, character morphing, and dropped temporal constraints.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import re


class ComplexityVector(BaseModel):
    subject_count_score: float = Field(ge=0.0, le=100.0)
    simultaneous_actions_score: float = Field(ge=0.0, le=100.0)
    camera_complexity_score: float = Field(ge=0.0, le=100.0)
    environment_complexity_score: float = Field(ge=0.0, le=100.0)
    text_requirements_score: float = Field(ge=0.0, le=100.0)
    character_requirements_score: float = Field(ge=0.0, le=100.0)
    object_interactions_score: float = Field(ge=0.0, le=100.0)
    temporal_transitions_score: float = Field(ge=0.0, le=100.0)
    physics_complexity_score: float = Field(ge=0.0, le=100.0)
    continuity_constraints_score: float = Field(ge=0.0, le=100.0)


class DecomposedSubShot(BaseModel):
    sub_shot_id: str
    phase_name: str  # Establishing, Subject Action, Interior/Detail, Macro Focus, Graphic Overlay
    duration_sec: float
    visual_objective: str
    camera_movement: str
    primary_engine: str  # Gemini Omni, Veo, Remotion, HyperFrames
    prompt_instruction: str


class ShotComplexityReport(BaseModel):
    shot_id: str
    total_complexity_score: float
    is_split_recommended: bool
    dominant_complexity_drivers: List[str]
    complexity_vector: ComplexityVector
    split_sub_shots: Optional[List[DecomposedSubShot]] = None
    architectural_advice: str


class ShotComplexityAnalyzer:
    """
    Analyzes shot complexity and orchestrates micro-shot decomposition.
    """

    SPLIT_THRESHOLD = 75.0

    def analyze_shot(
        self,
        shot_id: str,
        visual_objective: str,
        subject_action: str,
        camera_movement: str,
        duration_sec: float = 5.0,
        has_text: bool = False,
        has_character: bool = False,
        engine: str = "AUTO"
    ) -> ShotComplexityReport:
        combined_text = f"{visual_objective} {subject_action} {camera_movement}".lower()

        # 1. Subject Count
        subject_keywords = ["person", "researcher", "engineer", "robot", "drone", "car", "server", "cluster", "crowd", "team"]
        sub_count = sum(1 for k in subject_keywords if k in combined_text)
        sub_score = min(100.0, sub_count * 28.0)

        # 2. Simultaneous Actions
        action_verbs = ["walks", "talks", "flies", "enters", "transforms", "displays", "pushes", "morphs", "explodes", "clicks", "rotates", "zooms"]
        action_count = sum(1 for v in action_verbs if v in combined_text)
        action_score = min(100.0, action_count * 24.0)

        # 3. Camera Complexity
        cam_verbs = ["orbit", "360", "fly-through", "penetrates", "whip pan", "continuous zoom", "dolly into micro"]
        cam_complexity = sum(1 for c in cam_verbs if c in combined_text)
        cam_score = min(100.0, cam_complexity * 35.0 + (30.0 if "fast" in combined_text else 15.0))

        # 4. Environment Complexity
        env_keywords = ["city", "interior", "exterior", "datacenter", "laboratory", "subsea", "outer space", "cleanroom"]
        env_count = sum(1 for e in env_keywords if e in combined_text)
        env_score = min(100.0, env_count * 30.0)

        # 5. Text Requirements
        text_score = 85.0 if has_text or any(w in combined_text for w in ["text", "code", "terminal", "metric", "chart", "badge"]) else 15.0

        # 6. Character Requirements
        char_score = 80.0 if has_character or any(w in combined_text for w in ["face", "dialogue", "speaking", "expression", "portrait"]) else 10.0

        # 7. Object Interactions
        interact_score = 75.0 if any(w in combined_text for w in ["holds", "touches", "manipulates", "plugs", "types", "interacts"]) else 20.0

        # 8. Temporal Transitions (transformation during single shot)
        transition_score = 85.0 if any(w in combined_text for w in ["transforms into", "morphs into", "shifts from", "dissolves into"]) else 15.0

        # 9. Physics Complexity
        physics_score = 80.0 if any(w in combined_text for w in ["fluid", "smoke", "shatter", "combustion", "reflection", "refraction"]) else 20.0

        # 10. Continuity Constraints
        continuity_score = 70.0 if (has_character and has_text) or sub_count > 1 else 25.0

        # Weighted composite score with peak bottleneck penalty
        base_score = (
            sub_score * 0.12 +
            action_score * 0.16 +
            cam_score * 0.14 +
            env_score * 0.08 +
            text_score * 0.12 +
            char_score * 0.10 +
            interact_score * 0.08 +
            transition_score * 0.10 +
            physics_score * 0.05 +
            continuity_score * 0.05
        )

        # Extreme vectors create generation bottlenecks even if other dimensions are low
        critical_vectors = [v for v in [sub_score, action_score, cam_score, env_score, text_score, char_score, interact_score, transition_score, physics_score, continuity_score] if v >= 70.0]
        bottleneck_penalty = len(critical_vectors) * 8.0
        total_score = min(100.0, round(base_score + bottleneck_penalty, 1))

        vector = ComplexityVector(
            subject_count_score=sub_score,
            simultaneous_actions_score=action_score,
            camera_complexity_score=cam_score,
            environment_complexity_score=env_score,
            text_requirements_score=text_score,
            character_requirements_score=char_score,
            object_interactions_score=interact_score,
            temporal_transitions_score=transition_score,
            physics_complexity_score=physics_score,
            continuity_constraints_score=continuity_score
        )

        # Identify dominant complexity drivers
        drivers = []
        if action_score >= 60:
            drivers.append(f"Excessive simultaneous actions ({action_count} concurrent verbs)")
        if cam_score >= 60:
            drivers.append("High camera trajectory curvature")
        if text_score >= 70:
            drivers.append("In-shot typography rendering risk")
        if transition_score >= 70:
            drivers.append("Intra-shot state mutation / metamorphosis")
        if sub_score >= 60:
            drivers.append("Multi-subject coordination density")

        is_split = (total_score >= self.SPLIT_THRESHOLD) or (len(drivers) >= 3)
        sub_shots = None
        advice = "Shot density is within optimal single-generation bounds."

        if is_split:
            sub_shots = self._decompose_shot(shot_id, visual_objective, subject_action, camera_movement, duration_sec)
            advice = (
                f"Shot complexity ({total_score:.1f}/100) triggers decomposition. "
                f"Decomposed into {len(sub_shots)} dedicated micro-shots to eliminate visual hallucination."
            )

        return ShotComplexityReport(
            shot_id=shot_id,
            total_complexity_score=total_score,
            is_split_recommended=is_split,
            dominant_complexity_drivers=drivers,
            complexity_vector=vector,
            split_sub_shots=sub_shots,
            architectural_advice=advice
        )

    def _decompose_shot(
        self,
        parent_shot_id: str,
        visual_objective: str,
        subject_action: str,
        camera_movement: str,
        total_duration: float
    ) -> List[DecomposedSubShot]:
        dur_part = round(total_duration / 3.0, 1)
        return [
            DecomposedSubShot(
                sub_shot_id=f"{parent_shot_id}A",
                phase_name="Establishing Context",
                duration_sec=dur_part,
                visual_objective=f"Establishing wide view: {visual_objective}",
                camera_movement="Steady slow tracking establishing physical space",
                primary_engine="Gemini Omni",
                prompt_instruction=f"Wide cinematic establishing shot of environment. Clean spatial orientation without micro-actions."
            ),
            DecomposedSubShot(
                sub_shot_id=f"{parent_shot_id}B",
                phase_name="Primary Subject Action",
                duration_sec=dur_part,
                visual_objective=f"Isolated focal action: {subject_action}",
                camera_movement="Medium close-up push-in locked on central subject",
                primary_engine="Veo",
                prompt_instruction=f"Medium focal view. Single dominant action: {subject_action}. High physical plausibility."
            ),
            DecomposedSubShot(
                sub_shot_id=f"{parent_shot_id}C",
                phase_name="Macro Focus & Information Overlay",
                duration_sec=total_duration - (dur_part * 2),
                visual_objective=f"Extreme detail or analytical payoff: {visual_objective}",
                camera_movement="Planar lock-on with graphic reveal",
                primary_engine="Remotion",
                prompt_instruction="Extreme macro view with parameterized Remotion data overlay and metric verification."
            )
        ]


shot_complexity_analyzer = ShotComplexityAnalyzer()
