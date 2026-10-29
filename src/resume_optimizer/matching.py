"""Evidence-preserving keyword matching for resumes and job descriptions."""

from dataclasses import dataclass
import re

STOP_WORDS = {
    "about", "after", "also", "and", "are", "for", "from", "have", "into",
    "job", "need", "our", "that", "the", "their", "this", "we", "with", "you", "your",
}


@dataclass(frozen=True)
class MatchReport:
    matched_keywords: tuple[str, ...]
    missing_keywords: tuple[str, ...]
    source_evidence: dict[str, tuple[str, ...]]


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
    return {word.rstrip(".") for word in words if word not in STOP_WORDS}


def _sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+|\n+", text) if sentence.strip()]


def analyze_job_match(resume_text: str, job_description: str) -> MatchReport:
    """Compare keywords and retain exact resume sentences as evidence."""
    if not resume_text.strip() or not job_description.strip():
        raise ValueError("resume_text and job_description are required")
    resume_keywords = _keywords(resume_text)
    job_keywords = _keywords(job_description)
    matched = tuple(sorted(resume_keywords & job_keywords))
    missing = tuple(sorted(job_keywords - resume_keywords))
    evidence = {
        keyword: tuple(sentence for sentence in _sentences(resume_text)
                       if re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", sentence, re.I))
        for keyword in matched
    }
    return MatchReport(matched, missing, evidence)
