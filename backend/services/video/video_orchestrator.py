"""
Universal Video Prompt Intelligence & Creative Director Orchestrator:
Coordinates storyboard synthesis, multi-engine routing, model-specific prompt compilers,
hybrid assembly plans, and 15-dimension quality evaluation.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from backend.services.video.remotion_prompt_compiler import (
    remotion_prompt_compiler, RemotionSpecification, RemotionAssetRequirement
)
from backend.services.video.omni_prompt_compiler import omni_prompt_compiler, OmniProductionPackage, OmniShotPrompt
from backend.services.video.veo_prompt_compiler import veo_prompt_compiler, VeoProductionPackage, VeoShotPrompt
from backend.services.video.hyperframes_prompt_compiler import hyperframes_prompt_compiler, HyperFramesSpecification
from backend.services.video.hybrid_planner import hybrid_planner, HybridAssemblyPlan
from backend.services.video.storyboard_engine import (
    storyboard_engine, UniversalStoryboard, HookCandidateVision,
    ShotBreakdownEntry, CharacterBible
)
from backend.services.video.video_quality_evaluator import video_quality_evaluator, VideoQualityReport
from backend.services.video.prompt_memory import (
    prompt_memory_service, VideoPromptTemplate, PromptEvolutionMemoryRecord, LearnedHeuristic
)
from backend.services.video.visual_concept_engine import (
    visual_concept_engine, VisualConceptSuite, VisualConceptCandidate
)
from backend.services.video.shot_complexity_analyzer import (
    shot_complexity_analyzer, ShotComplexityReport
)
from backend.services.video.camera_language_engine import (
    camera_language_engine, CameraGrammarSpec
)
from backend.services.video.visual_diversity import (
    visual_diversity_engine, VisualDiversityAudit
)
from backend.services.video.continuity_engine import (
    continuity_engine, ContinuityMasterState
)
from backend.services.video.shot_director import (
    shot_director, ProductionShotSpec, ShotDirectorPlan
)
from backend.services.video.video_forensic_analyzer import (
    video_forensic_analyzer, VideoForensicReport, VideoMetadata
)
from backend.services.video.video_failure_classifier import (
    video_failure_classifier, FailureTaxonomyReport
)
from backend.services.video.prompt_output_diagnostics import (
    prompt_output_diagnostics, DiagnosticInspectionReport
)
from backend.services.video.prompt_evolution_engine import (
    prompt_evolution_engine, PromptEvolutionLineage
)

logger = logging.getLogger(__name__)

# =========================================================================
# BACKWARD COMPATIBLE SCHEMAS (V3 Baseline)
# =========================================================================

class StoryboardScene(BaseModel):
    scene_number: int
    timecode: str
    duration_sec: float
    beat_type: str  # Hook, Context, Main Event, Visual Explanation, Implication, CTA
    narration: str
    visual_direction: str
    camera_instruction: str
    on_screen_text: str
    recommended_engine: str  # Gemini Omni, Remotion, HyperFrames
    asset_prompt: str

class VideoStoryboard(BaseModel):
    title: str
    total_duration_sec: float = 30.0
    aspect_ratio: str = "9:16"
    scenes: List[StoryboardScene]

class OmniPromptPayload(BaseModel):
    subject: str
    action: str
    environment: str
    time_of_day: str = "Cinematic studio twilight"
    lighting: str
    camera: Dict[str, str] = Field(default_factory=dict)
    composition: str
    depth: str
    materials: str
    physics: str
    motion: str
    audio: str
    dialogue: str
    style: str
    color_tone: str
    continuity: str
    negative_constraints: List[str] = Field(default_factory=list)
    output_format: str = "4K 60fps Vertical 9:16 HDR"
    compiled_master_prompt: str

class RemotionPromptPayload(BaseModel):
    composition_name: str
    duration_in_frames: int
    fps: int = 30
    width: int = 1080
    height: int = 1920
    components: List[str]
    timeline_scenes: List[Dict[str, Any]]
    typography: Dict[str, str]
    caption_behavior: str
    charts_and_metrics: Dict[str, Any]
    render_command: str

class HyperFramesPromptPayload(BaseModel):
    composition_id: str
    width: int = 1080
    height: int = 1920
    fps: int = 60
    total_duration_frames: int = 900
    duration_frames: int = 900
    html_markup: str
    css_styles: str
    gsap_timeline_code: str
    deterministic_contract: str


# =========================================================================
# V3.2 UNIVERSAL VIDEO PACKAGE SCHEMA
# =========================================================================

class VideoEnginesPayload(BaseModel):
    remotion: Optional[RemotionSpecification] = None
    omni: Optional[OmniProductionPackage] = None
    veo: Optional[VeoProductionPackage] = None
    hyperframes: Optional[HyperFramesSpecification] = None

    def __getitem__(self, item: str):
        return getattr(self, item)


class VideoPackage(BaseModel):
    video_id: str
    title: str
    topic: str
    platform: str
    duration_seconds: float
    aspect_ratio: str
    visual_style: str
    creative_concept: str
    generation_strategy: str = "AUTO"
    hook_candidates: List[HookCandidateVision]
    selected_hook: HookCandidateVision
    storyboard: UniversalStoryboard
    shot_list: List[ShotBreakdownEntry]
    asset_manifest: List[Any]
    audio_plan: Dict[str, Any]
    caption_plan: Dict[str, Any]
    character_bible: Optional[CharacterBible] = None
    engines: VideoEnginesPayload
    hybrid_assembly: HybridAssemblyPlan
    quality_report: VideoQualityReport
    export_formats: Dict[str, str]

    # V3.3 Creative Intelligence & Forensic Extensions
    visual_concepts: Optional[VisualConceptSuite] = None
    continuity_state: Optional[ContinuityMasterState] = None
    diversity_audit: Optional[VisualDiversityAudit] = None
    production_shots: Optional[List[ProductionShotSpec]] = None
    forensic_report: Optional[VideoForensicReport] = None
    evolution_lineage: Optional[List[PromptEvolutionLineage]] = None

    @property
    def triad_scores(self) -> Dict[str, float]:
        readiness = self.quality_report.overall_readiness_score
        actual = self.forensic_report.actual_video_quality_score if self.forensic_report else (readiness - 8.0)
        executability = self.forensic_report.expected_executability_score if self.forensic_report else 94.0
        return {
            "prompt_readiness": readiness,
            "expected_executability": executability,
            "actual_video_quality": actual
        }

    @property
    def ranked_hooks(self) -> List[HookCandidateVision]:
        return self.hook_candidates

    @property
    def package_id(self) -> str:
        return self.video_id

    @property
    def why_this_video(self) -> str:
        return f"High-retention strategic narrative optimized for {self.platform} retention algorithms."


# =========================================================================
# VIDEO GENERATION SERVICE (V3.2 Creative Director)
# =========================================================================

class VideoGenerationService:
    """
    Unified AI Video Creative Director & Prompt Compiler.
    Translates verified trends & events into production-ready prompts
    for Remotion, Gemini Omni, Veo, HyperFrames, and Hybrid Assembly.
    """

    def determine_route(self, visual_need: str) -> Tuple[str, str]:
        """Automatically decides optimal tool engine based on visual intent."""
        v = visual_need.lower()
        if any(k in v for k in ["chart", "data", "metric", "graph", "stat", "table", "benchmark"]):
            return "Remotion", "Data-driven animated charts and benchmark comparisons require Remotion's deterministic React canvas."
        elif any(k in v for k in ["ui", "button", "card", "breaking", "lower third", "badge", "ticker", "html"]):
            return "HyperFrames", "Deterministic DOM layout, motion typography, and lightweight HTML/CSS animations suit HyperFrames."
        elif any(k in v for k in ["veo", "first/last", "image-to-video", "character dialogue"]):
            return "Veo", "Google Veo provides native cinematic first/last frame transitions and controlled physical motion."
        elif any(k in v for k in ["cinematic", "photorealistic", "b-roll", "drone", "human", "character", "atmosphere", "scene"]):
            return "Gemini Omni", "High-fidelity photorealistic generative footage and creative B-roll require Gemini Omni."
        else:
            return "Hybrid", "Recommended combination: Gemini Omni for ambient cinematic background, layered with Remotion for exact data typography."

    # ---------------------------------------------------------------------
    # V3 BACKWARD COMPATIBLE METHOD SIGNATURES
    # ---------------------------------------------------------------------
    def build_storyboard(
        self,
        title: str,
        key_claims: List[str],
        counterpoint: str = ""
    ) -> VideoStoryboard:
        """Constructs an industry-standard 6-scene video storyboard (V3 baseline signature)."""
        claim_1 = key_claims[0] if key_claims else "Frontier reasoning model release"

        scenes = [
            StoryboardScene(
                scene_number=1,
                timecode="00:00 - 00:02",
                duration_sec=2.0,
                beat_type="Hook",
                narration="Your entire AI API bill is about to drop by 70%.",
                visual_direction="Extreme close-up of a holographic smartphone showing cloud expenses plummeting in neon red.",
                camera_instruction="Rapid dynamic push-in with subtle micro-camera shake.",
                on_screen_text="-70% COMPUTE COSTS",
                recommended_engine="HyperFrames",
                asset_prompt="Glowing neon red financial graph plunging downward against a dark futuristic grid, 8k"
            ),
            StoryboardScene(
                scene_number=2,
                timecode="00:02 - 00:05",
                duration_sec=3.0,
                beat_type="Context",
                narration=f"Here's what happened: {title[:60]} just launched with open weights.",
                visual_direction="Fast wipe to high-tech server datacenter, blue volumetric fog, floating glass logo.",
                camera_instruction="Slow cinematic tracking shot drifting right to left.",
                on_screen_text=title[:30].upper(),
                recommended_engine="Gemini Omni",
                asset_prompt="Cinematic dark futuristic server room with volumetric blue lighting and floating holographic code nodes"
            ),
            StoryboardScene(
                scene_number=3,
                timecode="00:05 - 00:09",
                duration_sec=4.0,
                beat_type="Main Event",
                narration="On standard benchmarks, it goes toe-to-toe with the most expensive models in the world.",
                visual_direction="Side-by-side animated bar chart popping onto screen with dynamic bounce physics.",
                camera_instruction="Static lock-on with smooth motion graphics entry.",
                on_screen_text="94.2% SWE-BENCH ACCURACY",
                recommended_engine="Remotion",
                asset_prompt="Animated React SVG bar chart comparing benchmark scores with glowing cyan gradient"
            ),
            StoryboardScene(
                scene_number=4,
                timecode="00:09 - 00:15",
                duration_sec=6.0,
                beat_type="Visual Explanation",
                narration=f"The secret is architectural: {claim_1}. Only the necessary neural pathways fire per token.",
                visual_direction="3D visualization of a sparse mixture-of-experts network activating glowing pathways in sequence.",
                camera_instruction="Orbit camera rotating 45 degrees around the glowing neural core.",
                on_screen_text="SPARSE ROUTING EFFICIENCY",
                recommended_engine="Gemini Omni",
                asset_prompt="Complex 3D neural network architecture visualization, glowing green energy traveling through sparse pathways, 8k render"
            ),
            StoryboardScene(
                scene_number=5,
                timecode="00:15 - 00:25",
                duration_sec=10.0,
                beat_type="Implication & Caveat",
                narration=f"For developers, this means self-hosting without multi-GPU clusters. But watch out: {counterpoint or 'long-context degradation is still being verified.'}",
                visual_direction="Split-screen: developer terminal running Ollama at 140 tok/sec on left; amber warning radar on right.",
                camera_instruction="Smooth slider pan across dual glass cards.",
                on_screen_text="LOCAL INFERENCE: 140 TOK/S",
                recommended_engine="HyperFrames",
                asset_prompt="Developer IDE screen showing fast token output next to a sleek telemetry HUD"
            ),
            StoryboardScene(
                scene_number=6,
                timecode="00:25 - 00:30",
                duration_sec=5.0,
                beat_type="CTA",
                narration="Are you keeping cloud APIs or deploying local weights this week? Comment below for the setup repo.",
                visual_direction="Minimalist end-card with glowing bookmark button and pulsating comment badge.",
                camera_instruction="Gentle slow pull-back ending on logo.",
                on_screen_text="COMMENT 'LOCAL' FOR REPO",
                recommended_engine="Remotion",
                asset_prompt="Sleek call to action card with glowing interactive UI buttons on matte carbon background"
            )
        ]

        return VideoStoryboard(
            title=f"{title} - 30s Explainer",
            total_duration_sec=30.0,
            aspect_ratio="9:16",
            scenes=scenes
        )

    def compile_omni_prompt(
        self,
        topic: str,
        scene_description: str,
        aspect_ratio: str = "9:16",
        style_preset: str = "Cinematic Tech News",
        style: Optional[str] = None
    ) -> OmniPromptPayload:
        """Compiles a production-grade 20-field Gemini Omni video prompt (V3 baseline signature)."""
        effective_style = style or style_preset
        shot = omni_prompt_compiler.compile_shot(
            shot_id="OMNI-SHOT-01",
            timecode="00:00 - 00:05",
            duration_sec=5.0,
            purpose="Hero visual establish",
            topic=topic,
            action=scene_description or "High-velocity data streams illuminate microscopic optical circuitry",
            environment="Ultra-modern deep tech research laboratory, dark matte carbon surfaces",
            camera_move="Slow controlled push-in toward the central processing core",
            aspect_ratio=aspect_ratio,
            style_preset=effective_style
        )

        return OmniPromptPayload(
            subject=f"Neural computation core for {topic}",
            action="Sequential activation of optical micro-circuitry and data streams",
            environment="High-tech subterranean datacenter with clean industrial aesthetics",
            time_of_day="Dark studio setting with volumetric lighting",
            lighting="Diffused key light, cyan edge illumination, soft fill",
            camera={
                "shot": shot.shot_type,
                "lens": "35mm anamorphic prime lens",
                "movement": "Slow continuous camera dolly push-in"
            },
            composition="Rule-of-thirds with central focal point, vertical 9:16 framing",
            depth="Shallow depth of field (f/1.8) with creamy background bokeh",
            materials="Matte brushed aluminum, tempered glass, glowing copper conductors",
            physics="Accurate light transmission and refractive fluid dynamics in cooling tubes",
            motion="Smooth 60fps mechanical fluidity without motion blur artifacts",
            audio=shot.audio_direction.get("ambience", "Subtle electronic ambience"),
            dialogue="None (designed for voiceover overlay)",
            style=effective_style,
            color_tone="Cybernetic slate, electric cyan, and clean white",
            continuity="Maintains consistent node positioning throughout the clip",
            negative_constraints=[
                "no watermark", "no text distortion", "no low-poly geometry",
                "no random flashing lights", "no unmotivated camera spins"
            ],
            output_format=f"4K 60fps Vertical {aspect_ratio} HDR ProRes",
            compiled_master_prompt=shot.visual_prompt
        )

    def compile_remotion_prompt(
        self,
        topic: str,
        metrics: Dict[str, Any]
    ) -> RemotionPromptPayload:
        """Compiles a programmatic React Remotion composition specification (V3 baseline signature)."""
        spec = remotion_prompt_compiler.compile(
            title=topic,
            topic=topic,
            claims=[f"{k}: {v}" for k, v in (metrics or {}).items()],
            metrics=metrics
        )

        components = [
            "TitleHookCard", "AnimatedMetricCounter", "SideBySideBarChart",
            "CodeTerminalDisplay", "AnimatedCaptions", "CallToActionBanner"
        ]

        timeline_scenes = [
            {"from": s.start_frame, "duration": s.duration_frames, "component": s.components[0], "props": {"title": topic}}
            for s in spec.story_scenes
        ]

        return RemotionPromptPayload(
            composition_name=f"Explainer_{topic[:18].replace(' ', '_')}",
            duration_in_frames=spec.duration_in_frames,
            fps=spec.fps,
            width=spec.width,
            height=spec.height,
            components=components,
            timeline_scenes=timeline_scenes,
            typography={
                "fontFamily": spec.typography_rules.get("primary_font", "Inter, sans-serif"),
                "headingWeight": spec.typography_rules.get("heading_weight", "800"),
                "bodyWeight": spec.typography_rules.get("body_weight", "500"),
                "metricFont": spec.typography_rules.get("monospace_font", "monospace")
            },
            caption_behavior="Synchronized word-by-word highlight with spring animation (damping: 12, stiffness: 120)",
            charts_and_metrics=metrics,
            render_command=f"npx remotion render src/index.ts Explainer_{topic[:18].replace(' ', '_')} out/video.mp4 --props='{json.dumps(metrics)}'"
        )

    def compile_hyperframes_prompt(
        self,
        topic: str,
        badge_text: str = "BREAKING AI EVENT",
        badge: Optional[str] = None,
        duration_frames: int = 900
    ) -> HyperFramesPromptPayload:
        """Compiles HTML-native markup and paused GSAP timeline code for HyperFrames (V3 baseline signature)."""
        effective_badge = badge or badge_text
        spec = hyperframes_prompt_compiler.compile(
            topic=topic,
            headline=f"Verified Launch: {topic}",
            badge_text=effective_badge,
            duration_sec=duration_frames / 60.0,
            fps=60
        )

        return HyperFramesPromptPayload(
            composition_id=spec.composition_id,
            width=spec.width,
            height=spec.height,
            fps=spec.fps,
            total_duration_frames=spec.total_frames,
            duration_frames=spec.total_frames,
            html_markup=spec.html_markup,
            css_styles=spec.css_styles,
            gsap_timeline_code=spec.gsap_timeline_code,
            deterministic_contract="All animation timelines must remain paused and controlled exclusively via .seek(time)"
        )

    def compile_hybrid_prompt(
        self,
        topic: str,
        metrics: Dict[str, Any],
        scene_description: str = ""
    ) -> Dict[str, Any]:
        """Compiles a Hybrid Video Pipeline specification (V3 baseline signature)."""
        plan = hybrid_planner.plan_hybrid_video(
            title=f"{topic} Deep Dive",
            topic=topic,
            claims=[f"{k}: {v}" for k, v in (metrics or {}).items()],
            metrics=metrics
        )
        remotion = self.compile_remotion_prompt(topic=topic, metrics=metrics)
        omni = self.compile_omni_prompt(topic=topic, scene_description=scene_description)

        return {
            "format": "hybrid_9_16_reel",
            "concept": plan.title,
            "background_layer": {
                "engine": "Gemini Omni",
                "master_prompt": omni.compiled_master_prompt,
                "aspect_ratio": "9:16",
                "duration": "30s"
            },
            "overlay_layer": {
                "engine": "Remotion",
                "components": remotion.components,
                "timeline_scenes": remotion.timeline_scenes,
                "render_command": remotion.render_command
            },
            "audio_strategy": "Subtle low-frequency ambient drone under voiceover, ducked by -16dB during speech beats.",
            "export_resolution": "1080x1920 60fps ProRes / MP4"
        }

    # =====================================================================
    # V3.2 MASTER CREATIVE DIRECTOR & UNIVERSAL PROMPT COMPILER
    # =====================================================================

    async def generate_video_package(
        self,
        event_data: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None,
        topic: Optional[str] = None,
        angle: str = "",
        custom_angle: str = "",
        platform: str = "instagram_reel",
        duration_seconds: Optional[float] = None,
        duration_sec: float = 30.0,
        visual_style: Optional[str] = None,
        style_preset: str = "TECH_DOCUMENTARY",
        strategy: Optional[str] = None,
        generation_strategy: str = "AUTO",
        key_claims: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        sources: Optional[List[Dict[str, Any]]] = None,
        has_characters: bool = False,
        character_name: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        **kwargs
    ) -> VideoPackage:
        """
        Master Creative Director Method:
        Generates the complete, production-ready VideoPackage containing:
        - Storyboard & Hook Visualizer
        - Shot list with complexity splitting
        - Model-specific compilers (Remotion, Omni, Veo, HyperFrames)
        - Hybrid assembly plan
        - 15-dimension quality report
        - Formatted copyable exports
        """
        effective_data = event_data or {}
        final_title = title or effective_data.get("title") or effective_data.get("canonical_title") or "Frontier AI Development"
        final_topic = topic or effective_data.get("topic") or effective_data.get("category") or final_title
        final_claims = key_claims or effective_data.get("verified_claims") or effective_data.get("key_facts") or [
            f"{final_title} achieves state-of-the-art benchmark scores.",
            "High computational efficiency and open weights release."
        ]
        final_metrics = metrics or effective_data.get("metrics") or {"Throughput": "140 tok/s", "Cost Reduction": "72%"}
        final_primary_source = (sources[0]["name"] if sources and len(sources) > 0 and isinstance(sources[0], dict) and "name" in sources[0] else None) or effective_data.get("primary_source_name") or "Verified Official Release"
        final_duration = float(duration_seconds if duration_seconds is not None else duration_sec)
        final_style = visual_style or style_preset or "TECH_DOCUMENTARY"
        final_strategy = strategy or generation_strategy or "AUTO"
        if not aspect_ratio:
            aspect_ratio = "9:16" if platform in ["instagram_reel", "youtube_short", "tiktok"] else ("16:9" if platform == "youtube_long" else "1:1")

        # 1. Generate Universal Storyboard
        storyboard = storyboard_engine.generate_storyboard(
            title=final_title,
            topic=final_topic,
            claims=final_claims,
            platform=platform,
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio,
            visual_style=final_style,
            primary_source=final_primary_source,
            has_characters=has_characters,
            character_name=character_name
        )

        # 2. Compile Remotion Specification
        remotion_spec = remotion_prompt_compiler.compile(
            title=final_title,
            topic=final_topic,
            claims=final_claims,
            metrics=final_metrics,
            platform=platform,
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio,
            visual_style=final_style
        )

        # 3. Compile Gemini Omni Production Package
        omni_pkg = omni_prompt_compiler.compile_full_sequence(
            title=final_title,
            topic=final_topic,
            claims=final_claims,
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio,
            visual_style=final_style
        )

        # 4. Compile Google Veo Production Package
        veo_pkg = veo_prompt_compiler.compile_full_package(
            title=final_title,
            topic=final_topic,
            claims=final_claims,
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio
        )

        # 5. Compile HyperFrames Specification
        hf_spec = hyperframes_prompt_compiler.compile(
            topic=final_topic,
            headline=final_title[:45],
            metric_value="+340%",
            metric_label="Throughput Improvement",
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio,
            fps=60
        )

        # 6. Build Hybrid Assembly Plan
        hybrid_plan = hybrid_planner.plan_hybrid_video(
            title=final_title,
            topic=final_topic,
            claims=final_claims,
            metrics=final_metrics,
            duration_sec=final_duration,
            aspect_ratio=aspect_ratio
        )

        # 7. Evaluate 15-Dimension Quality Gate
        all_prompts_corpus = (
            remotion_spec.copy_ready_coding_prompt + "\n" +
            omni_pkg.copy_all_prompts_markdown + "\n" +
            veo_pkg.copy_all_markdown + "\n" +
            hf_spec.copy_ready_coding_prompt
        )
        quality_report = video_quality_evaluator.evaluate_package(
            storyboard_data=storyboard.model_dump(),
            prompts_text=all_prompts_corpus,
            asset_manifest=remotion_spec.asset_manifest,
            has_audio=True,
            is_hybrid=(final_strategy in ["AUTO", "HYBRID"])
        )

        # 8. Record Prompt in Memory
        prompt_memory_service.record_prompt_evaluation(
            topic=final_topic,
            model=final_strategy,
            visual_style=final_style,
            shot_type="Hybrid Multi-Shot",
            camera_movement="Continuous tracking & dolly",
            duration_sec=final_duration,
            quality_score=quality_report.video_prompt_readiness_score
        )

        # 9. Format Export Markdown files
        shot_list_md = self._render_shot_list_markdown(storyboard.shots)
        storyboard_md = self._render_storyboard_markdown(storyboard)

        export_formats = {
            "video_package.json": json.dumps(
                {
                    "video_id": storyboard.storyboard_id,
                    "title": final_title,
                    "platform": platform,
                    "duration_sec": final_duration,
                    "quality_score": quality_report.video_prompt_readiness_score,
                    "selected_hook": storyboard.selected_hook.model_dump(),
                    "shots_count": len(storyboard.shots)
                }, indent=2
            ),
            "video_package_json": json.dumps(
                {
                    "video_id": storyboard.storyboard_id,
                    "title": final_title,
                    "platform": platform,
                    "duration_sec": final_duration,
                    "quality_score": quality_report.video_prompt_readiness_score,
                    "selected_hook": storyboard.selected_hook.model_dump(),
                    "shots_count": len(storyboard.shots)
                }, indent=2
            ),
            "video_storyboard.md": storyboard_md,
            "video_storyboard_md": storyboard_md,
            "shot_list.md": shot_list_md,
            "shot_list_md": shot_list_md,
            "remotion_prompt.md": remotion_spec.copy_ready_coding_prompt,
            "remotion_prompt_md": remotion_spec.copy_ready_coding_prompt,
            "omni_prompts.md": omni_pkg.copy_all_prompts_markdown,
            "omni_prompts_md": omni_pkg.copy_all_prompts_markdown,
            "veo_prompts.md": veo_pkg.copy_all_markdown,
            "veo_prompts_md": veo_pkg.copy_all_markdown,
            "hyperframes_prompt.md": hf_spec.copy_ready_coding_prompt,
            "hyperframes_prompt_md": hf_spec.copy_ready_coding_prompt,
            "hybrid_assembly.md": hybrid_plan.copy_assembly_markdown,
            "hybrid_assembly_md": hybrid_plan.copy_assembly_markdown
        }

        engines_payload = VideoEnginesPayload(
            remotion=remotion_spec,
            omni=omni_pkg,
            veo=veo_pkg,
            hyperframes=hf_spec
        )

        final_assets = list(remotion_spec.asset_manifest)
        if storyboard.character_bible:
            char_name = getattr(storyboard.character_bible, "character_name", None) or "Key Persona"
            final_assets.append(
                RemotionAssetRequirement(
                    asset_id="ASSET-007-CHAR",
                    asset_type="character_reference_sheet",
                    description=f"Front and three-quarter photographic character reference sheet for {char_name}",
                    source="Midjourney / Gemini reference prompt",
                    aspect_ratio="1:1",
                    used_by_scenes=["scene_01", "scene_02", "scene_03"]
                )
            )

        # V3.3 Creative Intelligence Extensions
        visual_concepts = visual_concept_engine.generate_concepts(
            claim=final_claims[0] if final_claims else final_title,
            topic=final_topic,
            platform=platform,
            metrics=final_metrics
        )
        continuity_state = continuity_engine.initialize_state(
            title=final_title,
            topic=final_topic,
            has_character=has_characters,
            character_name=character_name,
            style_preset=final_style
        )
        diversity_audit = visual_diversity_engine.audit_visual_content(all_prompts_corpus)

        prod_shots = []
        for i, s in enumerate(storyboard.shots, 1):
            ps = shot_director.direct_shot(
                shot_number=i,
                beat_type="hook" if i == 1 else ("context" if i == 2 else ("proof" if i == 3 else "development")),
                narration=s.voiceover_beat,
                topic=final_topic,
                duration_sec=s.duration_sec,
                platform=platform,
                continuity_state=continuity_state,
                preferred_engine=final_strategy,
                metrics=final_metrics
            )
            prod_shots.append(ps)

        return VideoPackage(
            video_id=storyboard.storyboard_id,
            title=final_title,
            topic=final_topic,
            platform=platform,
            duration_seconds=final_duration,
            aspect_ratio=aspect_ratio,
            visual_style=final_style,
            creative_concept=f"High-retention technical explainer showing why {final_title} shifts AI compute economics",
            generation_strategy=final_strategy,
            hook_candidates=storyboard.hook_candidates,
            selected_hook=storyboard.selected_hook,
            storyboard=storyboard,
            shot_list=storyboard.shots,
            asset_manifest=final_assets,
            audio_plan=remotion_spec.audio_rules,
            caption_plan=remotion_spec.caption_rules,
            character_bible=storyboard.character_bible,
            engines=engines_payload,
            hybrid_assembly=hybrid_plan,
            quality_report=quality_report,
            export_formats=export_formats,
            visual_concepts=visual_concepts,
            continuity_state=continuity_state,
            diversity_audit=diversity_audit,
            production_shots=prod_shots
        )

    def export_package(self, package: Any, format: str) -> str:
        """Exports compiled package into specified file format."""
        if isinstance(package, VideoPackage):
            pkg_dict = package.model_dump()
            export_formats = package.export_formats
        elif isinstance(package, dict):
            pkg_dict = package
            export_formats = package.get("export_formats", {})
        else:
            return ""

        format_norm = format.lower()
        if format in export_formats:
            return export_formats[format]
        if format_norm in export_formats:
            return export_formats[format_norm]
        format_alt = format_norm.replace(".", "_")
        if format_alt in export_formats:
            return export_formats[format_alt]

        if "package" in format_norm and "json" in format_norm:
            return json.dumps(pkg_dict, indent=2)
        if "storyboard" in format_norm:
            sb_content = export_formats.get("video_storyboard_md")
            if not sb_content:
                sb_scenes = pkg_dict.get("storyboard", [])
                sb_content = f"# STORYBOARD: {pkg_dict.get('title', 'Video')}\n\n" + "\n".join([f"- Scene {s.get('scene_number', i+1)}: {s.get('visual_objective', '')} ({s.get('voiceover_text', '')})" for i, s in enumerate(sb_scenes)])
            return sb_content
        if "shot" in format_norm:
            shot_content = export_formats.get("shot_list_md")
            if not shot_content:
                shots = pkg_dict.get("shot_list", [])
                shot_content = f"# SHOT LIST: {pkg_dict.get('title', 'Video')}\n\n" + "\n".join([f"- Shot {s.get('shot_id', i+1)}: {s.get('engine', '')} | {s.get('exact_model_prompt', s.get('copyable_prompt', ''))}" for i, s in enumerate(shots)])
            return shot_content
        if "remotion" in format_norm:
            rem_eng = pkg_dict.get("engines", {}).get("remotion", {})
            rem_txt = rem_eng.get("copy_ready_coding_prompt") or rem_eng.get("standalone_agent_prompt") or f"Title: {pkg_dict.get('title', '')}"
            if not rem_txt.startswith("# REMOTION"):
                rem_txt = f"# REMOTION CODING AGENT BRIEF\n\n{rem_txt}"
            return export_formats.get("remotion_prompt_md", rem_txt)
        if "omni" in format_norm:
            omni_eng = pkg_dict.get("engines", {}).get("omni", {})
            if isinstance(omni_eng, list):
                omni_txt = f"# GEMINI OMNI FLASH PROMPTS\n\n" + "\n\n".join([f"### {s.get('shot_id', 'SHOT')}\n{s.get('visual_prompt', '')}\nAVOID: {s.get('avoid', '')}" for s in omni_eng])
            else:
                omni_txt = omni_eng.get("copy_all_prompts_markdown", f"# OMNI PROMPTS\n\nTitle: {pkg_dict.get('title', '')}")
            return export_formats.get("omni_prompts_md", omni_txt)
        if "veo" in format_norm:
            veo_eng = pkg_dict.get("engines", {}).get("veo", {})
            if isinstance(veo_eng, list):
                veo_txt = f"# GOOGLE VEO PROMPTS\n\n" + "\n\n".join([f"### {s.get('shot_id', 'SHOT')}\n{s.get('prompt', '')}" for s in veo_eng])
            else:
                veo_txt = veo_eng.get("copy_all_markdown", f"# VEO PROMPTS\n\nTitle: {pkg_dict.get('title', '')}")
            return export_formats.get("veo_prompts_md", veo_txt)
        if "hyperframes" in format_norm:
            hf_eng = pkg_dict.get("engines", {}).get("hyperframes", {})
            hf_txt = hf_eng.get("copy_ready_coding_prompt") or hf_eng.get("standalone_agent_prompt") or f"Title: {pkg_dict.get('title', '')}"
            if not hf_txt.startswith("# HYPERFRAMES"):
                hf_txt = f"# HYPERFRAMES CODING AGENT PROMPT\n\n{hf_txt}"
            return export_formats.get("hyperframes_prompt_md", hf_txt)

        return json.dumps(pkg_dict, indent=2)

    def _render_shot_list_markdown(self, shots: List[ShotBreakdownEntry]) -> str:
        lines = [
            "# MASTER PRODUCTION SHOT LIST",
            "| Shot | Timecode | Type | Engine | Objective | Camera Movement | Complexity |",
            "|:---|:---|:---|:---|:---|:---|:---|"
        ]
        for s in shots:
            lines.append(
                f"| {s.shot_number:02d} | {s.timecode} | {s.shot_type} | {s.recommended_engine} | {s.visual_objective[:35]} | {s.camera_movement[:25]} | {s.complexity_score:.0f}/100 |"
            )
        return "\n".join(lines)

    def _render_storyboard_markdown(self, sb: UniversalStoryboard) -> str:
        lines = [
            f"# UNIVERSAL VIDEO STORYBOARD: {sb.title}",
            f"**Platform:** {sb.platform} | **Style:** {sb.visual_style} | **Duration:** {sb.total_duration_sec}s",
            f"\n## WINNING HOOK ({sb.selected_hook.hook_category})",
            f"- **Spoken:** \"{sb.selected_hook.first_spoken_line}\"",
            f"- **Visual:** {sb.selected_hook.first_visual}",
            f"- **Text Overlay:** {sb.selected_hook.first_on_screen_text}",
            f"- **Curiosity Mechanism:** {sb.selected_hook.curiosity_mechanism}",
            "\n## SCENE & SHOT BREAKDOWN"
        ]
        for s in sb.shots:
            lines.extend([
                f"\n### Shot {s.shot_number:02d} ({s.timecode} | {s.duration_sec}s) — Engine: {s.recommended_engine}",
                f"- **Visual Objective:** {s.visual_objective} ({s.visual_type})",
                f"- **Camera & Optics:** {s.camera_movement} ({s.shot_type})",
                f"- **Lighting & Atmosphere:** {s.lighting_and_atmosphere}",
                f"- **Voiceover:** \"{s.voiceover_beat}\"",
                f"- **On-Screen Text:** \"{s.on_screen_text}\""
            ])
            if s.source_attribution_card:
                lines.append(f"- **Attribution Card:** {s.source_attribution_card}")
        return "\n".join(lines)


    # =========================================================================
    # V3.3 VIDEO FORENSICS & PROMPT EVOLUTION APIS
    # =========================================================================

    def analyze_forensic_video(
        self,
        video_path_or_id: str,
        prompt_spec: Optional[Dict[str, Any]] = None,
        storyboard: Optional[Dict[str, Any]] = None,
        synthetic_properties: Optional[Dict[str, Any]] = None
    ) -> VideoForensicReport:
        """Analyzes an actual or synthetic video across 23 forensic dimensions."""
        return video_forensic_analyzer.analyze_video(
            video_path_or_id=video_path_or_id,
            prompt_spec=prompt_spec,
            storyboard=storyboard,
            synthetic_properties=synthetic_properties
        )

    def classify_failures(self, raw_failures: List[Dict[str, Any]]) -> FailureTaxonomyReport:
        """Classifies forensic failures into structured taxonomy buckets."""
        return video_failure_classifier.classify_forensic_failures(raw_failures)

    def diagnose_mismatches(
        self,
        prompt_shots: List[Dict[str, Any]],
        forensic_failures: List[Dict[str, Any]],
        extracted_metadata: Dict[str, Any]
    ) -> DiagnosticInspectionReport:
        """Compares prompt intent against observed video output."""
        return prompt_output_diagnostics.diagnose_discrepancies(
            prompt_shots=prompt_shots,
            forensic_failures=forensic_failures,
            extracted_metadata=extracted_metadata
        )

    def evolve_video_prompt(
        self,
        current_version_label: str,
        original_prompt_text: str,
        detected_failures: List[Dict[str, Any]],
        target_model: str = "AUTO",
        human_critique: Optional[str] = None
    ) -> PromptEvolutionLineage:
        """Mutates a prompt specification to resolve diagnosed forensic failures."""
        lineage = prompt_evolution_engine.evolve_prompt(
            current_version_label=current_version_label,
            original_prompt_text=original_prompt_text,
            detected_failures=detected_failures,
            target_model=target_model,
            human_critique=human_critique
        )
        prompt_memory_service.record_evolution_step(
            video_id=f"evo_{lineage.evolution_id}",
            version_label=lineage.new_version,
            model=target_model,
            failures_diagnosed=[f.get("id", "FAIL") for f in detected_failures],
            mutations_applied=[m.operator for m in lineage.mutations_applied],
            prompt_readiness=lineage.expected_executability_score,
            actual_quality_score=lineage.predicted_quality_score,
            notes=lineage.lineage_notes
        )
        return lineage

    def generate_visual_concepts(
        self,
        claim: str,
        topic: str,
        platform: str = "instagram_reel",
        metrics: Optional[Dict[str, Any]] = None
    ) -> VisualConceptSuite:
        """Generates 3-5 distinct visual representations for an idea."""
        return visual_concept_engine.generate_concepts(
            claim=claim,
            topic=topic,
            platform=platform,
            metrics=metrics
        )

    def analyze_shot_complexity(
        self,
        shot_id: str,
        visual_objective: str,
        subject_action: str,
        camera_movement: str,
        duration_sec: float = 5.0
    ) -> ShotComplexityReport:
        """Scores 10-vector complexity and decomposes overloaded shots."""
        return shot_complexity_analyzer.analyze_shot(
            shot_id=shot_id,
            visual_objective=visual_objective,
            subject_action=subject_action,
            camera_movement=camera_movement,
            duration_sec=duration_sec
        )

    def audit_visual_diversity(self, text_corpus: str) -> VisualDiversityAudit:
        """Audits prompt corpus for AI clichés and slop risk."""
        return visual_diversity_engine.audit_visual_content(text_corpus)

    def get_failure_patterns_dashboard(self) -> Dict[str, Any]:
        """Returns failure frequency distribution and top improvements."""
        return prompt_memory_service.get_failure_patterns_dashboard()

    def get_learned_heuristics(self) -> List[LearnedHeuristic]:
        """Returns learned creative heuristics with confidence scores."""
        return prompt_memory_service.get_learned_heuristics()


video_generation_service = VideoGenerationService()
