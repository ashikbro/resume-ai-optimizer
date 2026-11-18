import pytest

from resume_optimizer.matching import analyze_job_match


def test_basic_match():
    resume = "Experienced Python developer. Built REST APIs with FastAPI."
    job = "Looking for a Python engineer who knows FastAPI and PostgreSQL."
    report = analyze_job_match(resume, job)
    assert "python" in report.matched_keywords
    assert "fastapi" in report.matched_keywords
    assert "postgresql" in report.missing_keywords


def test_preserves_source_sentences():
    resume = "Led a team of 5 engineers. Delivered a Python service on time."
    job = "Python experience required."
    report = analyze_job_match(resume, job)
    assert any("Python service" in s for s in report.source_evidence.get("python", ()))


def test_empty_inputs_raise():
    with pytest.raises(ValueError):
        analyze_job_match("", "job")
    with pytest.raises(ValueError):
        analyze_job_match("resume", "   ")
