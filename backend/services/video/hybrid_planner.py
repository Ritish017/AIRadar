"""
Hybrid Video Planner:
Coordinates multi-engine video production by decomposing scenes into explicit
visual layers and engine ownership (Omni for footage, Remotion for data/captions,
HyperFrames for technical DOM interfaces).
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HybridShotEntry(BaseModel):
    shot_number: int
    timecode: str
    duration_sec: float
    visual_objective: str
    primary_engine: str  # Gemini Omni, Remotion, HyperFrames
    asset_source: str
    layer_breakdown: Dict[str, str]  # background, overlay, text, audio
    transition_to_next: str


class HybridAssemblyPlan(BaseModel):
    plan_id: str
    title: str
    total_duration_sec: float
    aspect_ratio: str
    resolution: str
    shot_table: List[HybridShotEntry]
    layer_compositing_guide: Dict[str, str]
    audio_ducking_matrix: Dict[str, Any]
    external_assembly_instructions: str
    copy_assembly_markdown: str

    @property
    def layer_order(self) -> List[str]:
        return [f"{k}: {v}" for k, v in self.layer_compositing_guide.items()]

    @property
    def compositing_instructions(self) -> str:
        return self.copy_assembly_markdown



class HybridPlanner:
    """
    Constructs the unified multi-engine assembly specification.
    Guarantees unambiguous separation between generative video layers and code-driven graphics.
    """

    def plan_hybrid_video(
        self,
        title: str,
        topic: str,
        claims: List[str],
        metrics: Optional[Dict[str, Any]] = None,
        duration_sec: float = 30.0,
        aspect_ratio: str = "9:16"
    ) -> HybridAssemblyPlan:
        metrics = metrics or {"Throughput": "140 tok/s", "Speedup": "3.8x"}
        c1 = claims[0] if claims else "Open reasoning architecture"

        shots = [
            HybridShotEntry(
                shot_number=1,
                timecode="00:00 - 00:03",
                duration_sec=3.0,
                visual_objective="High-impact visual hook with numerical computing disruption",
                primary_engine="Gemini Omni",
                asset_source="Photorealistic datacenter footage with HyperFrames badge overlay",
                layer_breakdown={
                    "background_layer": "Gemini Omni: Anamorphic dolly into optical server rack",
                    "overlay_layer": "HyperFrames: '-75% COMPUTE COST' animated red badge",
                    "caption_layer": "Remotion: Word-by-word highlighted hook caption",
                    "audio_layer": "80Hz deep sub-boom + riser sfx"
                },
                transition_to_next="Hard cut to benchmark breakdown"
            ),
            HybridShotEntry(
                shot_number=2,
                timecode="00:03 - 00:08",
                duration_sec=5.0,
                visual_objective="Verified model release announcement and primary metric",
                primary_engine="Remotion",
                asset_source="React programmatic SVG counter and verification shield",
                layer_breakdown={
                    "background_layer": "Matte slate carbon canvas (#080c14) with subtle cyan radial gradient",
                    "overlay_layer": "Remotion: Animated numeric counter ticking from 0% to 94.2%",
                    "caption_layer": "Remotion: 'Verified across standard benchmarks'",
                    "audio_layer": "Data counter chirp + speech narration"
                },
                transition_to_next="Horizontal wipe transition"
            ),
            HybridShotEntry(
                shot_number=3,
                timecode="00:08 - 00:15",
                duration_sec=7.0,
                visual_objective="Architectural deep-dive comparing efficiency gains",
                primary_engine="Remotion",
                asset_source="React SideBySideBarChart with spring physics",
                layer_breakdown={
                    "background_layer": "Gemini Omni: 10% opacity blurred b-roll of silicon wafer",
                    "overlay_layer": f"Remotion: Animated bar graph proving {c1}",
                    "caption_layer": "Remotion: Highlighted technical takeaways",
                    "audio_layer": "Whoosh bar growth + Bell chime on delta badge"
                },
                transition_to_next="Crossfade into technical terminal"
            ),
            HybridShotEntry(
                shot_number=4,
                timecode="00:15 - 00:23",
                duration_sec=8.0,
                visual_objective="Developer proof and terminal deployment execution",
                primary_engine="HyperFrames",
                asset_source="DOM terminal window with syntax-highlighted code",
                layer_breakdown={
                    "background_layer": "Gemini Omni: Over-the-shoulder engineer silhouette at twilight",
                    "overlay_layer": "HyperFrames: DOM glass terminal running evaluation bash script",
                    "caption_layer": "Remotion: 'Zero rewrite required for existing pipelines'",
                    "audio_layer": "Mechanical keyboard typing burst"
                },
                transition_to_next="Scale contract into outro"
            ),
            HybridShotEntry(
                shot_number=5,
                timecode="00:23 - 00:30",
                duration_sec=7.0,
                visual_objective="Strategic conclusion and call to action",
                primary_engine="Remotion",
                asset_source="React ActionCard with pulsating bookmark badge and source attribution",
                layer_breakdown={
                    "background_layer": "Solid matte slate with subtle animated grid overlay",
                    "overlay_layer": "Remotion: Pulsating bookmark button + 'Source: Verified Paper'",
                    "caption_layer": "Remotion: Final community question prompt",
                    "audio_layer": "Warm resolving chord and audio outro"
                },
                transition_to_next="Hold on final frame for social loop"
            )
        ]

        table_rows = "\n".join([
            f"| {s.shot_number:02d} | {s.timecode} | {s.primary_engine:<12} | {s.visual_objective[:42]:<42} | {s.duration_sec}s |"
            for s in shots
        ])

        markdown = f"""# HYBRID VIDEO PRODUCTION PLAN
**Title:** {title}  
**Format:** Vertical 9:16 ({aspect_ratio})  
**Target Duration:** {duration_sec} seconds  

### HYBRID SHOT TABLE
| Shot | Timecode      | Engine       | Visual Objective                            | Duration |
|:-----|:--------------|:-------------|:--------------------------------------------|:---------|
{table_rows}

### LAYER COMPOSITING HIERARCHY
1. **Layer 0 (Base Footage):** Gemini Omni generative background video (4K ProRes 60fps).
2. **Layer 1 (Data & Code UI):** Remotion SVG charts / HyperFrames HTML DOM overlays.
3. **Layer 2 (Synchronized Captions):** Remotion word-by-word highlighted subtitles in platform-safe region.
4. **Layer 3 (Master Audio):** Voiceover (-2dB) + SFX track (-6dB) + Background music ducked to -16dB.
"""

        return HybridAssemblyPlan(
            plan_id=f"hybrid_{topic[:15].replace(' ', '_').lower()}",
            title=title,
            total_duration_sec=duration_sec,
            aspect_ratio=aspect_ratio,
            resolution="1080x1920 60fps",
            shot_table=shots,
            layer_compositing_guide={
                "Layer 0: Gemini Omni Photoreal Base": "Generative photographic footage from Gemini Omni / Veo",
                "Layer 1: Remotion Motion Graphics": "Exact deterministic SVG graphs from Remotion / HyperFrames",
                "Layer 2: Remotion Synchronized Captions": "Synchronized word-level highlighted captions",
                "Layer 3: Master Dynamic Audio": "Full audio mix with dynamic ducking curves"
            },
            audio_ducking_matrix={
                "voiceover_active": "-16dB music volume",
                "voiceover_pause": "-6dB music volume swell",
                "sfx_priority": "+3dB over music during metric drops"
            },
            external_assembly_instructions="Render Gemini Omni shots 1 & 4. Render Remotion scenes 2, 3, 5 with transparent background. Composite in Premiere / After Effects / FFmpeg.",
            copy_assembly_markdown=markdown
        )


hybrid_planner = HybridPlanner()
