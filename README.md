# Resume AI Optimizer

An AI-assisted tool for tailoring resumes and professional profiles to a
specific job description while preserving the candidate's factual experience.

## Status

**Foundation stage — deterministic matching is implemented.**

The repository includes plain-text keyword matching that reports matched and
missing terms and preserves exact resume sentences as evidence. It does not
invent experience or generate unsupported claims.

## First-release scope

- Import a resume as Markdown, plain text, or PDF
- Paste a job description and extract skills, responsibilities, and keywords
- Suggest clearer, evidence-based bullet points
- Show matched, missing, and potentially overused keywords
- Preserve an editable version history and the original document
- Export an optimized resume as Markdown and PDF
- Provide a change review before any content is accepted

The system must never invent employers, job titles, dates, degrees,
certifications, metrics, or responsibilities. Suggestions should be traceable
to source resume text or explicitly marked as requiring user confirmation.

## Recommended architecture

```text
web/       Resume editor, comparison view, and export controls
api/       User, document, optimization, and version APIs
worker/    Document parsing and model requests
db/        Users, documents, versions, jobs, and suggestions
```

Use a model-provider abstraction so hosted and local models can be selected
without changing the editor. Store the original document separately from every
generated draft and retain the prompt/model metadata needed to reproduce a
suggestion.

## Privacy and safety requirements

- Do not use uploaded resumes or job descriptions for model training by default.
- Encrypt documents at rest and in transit.
- Provide deletion and export controls for all user data.
- Redact or minimize personal data in application logs.
- Require explicit confirmation before overwriting a resume.
- Label generated text and show the source or rationale for each change.
- Never automate LinkedIn changes without a separate user confirmation step.

## Roadmap

1. Scaffold authenticated document storage and a plain-text editor.
2. Add job-description parsing and deterministic keyword matching.
3. Add model-backed suggestions with source-linked review.
4. Add version history, PDF export, and quality checks.
5. Add privacy documentation, retention controls, and deployment automation.

## Development

```sh
python -m venv .venv
.venv/bin/pip install pytest
PYTHONPATH=src .venv/bin/pytest
```
