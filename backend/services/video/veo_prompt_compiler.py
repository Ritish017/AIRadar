"""
Google Veo Prompt Compiler:
Implements Google's official Veo prompting principles:
Cinematography + Subject + Action + Context + Style/Ambience + Audio.
Includes specialized First/Last Frame workflows and Image-to-Video motion contracts.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class VeoFirstLastFrameWorkflow(BaseModel):
    workflow_id: str
    purpose: str
    duration_sec: float
    start_frame_image_prompt: str
    end_frame_image_prompt: str
    transition_motion_prompt: str
    immutable_elements: List[str]
    moving_elements: List[str]
    audio_direction: str


class VeoImageToVideoWorkflow(BaseModel):
    reference_image_description: str
    immutable_elements: List[str]
    moving_elements: List[str]
    camera_motion: str
    secondary_environmental_motion: str
    timing_progression: str
    compiled_motion_prompt: str


class VeoShotPrompt(BaseModel):
    shot_id: str
    timecode: str
    duration_sec: float
    purpose: str
    cinematography: str
    subject: str
    action: str
    context: str
    style_and_ambience: str
    audio: str
    compiled_veo_prompt: str
    first_last_frame_workflow: Optional[VeoFirstLastFrameWorkflow] = None
    image_to_video_workflow: Optional[VeoImageToVideoWorkflow] = None
    copyable_block: str

    @property
    def prompt(self) -> str:
        return self.compiled_veo_prompt

    @property
    def workflow_type(self) -> str:
        if self.first_last_frame_workflow:
            return "FIRST_LAST_FRAME"
        if self.image_to_video_workflow:
            return "IMAGE_TO_VIDEO"
        return "TEXT_TO_VIDEO"

    @property
    def start_frame_prompt(self) -> Optional[str]:
        return self.first_last_frame_workflow.start_frame_image_prompt if self.first_last_frame_workflow else None

    @property
    def end_frame_prompt(self) -> Optional[str]:
        return self.first_last_frame_workflow.end_frame_image_prompt if self.first_last_frame_workflow else None

    @property
    def motion_prompt(self) -> Optional[str]:
        return self.first_last_frame_workflow.transition_motion_prompt if self.first_last_frame_workflow else None


class VeoProductionPackage(BaseModel):
    project_title: str
    total_duration_sec: float
    aspect_ratio: str
    shots: List[VeoShotPrompt]
    copy_all_markdown: str

    def __len__(self) -> int:
        return len(self.shots)

    def __iter__(self):
        return iter(self.shots)

    def __getitem__(self, item):
        return self.shots[item]


class VeoPromptCompiler:
    """
    Production-grade Prompt Compiler for Google Veo.
    Translates event intelligence into the official 6-part Veo formula
    plus first/last frame and image-to-video motion control.
    """

    def compile_shot(
        self,
        shot_id: str,
        timecode: str,
        duration_sec: float,
        purpose: str,
        topic: str,
        action: str,
        cinematography: str,
        context: str,
        style: str = "Photorealistic documentary aesthetic, 35mm film grain, cinematic volumetric lighting",
        audio: str = "Delicate electronic frequency hum with deep low-end resonance",
        has_first_last_frame: bool = False,
        first_frame_desc: str = "",
        last_frame_desc: str = "",
        has_image_to_video: bool = False,
        reference_desc: str = ""
    ) -> VeoShotPrompt:
        # Standard Veo formula: Cinematography + Subject + Action + Context + Style + Audio
        compiled = (
            f"Cinematography: {cinematography}. "
            f"Subject: High-technology computing architecture representing {topic}. "
            f"Action: {action}. "
            f"Context: {context}. "
            f"Style & Ambience: {style}. "
            f"Audio: {audio}."
        )

        first_last_wf = None
        if has_first_last_frame:
            first_last_wf = VeoFirstLastFrameWorkflow(
                workflow_id=f"wf_{shot_id.lower()}",
                purpose=f"Smooth state transformation for {topic}",
                duration_sec=duration_sec,
                start_frame_image_prompt=(
                    f"Photorealistic 8k still: {first_frame_desc or 'Single dormant computing core, dark brushed titanium, subtle blue LED trace'}. "
                    f"Atmosphere: quiet, static, cold lighting."
                ),
                end_frame_image_prompt=(
                    f"Photorealistic 8k still: {last_frame_desc or 'The same computing core fully energized, intense cyan optical data paths glowing brightly'}. "
                    f"Atmosphere: active, heat shimmer, dynamic lighting."
                ),
                transition_motion_prompt=(
                    f"Smooth continuous transition from dormant state to fully energized state over {duration_sec}s. "
                    f"Camera executes a steady forward dolly toward the center of the core. "
                    f"Light channels ignite in outward sequence from center to perimeter. "
                    f"No sudden cuts, no random morphing artifacts, maintain exact geometric proportions of all mechanical components."
                ),
                immutable_elements=["Core chassis dimensions", "Camera trajectory vector", "Mounting bracket positions"],
                moving_elements=["Optical channel luminosity", "Subtle coolant fluid flow", "Heat shimmer refraction"],
                audio_direction=f"Rising electronic whine starting at 120Hz climbing smoothly to 2.4kHz over {duration_sec}s, ending in solid mechanical click."
            )

        i2v_wf = None
        if has_image_to_video:
            i2v_wf = VeoImageToVideoWorkflow(
                reference_image_description=reference_desc or f"Official screenshot of {topic} architecture diagram",
                immutable_elements=["Diagram layout geometry", "Axis labels", "Baseline data curve"],
                moving_elements=["Progress indicator bar", "Highlight glow along the winning curve", "Subtle ambient background drift"],
                camera_motion="Gentle 1.05x push-in toward the top-performing benchmark pillar",
                secondary_environmental_motion="Gentle dust particle drift caught in volumetric spotlight",
                timing_progression=f"0.0s-1.5s still hold, 1.5s-4.0s glow pulse advances, 4.0s-{duration_sec}s final steady state",
                compiled_motion_prompt=(
                    f"Animate the reference image: Maintain immutable chart geometry and typography exactly as shown. "
                    f"Camera performs slow 1.05x cinematic push-in. The winning performance curve illuminates with an electric cyan pulse "
                    f"traveling left to right over {duration_sec} seconds. Subtle dust particles drift in background lighting."
                )
            )

        copyable_text = (
            f"=== [VEO SHOT: {shot_id} | {timecode} | {duration_sec}s] ===\n"
            f"{compiled}\n"
        )
        if first_last_wf:
            copyable_text += (
                f"\n[VEO FIRST/LAST FRAME SPECIFICATION]\n"
                f"START FRAME: {first_last_wf.start_frame_image_prompt}\n"
                f"END FRAME: {first_last_wf.end_frame_image_prompt}\n"
                f"TRANSITION PROMPT: {first_last_wf.transition_motion_prompt}\n"
                f"IMMUTABLE: {', '.join(first_last_wf.immutable_elements)}\n"
                f"MOVING: {', '.join(first_last_wf.moving_elements)}\n"
            )
        if i2v_wf:
            copyable_text += (
                f"\n[VEO IMAGE-TO-VIDEO MOTION PROMPT]\n"
                f"{i2v_wf.compiled_motion_prompt}\n"
                f"IMMUTABLE ELEMENTS: {', '.join(i2v_wf.immutable_elements)}\n"
                f"MOVING ELEMENTS: {', '.join(i2v_wf.moving_elements)}\n"
            )

        return VeoShotPrompt(
            shot_id=shot_id,
            timecode=timecode,
            duration_sec=duration_sec,
            purpose=purpose,
            cinematography=cinematography,
            subject=f"Hardware architecture and deployment of {topic}",
            action=action,
            context=context,
            style_and_ambience=style,
            audio=audio,
            compiled_veo_prompt=compiled,
            first_last_frame_workflow=first_last_wf,
            image_to_video_workflow=i2v_wf,
            copyable_block=copyable_text
        )

    def compile_full_package(
        self,
        title: str,
        topic: str,
        claims: List[str],
        duration_sec: float = 30.0,
        aspect_ratio: str = "9:16"
    ) -> VeoProductionPackage:
        c1 = claims[0] if claims else "High-efficiency open reasoning model"
        c2 = claims[1] if len(claims) > 1 else "Hardware inference speedup"

        shots = [
            self.compile_shot(
                shot_id="VEO-SHOT-01",
                timecode="00:00 - 00:04",
                duration_sec=4.0,
                purpose="Opening hook establishing breakthrough speed",
                topic=topic,
                action="A transparent optical accelerator node powers up, glowing channels igniting from core to edge",
                cinematography="Medium close-up shot, 50mm prime lens, slow continuous push-in with shallow depth of field (f/1.4)",
                context="Advanced subterranean computing cleanroom, matte titanium chassis, cool volumetric lighting",
                style="Cinematic technology documentary, photorealistic glass and copper reflections, subtle natural lens flare",
                audio="Deep sub-bass impact transitioning into rising electric hum",
                has_first_last_frame=True,
                first_frame_desc=f"Dormant dark server rack with single soft standby light for {topic}",
                last_frame_desc=f"The same server rack blazing with active cyan data streams and cooling circulation"
            ),
            self.compile_shot(
                shot_id="VEO-SHOT-02",
                timecode="00:04 - 00:10",
                duration_sec=6.0,
                purpose="Visualizing the architectural breakthrough and inference speedup",
                topic=f"sparse routing engine for {c1}",
                action="Complex light pathways selectively pulse; inactive routes stay dark while active routes stream at 4x speed",
                cinematography="35mm wide lens, steady orbital tracking shot drifting 45 degrees around the processor core",
                context="High-vacuum chip chamber, micro-cooling channels refracting internal LEDs",
                style="Crisp scientific visualization aesthetic, ultra-clean edges, restrained industrial contrast",
                audio="High-frequency rhythmic data chirp synchronized with pulse bursts"
            ),
            self.compile_shot(
                shot_id="VEO-SHOT-03",
                timecode="00:10 - 00:18",
                duration_sec=8.0,
                purpose="Image-to-video animation of real benchmark evidence",
                topic=f"benchmark verification card for {title}",
                action="Verified performance metric card illuminates, highlighting 94% accuracy over previous 49% baseline",
                cinematography="Lock-off planar shot with slow 1.05x magnification push toward the benchmark title",
                context="Digital verification studio environment with diffused edge rim light",
                style="Sleek motion graphic and photo hybrid, crystal clear typography",
                audio="Confident mid-range chime followed by soft acoustic percussion beat",
                has_image_to_video=True,
                reference_desc=f"Official benchmark chart comparing {topic} vs industry frontier models"
            ),
            self.compile_shot(
                shot_id="VEO-SHOT-04",
                timecode="00:18 - 00:25",
                duration_sec=7.0,
                purpose="Real-world engineering impact and local execution",
                topic="developer workstation running local weights",
                action="Developer types single launch command, terminal immediately responds with 140 tokens per second stream",
                cinematography="Over-the-shoulder medium shot, 35mm lens, gentle handheld sway representing human presence",
                context="Developer studio at twilight, ambient desk light illuminating mechanical keyboard",
                style="Warm natural documentary realism, rich authentic shadow detail",
                audio="Satisfying mechanical keyboard clicks layered over ambient night atmosphere"
            ),
            self.compile_shot(
                shot_id="VEO-SHOT-05",
                timecode="00:25 - 00:30",
                duration_sec=5.0,
                purpose="Conclusion, takeaway and discussion trigger",
                topic=f"future of open-source deployment for {c2}",
                action="Hardware unit gently transitions to sustained monitoring state, glowing cyan logo stays sharp as frame fades",
                cinematography="Slow receding dolly shot drifting backward down the server aisle into soft vignette",
                context="Server vault vanishing into single-point perspective",
                style="Premium cinematic outro aesthetic with warm baseline illumination",
                audio="Warm low-frequency resolving chord, lingering ambient decay"
            )
        ]

        markdown = "\n\n".join([s.copyable_block for s in shots])

        return VeoProductionPackage(
            project_title=f"{topic} - Google Veo Cinematic Suite",
            total_duration_sec=duration_sec,
            aspect_ratio=aspect_ratio,
            shots=shots,
            copy_all_markdown=markdown
        )

    def compile_first_last_frame_shot(
        self,
        shot_id: str,
        purpose: str,
        start_frame_description: str,
        end_frame_description: str,
        motion_description: str,
        duration_sec: float = 4.0,
        aspect_ratio: str = "16:9"
    ) -> Any:
        fl_workflow = VeoFirstLastFrameWorkflow(
            workflow_id=f"fl_{shot_id.lower().replace('-', '_')}",
            purpose=purpose,
            duration_sec=duration_sec,
            start_frame_image_prompt=f"Cinematic photorealistic 8K keyframe: {start_frame_description}. Master studio lighting, 35mm anamorphic.",
            end_frame_image_prompt=f"Cinematic photorealistic 8K keyframe: {end_frame_description}. Master studio lighting, 35mm anamorphic.",
            transition_motion_prompt=f"Continuous camera transition: {motion_description}. Maintain strict physical geometry, zero intermediate hallucinations.",
            immutable_elements=["Environment color palette", "Primary focal geometry"],
            moving_elements=["Camera position", "Internal mechanism transformation"],
            audio_direction="Low cinematic bass drop transitioning into high-frequency metallic resonance"
        )
        prompt = (
            f"START FRAME PROMPT:\n{fl_workflow.start_frame_image_prompt}\n\n"
            f"END FRAME PROMPT:\n{fl_workflow.end_frame_image_prompt}\n\n"
            f"VIDEO TRANSITION PROMPT:\n{fl_workflow.transition_motion_prompt}"
        )
        from types import SimpleNamespace
        return SimpleNamespace(
            workflow_type="FIRST_LAST_FRAME",
            prompt=prompt,
            start_frame_prompt=fl_workflow.start_frame_image_prompt,
            end_frame_prompt=fl_workflow.end_frame_image_prompt,
            motion_prompt=fl_workflow.transition_motion_prompt
        )


veo_prompt_compiler = VeoPromptCompiler()
