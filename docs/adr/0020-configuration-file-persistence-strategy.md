# ADR-0020: Configuration File Persistence Strategy

## Status
Accepted

## Date
2025-07-15

## Context
The configuration management system requires a persistence strategy for the `config set` command. The system supports multiple configuration sources with precedence: project-local > global > defaults. When users modify configuration through CLI commands, the system must decide where to persist these changes while maintaining the established precedence hierarchy.

## Decision
Implement a **dual persistence strategy** where:
1. `config set` operations write to project-local configuration files (`.adr-ai-tools/config.toml`) by default
2. `config set --global` operations write to global configuration files (`~/.config/adr-ai-tools/config.toml`)
3. Use merge-based updates that preserve existing configuration values in both cases
4. Create configuration directories automatically if they don't exist

## Rationale
- **User choice**: Provides flexibility for both project-specific and global configuration management
- **Predictable behavior**: Clear distinction between local and global scope through explicit flags
- **Version control friendly**: Project-local configs can be committed to repositories
- **Team collaboration**: Teams can share project-specific settings while maintaining personal global preferences
- **Merge safety**: Preserving existing values prevents accidental configuration loss

## Implications

### Positive Implications
- Clear distinction between project and global configuration scope
- Project-local configuration files can be version controlled
- Users can maintain both project-specific and global preferences
- Explicit control over configuration scope through CLI flags

### Concerns
- Users need to understand the difference between local and global configuration
- Two configuration files to manage instead of one

## Alternatives
- **Project-local only**: Simple but doesn't support global user preferences - rejected due to limited flexibility
- **Global only**: Simpler but complicates team collaboration - rejected due to version control issues
- **Automatic scope detection**: Complex logic based on existing files - rejected due to unpredictable behavior

## Future Direction
- Monitor usage patterns between local and global configurations
- Consider adding commands like `config promote` to copy settings between scopes

## References
- [ADR-0018: Adopt Pydantic Settings for Configuration Management](./0018-adopt-pydantic-settings-for-configuration-management.md)
- [ADR-0019: Strict Configuration Validation](./0019-strict-configuration-validation.md)