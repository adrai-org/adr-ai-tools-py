# ADR-0023: File System Path Conventions for Application Data

## Status
Accepted

## Date
2025-07-15

## Context
The application needs to store configuration files and potentially other application data in consistent, predictable locations on the file system. The system must support both project-local and global configuration scopes while following established conventions for application data storage across different operating systems.

## Decision
Adopt the following file system path conventions:
- **Project-local configuration**: `.adr-ai-tools/config.toml` (relative to project root)
- **Global configuration**: `~/.config/adr-ai-tools/config.toml` (following XDG Base Directory Specification)
- **Automatic directory creation**: Create directories with appropriate permissions when needed

## Rationale
- **XDG compliance**: Global configuration follows XDG Base Directory Specification widely adopted on Unix-like systems
- **Version control friendly**: Project-local configuration uses dotfile convention, easily ignored or included as needed
- **Predictable locations**: Users and tools can reliably find configuration files
- **Namespace isolation**: Application-specific subdirectory prevents conflicts with other tools
- **Cross-platform compatibility**: Paths work consistently across supported Unix-like systems

## Implications

### Positive Implications
- Consistent and predictable file locations for users and automation
- Follows established conventions familiar to Unix users
- Clear separation between project and user scope
- Compatible with version control workflows

### Concerns
- Creates hidden directories that may not be obvious to users
- Directory creation requires appropriate file system permissions
- May accumulate configuration files in project directories over time

## Alternatives
- **Single global configuration**: Store all configuration globally - rejected due to lack of project-specific customization
- **Configuration in project root**: Use visible filenames like `adr-config.toml` - rejected due to namespace pollution
- **Platform-specific paths**: Use different conventions per OS - rejected due to added complexity for cross-platform support

## Future Direction
- Consider configuration cleanup utilities for removing unused project-local configurations
- Monitor for potential conflicts with other tools using similar directory names
- Evaluate extending pattern for other application data (templates, cache, logs)

## References
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [ADR-0010: Limit Platform Support to Unix-like Systems](./0010-limit-platform-support-to-unix-like-systems.md)
- [ADR-0020: Configuration File Persistence Strategy](./0020-configuration-file-persistence-strategy.md)