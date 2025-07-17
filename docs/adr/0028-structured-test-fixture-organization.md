# ADR-0028: Structured Test Fixture Organization

## Status
Accepted

## Date
2025-07-17

## Context
Test fixtures often return complex data structures or multiple related objects. Without structured organization, fixture return values are accessed through unclear tuple unpacking or attribute access patterns, leading to maintenance issues and reduced code clarity.

## Decision
Use `NamedTuple` for structured fixture return values and implement layered fixture organization by test scope and responsibility.

## Rationale
- **Clear Structure**: NamedTuple provides named access to fixture components
- **Type Safety**: Structured types enable better type checking
- **Organization**: Layered fixtures separate concerns by test type and scope
- **Maintainability**: Centralized fixture definitions reduce duplication

## Implications
### Positive Implications
- Improved code readability with named attribute access
- Better refactoring safety with structured types
- Reduced test setup duplication across modules

### Concerns
- Slightly more verbose fixture definitions
- Need to maintain NamedTuple definitions alongside implementations

## Alternatives
### Plain Tuple Returns
- **Pros**: Minimal syntax
- **Cons**: Unclear structure, positional access only
- **Rejected**: Poor readability and maintainability

### Dictionary Returns
- **Pros**: Named access, flexible structure
- **Cons**: No type safety, runtime key errors
- **Rejected**: Lacks compile-time type checking

## Future Direction
- Migrate existing fixtures to use structured return types
- Establish naming conventions for fixture organization
- Consider fixture dependency optimization

## References
- [NamedTuple documentation](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
- [pytest fixtures documentation](https://docs.pytest.org/en/stable/fixture.html)
- [ADR-0025: Shared Test Fixtures Pattern](./0025-shared-test-fixtures-pattern.md)
- [ADR-0027: Protocol Types for Test Fixtures](./0027-protocol-types-for-test-fixtures.md)