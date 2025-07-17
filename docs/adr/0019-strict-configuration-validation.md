# ADR-0019: Strict Configuration Validation

## Status
Accepted

## Date
2025-07-15

## Context
Configuration management needs to handle unknown or misspelled configuration keys. The application must decide whether to silently ignore unknown keys or provide strict validation with clear error messages.

## Decision
Use strict validation with `extra="forbid"` in Pydantic Settings to reject unknown configuration keys.

## Rationale
- **Error Prevention**: Catches configuration typos and mistakes early
- **Clear Feedback**: Provides explicit error messages for invalid keys
- **Configuration Integrity**: Ensures all configuration is recognized and valid
- **Developer Experience**: Immediate feedback on configuration errors

## Implications

### Positive Implications
- Clear error messages for configuration mistakes
- Prevents silent failures from typos
- Maintains configuration file integrity

### Concerns
- May break existing configurations with unknown keys
- Requires careful configuration file maintenance

## Alternatives
- **Permissive validation** (`extra="ignore"`): Silently ignores unknown keys but allows errors
- **Warning approach** (`extra="allow"`): Accepts but could log warnings

## Future Direction
- Monitor for any breaking changes in existing configurations
- Consider validation helpers for configuration file checking

## References
- [Pydantic Extra Fields Documentation](https://docs.pydantic.dev/latest/concepts/models/#extra-fields)
- [ADR-0018: Adopt Pydantic Settings](./0018-adopt-pydantic-settings-for-configuration-management.md)