# Architecture Decision Record (ADR)

## Title
Constants Extraction Pattern

## Status
Accepted

## Date
2025-07-17

## Context
As applications grow, magic strings and hardcoded values tend to proliferate throughout the codebase. This creates several problems:

- **Maintenance burden**: Changing a value requires finding and updating multiple locations
- **Inconsistency**: Similar values may have slight variations across different modules
- **Error-prone**: Typos in hardcoded strings can introduce bugs
- **Poor discoverability**: Developers may not be aware of existing constants and create duplicates

We need a consistent approach to manage shared constants across the application.

## Decision
We will extract constants, magic strings, and reusable values into a centralized constants module organized by domain:

- Constants should be grouped into logical classes by their purpose
- Path-related constants should include helper methods for path resolution
- Error messages should be templated strings for consistency
- Only extract constants that are shared across multiple modules

## Rationale
This decision was made based on:

- **Technical considerations**: Centralized constants improve maintainability and reduce duplication
- **Code quality**: Consistent error messages and path handling improve user experience
- **Team capabilities**: Pattern is straightforward to implement and understand
- **Maintenance efficiency**: Single source of truth reduces bugs and update overhead

## Implications
### Positive Implications
- **Single Source of Truth**: All shared constants are defined in one place
- **Easier Maintenance**: Changes require updates in only one location
- **Consistency**: Values are uniform across the application
- **Type Safety**: Constants can be properly typed and validated

### Concerns
- **Additional Indirection**: Accessing constants requires importing from the constants module
- **Potential Over-engineering**: Risk of extracting constants that don't need to be shared
- **Module Coupling**: Services become dependent on the constants module

## Alternatives
### Inline Constants
- **Characteristics**: Define constants directly in the modules where they're used
- **Pros**: No additional indirection, simpler initial implementation
- **Cons**: Duplication across modules, harder to maintain consistency
- **Rejection reason**: Doesn't solve the core problem of duplication and inconsistency

### Configuration-based Constants
- **Characteristics**: Store constants in configuration files
- **Pros**: Runtime configurability, external management
- **Cons**: Overhead for simple constants, requires configuration management
- **Rejection reason**: Adds unnecessary complexity for compile-time constants

## Future Direction
- Monitor usage patterns to identify constants that should be extracted
- Consider splitting constants module if it grows too large
- Evaluate opportunities for compile-time constant validation
- Review extraction guidelines periodically to prevent over-engineering

## References
- [Replace Magic Literal - Martin Fowler's Refactoring Catalog](https://refactoring.com/catalog/replaceMagicLiteral.html)
- [Constants in Java: Patterns and Anti-Patterns | Baeldung](https://www.baeldung.com/java-constants-good-practices)
- [Replace Magic Number with Symbolic Constant | Refactoring.Guru](https://refactoring.guru/replace-magic-number-with-symbolic-constant)
- [Refactoring 003 — Extract Constant | Medium](https://mcsee.medium.com/refactoring-003-extract-constant-cd15db177983)