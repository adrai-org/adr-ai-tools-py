# ADR-0011: Adopt pexpect for E2E Testing

## Status
Accepted

## Date
2025-07-14

## Context
The project needs to implement end-to-end (E2E) testing for the CLI application, particularly for interactive features like the `init` command that requires user confirmation. The testing strategy should complement the existing unit testing approach using Typer's CliRunner.

Key requirements for E2E testing:
- Test interactive CLI prompts and user input
- Verify actual command execution in real process environment
- Support future interactive features (ADR creation, search, configuration)
- Integrate with existing pytest-based testing framework

## Decision
Adopt pexpect for E2E testing of interactive CLI functionality.

## Rationale

### Interactive CLI Testing Requirements
The `init` command and future features require testing of interactive scenarios:
- **Directory confirmation**: "Directory 'docs/adr' already exists. Continue? (y/N)"
- **Future ADR creation**: Template selection, metadata input
- **Search functionality**: Result filtering, selection prompts
- **Configuration setup**: Interactive configuration wizards

### pexpect Advantages
- **Real TTY Environment**: Tests CLI in actual terminal environment
- **Interactive Pattern Matching**: Flexible expect/send patterns for complex dialogues
- **Real-time Response**: Can test immediate feedback and progressive output
- **Robust Input Handling**: Handles various input scenarios (Enter, Ctrl+C, timeouts)
- **Unix-native**: Aligns with ADR-0010 platform support decision

### Testing Architecture Integration
- **Complementary to Unit Tests**: pexpect for E2E, CliRunner for unit tests
- **pytest Integration**: Works seamlessly with existing pytest framework
- **Marker System**: Can use `@pytest.mark.e2e` for test organization
- **CI/CD Compatibility**: Runs well in Unix-based CI environments

### Future-proof Design
- **Scalable**: Can handle increasingly complex interactive scenarios
- **Comprehensive**: Tests full user experience including output formatting
- **Realistic**: Tests actual user interaction patterns

## Implications

### Positive Implications
- **Interactive Testing**: Comprehensive testing of user interaction flows
- **Real Environment**: Tests actual process execution and TTY behavior
- **Flexible Pattern Matching**: Can adapt to complex interactive scenarios
- **Better User Experience**: Ensures interactive features work as expected
- **Future-ready**: Supports planned interactive features

### Concerns
- **Unix-only**: Requires Unix-like environment (consistent with ADR-0010)
- **Additional Dependency**: Adds pexpect to development dependencies
- **Learning Curve**: Contributors need to understand pexpect patterns
- **Test Complexity**: More complex than simple subprocess testing

### Mitigation Strategies
- **Documentation**: Provide clear examples of pexpect test patterns
- **Test Helpers**: Create reusable helper functions for common patterns
- **Gradual Adoption**: Start with simple cases, expand complexity over time

## Alternatives

### Continue with subprocess
- **Pros**: Standard library, cross-platform, simple
- **Cons**: Cannot handle interactive input effectively, limited to non-interactive testing
- **Rejected**: Insufficient for interactive CLI testing requirements

### Use pytest-subprocess (mocking)
- **Pros**: Fast execution, predictable results
- **Cons**: Doesn't test real process execution, limited interactive capability
- **Rejected**: Doesn't provide true E2E testing

### Implement custom interaction handler
- **Pros**: Tailored to specific needs
- **Cons**: Significant development overhead, reinventing existing solutions
- **Rejected**: pexpect already provides robust solution

### Use Click's CliRunner for everything
- **Pros**: Consistent testing approach, fast execution
- **Cons**: Doesn't test real CLI environment, limited interactive patterns
- **Rejected**: Not suitable for comprehensive E2E testing

## Future Direction
- **Test Helper Library**: Develop reusable pexpect helpers for common CLI patterns
- **Interactive Feature Testing**: Expand E2E coverage as interactive features are added
- **CI Integration**: Optimize pexpect tests for reliable CI execution
- **Documentation**: Create comprehensive guide for writing pexpect-based E2E tests

## References
- [pexpect Documentation](https://pexpect.readthedocs.io/)
- [pytest Integration with pexpect](https://pexpect.readthedocs.io/en/stable/overview.html)
- [ADR-0010: Platform Support Decision](./0010-limit-platform-support-to-unix-like-systems.md)