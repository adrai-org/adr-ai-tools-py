# ADR-0033: Directory Structure for Three-Layer Architecture

## Title
Directory Structure for Three-Layer Architecture

## Status
Accepted

## Date
2025-07-21

## Context
The current codebase follows the three-layer service-oriented architecture defined in ADR-0015, but the physical directory structure does not clearly reflect the architectural layers. All services (both business logic and infrastructure) are currently placed in a single `src/adraitools/services/` directory, which creates confusion about layer boundaries and makes it difficult for new contributors to understand the architectural intent.

Key challenges include:
- Mixed placement of business logic and infrastructure services in the same directory
- Lack of clear physical boundaries between architectural layers
- Difficulty in understanding code organization without deep knowledge of ADR-0015
- Potential for architectural violations due to unclear boundaries

The current structure:
```
src/adraitools/
├── services/
│ ├── adr_initializer.py # Business Logic
│ ├── file_system_service.py # Infrastructure
│ ├── user_interaction_service.py # Infrastructure
│ └── configuration_service.py # Infrastructure
└── cli.py # CLI Layer
```

## Decision
Reorganize the directory structure to physically reflect the three-layer architecture defined in ADR-0015 by creating distinct directories for each architectural layer:

```
src/adraitools/
├── cli/             # CLI Layer (Presentation)
├── services/        # Service Layer (Business Logic)
└── infrastructure/  # Infrastructure Layer (External Dependencies)
```

Each layer directory will contain:
- **CLI Layer**: Command-line interface implementations, argument parsing, and user I/O formatting
- **Service Layer**: Business logic services that coordinate operations and implement core workflows
- **Infrastructure Layer**: Services that handle external dependencies, file system operations, configuration, and system interactions

**Example structure** (specific file placement to be determined through individual analysis):
```
src/adraitools/
├── cli/
│   ├── __init__.py
│   └── cli.py
├── services/
│   ├── __init__.py
│   └── adr_initializer.py
└── infrastructure/
    ├── __init__.py
    ├── constants.py
    ├── file_system_service.py
    ├── user_interaction_service.py
    └── configuration_service.py
```

The actual placement of each file will be determined through analysis of each class's responsibilities and dependencies to ensure proper layer assignment based on ADR-0015 criteria.

## Rationale
### Architectural Clarity
- **ADR-0015 Compliance**: Directory structure directly reflects the documented architecture decision
- **Clear Layer Boundaries**: Physical directories match the logical architecture layers

### Maintainability Benefits
- **Prevent Layer Violations**: Clear boundaries make it harder to accidentally violate architectural principles
- **Documentation Alignment**: Code organization matches architectural documentation

### Team Productivity
- **Reduced Cognitive Load**: Less mental mapping between physical and logical structure

## Implications
### Positive Implications
- **Enhanced Code Organization**: Clear separation of concerns at the directory level
- **Improved Maintainability**: Easier to locate and modify code within specific layers
- **Better Architecture Enforcement**: Physical structure reinforces architectural decisions
- **Simplified Navigation**: Developers can quickly find relevant code based on layer responsibility

### Concerns
- **Migration Effort**: Existing imports and references need to be updated
- **Temporary Disruption**: Development workflow may be temporarily affected during migration

### Mitigation Strategies
- **Gradual Migration**: Implement changes incrementally to minimize disruption
- **Automated Refactoring**: Use IDE tools to update import statements automatically
- **Comprehensive Testing**: Ensure all tests pass after migration to verify correctness

## Alternatives
### Keep Current Single Services Directory
- **Pros**: No migration required, familiar to current contributors
- **Cons**: Continues architectural confusion, doesn't scale well as codebase grows
- **Rejected**: Fails to address the core problem of unclear layer boundaries

### Flat Structure with Naming Conventions
- **Pros**: Simple, minimal file organization
- **Cons**: Relies on naming conventions rather than physical structure, doesn't enforce boundaries
- **Rejected**: Doesn't provide clear architectural guidance

### Domain-Driven Design Structure
- **Pros**: Rich domain modeling, business-focused organization
- **Cons**: Already rejected in ADR-0015 as over-engineered for CLI tools
- **Rejected**: Contradicts existing architectural decisions

## Future Direction
- **File Classification Analysis**: Conduct individual analysis of each existing file to determine appropriate layer assignment based on responsibilities and dependencies
- **Migration Planning**: Develop a detailed migration plan after completing the file classification analysis  
- **Import Path Updates**: Update all existing import statements to reflect the new directory structure
- **Test Verification**: Ensure all existing tests continue to pass after the restructuring
- **New Command Implementation**: Use this structure as the foundation when implementing future CLI commands (e.g., `new`, `list`, `generate` commands)
- **Architecture Documentation**: Consider creating developer guidelines that explain how to determine which layer new code belongs in

## References
- [ADR-0015: Service Layer Architecture for CLI Commands](./0015-service-layer-architecture-for-cli-commands.md)