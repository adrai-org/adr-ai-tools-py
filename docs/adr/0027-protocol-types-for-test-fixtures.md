# ADR-0027: Protocol Types for Test Fixtures

## Status
Accepted

## Date
2025-07-17

## Context
Test fixtures traditionally lack proper type hints, making it difficult to understand fixture return types and catch type-related errors at development time. Without explicit interfaces, fixtures can have unclear contracts and provide poor IDE support.

## Decision
Adopt `typing.Protocol` for defining explicit fixture interfaces, providing type-safe contracts for test fixture functions.

## Rationale
Protocol types provide:
- **Explicit Contracts**: Clear interfaces for fixture functions
- **IDE Support**: Better autocompletion and type checking
- **Runtime Safety**: Type checkers catch interface mismatches early
- **Documentation**: Protocols serve as living documentation

## Implications
### Positive Implications
- Type safety prevents runtime errors
- Better developer experience with IDE support
- Self-documenting fixture contracts

### Concerns
- Additional boilerplate code for type definitions
- Learning curve for developers unfamiliar with Protocol types

## Alternatives
### Duck Typing with Type Comments
- **Pros**: Minimal syntax overhead
- **Cons**: Weak type safety, poor IDE support
- **Rejected**: Insufficient type guarantees

### Abstract Base Classes
- **Pros**: Explicit inheritance relationships
- **Cons**: Runtime overhead, rigid inheritance
- **Rejected**: Protocols provide structural typing without inheritance

## Future Direction
- Migrate existing fixtures to use Protocol types
- Create fixture templates for common patterns
- Explore generic Protocol types for reusable patterns

## References
- [PEP 544 - Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
- [typing.Protocol documentation](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [ADR-0025: Shared Test Fixtures Pattern](./0025-shared-test-fixtures-pattern.md)