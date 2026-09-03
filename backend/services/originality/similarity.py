import re
from typing import Tuple, Dict, Any, List
from rapidfuzz import fuzz

def normalize_text(text: str) -> str:
    """Lowercase and strip non-alphanumerics."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()

def get_word_ngrams(words: List[str], n: int = 3) -> set:
    """Extract word n-grams as a set."""
    if len(words) < n:
        return set([" ".join(words)])
    return set(" ".join(words[i:i+n]) for i in range(len(words) - n + 1))

def calculate_ngram_jaccard(text1: str, text2: str, n: int = 3) -> float:
    """Calculate Jaccard similarity of 3-grams to detect copied phrases."""
    words1 = normalize_text(text1).split()
    words2 = normalize_text(text2).split()

    if not words1 or not words2:
        return 0.0

    ngrams1 = get_word_ngrams(words1, n)
    ngrams2 = get_word_ngrams(words2, n)

    intersection = len(ngrams1.intersection(ngrams2))
    union = len(ngrams1.union(ngrams2))

    if union == 0:
        return 0.0
    return intersection / union

class OriginalityChecker:
    def __init__(self, threshold: float = 0.60):
        self.threshold = threshold

    def check_similarity(self, source_text: str, generated_text: str) -> Dict[str, Any]:
        """
        Compares generated text against original source text using:
        1. Token Set Ratio (handles re-ordered words)
        2. Partial Ratio (detects copied sub-blocks)
        3. 3-gram Jaccard Overlap (detects verbatim phrasing)

        Returns composite similarity (0.0 to 1.0) and safety boolean.
        """
        if not source_text or not generated_text:
            return {"similarity": 0.0, "is_safe": True, "details": {}}

        clean_src = normalize_text(source_text)
        clean_gen = normalize_text(generated_text)

        # 1. RapidFuzz token set ratio (0 to 100)
        token_ratio = fuzz.token_set_ratio(clean_src, clean_gen) / 100.0

        # 2. RapidFuzz partial ratio
        partial_ratio = fuzz.partial_ratio(clean_src, clean_gen) / 100.0

        # 3. 3-gram phrase Jaccard
        jaccard_overlap = calculate_ngram_jaccard(clean_src, clean_gen, n=3)

        # Weighted composite score
        composite = (token_ratio * 0.45) + (partial_ratio * 0.30) + (jaccard_overlap * 0.25)
        composite = round(min(1.0, max(0.0, composite)), 3)

        is_safe = composite <= self.threshold

        return {
            "similarity": composite,
            "is_safe": is_safe,
            "threshold": self.threshold,
            "details": {
                "token_ratio": round(token_ratio, 3),
                "partial_ratio": round(partial_ratio, 3),
                "jaccard_overlap": round(jaccard_overlap, 3)
            }
        }

originality_checker = OriginalityChecker()
