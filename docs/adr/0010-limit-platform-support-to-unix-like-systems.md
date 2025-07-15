# ADR-0010: Limit Platform Support to Unix-like Systems

## Status
Accepted

## Date
2025-07-14

## Context
The project needs to define the scope of supported platforms for adr-ai-tools. As a developer-focused tool for managing Architecture Decision Records, we must balance development velocity with platform accessibility.

Key considerations include:
- Target audience (primarily developers working in Unix-like environments)
- Testing framework capabilities and development tool ecosystem
- Development and maintenance overhead of cross-platform support
- Quality assurance across different operating systems

## Decision
Limit platform support to Unix-like systems (Linux, macOS, WSL on Windows) for the initial development phase, with Windows support as future work.

## Rationale

### Target Audience Alignment
- **Developer-focused Tool**: ADR tools are primarily used by software development teams
- **Unix-prevalent Environment**: Most development, CI/CD, and deployment environments are Unix-based
- **Development Workflow**: Software teams typically work in Unix-like environments

### Technical Considerations
- **Testing Framework**: pexpect (essential for interactive CLI testing) is Unix-native
- **Python Limitations**: Key features like `os.fork()`, Unix-specific signals, and process management are not available on Windows
- **Development Tools**: Unix-specific tools provide better development experience

### Quality Assurance
- **Testing Coverage**: Cannot properly test Windows compatibility without Windows development environment
- **Maintenance Burden**: Supporting untested platforms creates maintenance debt
- **User Experience**: Better to explicitly not support than to provide poor, untested experience

### Development Efficiency
- **Simplified CI/CD**: Single platform family reduces complexity
- **Faster Development**: No need to handle platform-specific edge cases
- **Better Tool Selection**: Can use Unix-specific development tools without workarounds

## Implications

### Positive Implications
- **Quality Focus**: Can provide excellent experience on supported platforms
- **Development Velocity**: Faster development without cross-platform considerations
- **Tool Selection Freedom**: Access to Unix-specific development tools
- **Clear Expectations**: Users know exactly what is supported

### Concerns
- **Limited User Base**: Excludes Windows-only developers (temporarily)
- **Market Reach**: Smaller initial addressable market
- **Community Growth**: May limit initial contributor pool

### Mitigation Strategies
- **WSL Documentation**: Provide clear setup instructions for Windows users
- **Future Roadmap**: Clearly communicate Windows support as planned future work
- **Community Engagement**: Actively seek feedback from Windows users for future implementation

## Alternatives

### Immediate Cross-platform Support
- **Pros**: Broader initial user base, wider market reach
- **Cons**: Significant development overhead, testing complexity, quality risks for untested platforms
- **Rejected**: Would compromise quality and development velocity

### Windows-first Development
- **Pros**: Largest developer platform
- **Cons**: Misaligned with typical ADR usage patterns, technical limitations
- **Rejected**: Doesn't match target environment characteristics

### Docker-only Distribution
- **Pros**: Consistent environment across all platforms
- **Cons**: Additional complexity for users, resource overhead
- **Rejected**: Adds unnecessary friction for a CLI tool

## Future Direction
- **Windows Support**: Plan Windows support for future major version
- **Cross-platform Testing**: Implement Windows testing when adding support
- **Community Feedback**: Gather Windows user requirements for future implementation
- **WSL Integration**: Optimize experience for Windows users via WSL

## References
- [Python os.fork() Documentation](https://docs.python.org/3/library/os.html#os.fork)
- [Microsoft WSL Python Development Guide](https://learn.microsoft.com/en-us/windows/python/beginners)
- [pexpect Documentation](https://pexpect.readthedocs.io/)