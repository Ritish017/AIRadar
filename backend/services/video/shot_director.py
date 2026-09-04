"""
Shot Director (V3.3):
Transforms storyboard beats, visual concepts, and camera grammar into exhaustive, production-grade shot plans.
Executes story-first, capability-grounded model routing with explainable logic across 30+ structured fields.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid

from backend.services.video.visual_concept_engine import VisualConceptCandidate, visual_concept_engine
from backend.services.video.shot_complexity_analyzer import shot_complexity_analyzer, ShotComplexityReport
from backend.services.video.camera_language_engine import camera_language_engine, CameraGrammarSpec
from backend.services.video.continuity_engine import continuity_engine, ContinuityMasterState, ContinuityInjectionPayload
from backend.services.video.model_capabilities import model_capability_registry


class ProductionShotSpec(BaseModel):
    shot_id: str
    duration_sec: float
    purpose: str
    narration: str
    visual_concept: str
    subject: str
    environment: str
    action: str
    composition: str
    camera: str
    lens: str
    camera_movement: str
    lighting: str
    color_treatment: str
    depth: str
    foreground: str
    background: str
    motion: str
    transition_in: str
    transition_out: str
    typography: str
    captions: str
    audio: str
    sfx: str
    music_role: str
    asset_requirements: List[str]
    continuity_requirements: str
    negative_constraints: str
    model: str
    model_reason: str
    complexity_score: float
    generation_strategy: str
    copyable_prompt: str


class ShotDirectorPlan(BaseModel):
    director_plan_id: str
    title: str
    platform: str
    total_duration_sec: float
    total_shots: int
    shots: List[ProductionShotSpec]
    model_distribution: Dict[str, int]
    routing_rationale_summary: str


class ShotDirector:
    """
    Directs shot creation, conducts story-first routing, and compiles 30+ field production specifications.
    """

    def direct_shot(
        self,
        shot_number: int,
        beat_type: str,
        narration: str,
        topic: str,
        duration_sec: float,
        platform: str = "instagram_reel",
        continuity_state: Optional[ContinuityMasterState] = None,
        preferred_engine: str = "AUTO",
        metrics: Optional[Dict[str, Any]] = None
    ) -> ProductionShotSpec:
        shot_id = f"SHOT-{shot_number:02d}"

        # 1. Visual Concept Selection
        vc_suite = visual_concept_engine.generate_concepts(
            claim=narration,
            topic=topic,
            platform=platform,
            metrics=metrics
        )
        concept = vc_suite.selected_concept

        # 2. Camera Grammar Design
        is_data_beat = any(k in narration.lower() for k in ["benchmark", "percent", "%", "cost", "speed", "metric"])
        subject_type = "data_chart" if is_data_beat else ("silicon_hardware" if "chip" in topic.lower() or "hardware" in topic.lower() else "documentary_tech")
        cam_spec = camera_language_engine.design_camera(
            beat_type=beat_type,
            subject_type=subject_type,
            emotional_state="urgent_analytical" if beat_type == "hook" else "authoritative",
            platform=platform
        )

        # 3. Story-First Model Routing
        model, model_reason, gen_strategy = self._route_shot(
            beat_type=beat_type,
            narration=narration,
            concept=concept,
            preferred_engine=preferred_engine
        )

        # 4. Continuity Injection
        continuity_payload = None
        if continuity_state:
            has_char = len(continuity_state.characters) > 0
            continuity_payload = continuity_engine.generate_shot_continuity_anchor(
                state=continuity_state,
                shot_number=shot_number,
                requires_character=has_char and beat_type in ["hook", "context", "dialogue"]
            )
            continuity_text = continuity_payload.continuity_instruction
        else:
            continuity_text = "Standard studio lighting continuity and color temperature lock."

        # 5. Complexity Analysis
        complexity_rep = shot_complexity_analyzer.analyze_shot(
            shot_id=shot_id,
            visual_objective=concept.what_viewer_sees,
            subject_action=concept.core_visual_metaphor,
            camera_movement=cam_spec.movement_vector,
            duration_sec=duration_sec,
            has_text=is_data_beat,
            engine=model
        )

        # 6. Assemble 30+ Field Production Spec
        composition = "9:16 Vertical Rule-of-Thirds with 15% top/bottom safe zone" if platform in ["instagram_reel", "youtube_short"] else "16:9 Cinematic Golden Ratio framing"
        lighting = "4500K neutral key light, soft diffused fill, subtle electric cyan rim light separating subject from dark backdrop"
        color = "Obsidian slate #0B0F17, clean white #FFFFFF, electric cyan #06B6D4, high dynamic range"
        depth = cam_spec.depth_of_field
        foreground = "Clean platform caption safe-zone with zero visual occlusion"
        background = "Restrained research cleanroom or matte dark telemetry surfaces"
        motion = f"Smooth 60fps {cam_spec.movement_vector} with physically realistic inertial damping"
        trans_in = "Hard cut" if shot_number > 1 else "Direct opening frame (zero black delay)"
        trans_out = "Seamless cut on motion vector into subsequent perspective"
        typography = "Inter 800 for numerical badges, JetBrains Mono 500 for technical labels, high contrast"
        captions = f"Synchronized word-level highlighted subtitle: '{narration}'"
        audio = f"Spoken narration: \"{narration}\""
        sfx = "80Hz deep sub-thud on visual impact" if beat_type == "hook" else "Subtle metallic interface click"
        music_role = "Pulsating electronic synth underpinning cognitive tension; ducked -16dB under voiceover"
        negative = "No distorted typography, no floating fantasy particles, no deformed hands, no unmotivated handheld camera shake, no low-poly geometry"

        copyable_prompt = (
            f"[{shot_id}] ({duration_sec}s) Engine: {model.upper()}\n"
            f"Visual: {concept.what_viewer_sees}\n"
            f"Action: {concept.core_visual_metaphor}\n"
            f"Camera: {cam_spec.shot_scale}, {cam_spec.lens_focal_length}, {cam_spec.movement_vector}. {cam_spec.narrative_justification}\n"
            f"Lighting: {lighting}\n"
            f"Color: {color} | Depth: {depth}\n"
            f"Audio: Voiceover '{narration}' | SFX: {sfx} | Music: {music_role}\n"
            f"Continuity: {continuity_text}\n"
            f"Avoid: {negative}"
        )

        return ProductionShotSpec(
            shot_id=shot_id,
            duration_sec=duration_sec,
            purpose=f"Communicate {beat_type.upper()}: {concept.headline}",
            narration=narration,
            visual_concept=concept.headline,
            subject=concept.core_visual_metaphor,
            environment=continuity_state.environment.location_name if continuity_state else "Advanced Neural Facility",
            action=concept.core_visual_metaphor,
            composition=composition,
            camera=cam_spec.rig_style,
            lens=cam_spec.lens_focal_length,
            camera_movement=cam_spec.movement_vector,
            lighting=lighting,
            color_treatment=color,
            depth=depth,
            foreground=foreground,
            background=background,
            motion=motion,
            transition_in=trans_in,
            transition_out=trans_out,
            typography=typography,
            captions=captions,
            audio=audio,
            sfx=sfx,
            music_role=music_role,
            asset_requirements=concept.asset_requirements,
            continuity_requirements=continuity_text,
            negative_constraints=negative,
            model=model,
            model_reason=model_reason,
            complexity_score=complexity_rep.total_complexity_score,
            generation_strategy=gen_strategy,
            copyable_prompt=copyable_prompt
        )

    def _route_shot(
        self,
        beat_type: str,
        narration: str,
        concept: VisualConceptCandidate,
        preferred_engine: str
    ) -> (str, str, str):
        if preferred_engine and preferred_engine.upper() != "AUTO":
            eng = preferred_engine.upper()
            return eng, f"User-selected generation strategy override ({eng}).", eng

        narr_lower = narration.lower()

        # Rule 1: Exact numerical data, charts, benchmark percentages -> Remotion
        if any(k in narr_lower for k in ["benchmark", "accuracy", "%", "swe-bench", "score", "delta", "bar graph"]):
            return (
                "Remotion",
                "Exact numerical precision and pixel-perfect SVG typography required. Generative models hallucinate exact values.",
                "REMOTION_DATA_COMPILATION"
            )

        # Rule 2: Real CLI terminal commands, code inspection, DOM telemetry -> HyperFrames
        if any(k in narr_lower for k in ["terminal", "command", "bash", "curl", "cli", "kernel", "ebpf", "code"]):
            return (
                "HyperFrames",
                "Deterministic seekable HTML5/CSS terminal rendering with microsecond timestamps required.",
                "HYPERFRAMES_DOM_COMPOSITION"
            )

        # Rule 3: Start/End keyframe state transformation -> Veo
        if any(k in narr_lower for k in ["transforms into", "morphs into", "scales down", "converts from"]):
            return (
                "Veo",
                "Visual transformation benefits from Veo's native First/Last Frame keyframe interpolation without intermediate drift.",
                "VEO_KEYFRAME_TRANSFORMATION"
            )

        # Rule 4: Photorealistic cinematic environments, research lab B-roll -> Gemini Omni Flash
        if any(k in narr_lower for k in ["researcher", "laboratory", "subsea", "datacenter", "facility", "hardware"]):
            return (
                "Gemini Omni",
                "Requires high-fidelity photorealistic cinematography, 35mm anamorphic optics, and complex spatial lighting.",
                "OMNI_CINEMATIC_SYNTHESIS"
            )

        # Default fallback to Hybrid or Omni
        return (
            "Gemini Omni",
            "Narrative requires photorealistic visual storytelling with restrained commercial documentary contrast.",
            "OMNI_CINEMATIC_SYNTHESIS"
        )


shot_director = ShotDirector()
