# ADR-0022: Runtime Type Introspection Pattern for Dynamic Type Conversion

## Status
Accepted

## Date
2025-07-15

## Context
The configuration management system needs to convert string values from CLI input to appropriate Python types based on Pydantic model field annotations. Since CLI commands always receive string arguments, but configuration fields may have various types (Path, str, int, etc.), a mechanism is needed to perform runtime type conversion while maintaining type safety.

## Decision
Use Python's `typing.get_origin()` for runtime type introspection combined with Pydantic model field metadata to dynamically convert string values to appropriate types based on field annotations.

## Rationale
- **Type safety**: Leverages Pydantic's type annotations as the source of truth
- **Dynamic conversion**: Handles different field types without hardcoding type mappings
- **Maintainability**: Adding new configuration field types doesn't require code changes
- **Standard library approach**: Uses Python's built-in typing utilities rather than external libraries
- **Pydantic integration**: Works seamlessly with Pydantic model introspection

## Implications

### Positive Implications
- Automatic type conversion based on model definitions
- Type-safe configuration value handling
- Extensible pattern for future configuration field types
- Consistent approach that can be reused across services

### Concerns
- Runtime type introspection adds complexity
- Potential performance impact for frequently called operations
- Limited to types that can be constructed from string representations

## Alternatives
- **Hardcoded type mapping**: Manual mapping of field names to types - rejected due to maintenance burden
- **Pydantic parsing**: Use Pydantic's built-in parsing for each field - rejected due to complexity of isolating single field validation
- **String-only configuration**: Keep all values as strings - rejected due to loss of type safety and API clarity

## Future Direction
- Monitor for additional configuration field types that may need special handling
- Consider caching type introspection results if performance becomes a concern
- Evaluate extending pattern to other services that need dynamic type conversion

## References
- [Python typing module documentation](https://docs.python.org/3/library/typing.html)
- [Pydantic model introspection](https://docs.pydantic.dev/latest/concepts/models/#model-introspection)
- [ADR-0018: Adopt Pydantic Settings for Configuration Management](./0018-adopt-pydantic-settings-for-configuration-management.md)