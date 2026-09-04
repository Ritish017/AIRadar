"""
Remotion Prompt Compiler:
Transforms verified intelligence and storyboards into an exhaustive, production-grade
implementation specification for an external AI coding agent or senior motion graphics engineer.
Enforces real Remotion primitives, exact physics parameters, safe zones, and anti-generic visual rules.
"""

import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RemotionElementAnimation(BaseModel):
    element_id: str
    start_frame: int
    end_frame: int
    initial_state: Dict[str, Any]
    final_state: Dict[str, Any]
    timing_type: str  # "spring" or "interpolate"
    spring_config: Optional[Dict[str, float]] = None  # damping, stiffness, mass
    interpolation_config: Optional[Dict[str, Any]] = None  # input_range, output_range, easing


class RemotionSceneSpec(BaseModel):
    scene_number: int
    name: str
    start_frame: int
    end_frame: int
    duration_frames: int
    narrative_purpose: str
    visual_objective: str
    voiceover_script: str
    on_screen_text: str
    components: List[str]
    animations: List[RemotionElementAnimation]
    transition_out: str
    transition_reason: str
    sfx_cues: List[Dict[str, Any]]


class RemotionAssetRequirement(BaseModel):
    asset_id: str
    asset_type: str  # svg_icon, generated_image, data_payload, screen_recording, sound_effect
    description: str
    source: str
    aspect_ratio: str
    used_by_scenes: List[str]


class RemotionSpecification(BaseModel):
    project_title: str
    purpose: str
    platform: str
    aspect_ratio: str
    width: int
    height: int
    fps: int
    duration_in_frames: int
    duration_sec: float
    visual_style: str
    target_audience: str
    tone: str
    creative_direction: Dict[str, str]
    story_scenes: List[RemotionSceneSpec]
    asset_manifest: List[RemotionAssetRequirement]
    typography_rules: Dict[str, Any]
    caption_rules: Dict[str, Any]
    audio_rules: Dict[str, Any]
    responsive_adaptations: Dict[str, Any]
    data_contract_ts: str
    copy_ready_coding_prompt: str

    @property
    def standalone_agent_prompt(self) -> str:
        return self.copy_ready_coding_prompt

    @property
    def video_props_interface(self) -> str:
        return self.data_contract_ts


class RemotionPromptCompiler:
    """
    Production-grade Remotion Prompt Compiler.
    Emits deep, unambiguous specifications for AI coding agents building Remotion videos.
    """

    def compile(
        self,
        title: str,
        topic: str,
        claims: List[str],
        metrics: Optional[Dict[str, Any]] = None,
        platform: str = "instagram_reel",
        duration_sec: float = 30.0,
        aspect_ratio: str = "9:16",
        visual_style: str = "TECH_DOCUMENTARY"
    ) -> RemotionSpecification:
        fps = 30
        total_frames = int(duration_sec * fps)
        width, height = (1080, 1920) if aspect_ratio == "9:16" else ((1920, 1080) if aspect_ratio == "16:9" else (1080, 1080))
        metrics = metrics or {"Speedup": "3.8x", "Cost Reduction": "72%", "Parameters": "671B"}

        # 1. Build Story Scenes & Element Animations
        scenes = self._generate_scene_specs(title, topic, claims, metrics, total_frames, fps)

        # 2. Build Asset Manifest
        assets = self._generate_asset_manifest(topic, metrics, aspect_ratio)

        # 3. Creative Direction
        creative_dir = {
            "viewer_emotion": "Empowered clarity, urgency without panic, technical mastery",
            "viewer_understanding": f"Understands exact architectural reasons why {topic} shifts the performance-cost curve",
            "visual_hierarchy": "1. Bold central data metric (high contrast) -> 2. Contextual label -> 3. Dynamic supporting chart -> 4. Bottom caption safe zone",
            "pacing": "Rapid 2-second hook beat followed by deliberate 4-6 second analytical segments and punchy conclusion",
            "visual_rhythm": "Anticipatory pause (6 frames) -> spring snap entrance -> gradual scale drift (0.2%/sec) -> crisp directional exit wipe",
            "branding": "Minimalist matte slate (#0f172a) base, high-contrast crisp white typography, single electric accent color (#38bdf8)"
        }

        # 4. Typography Rules
        typography = {
            "primary_font": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            "monospace_font": "'JetBrains Mono', 'Fira Code', monospace",
            "heading_weight": "800 (ExtraBold)",
            "body_weight": "500 (Medium)",
            "metric_weight": "900 (Black)",
            "tracking": "-0.02em for headings, +0.05em for uppercase labels",
            "line_height": "1.05 for titles, 1.35 for captions",
            "safe_zone": "Top 120px safe (avoid reels header), Bottom 260px safe (avoid Reels UI icons/caption overlay), Left/Right 72px safe"
        }

        # 5. Caption Rules
        captions = {
            "source": "Synchronized word-level voiceover timestamps",
            "word_grouping": "2 to 4 words per beat",
            "highlight_color": "#38bdf8",
            "inactive_color": "rgba(255, 255, 255, 0.4)",
            "box_background": "rgba(15, 23, 42, 0.75)",
            "border_radius": "16px",
            "position": f"bottom: {height * 0.18}px; left: 50%; transform: translateX(-50%);",
            "emphasis_animation": "spring scale(1.08) with zero blur"
        }

        # 6. Audio Rules
        audio = {
            "voiceover": {
                "pacing": "140 words per minute",
                "timings": [
                    {"scene": 1, "start": "0:00.00", "pause_at": "0:01.80"},
                    {"scene": 2, "start": "0:02.50", "pause_at": "0:06.50"},
                    {"scene": 3, "start": "0:07.00", "pause_at": "0:13.50"},
                    {"scene": 4, "start": "0:14.00", "pause_at": "0:22.00"},
                    {"scene": 5, "start": "0:22.50", "pause_at": "0:29.00"}
                ]
            },
            "music": {
                "genre": "Minimal Cinematic Electro-Acoustic / Tech Pulse",
                "bpm": "118 - 124 BPM",
                "role": "Continuous driving momentum without melodic distraction",
                "ducking": "Volume drops to -16dB under voiceover; swells to -6dB during visual metric drops"
            },
            "sfx": [
                {"time": "0:00.00", "event": "Low deep sub-boom (80Hz)", "intensity": "0.9"},
                {"time": "0:00.20", "event": "Sharp air riser / whoosh", "intensity": "0.6"},
                {"time": "0:02.40", "event": "Mechanical camera aperture click", "intensity": "0.5"},
                {"time": "0:07.10", "event": "Data chime / digital blip", "intensity": "0.7"},
                {"time": "0:14.00", "event": "Subtle terminal keypress clacks", "intensity": "0.4"},
                {"time": "0:22.50", "event": "Low kinetic transition swoosh", "intensity": "0.8"}
            ]
        }

        # 7. Responsive Adaptations
        responsive = {
            "aspect_9_16": "Vertical stacking. Metric sits directly above the chart. Labels use 32px-40px font. Safe zone avoids Reels buttons.",
            "aspect_16_9": "Side-by-side layout. Metric sits on left 40% of screen; animated React chart occupies right 60%. Full widescreen camera sweeps.",
            "aspect_1_1": "Square balanced composition. Centered metric with compact circular gauge or 3-bar vertical chart underneath."
        }

        # 8. Data Contract (TypeScript)
        data_contract = f"""export interface VideoProps {{
  title: string;
  topic: string;
  headline: string;
  benchmarkScore: string;
  metricComparison: Array<{{
    label: string;
    modelValue: number;
    baselineValue: number;
    unit: string;
  }}>;
  terminalCodeSnippet: string;
  primaryColor: string;
  accentColor: string;
  callToAction: string;
  voiceoverAudioUrl?: string;
  musicAudioUrl?: string;
}}"""

        # 9. Complete Standalone Prompt for External AI Coding Agent
        coding_prompt = self._build_coding_agent_prompt(
            title=title,
            topic=topic,
            aspect_ratio=aspect_ratio,
            width=width,
            height=height,
            fps=fps,
            total_frames=total_frames,
            scenes=scenes,
            creative_dir=creative_dir,
            typography=typography,
            captions=captions,
            audio=audio,
            assets=assets,
            data_contract=data_contract
        )

        return RemotionSpecification(
            project_title=f"{topic} - Remotion Production Suite",
            purpose=f"Synthesizes high-retention data and architectural explainers for {topic}",
            platform=platform,
            aspect_ratio=aspect_ratio,
            width=width,
            height=height,
            fps=fps,
            duration_in_frames=total_frames,
            duration_sec=duration_sec,
            visual_style=visual_style,
            target_audience="AI Engineers, Technical Founders, and Systems Architects",
            tone="Direct, authoritative, data-dense, visually sharp",
            creative_direction=creative_dir,
            story_scenes=scenes,
            asset_manifest=assets,
            typography_rules=typography,
            caption_rules=captions,
            audio_rules=audio,
            responsive_adaptations=responsive,
            data_contract_ts=data_contract,
            copy_ready_coding_prompt=coding_prompt
        )

    def _generate_scene_specs(
        self,
        title: str,
        topic: str,
        claims: List[str],
        metrics: Dict[str, Any],
        total_frames: int,
        fps: int
    ) -> List[RemotionSceneSpec]:
        c1 = claims[0] if claims else "Frontier open weights breakthrough"
        c2 = claims[1] if len(claims) > 1 else "Substantial compute efficiency leap"

        # Frame allocations for 5 scenes (30s = 900 frames)
        f_s1 = int(total_frames * 0.10)  # 0 to 90 (0s to 3s)
        f_s2 = int(total_frames * 0.20)  # 90 to 270 (3s to 9s)
        f_s3 = int(total_frames * 0.25)  # 270 to 495 (9s to 16.5s)
        f_s4 = int(total_frames * 0.25)  # 495 to 720 (16.5s to 24s)
        f_s5 = total_frames - (f_s1 + f_s2 + f_s3 + f_s4)  # 720 to 900 (24s to 30s)

        return [
            RemotionSceneSpec(
                scene_number=1,
                name="Hook & Value Drop",
                start_frame=0,
                end_frame=f_s1,
                duration_frames=f_s1,
                narrative_purpose="Stop the infinite scroll with concrete numerical disruption",
                visual_objective="Pop massive animated metric onto screen with physical spring recoil",
                voiceover_script="Your compute budget just got divided by four.",
                on_screen_text=f"-75% COMPUTE COST // {topic.upper()}",
                components=["TitleHookCard", "SpringHeadline", "AudioImpactBeep"],
                animations=[
                    RemotionElementAnimation(
                        element_id="headline_metric",
                        start_frame=0,
                        end_frame=18,
                        initial_state={"opacity": 0.0, "scale": 0.85, "translateY": 40},
                        final_state={"opacity": 1.0, "scale": 1.0, "translateY": 0},
                        timing_type="spring",
                        spring_config={"damping": 12.0, "stiffness": 180.0, "mass": 0.8}
                    ),
                    RemotionElementAnimation(
                        element_id="category_pill",
                        start_frame=6,
                        end_frame=24,
                        initial_state={"opacity": 0.0, "translateX": -20},
                        final_state={"opacity": 1.0, "translateX": 0},
                        timing_type="interpolate",
                        interpolation_config={"input_range": [6, 24], "output_range": [0, 1], "easing": "ease-out"}
                    )
                ],
                transition_out="hard_cut",
                transition_reason="Hard cut maintains urgent tempo from hook directly into the core event explanation",
                sfx_cues=[{"frame": 0, "sound": "sub_impact_80hz"}, {"frame": 6, "sound": "crisp_ui_click"}]
            ),
            RemotionSceneSpec(
                scene_number=2,
                name="The Core Breakthrough",
                start_frame=f_s1,
                end_frame=f_s1 + f_s2,
                duration_frames=f_s2,
                narrative_purpose="Introduce the verified event and key technical metric",
                visual_objective="Display animated counter ticking up from zero to verified benchmark score",
                voiceover_script=f"This is {title}. Verified across standard benchmarks, matching closed frontier performance.",
                on_screen_text=f"VERIFIED SOTA // {list(metrics.keys())[0] if metrics else 'ACCURACY'}",
                components=["AnimatedCounter", "VerificationBadge", "SourceCitationCard"],
                animations=[
                    RemotionElementAnimation(
                        element_id="benchmark_counter",
                        start_frame=f_s1 + 5,
                        end_frame=f_s1 + 45,
                        initial_state={"numeric_value": 0, "opacity": 0.0},
                        final_state={"numeric_value": 94.2, "opacity": 1.0},
                        timing_type="interpolate",
                        interpolation_config={"input_range": [f_s1 + 5, f_s1 + 45], "output_range": [0, 1], "easing": "ease-out"}
                    ),
                    RemotionElementAnimation(
                        element_id="verified_badge",
                        start_frame=f_s1 + 30,
                        end_frame=f_s1 + 50,
                        initial_state={"scale": 0.0, "opacity": 0.0},
                        final_state={"scale": 1.0, "opacity": 1.0},
                        timing_type="spring",
                        spring_config={"damping": 14.0, "stiffness": 140.0, "mass": 0.9}
                    )
                ],
                transition_out="push_wipe_left",
                transition_reason="Wipe signals horizontal progression into comparative evaluation",
                sfx_cues=[{"frame": f_s1 + 5, "sound": "data_counter_tick"}, {"frame": f_s1 + 30, "sound": "positive_ding"}]
            ),
            RemotionSceneSpec(
                scene_number=3,
                name="Comparative Benchmark Graph",
                start_frame=f_s1 + f_s2,
                end_frame=f_s1 + f_s2 + f_s3,
                duration_frames=f_s3,
                narrative_purpose="Provide visual proof via side-by-side metric comparison",
                visual_objective="Two animated bars grow from bottom, showing new model outperforming previous industry standard",
                voiceover_script=f"Notice the disparity: {c1}. Throughput nearly doubles while total memory footprint remains constant.",
                on_screen_text="COMPARATIVE PERFORMANCE LEAP",
                components=["SideBySideBarChart", "PercentageDeltaPill", "AxisLabels"],
                animations=[
                    RemotionElementAnimation(
                        element_id="bar_frontier",
                        start_frame=f_s1 + f_s2 + 10,
                        end_frame=f_s1 + f_s2 + 50,
                        initial_state={"height_pct": 0, "opacity": 0.0},
                        final_state={"height_pct": 94, "opacity": 1.0},
                        timing_type="spring",
                        spring_config={"damping": 15.0, "stiffness": 110.0, "mass": 1.0}
                    ),
                    RemotionElementAnimation(
                        element_id="delta_badge",
                        start_frame=f_s1 + f_s2 + 45,
                        end_frame=f_s1 + f_s2 + 65,
                        initial_state={"scale": 0.7, "opacity": 0.0},
                        final_state={"scale": 1.0, "opacity": 1.0},
                        timing_type="spring",
                        spring_config={"damping": 12.0, "stiffness": 160.0, "mass": 0.8}
                    )
                ],
                transition_out="fade_to_terminal",
                transition_reason="Smooth fade transitions from abstract graph into concrete code demonstration",
                sfx_cues=[{"frame": f_s1 + f_s2 + 10, "sound": "whoosh_bar_growth"}, {"frame": f_s1 + f_s2 + 45, "sound": "bell_accent"}]
            ),
            RemotionSceneSpec(
                scene_number=4,
                name="Developer Terminal & Architectural Truth",
                start_frame=f_s1 + f_s2 + f_s3,
                end_frame=f_s1 + f_s2 + f_s3 + f_s4,
                duration_frames=f_s4,
                narrative_purpose="Demonstrate concrete implementation and developer accessibility",
                visual_objective="Clean syntax-highlighted terminal typing out command with live execution indicator",
                voiceover_script=f"Under the hood: {c2}. Developers can deploy this directly without rewriting orchestration backends.",
                on_screen_text="NATIVE ACCELERATION // ZERO REWRITE",
                components=["TerminalWindow", "TypewriterCode", "ExecutionSpeedIndicator"],
                animations=[
                    RemotionElementAnimation(
                        element_id="terminal_window",
                        start_frame=f_s1 + f_s2 + f_s3 + 5,
                        end_frame=f_s1 + f_s2 + f_s3 + 25,
                        initial_state={"translateY": 30, "opacity": 0.0},
                        final_state={"translateY": 0, "opacity": 1.0},
                        timing_type="spring",
                        spring_config={"damping": 16.0, "stiffness": 130.0, "mass": 1.0}
                    ),
                    RemotionElementAnimation(
                        element_id="typewriter_text",
                        start_frame=f_s1 + f_s2 + f_s3 + 25,
                        end_frame=f_s1 + f_s2 + f_s3 + 75,
                        initial_state={"character_count": 0},
                        final_state={"character_count": 64},
                        timing_type="interpolate",
                        interpolation_config={"input_range": [f_s1 + f_s2 + f_s3 + 25, f_s1 + f_s2 + f_s3 + 75], "output_range": [0, 64], "easing": "linear"}
                    )
                ],
                transition_out="scale_down_exit",
                transition_reason="Scale down contracts focus toward final call to action card",
                sfx_cues=[{"frame": f_s1 + f_s2 + f_s3 + 25, "sound": "mechanical_keyboard_burst"}]
            ),
            RemotionSceneSpec(
                scene_number=5,
                name="Strategic Conclusion & Call to Action",
                start_frame=f_s1 + f_s2 + f_s3 + f_s4,
                end_frame=total_frames,
                duration_frames=f_s5,
                narrative_purpose="Leave clear tactical takeaway and prompt community engagement",
                visual_objective="Pulsating bookmark/share card with clear high-contrast directive",
                voiceover_script="Are you migrating your workloads or waiting for commercial API price cuts? Comment below.",
                on_screen_text="SAVE TO REVISIT // COMMENT 'BENCHMARK'",
                components=["ActionCard", "ShareIconBadge", "SourceAttributionFooter"],
                animations=[
                    RemotionElementAnimation(
                        element_id="cta_card",
                        start_frame=f_s1 + f_s2 + f_s3 + f_s4 + 5,
                        end_frame=f_s1 + f_s2 + f_s3 + f_s4 + 25,
                        initial_state={"scale": 0.9, "opacity": 0.0},
                        final_state={"scale": 1.0, "opacity": 1.0},
                        timing_type="spring",
                        spring_config={"damping": 12.0, "stiffness": 150.0, "mass": 0.8}
                    )
                ],
                transition_out="none_end_of_video",
                transition_reason="Holds on final frame for social loop playback",
                sfx_cues=[{"frame": f_s1 + f_s2 + f_s3 + f_s4 + 5, "sound": "warm_chime_outro"}]
            )
        ]

    def _generate_asset_manifest(
        self,
        topic: str,
        metrics: Dict[str, Any],
        aspect_ratio: str
    ) -> List[RemotionAssetRequirement]:
        return [
            RemotionAssetRequirement(
                asset_id="ASSET-001-ICON",
                asset_type="svg_icon",
                description="Verified Shield SVG icon representing empirical confirmation",
                source="bundled_svg_asset",
                aspect_ratio="1:1",
                used_by_scenes=["scene_02"]
            ),
            RemotionAssetRequirement(
                asset_id="ASSET-002-DATA",
                asset_type="data_payload",
                description=f"JSON benchmark comparison data for {topic}: {json.dumps(metrics)}",
                source="parameterized_props",
                aspect_ratio="n/a",
                used_by_scenes=["scene_02", "scene_03"]
            ),
            RemotionAssetRequirement(
                asset_id="ASSET-003-TERMINAL",
                asset_type="code_snippet",
                description="Bash deployment command showing Ollama / vLLM execution",
                source="code_string",
                aspect_ratio="n/a",
                used_by_scenes=["scene_04"]
            ),
            RemotionAssetRequirement(
                asset_id="ASSET-004-AUDIO",
                asset_type="sound_effects",
                description="Synthesized UI impacts, typing clacks, and frequency sweep chimes",
                source="staticFile('sfx/*.mp3')",
                aspect_ratio="n/a",
                used_by_scenes=["scene_01", "scene_02", "scene_03", "scene_04", "scene_05"]
            ),
            RemotionAssetRequirement(
                asset_id="ASSET-005-BROLL",
                asset_type="generated_footage",
                description=f"B-roll cinematic background footage illustrating {topic}",
                source="Gemini Omni / Veo 4K output",
                aspect_ratio=aspect_ratio,
                used_by_scenes=["scene_01", "scene_03"]
            ),
            RemotionAssetRequirement(
                asset_id="ASSET-006-DIAGRAM",
                asset_type="technical_diagram",
                description=f"Micro-architecture and dataflow diagram for {topic}",
                source="external_svg_or_hyperframes",
                aspect_ratio=aspect_ratio,
                used_by_scenes=["scene_03", "scene_04"]
            )
        ]

    def _build_coding_agent_prompt(
        self,
        title: str,
        topic: str,
        aspect_ratio: str,
        width: int,
        height: int,
        fps: int,
        total_frames: int,
        scenes: List[RemotionSceneSpec],
        creative_dir: Dict[str, str],
        typography: Dict[str, Any],
        captions: Dict[str, Any],
        audio: Dict[str, Any],
        assets: List[RemotionAssetRequirement],
        data_contract: str
    ) -> str:
        scenes_formatted = []
        for s in scenes:
            anim_lines = []
            for a in s.animations:
                if a.spring_config:
                    cfg_str = f"(damping: {a.spring_config.get('damping')}, stiffness: {a.spring_config.get('stiffness')}, mass: {a.spring_config.get('mass')})"
                else:
                    easing_val = a.interpolation_config.get('easing', 'ease-out') if a.interpolation_config else 'ease-out'
                    cfg_str = f"Interpolation easing: {easing_val}"
                anim_lines.append(
                    f"  * Element `{a.element_id}`: Start frame {a.start_frame}, End frame {a.end_frame}. "
                    f"Initial state: {a.initial_state} -> Final state: {a.final_state}. "
                    f"Timing: {a.timing_type.upper()} {cfg_str}"
                )
            anims_text = "\n".join(anim_lines)
            sfx_text = ", ".join([f"{c['sound']} at frame {c['frame']}" for c in s.sfx_cues])
            scenes_formatted.append(
                f"### SCENE {s.scene_number}: {s.name.upper()} (Frames {s.start_frame}–{s.end_frame} | Duration: {s.duration_frames / fps:.1f}s)\n"
                f"- **Narrative Purpose:** {s.narrative_purpose}\n"
                f"- **Visual Objective:** {s.visual_objective}\n"
                f"- **Voiceover Track:** \"{s.voiceover_script}\"\n"
                f"- **On-Screen Typography:** \"{s.on_screen_text}\"\n"
                f"- **Required React Components:** {', '.join(s.components)}\n"
                f"- **Exact Animation Specs:**\n{anims_text}\n"
                f"- **Exit Transition:** {s.transition_out} (Rationale: {s.transition_reason})\n"
                f"- **SFX Triggers:** {sfx_text}"
            )
        scenes_text = "\n\n".join(scenes_formatted)

        assets_text = "\n".join([
            f"- **{a.asset_id}** ({a.asset_type}): {a.description} [Used by: {', '.join(a.used_by_scenes)}]"
            for a in assets
        ])

        return f"""================================================================================
COPY THIS INTO A REMOTION CODING AGENT
================================================================================
You are an expert Remotion video engineer, creative technologist, and senior motion designer.
Your goal is to implement a pixel-perfect, deterministic, production-grade Remotion composition in React and TypeScript.

DO NOT build a generic AI video.
REJECT random floating shapes, meaningless neon gradients, excessive glassmorphism, or constant unmotivated zooming.
Every frame, animation curve, and typography choice must serve technical clarity and high-retention storytelling.

--------------------------------------------------------------------------------
1. COMPOSITION PARAMETERS
--------------------------------------------------------------------------------
- Composition Name: Explainer_{topic[:18].replace(' ', '_')}
- Aspect Ratio: {aspect_ratio} ({width}x{height})
- Frame Rate: {fps} FPS
- Duration: {total_frames} frames ({total_frames / fps:.1f} seconds)
- Primary Subject: {title}

--------------------------------------------------------------------------------
2. MANDATORY REMOTION PRIMITIVES & RULES
--------------------------------------------------------------------------------
- Use `useCurrentFrame()` for all frame-driven coordinate and opacity transforms.
- Use `useVideoConfig()` to access `fps`, `width`, `height`, and `durationInFrames`.
- Use `spring()` from 'remotion' for physically-motivated entrances. Never guess damping/stiffness; use the exact parameters specified below.
- Use `interpolate()` from 'remotion' with explicit `inputRange` and `outputRange` and `extrapolateRight: 'clamp'`.
- Use `<Sequence>` or `<Series>` to encapsulate scene boundaries.
- For external video or images, wrap with `<OffthreadVideo>` and `staticFile()` to ensure zero frame-dropping during headless renders.
- Provide parameterized props conforming to the `VideoProps` TypeScript contract below.
- Include a `calculateMetadata()` function exporting dynamic composition dimensions if props vary.

--------------------------------------------------------------------------------
3. DATA CONTRACT
--------------------------------------------------------------------------------
```typescript
{data_contract}
```

--------------------------------------------------------------------------------
4. CREATIVE DIRECTION & VISUAL HIERARCHY
--------------------------------------------------------------------------------
- Emotional Goal: {creative_dir['viewer_emotion']}
- Cognitive Takeaway: {creative_dir['viewer_understanding']}
- Visual Hierarchy: {creative_dir['visual_hierarchy']}
- Motion Rhythm: {creative_dir['visual_rhythm']}
- Color System: {creative_dir['branding']}

--------------------------------------------------------------------------------
5. TYPOGRAPHY & PLATFORM-SAFE ZONES
--------------------------------------------------------------------------------
- Primary Font: {typography['primary_font']}
- Code Font: {typography['monospace_font']}
- Hierarchy: Headings ({typography['heading_weight']}), Labels ({typography['body_weight']}), Numbers ({typography['metric_weight']})
- Safe Area Directive: {typography['safe_zone']}

--------------------------------------------------------------------------------
6. CAPTIONS & AUDIO TIMELINE
--------------------------------------------------------------------------------
- Caption Pacing: {captions['word_grouping']}
- Highlight Color: {captions['highlight_color']}
- Position: {captions['position']}
- Music Policy: {audio['music']['genre']} ({audio['music']['bpm']}). Duck volume to -16dB under voiceover.

--------------------------------------------------------------------------------
7. DETAILED SCENE-BY-SCENE SPECIFICATION
--------------------------------------------------------------------------------
{scenes_text}

--------------------------------------------------------------------------------
8. REQUIRED ASSETS
--------------------------------------------------------------------------------
{assets_text}

--------------------------------------------------------------------------------
9. PRODUCTION VERIFICATION CHECKLIST
--------------------------------------------------------------------------------
[ ] Video renders headlessly with `npx remotion render` with 0 dropped frames.
[ ] No text overflows the platform-safe boundaries.
[ ] All spring animations have damping >= 10 to prevent endless oscillation.
[ ] Audio ducking accurately drops background music during speech.
[ ] Component is fully typed with zero TypeScript `any` types.
================================================================================"""


remotion_prompt_compiler = RemotionPromptCompiler()
