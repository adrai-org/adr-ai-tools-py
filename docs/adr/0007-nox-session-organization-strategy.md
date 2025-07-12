# Architecture Decision Record (ADR)

## Title
Nox Session Organization Strategy

## Status
Accepted

## Date
2025-07-12

## Context
The project uses nox for automating testing and code quality checks across multiple Python versions. The organization of nox sessions directly impacts developer workflow, CI efficiency, and maintenance overhead. We needed to establish clear patterns for session naming, responsibility, and execution strategy that balance granular control with simplicity.

## Decision
We will organize nox sessions into distinct categories with clear responsibilities:

### Test Sessions
- **`tests_unit`**: Fast tests excluding e2e (`pytest -m "not e2e"`)
- **`tests_e2e`**: End-to-end tests only (`pytest -m "e2e"`)
- **`tests`**: All tests with comprehensive coverage reporting
- **`tests_all_versions`**: All tests across Python 3.9-3.13 (no coverage)

### Code Quality Sessions
- **`mypy`**: Type checking for source and test code
- **`lint`**: Ruff linting checks
- **`format_code`**: Ruff code formatting

### Composite Sessions
- **`quality`**: Combined type checking and linting
- **`check_all`**: Complete validation (tests + type checking + linting)

## Rationale

### Session Granularity
- **Targeted execution**: Developers can run specific checks during development
- **Fast feedback loops**: Unit tests can be run quickly without e2e overhead
- **Flexible CI**: Different CI stages can run appropriate session combinations

### Naming Convention
- **Descriptive prefixes**: `tests_*` for testing, clear purpose identification
- **Underscore separation**: Consistent with Python naming conventions
- **Composite clarity**: `quality` and `check_all` indicate combined operations

### Python Version Strategy
- **Development focus**: Single version (3.11) for daily development tasks
- **Compatibility validation**: Multi-version testing (3.9-3.13) for compatibility assurance
- **Performance optimization**: Avoid multi-version overhead for development sessions

### Responsibility Separation
- **Single concern**: Each session has one primary responsibility
- **Composability**: Composite sessions combine single-concern sessions
- **Independence**: Sessions can be run individually without dependencies

## Implications
### Positive Implications
- Clear development workflow with appropriate session for each use case
- Fast iteration during development with targeted session execution
- Comprehensive validation available for CI and release processes
- Consistent session interface across different types of checks
- Easy to add new sessions following established patterns

### Concerns
- Increased number of sessions to maintain and document
- Potential confusion about which session to use for specific scenarios
- Need to keep composite sessions synchronized with individual sessions

## Alternatives
### Monolithic Sessions
- **Characteristics**: Few sessions covering broad functionality
- **Pros**: Simpler session management, fewer commands to remember
- **Cons**: Slow feedback loops, inability to run targeted checks
- **Rejection reason**: Poor developer experience during iterative development

### Command-line Parameter Approach
- **Characteristics**: Single session with extensive parameter customization
- **Pros**: Single interface, flexible configuration
- **Cons**: Complex parameter management, unclear execution patterns
- **Rejection reason**: Reduces nox's declarative advantage

### Tool-specific Sessions Only
- **Characteristics**: One session per tool (pytest, mypy, ruff), no composites
- **Pros**: Clear tool boundaries, minimal session count
- **Cons**: No convenient way to run related checks together
- **Rejection reason**: Misses common workflow patterns

## Future Direction
- Monitor session usage patterns to identify optimization opportunities
- Consider adding specialized sessions for performance testing or documentation
- Evaluate integration with pre-commit hooks for automated session execution
- Potential addition of deployment or release validation sessions
- Consider parameterized sessions if configuration complexity increases

## References
- [Nox documentation](https://nox.thea.codes/)
- [Issue #9: Set up nox for automated testing and code quality checks](https://github.com/adrai-org/adr-ai-tools-py/issues/9)
- [ADR 0006: Test Coverage and Marker Strategy](./0006-test-coverage-and-marker-strategy.md)