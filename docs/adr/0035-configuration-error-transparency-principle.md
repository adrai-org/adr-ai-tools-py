# ADR-0035: Configuration Error Transparency Principle

## Title
Configuration Error Transparency Principle

## Status
Accepted

## Date
2025-09-17

## Context
Configuration file handling needs to balance user experience with system robustness. When configuration files are corrupted or invalid, the system must decide whether to silently ignore the problematic files or explicitly report the issues to users.

The `doctor` command revealed that corrupted configuration files could be silently ignored, leaving users unaware that their intended configuration is not being applied. This creates confusion when users expect certain settings to be active but they are actually being ignored due to file corruption.

## Decision
Adopt a transparency principle for configuration errors: explicitly report configuration file problems to users with specific file paths and actionable information rather than silently ignoring corrupted files.

## Rationale
- **User Awareness**: Users need to know when their configuration is not being applied
- **Actionable Information**: File paths and specific error details enable users to fix problems
- **Trust**: Transparent error reporting builds user confidence in the system
- **Debugging Efficiency**: Clear error messages reduce support burden and troubleshooting time

## Implications

### Positive Implications
- Users can identify and fix configuration problems quickly
- No silent failures that lead to unexpected behavior
- Enhanced user trust through transparent error communication
- Reduced debugging time for configuration issues

### Concerns
- **Verbose error output**: May overwhelm users with too much technical information
  - *Mitigation*: Design clear, user-friendly error message formats with essential information highlighted
- **Technical complexity for non-technical users**: Error messages may be difficult to understand
  - *Mitigation*: Include suggested actions and links to documentation in error messages

## Alternatives

### Silent Ignore Strategy
- **Key characteristics**: Skip corrupted configuration files without notifying users
- **Pros**: Simple implementation, no user disruption, system continues to function
- **Cons**: Users unaware of configuration problems, debugging difficulties, unexpected behavior
- **Reasons for rejection**: Leaves users confused about why their configuration isn't working

### Warning-Only Approach
- **Key characteristics**: Log warnings about corrupted files but continue operation
- **Pros**: Less disruptive than errors, provides some user feedback
- **Cons**: Warnings are frequently ignored or missed, doesn't force problem resolution
- **Reasons for rejection**: Users often miss warnings, leading to same confusion as silent failures

### Best-Effort Parsing
- **Key characteristics**: Attempt to parse what's possible from corrupted files
- **Pros**: Maximizes configuration usage, potentially less user disruption
- **Cons**: Complex implementation, unpredictable behavior, partial configuration may be worse than none
- **Reasons for rejection**: Unclear behavior creates more confusion than helpful recovery

## Future Direction
- Apply this principle to other configuration-related errors
- Consider user-friendly error message formatting
- Evaluate options for different verbosity levels based on user preferences

## References
- [ADR-0019: Strict Configuration Validation](./0019-strict-configuration-validation.md)
- [ADR-0034: Custom Exception Strategy](./0034-custom-exception-strategy-for-domain-specific-errors.md)