"""CLI for evidence-preserving resume matching."""

import argparse
from pathlib import Path

from resume_optimizer.matching import analyze_job_match


def main() -> None:
    parser = argparse.ArgumentParser(description="Match a resume against a job description")
    parser.add_argument("resume", type=Path, help="Path to resume text file")
    parser.add_argument("job", type=Path, help="Path to job description text file")
    args = parser.parse_args()

    resume_text = args.resume.read_text()
    job_text = args.job.read_text()
    report = analyze_job_match(resume_text, job_text)

    print("Matched:", ", ".join(report.matched_keywords) or "(none)")
    print("Missing:", ", ".join(report.missing_keywords) or "(none)")
    print()
    print("Evidence:")
    for keyword, sentences in report.source_evidence.items():
        if sentences:
            print(f"  {keyword}:")
            for s in sentences:
                print(f"    - {s[:120]}")


if __name__ == "__main__":
    main()
