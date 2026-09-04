"""
Gemini Omni Flash Prompt Compiler:
Generates shot-level, production-grade video synthesis prompts for Gemini Omni Flash.
Enforces high control density, observable physical actions, anamorphic lens optics,
continuity constraints, and strict failure mode avoidance.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class OmniShotPrompt(BaseModel):
    shot_id: str
    timecode: str
    duration_sec: float
    purpose: str
    inputs: Dict[str, Any]
    visual_prompt: str
    shot_type: str
    subject_details: str
    action_details: str
    environment_details: str
    camera_and_lens: str
    lighting_and_atmosphere: str
    color_palette: str
    audio_direction: Dict[str, str]
    continuity_requirements: List[str]
    avoid_constraints: List[str]
    copyable_prompt: str

    @property
    def avoid(self) -> str:
        return " | ".join(self.avoid_constraints)

    @property
    def continuity(self) -> str:
        return " | ".join(self.continuity_requirements)


class OmniProductionPackage(BaseModel):
    project_title: str
    total_duration_sec: float
    aspect_ratio: str
    resolution: str
    shots: List[OmniShotPrompt]
    global_continuity_bible: str
    copy_all_prompts_markdown: str

    def __len__(self) -> int:
        return len(self.shots)

    def __iter__(self):
        return iter(self.shots)

    def __getitem__(self, item):
        return self.shots[item]


class OmniPromptCompiler:
    """
    Compiler for Google Gemini Omni Flash.
    Produces shot-level, physically observable prompts with explicit cinematic direction.
    """

    def compile_shot(
        self,
        shot_id: str,
        timecode: str,
        duration_sec: float,
        purpose: str,
        topic: str,
        action: str,
        environment: str,
        camera_move: str,
        aspect_ratio: str = "9:16",
        style_preset: str = "Cinematic Technology Documentary",
        audio_cue: str = "Low atmospheric sub-bass drone with electronic resonance",
        continuity_note: str = "Consistent dark matte carbon datacenter aesthetic and cyan rim lighting"
    ) -> OmniShotPrompt:
        shot_type = "Medium-wide cinematic tracking shot" if "track" in camera_move.lower() else "Medium close-up with slow dolly push-in"
        camera_and_lens = "35mm anamorphic prime lens, aperture f/1.8, shallow depth of field, slow controlled dolly push-in"
        lighting = "3200K key light, subtle cyan edge separation lighting, volumetric studio haze with restrained contrast"
        color = "Deep charcoal (#0f172a), electric cyan (#06b6d4), and surgical white accents"

        visual_prompt = (
            f"{shot_type} of {topic} in a {environment}. "
            f"Action: {action}. "
            f"Camera & Lens: {camera_and_lens}, executing a {camera_move}. "
            f"Lighting: {lighting}. "
            f"Atmosphere & Color: {color}, cinematic documentary realism, physically plausible reflections on matte aluminum and glass. "
            f"Framing: Vertical {aspect_ratio}, rule-of-thirds composition, central subject remains in sharp focal plane while background softly blurs."
        )

        avoid_constraints = [
            "no floating text or holographic letters in empty air",
            "no random unmotivated camera shakes or handheld jitter",
            "no CGI cartoon plasticity or oversaturated neon glow",
            "no distorted human faces or extra morphing fingers",
            "no watermark, logo artifact, or low-resolution textures"
        ]

        continuity = [
            continuity_note,
            "Maintain exact architectural node scale and spatial orientation",
            "Preserve identical lighting color temperature across surrounding shots"
        ]

        audio_dir = {
            "ambience": audio_cue,
            "dialogue": "None (allocated for clean voiceover mix)",
            "sfx": "Subtle mechanical activation click transitioning into fluid coolant circulation"
        }

        copyable = (
            f"--- [SHOT: {shot_id} | TIMECODE: {timecode} | DURATION: {duration_sec}s] ---\n"
            f"PROMPT:\n{visual_prompt}\n\n"
            f"AUDIO:\nAmbience: {audio_dir['ambience']} | SFX: {audio_dir['sfx']}\n\n"
            f"CONTINUITY:\n- " + "\n- ".join(continuity) + "\n\n"
            f"AVOID:\n- " + ", ".join(avoid_constraints)
        )

        return OmniShotPrompt(
            shot_id=shot_id,
            timecode=timecode,
            duration_sec=duration_sec,
            purpose=purpose,
            inputs={
                "text_prompt": True,
                "reference_image": "Optional architectural wireframe",
                "aspect_ratio": aspect_ratio
            },
            visual_prompt=visual_prompt,
            shot_type=shot_type,
            subject_details=f"Core architectural node for {topic}",
            action_details=action,
            environment_details=environment,
            camera_and_lens=camera_and_lens,
            lighting_and_atmosphere=lighting,
            color_palette=color,
            audio_direction=audio_dir,
            continuity_requirements=continuity,
            avoid_constraints=avoid_constraints,
            copyable_prompt=copyable
        )

    def compile_full_sequence(
        self,
        title: str,
        topic: str,
        claims: List[str],
        duration_sec: float = 30.0,
        aspect_ratio: str = "9:16",
        visual_style: str = "TECH_DOCUMENTARY"
    ) -> OmniProductionPackage:
        c1 = claims[0] if claims else "High-efficiency open reasoning model"
        c2 = claims[1] if len(claims) > 1 else "Hardware inference speedup"

        shots = [
            self.compile_shot(
                shot_id="OMNI-SHOT-01",
                timecode="00:00 - 00:03",
                duration_sec=3.0,
                purpose="Establish massive scale and hook visual curiosity",
                topic=f"high-density computation cluster representing {topic}",
                action="Rapid data pulse propagates through rows of optical interconnects from dark idle to brilliant cyan luminescence",
                environment="Subterranean server laboratory with matte carbon rack enclosures and polished dark concrete floors",
                camera_move="Extreme slow continuous forward tracking shot on a slider",
                aspect_ratio=aspect_ratio,
                continuity_note="Baseline dark slate aesthetic with cyan illumination"
            ),
            self.compile_shot(
                shot_id="OMNI-SHOT-02",
                timecode="00:03 - 00:08",
                duration_sec=5.0,
                purpose="Focus on the primary hardware / model breakthrough",
                topic=f"macro semiconductor chip package running {title}",
                action="Transparent liquid cooling system activates, micro-fluidic coolant streams refract internal copper circuitry",
                environment="Cleanroom test bench, surgical precision tools resting softly blurred in background",
                camera_move="Controlled macro pan drifting 45 degrees across the silicon substrate",
                aspect_ratio=aspect_ratio,
                continuity_note="Maintains identical liquid cooling hue and surface reflection fidelity"
            ),
            self.compile_shot(
                shot_id="OMNI-SHOT-03",
                timecode="00:08 - 00:15",
                duration_sec=7.0,
                purpose="Visual explanation of architectural efficiency leap",
                topic=f"sparse mixture-of-experts routing pathways for {c1}",
                action="Only 8 out of 64 glowing neural interconnects fire simultaneously per data cycle, conserving massive power",
                environment="Abstract architectural chamber with dark non-reflective surfaces",
                camera_move="Slow 30-degree orbital rotation keeping the central processing node centered",
                aspect_ratio=aspect_ratio,
                continuity_note="Exact same node geometry and scale as Shot 01"
            ),
            self.compile_shot(
                shot_id="OMNI-SHOT-04",
                timecode="00:15 - 00:23",
                duration_sec=8.0,
                purpose="Human developer context and real-world deployment",
                topic="software engineer observing real-time model rollout on workstation",
                action="Engineer reviews real-time token throughput metrics; terminal displays clean continuous text stream without hesitation",
                environment="Modern minimalist engineering studio at dusk, floor-to-ceiling city window softly out of focus",
                camera_move="Over-the-shoulder medium shot with slow lateral push to right",
                aspect_ratio=aspect_ratio,
                continuity_note="Workspace monitor displays matching cyan telemetry interface"
            ),
            self.compile_shot(
                shot_id="OMNI-SHOT-05",
                timecode="00:23 - 00:30",
                duration_sec=7.0,
                purpose="Conclusion and forward-looking strategic takeaway",
                topic=f"monolithic server cluster transitioning to quiet steady-state operation for {c2}",
                action="Lighting softly dims to ambient standby mode, single glowing indicator light pulses with steady heartbeat rhythm",
                environment="Server vault corridor extending into clean one-point perspective vanishing line",
                camera_move="Slow deliberate pull-back shot receding along central aisle",
                aspect_ratio=aspect_ratio,
                continuity_note="Closes the loop back to Shot 01 datacenter environment"
            )
        ]

        markdown_all = "\n\n".join([s.copyable_prompt for s in shots])

        continuity_bible = (
            "GLOBAL CONTINUITY BIBLE:\n"
            "- Color Anchor: Charcoal Slate (#0f172a), Electric Cyan (#06b6d4), White Accent.\n"
            "- Lighting Profile: 3200K key light with 5600K cyan rim edge; low haze ratio.\n"
            "- Optics: Consistent 35mm / 50mm anamorphic prime lens simulation throughout all shots.\n"
            "- Character / Hardware: All hardware enclosures must share identical matte carbon texture and brushed aluminum bevels."
        )

        return OmniProductionPackage(
            project_title=f"{topic} - Gemini Omni Production Suite",
            total_duration_sec=duration_sec,
            aspect_ratio=aspect_ratio,
            resolution="4K ProRes 60fps HDR",
            shots=shots,
            global_continuity_bible=continuity_bible,
            copy_all_prompts_markdown=markdown_all
        )


omni_prompt_compiler = OmniPromptCompiler()
