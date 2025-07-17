# ADR-0021: TOML Parsing Library Selection for Configuration Persistence

## Status
Accepted

## Date
2025-07-15

## Context
The configuration management system requires TOML file parsing for both reading and writing configuration files. While Pydantic Settings provides built-in TOML support for reading configuration files, the configuration persistence functionality (config set operations) requires explicit control over TOML file writing to implement merge-based updates and maintain precise control over file formatting.

## Decision
Use `tomli` for reading TOML files and `tomli-w` for writing TOML files in the ConfigurationService, rather than relying solely on Pydantic Settings' built-in TOML support.

## Rationale
- **Explicit control**: Direct TOML manipulation allows merge-based updates that preserve existing configuration values
- **Write capability**: Pydantic Settings focuses on reading configuration, not writing
- **Standard library alignment**: `tomli` is the reference implementation that will be included in Python 3.11+ standard library
- **Separation of concerns**: Configuration reading (Pydantic Settings) vs configuration writing (explicit TOML manipulation)
- **File formatting control**: Ensures consistent TOML output format

## Implications

### Positive Implications
- Fine-grained control over TOML file structure and formatting
- Enables merge-based configuration updates without data loss
- Clear separation between configuration loading and persistence logic
- Uses standard library-aligned implementation

### Concerns
- Additional dependencies beyond Pydantic Settings
- Manual TOML serialization instead of leveraging Pydantic's built-in mechanisms
- Potential for inconsistency between reading and writing implementations

## Alternatives
- **Pydantic Settings only**: Use only Pydantic's built-in TOML support - rejected due to lack of write capability and merge functionality
- **toml library**: Use the older `toml` library - rejected due to lack of Python 3.11+ compatibility
- **Custom TOML implementation**: Build custom TOML handling - rejected due to unnecessary complexity

## Future Direction
- Monitor Python 3.11+ adoption for potential migration to standard library `tomllib`
- Consider consolidating TOML operations if Pydantic Settings adds write capabilities

## References
- [tomli library documentation](https://github.com/hukkin/tomli)
- [tomli-w library documentation](https://github.com/hukkin/tomli-w)
- [ADR-0018: Adopt Pydantic Settings for Configuration Management](./0018-adopt-pydantic-settings-for-configuration-management.md)
- [ADR-0020: Configuration File Persistence Strategy](./0020-configuration-file-persistence-strategy.md)