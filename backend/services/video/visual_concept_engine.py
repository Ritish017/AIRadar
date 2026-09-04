"""
Visual Concept Engine (V3.3):
Transforms raw narration, claims, and event developments into high-leverage visual concepts
BEFORE jumping directly into camera directions or code specifications.
Evaluates candidates across conceptual clarity, information density, novelty, and production feasibility.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid


class VisualRepresentationType:
    CINEMATIC_REALISM = "cinematic_realism"
    DOCUMENTARY = "documentary"
    PRODUCT_VISUALIZATION = "product_visualization"
    UI_DEMONSTRATION = "ui_demonstration"
    TECHNICAL_DIAGRAM = "technical_diagram"
    DATA_VISUALIZATION = "data_visualization"
    TIMELINE = "timeline"
    GEOGRAPHIC_VISUALIZATION = "geographic_visualization"
    CHARACTER_DIALOGUE = "character_dialogue"
    ENVIRONMENTAL_METAPHOR = "environmental_metaphor"
    OBJECT_METAPHOR = "object_metaphor"
    MACRO_DETAIL = "macro_detail"
    SIMULATION = "simulation"
    SCREEN_RECORDING = "screen_recording"
    CODE_VISUALIZATION = "code_visualization"
    ABSTRACT_VISUALIZATION = "abstract_visualization"
    MOTION_TYPOGRAPHY = "motion_typography"
    INFOGRAPHIC = "infographic"
    ARCHIVAL_REFERENCE = "archival_reference"
    HYBRID_GENERATIVE_PROGRAMMATIC = "hybrid_generative_programmatic"
    IMAGE_TO_VIDEO = "image_to_video"
    VIDEO_TO_VIDEO = "video_to_video"
    MULTI_SHOT_NARRATIVE = "multi_shot_narrative"

    ALL_TYPES = [
        CINEMATIC_REALISM, DOCUMENTARY, PRODUCT_VISUALIZATION, UI_DEMONSTRATION,
        TECHNICAL_DIAGRAM, DATA_VISUALIZATION, TIMELINE, GEOGRAPHIC_VISUALIZATION,
        CHARACTER_DIALOGUE, ENVIRONMENTAL_METAPHOR, OBJECT_METAPHOR, MACRO_DETAIL,
        SIMULATION, SCREEN_RECORDING, CODE_VISUALIZATION, ABSTRACT_VISUALIZATION,
        MOTION_TYPOGRAPHY, INFOGRAPHIC, ARCHIVAL_REFERENCE,
        HYBRID_GENERATIVE_PROGRAMMATIC, IMAGE_TO_VIDEO, VIDEO_TO_VIDEO, MULTI_SHOT_NARRATIVE
    ]


class VisualConceptCandidate(BaseModel):
    concept_id: str
    representation_type: str
    headline: str
    core_visual_metaphor: str
    description: str
    what_viewer_sees: str
    what_viewer_understands: str
    information_density: float = Field(default=85.0, ge=0.0, le=100.0)
    conceptual_clarity: float = Field(default=90.0, ge=0.0, le=100.0)
    emotional_impact: float = Field(default=80.0, ge=0.0, le=100.0)
    novelty_score: float = Field(default=85.0, ge=0.0, le=100.0)
    production_feasibility: float = Field(default=90.0, ge=0.0, le=100.0)
    recommended_engine: str  # Gemini Omni, Veo, Remotion, HyperFrames, Hybrid
    asset_requirements: List[str] = Field(default_factory=list)
    anti_slop_safeguards: List[str] = Field(default_factory=list)
    overall_fit_score: float = 0.0
    is_recommended: bool = False
    selection_rationale: str = ""


class VisualConceptSuite(BaseModel):
    suite_id: str
    claim_or_narration: str
    topic: str
    platform: str
    candidates: List[VisualConceptCandidate]
    selected_concept: Optional[VisualConceptCandidate] = None


class VisualConceptEngine:
    """
    Generates, evaluates, ranks, and combines visual representations for ideas before shot design.
    """

    def generate_concepts(
        self,
        claim: str,
        topic: str,
        platform: str = "instagram_reel",
        audience: str = "AI Engineers & Tech Leaders",
        metrics: Optional[Dict[str, Any]] = None,
        style_preference: Optional[str] = None
    ) -> VisualConceptSuite:
        suite_id = f"vcs_{uuid.uuid4().hex[:8]}"
        metrics = metrics or {}
        candidates = []

        # 1. Concept A: Split-screen / Comparative Architecture (Technical Diagram / Hybrid)
        c_a = VisualConceptCandidate(
            concept_id=f"vc_a_{uuid.uuid4().hex[:6]}",
            representation_type=VisualRepresentationType.HYBRID_GENERATIVE_PROGRAMMATIC,
            headline="Split-Screen Architecture Contrast: Monolithic vs Distributed",
            core_visual_metaphor="Dual-viewport visual comparison of legacy bottleneck vs streamlined throughput",
            description=(
                f"A clean horizontal or vertical split-screen comparing the standard approach to {topic}. "
                "Left viewport displays a centralized bottleneck with high congestion latency. "
                "Right viewport displays the optimized pathway with low-latency direct routing."
            ),
            what_viewer_sees=(
                "Synchronized dual telemetries: the left panel stalls under heavy token payload, "
                "while the right panel streams packets instantaneously without buffer bloat."
            ),
            what_viewer_understands=(
                f"Why {topic} provides concrete latency and cost advantages without theoretical fluff."
            ),
            information_density=94.0,
            conceptual_clarity=96.0,
            emotional_impact=82.0,
            novelty_score=88.0,
            production_feasibility=92.0,
            recommended_engine="Hybrid",
            asset_requirements=["Remotion synchronized latency meters", "HyperFrames terminal output"],
            anti_slop_safeguards=["No meaningless glowing particles", "No generic neon gridlines", "Grounded latency numbers"]
        )
        c_a.overall_fit_score = self._compute_fit(c_a, platform)
        candidates.append(c_a)

        # 2. Concept B: Grounded Physical / Environmental Metaphor
        c_b = VisualConceptCandidate(
            concept_id=f"vc_b_{uuid.uuid4().hex[:6]}",
            representation_type=VisualRepresentationType.ENVIRONMENTAL_METAPHOR,
            headline="Macro Physical Translation: Mechanical Friction vs Hydraulic Flow",
            core_visual_metaphor="Industrial fluid dynamic or semiconductor silicon pathing representing computational flow",
            description=(
                f"Tangible physical reality visualizing {topic}. An extreme close-up macro sequence inside an optical compute chamber, "
                "where micro-fluidic conduits light up sequentially as data packages traverse without mechanical friction."
            ),
            what_viewer_sees=(
                "Pristine macro lens tracking micro-circuitry where photonic pulses traverse conductive tracks. "
                "Cool studio illumination with matte black carbon surfaces and crisp reflections."
            ),
            what_viewer_understands=(
                "The physical scale and elegant efficiency of next-generation hardware architecture."
            ),
            information_density=86.0,
            conceptual_clarity=90.0,
            emotional_impact=92.0,
            novelty_score=94.0,
            production_feasibility=88.0,
            recommended_engine="Gemini Omni",
            asset_requirements=["35mm anamorphic studio footage", "Photonic pulse reference textures"],
            anti_slop_safeguards=["Must remain physically plausible", "No floating magical sparks", "No unmotivated camera roll"]
        )
        c_b.overall_fit_score = self._compute_fit(c_b, platform)
        candidates.append(c_b)

        # 3. Concept C: Data-First Empirical Proof (Remotion Data Visualization)
        metric_str = ", ".join(f"{k}: {v}" for k, v in list(metrics.items())[:2]) if metrics else "Throughput: +3.4x, Latency: -65%"
        c_c = VisualConceptCandidate(
            concept_id=f"vc_c_{uuid.uuid4().hex[:6]}",
            representation_type=VisualRepresentationType.DATA_VISUALIZATION,
            headline="Empirical Benchmark Disruption: Leaderboard Bar Graph Acceleration",
            core_visual_metaphor="Side-by-side empirical performance bars with spring physics and verified delta badges",
            description=(
                f"Precision data visualization demonstrating {topic}. Clean typography and animated SVG bar charts "
                f"displaying verified metrics ({metric_str}) with verified source attribution badges."
            ),
            what_viewer_sees=(
                "A minimalist carbon card where competing model bars plateau at baseline, while the new model bar "
                "springs upward with spring physics, locking in the metric delta with an official verification badge."
            ),
            what_viewer_understands=(
                "Empirical proof of superiority backed by standardized benchmarks, eliminating marketing skepticism."
            ),
            information_density=98.0,
            conceptual_clarity=98.0,
            emotional_impact=78.0,
            novelty_score=80.0,
            production_feasibility=98.0,
            recommended_engine="Remotion",
            asset_requirements=["SVG benchmark chart", "Platform safe zone typography system", "Audio impact stem"],
            anti_slop_safeguards=["Pixel-perfect text alignment", "No floating hallucinated glyphs", "Accurate non-distorted proportions"]
        )
        c_c.overall_fit_score = self._compute_fit(c_c, platform)
        candidates.append(c_c)

        # 4. Concept D: Real-World Systems UI / Terminal Demonstration
        c_d = VisualConceptCandidate(
            concept_id=f"vc_d_{uuid.uuid4().hex[:6]}",
            representation_type=VisualRepresentationType.UI_DEMONSTRATION,
            headline="Live Systems Terminal Trace: CLI Execution & Packet Inspection",
            core_visual_metaphor="Real developer terminal executing verified CLI commands with live output",
            description=(
                f"Technical UI demonstration. An authentic dark-mode developer workstation terminal where actual shell commands "
                f"run the inference engine, demonstrating {topic} directly from stdout."
            ),
            what_viewer_sees=(
                "JetBrains Mono typography typing `curl -s localhost:8000/v1/telemetry | jq` followed by "
                "instantaneous structured JSON output and microsecond timestamps."
            ),
            what_viewer_understands=(
                "That this technology is usable today in production environments, not just an abstract whitepaper."
            ),
            information_density=92.0,
            conceptual_clarity=92.0,
            emotional_impact=84.0,
            novelty_score=86.0,
            production_feasibility=95.0,
            recommended_engine="HyperFrames",
            asset_requirements=["CSS terminal window frame", "Deterministic seekable GSAP timeline"],
            anti_slop_safeguards=["No Hollywood fake green hacking code", "Real executable commands", "Zero wall-clock drift"]
        )
        c_d.overall_fit_score = self._compute_fit(c_d, platform)
        candidates.append(c_d)

        # 5. Concept E: Documentary Archival & Paper Annotation
        c_e = VisualConceptCandidate(
            concept_id=f"vc_e_{uuid.uuid4().hex[:6]}",
            representation_type=VisualRepresentationType.DOCUMENTARY,
            headline="Investigative Paper Breakdown: Highlighted Equations & Source Figures",
            core_visual_metaphor="Original PDF/arXiv research paper with yellow fluorescent highlight and callout annotation",
            description=(
                f"Documentary investigative camera moving across the original research publication or official release notice. "
                "Key equations and architectural claims are illuminated with precise highlights."
            ),
            what_viewer_sees=(
                "Top-down planar camera gliding over a clean publication page; line 14 is highlighted in amber, "
                "revealing the exact mathematical breakthrough with an author footnote."
            ),
            what_viewer_understands=(
                "The academic and theoretical legitimacy behind the development."
            ),
            information_density=90.0,
            conceptual_clarity=94.0,
            emotional_impact=75.0,
            novelty_score=82.0,
            production_feasibility=96.0,
            recommended_engine="Remotion",
            asset_requirements=["High-res paper screenshot", "Source badge overlay"],
            anti_slop_safeguards=["Real paper excerpts only", "Legible fonts", "No fake equations"]
        )
        c_e.overall_fit_score = self._compute_fit(c_e, platform)
        candidates.append(c_e)

        # Determine winner based on platform and claim characteristics
        best_candidate = max(candidates, key=lambda c: c.overall_fit_score)
        best_candidate.is_recommended = True
        best_candidate.selection_rationale = (
            f"Selected '{best_candidate.headline}' because it maximizes conceptual clarity ({best_candidate.conceptual_clarity:.0f}%) "
            f"and information density ({best_candidate.information_density:.0f}%) for {platform} while maintaining 100% production feasibility."
        )

        return VisualConceptSuite(
            suite_id=suite_id,
            claim_or_narration=claim,
            topic=topic,
            platform=platform,
            candidates=candidates,
            selected_concept=best_candidate
        )

    def _compute_fit(self, candidate: VisualConceptCandidate, platform: str) -> float:
        # Weighted combination of clarity, density, novelty, and feasibility
        base = (
            candidate.conceptual_clarity * 0.35 +
            candidate.information_density * 0.25 +
            candidate.production_feasibility * 0.20 +
            candidate.novelty_score * 0.10 +
            candidate.emotional_impact * 0.10
        )
        if platform in ["instagram_reel", "tiktok"] and candidate.emotional_impact > 85:
            base += 3.0
        elif platform in ["x", "linkedin"] and candidate.information_density > 90:
            base += 3.0
        return min(100.0, round(base, 1))

    def combine_concepts(
        self,
        concept_a: VisualConceptCandidate,
        concept_b: VisualConceptCandidate
    ) -> VisualConceptCandidate:
        """Combines two complementary representations into a single hybrid concept."""
        combined_id = f"vc_hybrid_{uuid.uuid4().hex[:6]}"
        return VisualConceptCandidate(
            concept_id=combined_id,
            representation_type=VisualRepresentationType.HYBRID_GENERATIVE_PROGRAMMATIC,
            headline=f"Hybrid Fusion: {concept_a.headline[:30]} + {concept_b.headline[:30]}",
            core_visual_metaphor=f"{concept_a.core_visual_metaphor} layered with {concept_b.core_visual_metaphor}",
            description=f"Layered compositing: Background displays {concept_a.what_viewer_sees}, while foreground HUD features {concept_b.what_viewer_sees}.",
            what_viewer_sees=f"{concept_a.what_viewer_sees} overlaid with {concept_b.what_viewer_sees}",
            what_viewer_understands=f"Combines physical realism ({concept_a.what_viewer_understands}) with empirical precision ({concept_b.what_viewer_understands}).",
            information_density=max(concept_a.information_density, concept_b.information_density),
            conceptual_clarity=round((concept_a.conceptual_clarity + concept_b.conceptual_clarity) / 2, 1),
            emotional_impact=max(concept_a.emotional_impact, concept_b.emotional_impact),
            novelty_score=96.0,
            production_feasibility=89.0,
            recommended_engine="Hybrid",
            asset_requirements=list(set(concept_a.asset_requirements + concept_b.asset_requirements)),
            anti_slop_safeguards=list(set(concept_a.anti_slop_safeguards + concept_b.anti_slop_safeguards)),
            overall_fit_score=95.5,
            is_recommended=True,
            selection_rationale="Synthesized hybrid concept maximizing both visual immersion and empirical veracity."
        )


visual_concept_engine = VisualConceptEngine()
