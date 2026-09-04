"""
Visual Diversity & Anti-Slop Engine (V3.3):
Detects repetitive AI video clichés and enforces grounded, narrative-driven aesthetic choices.
Replaces generic sci-fi tropes with tangible documentary or technical representations.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import re


class ClicheDetectionResult(BaseModel):
    cliche_name: str
    severity: str  # Critical, Warning, Moderate
    matched_phrase: str
    why_rejected: str
    suggested_grounded_alternative: str


class VisualDiversityAudit(BaseModel):
    diversity_score: float = Field(ge=0.0, le=100.0)
    slop_risk_index: float = Field(ge=0.0, le=100.0)
    has_prohibited_cliches: bool
    detected_cliches: List[ClicheDetectionResult]
    creative_novelty_rating: str  # HIGHLY_ORIGINAL, DISTINCT, MODERATELY_DISTINCT, HIGHLY_GENERIC
    remediation_guidance: str


class VisualDiversityEngine:
    """
    Audits visual concepts and prompt drafts against a known taxonomy of repetitive AI generation clichés.
    """

    KNOWN_CLICHES = [
        {
            "name": "Neon Blue Cyberpunk Lighting",
            "regex": r"(neon blue|cyberpunk glow|electric cyan lighting everywhere|glowing blue everywhere)",
            "severity": "Warning",
            "reason": "Overused sci-fi aesthetic that diminishes factual documentary credibility.",
            "alternative": "Authentic datacenter cold-cathode practical lighting (4500K neutral white with subtle amber LED accents)."
        },
        {
            "name": "Floating Hologram in Mid-Air",
            "regex": r"(floating hologram|holographic display floating in air|hologram in mid[- ]air|floating screens)",
            "severity": "Critical",
            "reason": "Physically implausible sci-fi trope that confuses viewers regarding actual software interfaces.",
            "alternative": "Physical ultra-wide matte display screen, physical tablet UI, or clean Remotion HUD overlay."
        },
        {
            "name": "Infinite Hall of Generic Server Racks",
            "regex": r"(infinite rows? of server racks|endless server racks|generic server room)",
            "severity": "Moderate",
            "reason": "Stock AI B-roll cliché that conveys zero specific technical information.",
            "alternative": "Specific named cluster architecture: Nvidia DGX SuperPOD or liquid-cooled subsea container."
        },
        {
            "name": "Arbitrary Floating Sparks and Dust Particles",
            "regex": r"(floating dust particles|glowing embers|magical sparkles|floating glowing particles|arbitrary particles)",
            "severity": "Critical",
            "reason": "Meaningless decorative noise that clutters the visual field and signals amateur prompt engineering.",
            "alternative": "Pristine ISO Class 1 cleanroom environment with laminar airflow and zero atmospheric debris."
        },
        {
            "name": "Slow-Motion Hero Strutting Towards Camera",
            "regex": r"(slow[- ]motion hero walk|walks in slow motion towards camera|dramatic walking towards camera)",
            "severity": "Warning",
            "reason": "Unmotivated dramatic posturing that slows pacing and wastes critical early retention seconds.",
            "alternative": "Active purposeful engineering task: reviewing live deployment telemetry at a workstation."
        },
        {
            "name": "Generic Humanoid Metallic AI Robot",
            "regex": r"(humanoid robot|glowing robot head|silver android|generic metallic robot)",
            "severity": "Critical",
            "reason": "Misleading personification of algorithmic software; damages technical authority.",
            "alternative": "Software visualizer, automated robotic manipulator arm in semiconductor fab, or code trace."
        },
        {
            "name": "Meaningless Glowing Circuits in Brain / Air",
            "regex": r"(circuits glowing in a brain|glowing neural pathways in the air|wires connecting to a brain)",
            "severity": "Critical",
            "reason": "Outdated 1990s visual metaphor rejected by modern technical audiences.",
            "alternative": "Authentic sparse attention matrix heatmap or architectural tensor flow diagram."
        },
        {
            "name": "Omnipresent 35mm Anamorphic Shallow DOF Boilerplate",
            "regex": r"(cinematic 35mm anamorphic shallow depth of field.*epic volumetric atmosphere)",
            "severity": "Warning",
            "reason": "Copy-pasted buzzword boilerplate inserted without regard for whether deep focus is required for diagrams.",
            "alternative": "Tailor camera lens specifically to the subject (e.g. 50mm flat plane for data, 100mm macro for silicon)."
        }
    ]

    def audit_visual_content(self, text_corpus: str) -> VisualDiversityAudit:
        detected = []
        text_lower = text_corpus.lower()

        for c in self.KNOWN_CLICHES:
            match = re.search(c["regex"], text_lower)
            if match:
                detected.append(
                    ClicheDetectionResult(
                        cliche_name=c["name"],
                        severity=c["severity"],
                        matched_phrase=match.group(0),
                        why_rejected=c["reason"],
                        suggested_grounded_alternative=c["alternative"]
                    )
                )

        slop_penalty = sum(25.0 if d.severity == "Critical" else (15.0 if d.severity == "Warning" else 8.0) for d in detected)
        slop_risk = min(100.0, slop_penalty)
        diversity_score = max(0.0, 100.0 - slop_risk)

        if diversity_score >= 90.0:
            rating = "HIGHLY_ORIGINAL"
            guidance = "Visual description is grounded, documentary-grade, and free of AI generation clichés."
        elif diversity_score >= 75.0:
            rating = "DISTINCT"
            guidance = "Good creative grounding; minor aesthetic adjustments recommended."
        elif diversity_score >= 50.0:
            rating = "MODERATELY_DISTINCT"
            guidance = "Several repetitive AI tropes detected. Replace detected clichés with suggested grounded alternatives."
        else:
            rating = "HIGHLY_GENERIC"
            guidance = "Excessive cliché density detected. Rewrite visual concepts using tangible real-world mechanisms."

        return VisualDiversityAudit(
            diversity_score=round(diversity_score, 1),
            slop_risk_index=round(slop_risk, 1),
            has_prohibited_cliches=len(detected) > 0,
            detected_cliches=detected,
            creative_novelty_rating=rating,
            remediation_guidance=guidance
        )


visual_diversity_engine = VisualDiversityEngine()
