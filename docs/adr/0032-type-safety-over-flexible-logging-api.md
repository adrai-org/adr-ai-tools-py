# Architecture Decision Record (ADR)

## Title
Type Safety Over Flexible Logging API

## Status
Accepted

## Date
2024-07-18

## Context
When implementing LoggingService, we faced a choice between providing a flexible logging API with `**kwargs` support (similar to Python's logging module) or maintaining strict type safety with explicit method signatures.

The flexible approach would allow:
```python
service.log_info("User %s logged in", username)
service.log_error("Error occurred", exc_info=True)
```

The type-safe approach requires:
```python
service.log_info(f"User {username} logged in")
service.log_error("Error occurred")
```

## Decision
Prioritize type safety by using explicit method signatures without `**kwargs`:

**Method Signatures**: All logging methods use explicit, typed parameters
**Current Implementation**: Start with simple `message: str` parameter
**Future Extensions**: Add necessary parameters as explicit, typed arguments when needed
**Type Checking**: Ensure all logging calls are statically verifiable by mypy
**API Predictability**: Provide discoverable, well-documented method interfaces

## Rationale
**Type Safety First**: The project prioritizes type safety (ADR-0004) and static analysis. `**kwargs` parameters cannot be statically verified and may cause runtime errors.

**API Predictability**: Explicit method signatures are easier to understand, document, and test. There's no ambiguity about what parameters are accepted.

**Consistency**: All service interfaces in the project use explicit, typed parameters rather than flexible `**kwargs` patterns.

**Development Experience**: IDE auto-completion and type checking work better with explicit parameters, improving developer productivity.

**Incremental Enhancement**: New parameters can be added as explicit arguments when use cases emerge, maintaining type safety throughout evolution.

## Implications
### Positive Implications
- Complete static type checking of all logging calls
- Clear, predictable API that's easy to understand and use
- Better IDE support with auto-completion and error detection
- Consistent with other service interfaces in the project
- Eliminates runtime errors from incorrect parameter usage
- API can evolve incrementally with explicit parameter additions

### Concerns
- Less flexible than Python's standard logging interface initially
- Requires API evolution when new parameters are needed
- May be less familiar to developers used to logging module patterns

## Alternatives
### Flexible kwargs interface
**Characteristics**: Support `**kwargs` with `Any` type annotation
**Pros**: More flexible, familiar to logging module users
**Cons**: No type safety, potential runtime errors, harder to test

### Multiple method overloads
**Characteristics**: Provide both simple and flexible method variants
**Pros**: Best of both worlds, gradual adoption
**Cons**: API complexity, maintenance burden, potential confusion

### Typed kwargs with TypedDict
**Characteristics**: Use TypedDict to define allowed kwargs
**Pros**: Type safety with some flexibility
**Cons**: Complex type definitions, limited kwargs support

## Future Direction
- Add explicit parameters (e.g., `exc_info: bool`, `extra: dict`) when specific use cases emerge
- Consider structured logging support for complex logging scenarios
- Evaluate logging method specialization for common patterns
- Monitor developer feedback for most needed parameter additions

## References
- ADR-0004: Adopt mypy for static type checking
- ADR-0029: LoggingService Infrastructure Architecture
- Python typing documentation: https://docs.python.org/3/library/typing.html
- Issue #19: Implement logging strategy for CLI application