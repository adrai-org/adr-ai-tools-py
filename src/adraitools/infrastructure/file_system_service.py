"""File system operations service."""

from pathlib import Path


class FileSystemService:
    """Service for file system operations."""

    def directory_exists(self, path: Path) -> bool:
        """Check if directory exists."""
        return path.exists() and path.is_dir()

    def create_directory(self, path: Path) -> None:
        """Create directory."""
        path.mkdir(parents=True, exist_ok=True)

    def create_template_file(self, path: Path) -> None:
        """Create ADR template file."""
        template_content = """# Architecture Decision Record (ADR)

## Title
Short title of the architectural decision

## Status
[Proposed | Accepted | Deprecated | Superseded]
<!-- If superseded, include a reference to the new ADR -->

## Date
YYYY-MM-DD

## Context
Describe the context and problem statement. What is the architectural challenge
that needs to be addressed? Include any relevant constraints or requirements
that influenced the decision.

## Decision
State the architectural decision clearly and concisely. What specific approach,
technology, pattern, or solution was chosen?

## Rationale
Explain the reasoning that led to this decision. Why was this particular option
selected among the alternatives? Include relevant factors such as:
- Technical considerations
- Business requirements
- Team capabilities
- Time constraints
- Cost implications

## Implications
### Positive Implications
List the benefits and positive outcomes expected from this decision.

### Concerns
List potential challenges, risks, or negative consequences along with possible
mitigation strategies.

## Alternatives
Describe other options that were considered and why they were not selected.
For each alternative, briefly explain:
- Key characteristics
- Pros and cons relative to the chosen solution
- Reasons for rejection

## Future Direction
Outline any follow-up actions, future considerations, or potential changes
that might be necessary as a result of this decision. Include potential
triggers for revisiting this decision.

## References
List any relevant documents, articles, books, or other resources that
supported this decision:
- Links to relevant documentation
- Research materials
- Benchmarks or performance data
- Team discussions or meeting notes
"""
        path.write_text(template_content)
