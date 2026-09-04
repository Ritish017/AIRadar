"""
HyperFrames Prompt Compiler:
Generates deterministic, HTML/CSS/GSAP motion graphics specifications for HyperFrames.
Enforces paused timelines, absolute position keyframes, zero wall-clock drift,
and seekable frame rendering contracts.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HyperFramesAnimationEntry(BaseModel):
    start_sec: float
    duration_sec: float
    target_selector: str
    properties: Dict[str, Any]
    ease: str


class HyperFramesSpecification(BaseModel):
    composition_id: str
    duration_sec: float
    fps: int = 60
    total_frames: int
    width: int
    height: int
    aspect_ratio: str
    html_markup: str
    css_styles: str
    gsap_timeline_code: str
    animations: List[HyperFramesAnimationEntry]
    assets: List[Dict[str, str]]
    audio_timeline: List[Dict[str, Any]]
    render_instructions: str
    quality_checklist: List[str]
    copy_ready_coding_prompt: str

    @property
    def standalone_agent_prompt(self) -> str:
        return self.copy_ready_coding_prompt


class HyperFramesPromptCompiler:
    """
    Compiler for HyperFrames HTML5 Motion Graphics.
    Outputs strict deterministic DOM and GSAP code for frame-accurate renderers.
    """

    def compile(
        self,
        topic: str,
        headline: str,
        metric_value: str = "+340%",
        metric_label: str = "Throughput Improvement",
        badge_text: str = "VERIFIED BREAKTHROUGH",
        duration_sec: float = 30.0,
        aspect_ratio: str = "9:16",
        fps: int = 60
    ) -> HyperFramesSpecification:
        total_frames = int(duration_sec * fps)
        width, height = (1080, 1920) if aspect_ratio == "9:16" else ((1920, 1080) if aspect_ratio == "16:9" else (1080, 1080))
        comp_id = f"hf_{topic[:12].replace(' ', '_').lower()}_{int(duration_sec)}s"

        # 1. HTML DOM Structure
        html_markup = f"""<div class="hyperframe-container" id="{comp_id}" style="width: {width}px; height: {height}px;">
  <!-- Ambient background glow -->
  <div class="glow-orb glow-cyan"></div>
  <div class="glow-orb glow-indigo"></div>
  <div class="grid-overlay"></div>

  <!-- Header Category Badge -->
  <div class="badge-container">
    <span class="badge-pill">{badge_text}</span>
    <span class="live-indicator">LIVE TELEMETRY</span>
  </div>

  <!-- Main Focal Headline -->
  <div class="headline-container">
    <h1 class="main-headline">{headline}</h1>
    <p class="sub-headline">{topic} verified performance benchmark</p>
  </div>

  <!-- Central Primary Metric HUD Card -->
  <div class="metric-hud-card">
    <div class="card-header">
      <span class="card-tag">EMPIRICAL DELTA</span>
      <span class="card-source">SOURCE: VERIFIED BENCHMARK</span>
    </div>
    <div class="card-metric-value">{metric_value}</div>
    <div class="card-metric-label">{metric_label}</div>
    <div class="metric-progress-bar">
      <div class="metric-progress-fill"></div>
    </div>
  </div>

  <!-- Secondary Proof Ticker / Terminal -->
  <div class="terminal-preview-card">
    <div class="terminal-header">
      <span class="terminal-dot red"></span>
      <span class="terminal-dot yellow"></span>
      <span class="terminal-dot green"></span>
      <span class="terminal-title">runtime_eval.sh</span>
    </div>
    <div class="terminal-body">
      <span class="code-prompt">$</span> <span class="code-text">curl -s localhost:8000/v1/models | jq '.status'</span>
      <div class="code-output">> "SERVING: 140.4 tokens/sec (fp8_gemm)"</div>
    </div>
  </div>

  <!-- Footer Call to Action -->
  <div class="footer-action-bar">
    <div class="footer-icon">★</div>
    <div class="footer-cta-text">Bookmark this benchmark breakdown // Share with engineering team</div>
  </div>
</div>"""

        # 2. CSS Stylesystem
        css_styles = f"""/* HyperFrames Scoped Styling */
#{comp_id}.hyperframe-root {{
  position: relative;
  overflow: hidden;
  background-color: #080c14;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #f8fafc;
  box-sizing: border-box;
}}

#{comp_id} .glow-orb {{
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
}}

#{comp_id} .glow-cyan {{
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, rgba(0, 0, 0, 0) 70%);
  top: 10%;
  left: 20%;
}}

#{comp_id} .glow-indigo {{
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, rgba(0, 0, 0, 0) 70%);
  bottom: 15%;
  right: 10%;
}}

#{comp_id} .grid-overlay {{
  position: absolute;
  inset: 0;
  background-size: 40px 40px;
  background-image: linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  pointer-events: none;
}}

#{comp_id} .badge-container {{
  position: absolute;
  top: 140px;
  left: 80px;
  right: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

#{comp_id} .badge-pill {{
  background: #f43f5e;
  color: #ffffff;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 0.08em;
  padding: 8px 24px;
  border-radius: 9999px;
  text-transform: uppercase;
}}

#{comp_id} .live-indicator {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  color: #38bdf8;
  font-weight: 700;
  letter-spacing: 0.1em;
}}

#{comp_id} .headline-container {{
  position: absolute;
  top: 240px;
  left: 80px;
  right: 80px;
}}

#{comp_id} .main-headline {{
  font-size: 78px;
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin: 0 0 16px 0;
  color: #ffffff;
}}

#{comp_id} .sub-headline {{
  font-size: 34px;
  font-weight: 500;
  color: #94a3b8;
  margin: 0;
}}

#{comp_id} .metric-hud-card {{
  position: absolute;
  top: 680px;
  left: 80px;
  right: 80px;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(56, 189, 248, 0.25);
  border-radius: 36px;
  padding: 48px;
  backdrop-filter: blur(24px);
  box-shadow: 0 24px 64px -12px rgba(0, 0, 0, 0.6);
}}

#{comp_id} .card-header {{
  display: flex;
  justify-content: space-between;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #38bdf8;
  margin-bottom: 20px;
}}

#{comp_id} .card-metric-value {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 140px;
  font-weight: 900;
  line-height: 1.0;
  color: #38bdf8;
  margin-bottom: 12px;
}}

#{comp_id} .card-metric-label {{
  font-size: 36px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 28px;
}}

#{comp_id} .metric-progress-bar {{
  height: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 9999px;
  overflow: hidden;
}}

#{comp_id} .metric-progress-fill {{
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, #06b6d4, #38bdf8);
  border-radius: 9999px;
}}

#{comp_id} .terminal-preview-card {{
  position: absolute;
  top: 1240px;
  left: 80px;
  right: 80px;
  background: #020617;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 28px;
  overflow: hidden;
}}

#{comp_id} .terminal-header {{
  background: #0f172a;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}}

#{comp_id} .terminal-dot {{
  width: 14px;
  height: 14px;
  border-radius: 50%;
}}
#{comp_id} .terminal-dot.red {{ background: #f43f5e; }}
#{comp_id} .terminal-dot.yellow {{ background: #f59e0b; }}
#{comp_id} .terminal-dot.green {{ background: #10b981; }}

#{comp_id} .terminal-title {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
  color: #64748b;
  margin-left: 8px;
}}

#{comp_id} .terminal-body {{
  padding: 32px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 26px;
  line-height: 1.6;
  color: #e2e8f0;
}}

#{comp_id} .code-prompt {{ color: #06b6d4; font-weight: 700; }}
#{comp_id} .code-output {{ color: #34d399; margin-top: 12px; font-weight: 600; }}

#{comp_id} .footer-action-bar {{
  position: absolute;
  bottom: 120px;
  left: 80px;
  right: 80px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 24px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
}}

#{comp_id} .footer-icon {{
  font-size: 36px;
  color: #f59e0b;
}}

#{comp_id} .footer-cta-text {{
  font-size: 26px;
  font-weight: 600;
  color: #94a3b8;
}}
"""

        # 3. GSAP Timeline Animations (All absolute positions!)
        animations = [
            HyperFramesAnimationEntry(
                start_sec=0.2,
                duration_sec=0.6,
                target_selector=f"#{comp_id} .badge-container",
                properties={"opacity": 1, "scale": 1, "y": 0},
                ease="back.out(1.6)"
            ),
            HyperFramesAnimationEntry(
                start_sec=0.5,
                duration_sec=0.8,
                target_selector=f"#{comp_id} .main-headline",
                properties={"opacity": 1, "y": 0},
                ease="power3.out"
            ),
            HyperFramesAnimationEntry(
                start_sec=0.8,
                duration_sec=0.6,
                target_selector=f"#{comp_id} .sub-headline",
                properties={"opacity": 1, "y": 0},
                ease="power2.out"
            ),
            HyperFramesAnimationEntry(
                start_sec=1.5,
                duration_sec=1.0,
                target_selector=f"#{comp_id} .metric-hud-card",
                properties={"opacity": 1, "y": 0, "scale": 1},
                ease="power4.out"
            ),
            HyperFramesAnimationEntry(
                start_sec=2.2,
                duration_sec=1.4,
                target_selector=f"#{comp_id} .metric-progress-fill",
                properties={"width": "86%"},
                ease="power2.inOut"
            ),
            HyperFramesAnimationEntry(
                start_sec=4.0,
                duration_sec=0.9,
                target_selector=f"#{comp_id} .terminal-preview-card",
                properties={"opacity": 1, "y": 0},
                ease="power3.out"
            ),
            HyperFramesAnimationEntry(
                start_sec=5.2,
                duration_sec=0.8,
                target_selector=f"#{comp_id} .code-output",
                properties={"opacity": 1},
                ease="steps(1)"
            ),
            HyperFramesAnimationEntry(
                start_sec=7.0,
                duration_sec=0.7,
                target_selector=f"#{comp_id} .footer-action-bar",
                properties={"opacity": 1, "scale": 1},
                ease="back.out(1.4)"
            )
        ]

        # 4. GSAP Code string
        gsap_code = f"""// HyperFrames Deterministic GSAP Timeline Contract
// Rules: timeline is paused, registered on window.__timelines, uses absolute positions
window.__timelines = window.__timelines || {{}};

const root = document.querySelector("#{comp_id}");
if (!root) throw new Error("HyperFrames composition root '#{comp_id}' not found.");

// Set initial invisible states
gsap.set("#{comp_id} .badge-container", {{ opacity: 0, scale: 0.8, y: -20 }});
gsap.set("#{comp_id} .main-headline", {{ opacity: 0, y: 40 }});
gsap.set("#{comp_id} .sub-headline", {{ opacity: 0, y: 20 }});
gsap.set("#{comp_id} .metric-hud-card", {{ opacity: 0, y: 80, scale: 0.95 }});
gsap.set("#{comp_id} .metric-progress-fill", {{ width: "0%" }});
gsap.set("#{comp_id} .terminal-preview-card", {{ opacity: 0, y: 60 }});
gsap.set("#{comp_id} .code-output", {{ opacity: 0 }});
gsap.set("#{comp_id} .footer-action-bar", {{ opacity: 0, scale: 0.9 }});

// Construct deterministic paused timeline
const tl = gsap.timeline({{ paused: true }});

tl.to("#{comp_id} .badge-container", {{ opacity: 1, scale: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }}, 0.2)
  .to("#{comp_id} .main-headline", {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, 0.5)
  .to("#{comp_id} .sub-headline", {{ opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }}, 0.8)
  .to("#{comp_id} .metric-hud-card", {{ opacity: 1, y: 0, scale: 1, duration: 1.0, ease: "power4.out" }}, 1.5)
  .to("#{comp_id} .metric-progress-fill", {{ width: "86%", duration: 1.4, ease: "power2.inOut" }}, 2.2)
  .to("#{comp_id} .terminal-preview-card", {{ opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }}, 4.0)
  .to("#{comp_id} .code-output", {{ opacity: 1, duration: 0.1, ease: "none" }}, 5.2)
  .to("#{comp_id} .footer-action-bar", {{ opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.4)" }}, 7.0);

// Expose timeline and frame seeker to HyperFrames renderer
window.__timelines["{comp_id}"] = tl;
window.renderFrame = function(timeInSeconds) {{
  tl.seek(timeInSeconds);
}};
"""

        checklist = [
            "Timeline instantiated with { paused: true }",
            "Registered on window.__timelines[comp_id]",
            "Window.renderFrame(timeInSeconds) bound to tl.seek(time)",
            "Zero wall-clock time (no Date.now, setTimeout, or setInterval)",
            "Zero unseeded Math.random calls",
            "All GSAP offsets use absolute timeline positions (e.g. 0.2, 1.5)",
            "CSS layout fully contained within dimensions (1080x1920)",
            "High contrast text meeting WCAG AAA standard against dark background"
        ]

        coding_prompt = f"""================================================================================
COPY THIS INTO A HYPERFRAMES CODING AGENT
================================================================================
You are an expert HyperFrames engineer and DOM motion graphics specialist.
Your goal is to render a deterministic, seekable HTML5 motion composition.

--------------------------------------------------------------------------------
1. COMPOSITION METADATA
--------------------------------------------------------------------------------
- ID: {comp_id}
- Dimensions: {width}x{height} ({aspect_ratio})
- Frame Rate: {fps} FPS
- Duration: {duration_sec}s ({total_frames} frames)

--------------------------------------------------------------------------------
2. DETERMINISM & HYPERFRAMES RULES
--------------------------------------------------------------------------------
- HTML is the absolute source of truth for DOM hierarchy.
- CSS controls visual appearance, fonts, colors, and borders.
- GSAP controls animation: MUST use `gsap.timeline({{ paused: true }})`.
- The timeline MUST be registered on `window.__timelines['{comp_id}'] = tl`.
- The headless renderer will call `window.renderFrame(timeInSeconds)`.
- Use ABSOLUTE timeline positions (the final argument in `.to(...)`). NEVER use relative chaining.
- FORBIDDEN: DO NOT use setTimeout, setInterval, requestAnimationFrame, Date.now(), or unseeded Math.random(). Must remain 100% deterministic and seekable.

--------------------------------------------------------------------------------
3. HTML MARKUP
--------------------------------------------------------------------------------
```html
{html_markup}
```

--------------------------------------------------------------------------------
4. CSS STYLES
--------------------------------------------------------------------------------
```css
{css_styles}
```

--------------------------------------------------------------------------------
5. DETERMINISTIC GSAP TIMELINE CODE
--------------------------------------------------------------------------------
```javascript
{gsap_code}
```
================================================================================"""

        return HyperFramesSpecification(
            composition_id=comp_id,
            duration_sec=duration_sec,
            fps=fps,
            total_frames=total_frames,
            width=width,
            height=height,
            aspect_ratio=aspect_ratio,
            html_markup=html_markup,
            css_styles=css_styles,
            gsap_timeline_code=gsap_code,
            animations=animations,
            assets=[
                {"id": "font-inter", "type": "google_font", "name": "Inter:wght@400;500;700;800;900"},
                {"id": "font-mono", "type": "google_font", "name": "JetBrains+Mono:wght@500;700;900"}
            ],
            audio_timeline=[
                {"time_sec": 0.2, "sound": "ui_blip_high"},
                {"time_sec": 1.5, "sound": "sub_thud_deep"},
                {"time_sec": 4.0, "sound": "keyboard_click_short"}
            ],
            render_instructions="Load HTML/CSS, run script, then invoke window.renderFrame(t) at 1/60s intervals.",
            quality_checklist=checklist,
            copy_ready_coding_prompt=coding_prompt
        )


hyperframes_prompt_compiler = HyperFramesPromptCompiler()
