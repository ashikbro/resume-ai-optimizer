import pytest

from resume_optimizer import analyze_job_match


def test_matching_reports_source_evidence_without_inventing_content():
    report = analyze_job_match(
        "Built Python data pipelines and improved reporting.",
        "We need Python, SQL, and reporting experience.",
    )
    assert report.matched_keywords == ("python", "reporting")
    assert report.missing_keywords == ("experience", "sql")
    assert report.source_evidence["python"] == ("Built Python data pipelines and improved reporting.",)


def test_empty_inputs_are_rejected():
    with pytest.raises(ValueError):
        analyze_job_match("", "Python")
