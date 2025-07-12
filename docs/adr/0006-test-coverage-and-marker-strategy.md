# Architecture Decision Record (ADR)

## Title
Test Coverage and Marker Strategy

## Status
Accepted

## Date
2025-07-12

## Context
The project needed clear guidelines for test coverage reporting and test categorization through markers. The initial pytest configuration enabled coverage reporting by default for all test executions, which created noise during development and IDE usage. Additionally, the project had multiple test markers (unit, integration, e2e, slow) that required clarification on when and how to use them effectively.

## Decision
We will implement a selective coverage reporting strategy and simplified marker approach:

### Coverage Strategy
- **No default coverage**: Remove coverage options from pytest default configuration
- **Explicit coverage in nox**: Enable coverage only in dedicated nox session for comprehensive testing
- **Focused coverage scope**: Cover only source code (`src/adraitools`), excluding test code from coverage

### Marker Strategy  
- **Simplified categorization**: Use only `e2e` and `slow` markers
- **Default behavior**: Tests without markers are treated as unit/integration tests
- **Marker-based execution**: Use `not e2e` to run fast tests, `e2e` for end-to-end tests

## Rationale

### Coverage Approach
- **Development efficiency**: Developers can run individual tests without coverage overhead
- **Clear reporting context**: Coverage metrics are generated only when explicitly requested
- **Performance**: Avoiding coverage calculation speeds up test execution during development
- **Focused metrics**: E2E test coverage is not meaningful for code coverage analysis

### Marker Simplification
- **Reduced maintenance**: No need to explicitly mark every unit or integration test
- **Practical categorization**: Distinction between fast tests (`not e2e`) and slow tests (`e2e`) is most relevant for development workflow
- **Future flexibility**: `slow` marker available for performance-critical test categorization

## Implications
### Positive Implications
- Faster test execution during development and IDE usage
- Cleaner test output without unwanted coverage reports
- Simplified test categorization with minimal maintenance overhead
- Clear separation between development testing and comprehensive CI testing
- Focused coverage metrics that reflect actual code quality

### Concerns
- Developers must remember to use nox for coverage reporting
- Risk of running tests without coverage awareness during development
- Need to ensure e2e tests are properly marked

## Alternatives
### Always-on coverage
- **Characteristics**: Enable coverage reporting for all test executions
- **Pros**: Consistent coverage awareness, no separate commands needed
- **Cons**: Slower test execution, cluttered output, irrelevant for e2e tests
- **Rejection reason**: Negatively impacts development experience

### Detailed marker hierarchy
- **Characteristics**: Explicit unit, integration, e2e, slow markers for all tests
- **Pros**: Fine-grained test categorization, clear test boundaries
- **Cons**: High maintenance overhead, complex marker management
- **Rejection reason**: Over-engineering for current project needs

### Coverage in separate tool
- **Characteristics**: Use separate coverage tools outside pytest
- **Pros**: Complete separation of concerns
- **Cons**: Additional tool complexity, inconsistent reporting format
- **Rejection reason**: pytest-cov integration provides sufficient functionality

## Future Direction
- Monitor test execution patterns to evaluate if additional markers become necessary
- Consider adding performance markers (`slow`) when test suite grows significantly
- Evaluate coverage thresholds and adjust based on actual project needs
- Potential integration of coverage reporting with CI/CD pipeline

## References
- [pytest markers documentation](https://docs.pytest.org/en/stable/example/markers.html)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Issue #11: Set up pytest for comprehensive testing framework](https://github.com/adrai-org/adr-ai-tools-py/issues/11)