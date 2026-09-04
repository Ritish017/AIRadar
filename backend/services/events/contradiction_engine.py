"""
Contradiction Detection Engine.
Detects conflicting reports, timeline disputes, and metric discrepancies across multiple sources
for the same canonical event to prevent generating definitive claims on contested developments.
"""

import re
import logging
from typing import List, Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

# Patterns signaling timeline or release status conflicts
TIMELINE_CONFLICT_PAIRS = [
    (r"\b(released today|available now|out now|launched today|live now|shipped)\b",
     r"\b(expected next (week|month)|coming soon|not yet released|rumored to launch|delayed|slated for)\b"),
    (r"\b(official|confirmed by|verified)\b",
     r"\b(unconfirmed|leak|alleged|rumor|denied|refuted|debunked)\b"),
    (r"\b(open source|weights available|free download|public weights)\b",
     r"\b(closed source|api only|waitlist only|internal preview|gated access)\b")
]

class ContradictionEngine:
    """
    Analyzes multiple text snippets / articles belonging to a candidate event
    to detect conflicting claims, discrepancies, or disputed developments.
    """

    def _extract_benchmark_metrics(self, text: str) -> Dict[str, float]:
        """Extracts benchmark name -> score % regardless of word order."""
        benchmarks = ["swe-bench", "human-eval", "math", "mmlu", "gpqa", "gsm8k", "arc"]
        results = {}
        text_lower = text.lower()
        for b in benchmarks:
            # Pattern 1: benchmark name ... number%
            p1 = rf"\b{b}\b[^\d%]{{1,35}}(\d{{1,3}}(?:\.\d{{1,2}})?)\s*%"
            m1 = re.search(p1, text_lower)
            if m1:
                results[b] = float(m1.group(1))
                continue
            # Pattern 2: number% ... benchmark name
            p2 = rf"(\d{{1,3}}(?:\.\d{{1,2}})?)\s*%[^\d%]{{1,35}}\b{b}\b"
            m2 = re.search(p2, text_lower)
            if m2:
                results[b] = float(m2.group(1))
        return results

    def detect_contradictions(self, sources_content: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]], str]:
        """
        Evaluates a list of source items for factual, temporal, or confirmation contradictions.
        Returns:
            (has_contradiction: bool, contradictions: List[dict], conflict_summary: str)
        """
        if len(sources_content) < 2:
            return False, [], ""

        contradictions: List[Dict[str, Any]] = []

        # 1. Timeline & Release Status Contradiction Check
        for i, src_a in enumerate(sources_content):
            text_a = f"{src_a.get('title', '')} {src_a.get('content', '')}".lower()
            name_a = src_a.get("source", f"Source {i+1}")

            for j, src_b in enumerate(sources_content[i+1:], start=i+1):
                text_b = f"{src_b.get('title', '')} {src_b.get('content', '')}".lower()
                name_b = src_b.get("source", f"Source {j+1}")

                for pat_a, pat_b in TIMELINE_CONFLICT_PAIRS:
                    match_a1 = re.search(pat_a, text_a)
                    match_b2 = re.search(pat_b, text_b)
                    
                    match_a2 = re.search(pat_b, text_a)
                    match_b1 = re.search(pat_a, text_b)

                    if (match_a1 and match_b2) or (match_a2 and match_b1):
                        claim_a = match_a1.group(0) if match_a1 else match_a2.group(0)
                        claim_b = match_b2.group(0) if match_b2 else match_b1.group(0)
                        
                        contra = {
                            "type": "TIMELINE_OR_STATUS_CONFLICT",
                            "source_a": name_a,
                            "source_b": name_b,
                            "claim_a": claim_a,
                            "claim_b": claim_b,
                            "description": f"{name_a} states '{claim_a}' whereas {name_b} reports '{claim_b}'."
                        }
                        contradictions.append(contra)
                        break

                # 2. Benchmark Score Discrepancies (e.g., "70.3% on SWE-bench" vs "reproduces only 62.1%")
                metrics_a = self._extract_benchmark_metrics(text_a)
                metrics_b = self._extract_benchmark_metrics(text_b)

                common_benchmarks = set(metrics_a.keys()) & set(metrics_b.keys())
                for bench in common_benchmarks:
                    val_a = metrics_a[bench]
                    val_b = metrics_b[bench]
                    if abs(val_a - val_b) >= 5.0:  # >= 5% discrepancy
                        contra = {
                            "type": "METRIC_DISCREPANCY",
                            "benchmark": bench.upper(),
                            "source_a": name_a,
                            "val_a": f"{val_a}%",
                            "source_b": name_b,
                            "val_b": f"{val_b}%",
                            "description": f"Conflicting evaluations on {bench.upper()}: {name_a} reports {val_a}% vs {name_b} reports {val_b}%."
                        }
                        contradictions.append(contra)

                # 3. Explicit Dispute / Challenge Signals
                dispute_pattern = r"\b(disputes?|disputed|refutes?|refuted|contests?|contested|reproduces only|failed to reproduce)\b"
                if re.search(dispute_pattern, text_b) and not any(c.get("type") == "METRIC_DISCREPANCY" for c in contradictions):
                    contra = {
                        "type": "DISPUTED_CLAIM",
                        "source_a": name_a,
                        "source_b": name_b,
                        "description": f"{name_b} disputes claims reported by {name_a}."
                    }
                    contradictions.append(contra)

        if contradictions:
            first_contra = contradictions[0]
            summary = (
                f"Contradiction Detected: {first_contra.get('description', 'Conflicting reports between sources.')} "
                "Event held in DEVELOPING status. Definitive claims must be suspended until primary lab verification."
            )
            logger.info(f"Contradiction identified across {len(contradictions)} points: {summary}")
            return True, contradictions, summary

        return False, [], ""

contradiction_engine = ContradictionEngine()
