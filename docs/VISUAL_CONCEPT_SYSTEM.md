# AI Viral Radar V3.3: Visual Concept System

## 1. The Directorial Axiom

A major pitfall of automated video generation is taking a sentence of spoken narration and immediately appending camera commands:
> Narration: *"AI inference is moving from the cloud toward the edge."*
> Flawed Prompt: *"Cinematic 35mm anamorphic shot of a server room with glowing lights."*

The **Visual Concept Engine** (`backend/services/video/visual_concept_engine.py`) introduces a mandatory conceptual intermediate:
```
NARRATION / CLAIM  ──►  WHAT IS THE BEST VISUAL METAPHOR?  ──►  SHOT SPECIFICATION
```

For every technical claim, the engine produces **3 to 5 distinct visual representation concepts** evaluated for conceptual clarity, information density, emotional impact, novelty, and production feasibility.

---

## 2. Controlled Visual Representation Taxonomy

The system dynamically routes across 22+ representation modalities:

1. `split_screen_contrast`: Dual viewports comparing bottleneck vs streamlined architecture.
2. `animated_geographic_flow`: Geospatial packet routing across distributed edge nodes.
3. `physical_metaphor`: Industrial hydraulic flow or mechanical friction illustrating compute latency.
4. `technical_diagram`: Clean SVG vector charts with numerical callout badges.
5. `data_visualization`: Animated bar graphs with spring physics and verified metric deltas.
6. `macro_hardware_detail`: 100mm macro semiconductor cinematography showing die layouts.
7. `ui_demonstration`: 60 FPS Monaco editor code diffs and terminal CLI logs.
8. `screen_recording_simulation`: Deterministic DOM desktop interface trace.
9. `character_dialogue`: Two-character conversational shot-reverse-shot.
10. `documentary_realism`: Grounded real-world archival footage and journalistically attributed quotes.
11. `cinematic_realism`: 35mm anamorphic daylight cinematography in natural environments.
12. `abstract_visualization`: High-dimensional latent vector clouds and sparse attention heatmaps.
13. `timeline_progression`: Multi-scene historical evolution chronologies.
14. `hybrid_generative_programmatic`: Photorealistic base footage composited under vector HUD overlays.

---

## 3. Anti-Slop & Visual Diversity Engine

The **Anti-Slop Engine** (`backend/services/video/visual_diversity.py`) audits prompts to purge unmotivated clichés:
- **Neon Blue Cyberpunk Glow**: Replaced by authentic 4500K neutral cold-cathode practical lighting.
- **Floating Holograms**: Replaced by physical tablet displays, widescreen monitors, or Remotion HUD overlays.
- **Infinite Halls of Server Racks**: Replaced by specific named architectures (e.g. Nvidia DGX SuperPOD or liquid-cooled subsea pods).
- **Arbitrary Floating Dust & Sparks**: Replaced by pristine ISO Class 1 cleanroom environments.
- **Generic Humanoid Robots**: Replaced by actual robotic arms in semiconductor foundries or software architecture diagrams.

---

## 4. Camera Language Engine

Camera choices must be narratively justified rather than copied from generic recipes:
- **Data Charts & Benchmarks**: Geared head tripod with orthogonal lock and deep focus (f/5.6), preventing parallax perspective distortion of chart axes.
- **Urgent Hooks**: Precision dolly push-in (1.2-second deceleration to dead stop) creating immediate retention pattern interrupts.
- **Semiconductor Hardware**: 100mm macro telephoto with commercial restrained shallow focus (f/2.8) and motor micro-tracking.

---

## 5. Shot Complexity Engine & Micro-Shot Decomposition

When a shot attempts too many actions, diffusion models suffer object morphing and anatomical glitches.
The **Shot Complexity Analyzer** (`backend/services/video/shot_complexity_analyzer.py`) audits 10 vectors:
`subject_count`, `simultaneous_actions`, `camera_complexity`, `environment_complexity`, `text_requirements`, `character_requirements`, `object_interactions`, `temporal_transitions`, `physics_complexity`, `continuity_constraints`.

If complexity score exceeds 75.0 or triggers 3+ bottleneck drivers, the shot is automatically decomposed:
- Overloaded: *"Camera flies through city, zooms into building, tracks drone dropping chip while text rotates."*
- Decomposed:
  1. `Shot A`: Establishing aerial city tracking.
  2. `Shot B`: Exterior building approach.
  3. `Shot C`: Interior workstation delivery.
  4. `Shot D`: Macro semiconductor reveal.
  5. `Shot E`: Remotion typography overlay.
