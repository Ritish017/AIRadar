"""
Camera Language Engine (V3.3):
Determines intentional, story-driven camera behavior rather than repeating generic cinematic recipes.
Translates narrative beats and emotional stakes into concrete focal lengths, rigs, and movements.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CameraGrammarSpec(BaseModel):
    shot_scale: str  # Extreme Wide, Wide Establishing, Medium, Medium Close-Up, Close-Up, Extreme Macro
    lens_focal_length: str  # 18mm Ultra-Wide, 35mm Narrative, 50mm Human Natural, 85mm Portrait, 100mm Macro Telephoto
    rig_style: str  # Steadicam, Geared Head Tripod, Micro-Jib, Precision Dolly, Handheld Observational
    movement_vector: str  # Locked Static, Slow Push-In, Reveal Pull-Back, Lateral Parallax Tracking, 180 Orbit
    depth_of_field: str  # Deep Focus (f/8), Commercial Restrained (f/4), Atmospheric Shallow (f/1.8)
    narrative_justification: str


class CameraLanguageEngine:
    """
    Selects camera language based on story purpose, emotional tension, and cognitive density.
    """

    def design_camera(
        self,
        beat_type: str,  # hook, context, proof, architecture, tension, resolution, cta
        subject_type: str,  # hardware, data_chart, human_researcher, code_terminal, abstract_math
        emotional_state: str = "urgent_analytical",
        platform: str = "instagram_reel",
        pacing_bpm: int = 120
    ) -> CameraGrammarSpec:
        beat = beat_type.lower()
        subject = subject_type.lower()

        # 1. Data Charts / Benchmarks -> Geared Head Tripod / Planar Lock
        if "chart" in subject or "benchmark" in subject or "data" in subject or beat == "proof":
            return CameraGrammarSpec(
                shot_scale="Medium Frontal Planar",
                lens_focal_length="50mm Natural Perspective",
                rig_style="Geared Head Tripod (Locked Orthogonal)",
                movement_vector="Micro push-in (0.5% scale per second) keeping chart numbers perfectly crisp",
                depth_of_field="Deep Focus (f/5.6) ensuring all labels and legend axes remain razor-sharp",
                narrative_justification="Orthogonal lock prevents parallax distortion of bar charts and numeric metrics, maximizing empirical authority."
            )

        # 2. Hook / Disruption -> Rapid Controlled Dolly Push-In
        if beat == "hook" or "urgent" in emotional_state:
            return CameraGrammarSpec(
                shot_scale="Medium Close-Up with Strong Center Weighting",
                lens_focal_length="35mm Anamorphic Prime",
                rig_style="Precision Dolly on High-Speed Track",
                movement_vector="Rapid 1.2-second controlled push-in toward central subject, decelerating to a dead stop",
                depth_of_field="Restrained Shallow (f/2.8) creating subject-to-background separation without bokeh distraction",
                narrative_justification="Accelerated push-in creates instantaneous visual pattern interrupt in first 1.5 seconds, capturing viewer retention."
            )

        # 3. Systems Code / CLI Terminal -> Top-Down or Over-the-Shoulder Ergonomic
        if "code" in subject or "terminal" in subject or "ui" in subject:
            return CameraGrammarSpec(
                shot_scale="Medium Close-Up Monitor Viewport",
                lens_focal_length="50mm Clean Prime",
                rig_style="Ergonomic Workstation Rig",
                movement_vector="Subtle 2-degree horizontal pan following cursor execution from prompt to output",
                depth_of_field="Crisp Flat Plane (f/4.0) with zero chromatic aberration on terminal fonts",
                narrative_justification="Mimics authentic software engineering workflow without artificial handheld shaking."
            )

        # 4. Deep Architecture / Silicon -> Macro Telephoto
        if "silicon" in subject or "hardware" in subject or "architecture" in subject or beat == "architecture":
            return CameraGrammarSpec(
                shot_scale="Extreme Macro Detail",
                lens_focal_length="100mm Macro Telephoto with 2:1 Magnification",
                rig_style="Precision Motorized Motion-Control Slider",
                movement_vector="Continuous linear lateral glide across circuit die interconnects",
                depth_of_field="Razor-thin depth of field (f/2.0) with creamy linear background blur",
                narrative_justification="Extreme macro magnification communicates microscopic computational density and extreme hardware engineering precision."
            )

        # 5. Human Researcher / Character Dialogue -> 85mm Portrait Steadicam
        if "human" in subject or "researcher" in subject or "dialogue" in beat:
            return CameraGrammarSpec(
                shot_scale="Medium Close-Up (Chest to Head)",
                lens_focal_length="85mm Portrait Prime Lens",
                rig_style="Steadicam Operator (Subtle Breathing Motion)",
                movement_vector="Slow orbital arc (15 degrees) maintaining subject eye-line on upper third",
                depth_of_field="Cinematic Shallow (f/1.8) isolating speaker from background lab equipment",
                narrative_justification="Subtle human breathing movement creates emotional connection and intellectual credibility during technical explanation."
            )

        # Default: Editorial Documentary Standard
        return CameraGrammarSpec(
            shot_scale="Medium-Wide Establishing",
            lens_focal_length="35mm Documentary Lens",
            rig_style="Fluid Head Tripod",
            movement_vector="Slow controlled tilt-down from environment into focal subject",
            depth_of_field="Medium Deep (f/4.0) providing clear environmental context",
            narrative_justification="Establishes spatial geography and narrative orientation without distracting visual gymnastics."
        )


camera_language_engine = CameraLanguageEngine()
