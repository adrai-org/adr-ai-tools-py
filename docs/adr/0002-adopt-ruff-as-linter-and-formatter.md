# Architecture Decision Record (ADR)

## Title
Adopt Ruff as Python Linter and Formatter

## Status
Accepted

## Date
2025-05-17

## Context
The adr-ai-tools-py project requires consistent code quality and style across all code contributions. We need a tool that can:

- Enforce coding standards and identify potential issues
- Format code consistently across the project
- Integrate well with our existing development workflow
- Have minimal performance impact on development and CI/CD pipelines
- Support our Python 3.11+ requirement
- Work well with our chosen dependency manager (UV)

Previously, Python projects often required multiple tools such as flake8 for linting, black for formatting, isort for import sorting, and additional plugins for more specialized checks. This fragmentation creates complexity in configuration and can lead to inconsistent enforcement of standards.

## Decision
We have decided to adopt Ruff as our primary Python linter and formatter for the adr-ai-tools-py project.

## Rationale
Ruff was selected for the following reasons:

- **Performance**: Ruff is implemented in Rust, making it significantly faster than traditional Python-based tools like flake8, pylint, or black.
- **Consolidation**: Ruff combines linting, formatting, and import sorting in a single tool, reducing the number of dependencies and configuration files needed.
- **Compatibility**: Ruff is designed to be compatible with popular tools like flake8 and black, making migration straightforward.
- **Extensibility**: Ruff supports a wide range of rules, including those from flake8 plugins, providing comprehensive code quality checks.
- **Modern Standards**: Ruff fully supports modern Python features and has good compatibility with Python 3.11+.
- **Active Development**: Ruff has an active development community with regular updates and improvements.
- **IDE Integration**: Ruff works well with popular IDEs and editors used by our team.
- **Configuration**: Ruff configuration is straightforward and can be included in our pyproject.toml file.

## Implications
### Positive Implications
- Significantly faster linting and formatting will improve developer productivity
- Consistent code style across the codebase will improve readability and maintenance
- Single tool for multiple functions reduces cognitive load and configuration complexity
- Better CI/CD performance due to faster checks
- Comprehensive rule set catches more potential issues
- Simplified onboarding for new contributors with a single tool to learn

### Concerns
- Ruff is relatively newer compared to established tools like flake8 or pylint
- Some team members may need to adjust to Ruff-specific rules and configuration
- Certain specialized linting rules may not yet be available in Ruff
- Migration from other tools may require adjustments to existing code

## Alternatives
### flake8 + black + isort
- **Pros**: Well-established tools with mature ecosystems, widely understood
- **Cons**: Multiple tools to configure and maintain, slower performance, potential conflicts
- **Rejection Reason**: Complexity of managing multiple tools and significantly slower performance

### pylint
- **Pros**: Very comprehensive checks, highly configurable
- **Cons**: Extremely slow performance, verbose output, complex configuration
- **Rejection Reason**: Performance issues and complexity outweigh the benefits

### pycodestyle/pep8
- **Pros**: Focuses specifically on PEP 8 style guidelines, simple
- **Cons**: Limited scope, no formatting capabilities, no modern rule sets
- **Rejection Reason**: Too limited in functionality for our needs

### mypy (for type checking only)
- **Pros**: Excellent static type checking
- **Cons**: Focused only on type checking, requires additional tools for style and linting
- **Rejection Reason**: Too specialized; we still need Ruff for other linting tasks (Note: We may adopt mypy alongside Ruff in the future specifically for type checking)

## Future Direction
- Create standardized Ruff configurations for the project
- Document Ruff usage in the contributor guidelines
- Set up pre-commit hooks to run Ruff automatically
- Integrate Ruff checks into our CI/CD pipeline
- Periodically update Ruff to take advantage of new rules and improvements
- Consider adding mypy for static type checking to complement Ruff's capabilities

## References
- Ruff documentation: https://github.com/astral-sh/ruff
- Performance benchmarks comparing Ruff to other linting/formatting tools
- Current project setup with Ruff configuration in pyproject.toml
- Team discussions about code quality enforcement requirements