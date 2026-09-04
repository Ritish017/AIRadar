"""
Model Capabilities Registry & Versioning:
Maintains structured metadata, verified capability matrices, and limitation guards
for Remotion, HyperFrames, Gemini Omni Flash, and Google Veo.
"""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class ModelCapabilityProfile(BaseModel):
    model_name: str
    version: str
    last_verified: str
    source_url: str
    text_to_video: bool = False
    image_to_video: bool = False
    video_to_video: bool = False
    reference_images: bool = False
    reference_video: bool = False
    audio: bool = False
    dialogue: bool = False
    first_last_frame: bool = False
    maximum_duration_sec: float
    supported_aspect_ratios: List[str] = Field(default_factory=lambda: ["16:9", "9:16", "1:1"])
    output_resolution: str
    capabilities: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)


class ModelCapabilityRegistry:
    """
    Central Registry for Video Generation & Motion Graphics Engines.
    Enforces strict capability boundaries, preventing prompts from claiming
    or requesting unsupported model operations.
    """

    def __init__(self):
        self._profiles: Dict[str, ModelCapabilityProfile] = {
            "Remotion": ModelCapabilityProfile(
                model_name="Remotion",
                version="v4.0.0",
                last_verified="2026-02-15",
                source_url="https://www.remotion.dev/docs",
                text_to_video=False,  # Code-driven React
                image_to_video=False,
                video_to_video=False,
                reference_images=True,  # Supports static assets & OffthreadVideo
                reference_video=True,
                audio=True,  # Audio tags & sequencing
                dialogue=False,  # Code engine, not generative TTS
                first_last_frame=False,
                maximum_duration_sec=3600.0,  # Arbitrary length support
                supported_aspect_ratios=["16:9", "9:16", "1:1", "4:5", "21:9"],
                output_resolution="Up to 4K (3840x2160) at 60fps",
                capabilities=[
                    "data_visualization", "charts", "graphs", "statistics",
                    "timelines", "rankings", "ui_mockups", "code_terminals",
                    "animated_typography", "captions", "spring_physics",
                    "deterministic_rendering", "parameterized_props",
                    "svg_animations", "motion_graphics"
                ],
                limitations=[
                    "Cannot generate photorealistic physical footage or human actors",
                    "Requires programmatic React component implementations",
                    "Heavy GPU 3D rendering requires Three.js integration",
                    "Cannot synthesize generative natural audio from text"
                ]
            ),
            "HyperFrames": ModelCapabilityProfile(
                model_name="HyperFrames",
                version="v2.4.0",
                last_verified="2026-01-20",
                source_url="https://hyperframes.io/docs",
                text_to_video=False,  # HTML/CSS/GSAP engine
                image_to_video=False,
                video_to_video=False,
                reference_images=True,
                reference_video=False,
                audio=True,  # Web Audio timeline sync
                dialogue=False,
                first_last_frame=False,
                maximum_duration_sec=600.0,
                supported_aspect_ratios=["16:9", "9:16", "1:1"],
                output_resolution="1080p to 4K WebM/MP4 at 60fps",
                capabilities=[
                    "html_motion_graphics", "kinetic_typography", "browser_interfaces",
                    "css_compositions", "gsap_timelines", "deterministic_render",
                    "seekable_timeline", "breaking_news_tickers", "hud_elements",
                    "lightweight_dom_animation"
                ],
                limitations=[
                    "Cannot generate organic 3D camera sweeps or photorealistic world physics",
                    "Must strictly avoid wall-clock time, setInterval, or unseeded Math.random",
                    "DOM complexity must remain bounded to prevent dropped frames",
                    "No native video codec decoding without external media layers"
                ]
            ),
            "Gemini Omni Flash": ModelCapabilityProfile(
                model_name="Gemini Omni Flash",
                version="v2.5-omni",
                last_verified="2026-02-28",
                source_url="https://ai.google.dev/gemini-api/docs/vision",
                text_to_video=True,
                image_to_video=True,
                video_to_video=True,
                reference_images=True,
                reference_video=True,
                audio=True,
                dialogue=True,
                first_last_frame=False,
                maximum_duration_sec=30.0,  # Optimal per-shot 3-10s
                supported_aspect_ratios=["16:9", "9:16", "1:1"],
                output_resolution="1080p / 4K ProRes at 24fps / 30fps / 60fps",
                capabilities=[
                    "cinematic_footage", "photorealistic_environments", "human_characters",
                    "physical_action", "complex_camera_movement", "volumetric_atmosphere",
                    "multimodal_scene_generation", "image_to_video", "cinematic_b_roll",
                    "natural_lighting", "shallow_depth_of_field", "spatial_audio"
                ],
                limitations=[
                    "Cannot render pixel-perfect exact text or numeric charts without artifacts",
                    "Long continuous single shots (>10s) exhibit narrative drift",
                    "Complex multi-stage actions in one shot fail; requires shot decomposition",
                    "Cannot guarantee deterministic millisecond-exact data synchronization"
                ]
            ),
            "Veo": ModelCapabilityProfile(
                model_name="Veo",
                version="v2.0",
                last_verified="2026-03-01",
                source_url="https://deepmind.google/technologies/veo",
                text_to_video=True,
                image_to_video=True,
                video_to_video=True,
                reference_images=True,
                reference_video=False,
                audio=True,  # Native audio and dialogue generation
                dialogue=True,
                first_last_frame=True,  # Native start/end keyframe interpolation
                maximum_duration_sec=60.0,  # High-fidelity short-to-medium shots
                supported_aspect_ratios=["16:9", "9:16", "1:1"],
                output_resolution="1080p / 4K cinematic at 24fps / 30fps",
                capabilities=[
                    "high_fidelity_cinematics", "first_last_frame_interpolation",
                    "image_to_video_motion", "native_dialogue", "cinematographic_control",
                    "visual_continuity", "physics_simulation", "lighting_consistency",
                    "controlled_pans_and_dollies", "lens_simulation"
                ],
                limitations=[
                    "Cannot render exact dynamic charts or animated SVG code",
                    "First/last frame workflows require both static images to be semantically continuous",
                    "Requires explicit cinematography, subject, action, context, style, and audio structure",
                    "Cannot perform browser DOM or React UI rendering"
                ]
            )
        }

    def get_profile(self, model_name: str) -> Optional[ModelCapabilityProfile]:
        for k, v in self._profiles.items():
            if k.lower() == model_name.lower():
                return v
        return None

    def validate_capability(self, model_name: str, required_capability: str) -> Tuple[bool, Optional[str]]:
        """
        Validates if a model legitimately supports the requested operation.
        Returns (is_valid, error_message).
        """
        profile = self.get_profile(model_name)
        if not profile:
            return False, f"Unknown model '{model_name}'. Available models: {list(self._profiles.keys())}"

        cap = required_capability.lower().replace(" ", "_").replace("-", "_")

        # Check boolean flags
        if cap in {"first_last_frame", "first_last_frame_interpolation"}:
            if not profile.first_last_frame:
                return False, f"Model '{model_name}' does NOT support first/last frame workflows. Use Veo or multi-shot decomposition."
            return True, None
        elif cap in {"text_to_video", "generative_video"}:
            if not profile.text_to_video:
                return False, f"Model '{model_name}' is a code/motion engine and does not support generative text-to-video. Use Gemini Omni or Veo."
            return True, None
        elif cap in {"image_to_video"}:
            if not profile.image_to_video:
                return False, f"Model '{model_name}' does not support image-to-video motion synthesis."
            return True, None
        elif cap in {"audio", "native_audio", "sound_synthesis"}:
            if not profile.audio:
                return False, f"Model '{model_name}' does not natively support audio synthesis."
            return True, None
        elif cap in {"dialogue", "speech_generation"}:
            if not profile.dialogue:
                return False, f"Model '{model_name}' does not natively synthesize dialogue audio."
            return True, None

        # Check capabilities list
        if cap in profile.capabilities:
            return True, None

        # Check sub-strings in capabilities
        if any(cap in c or c in cap for c in profile.capabilities):
            return True, None

        # Check limitations
        for lim in profile.limitations:
            if cap in lim.lower():
                return False, f"Operation '{required_capability}' is an explicit limitation of '{model_name}': {lim}"

        return False, f"Model '{model_name}' does not list capability '{required_capability}' in its verified profile."

    def list_all_models(self) -> List[Dict[str, Any]]:
        return [p.model_dump() for p in self._profiles.values()]


model_capability_registry = ModelCapabilityRegistry()
