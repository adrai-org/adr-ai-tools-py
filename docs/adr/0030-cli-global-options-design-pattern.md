# Architecture Decision Record (ADR)

## Title
CLI Global Options Design Pattern

## Status
Accepted

## Date
2024-07-18

## Context
The CLI application needed to support global options that affect the behavior of all subcommands, specifically logging-related options (--verbose, --quiet, --log-file). The challenge was to implement these options in a way that:

- Follows Typer framework conventions
- Maintains separation of concerns between CLI and service layers
- Provides consistent behavior across all subcommands
- Allows for future extension with additional global options

## Decision
Implement global options using Typer's `@app.callback()` decorator with the following pattern:

**Option Definition**: Use `Annotated` type hints with `typer.Option` for clear parameter documentation
**Service Integration**: Instantiate and configure services directly in the callback function
**Responsibility Separation**: CLI callback handles option parsing and service configuration, services handle actual functionality
**Naming Convention**: Use kebab-case for CLI options (--log-file) and snake_case for Python parameters (log_file)

## Rationale
**Typer Framework Alignment**: The `@app.callback()` decorator is the standard Typer pattern for global options, ensuring consistency with framework conventions.

**Service Layer Architecture (ADR-0015)**: The callback acts as the CLI layer, delegating actual work to appropriate services while maintaining clean separation of concerns.

**Type Safety**: `Annotated` type hints provide clear documentation and enable static type checking of CLI parameters.

**Extensibility**: The callback pattern allows easy addition of new global options without modifying existing subcommand logic.

## Implications
### Positive Implications
- Clear separation between CLI parsing and service logic
- Consistent global option behavior across all subcommands
- Type-safe CLI parameter handling
- Easy to extend with additional global options
- Follows established Typer patterns

### Concerns
- Service configuration happens early in CLI lifecycle
- Global options are processed even when not needed by specific subcommands
- Callback function could become complex with many global options

## Alternatives
### Subcommand-level options
**Characteristics**: Add logging options to each individual subcommand
**Pros**: More granular control, options only processed when needed
**Cons**: Duplicated option definitions, inconsistent behavior possible, harder to maintain

### Configuration file only
**Characteristics**: Store logging preferences in configuration file
**Pros**: Persistent settings, cleaner CLI interface
**Cons**: Less flexible for one-off usage, harder to debug issues

### Environment variables
**Characteristics**: Use environment variables for logging configuration
**Pros**: Works well in containerized environments, persistent across commands
**Cons**: Less discoverable, harder to document, potential conflicts

## Future Direction
- Consider option grouping if global options become numerous
- Evaluate configuration file integration for persistent preferences
- Potential for context-aware option validation
- Consider subcommand-specific option inheritance patterns

## References
- ADR-0015: Service Layer Architecture for CLI Commands
- ADR-0029: LoggingService Infrastructure Architecture
- Typer documentation: https://typer.tiangolo.com/tutorial/commands/callback/
- Issue #19: Implement logging strategy for CLI application