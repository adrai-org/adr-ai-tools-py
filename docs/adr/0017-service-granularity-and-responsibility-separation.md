# ADR-0017: Service Granularity and Responsibility Separation

## Status
Accepted

## Date
2025-07-14

## Context
The service layer architecture requires clear guidelines for determining service boundaries, granularity, and responsibility allocation. The `init` command implementation establishes patterns for service design that will influence the entire application architecture.

Key considerations include:
- Service size and scope definition
- Responsibility allocation between services
- Service reusability and composability
- Testing complexity and isolation
- Future extensibility and maintenance

## Decision
Adopt fine-grained service design based on the Single Responsibility Principle, creating focused services with distinct, cohesive responsibilities.

## Rationale

### Implemented Service Structure

#### AdrInitializer (Business Logic Service)
- **Responsibility**: Orchestrate ADR initialization business logic
- **Scope**: Single business operation (ADR directory setup)
- **Dependencies**: FileSystemService, UserInteractionService
- **Justification**: Encapsulates complex business rules and workflow coordination

#### FileSystemService (Infrastructure Service)
- **Responsibility**: Abstract file system operations
- **Scope**: File and directory operations only
- **Dependencies**: None (external system interaction)
- **Justification**: Isolates external dependency, enables testing without filesystem

#### UserInteractionService (Infrastructure Service)
- **Responsibility**: Handle user input and interaction
- **Scope**: Console input/output operations only
- **Dependencies**: None (external system interaction)
- **Justification**: Isolates user interaction, enables testing without user input

### Single Responsibility Principle Application
Each service has exactly one reason to change:
- **AdrInitializer**: Changes when business rules for initialization change
- **FileSystemService**: Changes when file operation requirements change
- **UserInteractionService**: Changes when user interaction patterns change

### Service Interaction Pattern
```python
# Business Logic Service coordinates Infrastructure Services
class AdrInitializer:
    def initialize(self) -> InitializationResult:
        # Check directory existence (FileSystemService)
        if self.file_system_service.directory_exists(adr_dir):
            # Ask user confirmation (UserInteractionService)
            if not self.user_interaction_service.ask_confirmation(message):
                return InitializationResult(success=False, message="Cancelled")
        
        # Create directory and template (FileSystemService)
        self.file_system_service.create_directory(adr_dir)
        self.file_system_service.create_template_file(template_file)
```

## Service Design Guidelines

### Granularity Criteria
**Create a new service when:**
- The functionality represents a distinct external dependency
- The logic has a clear, single responsibility
- The operations would benefit from isolated testing
- The functionality could be reused by other services

**Avoid creating a service when:**
- The functionality is too small to justify the overhead
- It would create unnecessary coupling between services
- The logic is tightly coupled to a specific business operation

### Service Categories

#### Business Logic Services
- **Purpose**: Implement domain-specific operations and workflows
- **Characteristics**: Orchestrate other services, contain business rules
- **Examples**: AdrInitializer, AdrValidator, AdrSearcher
- **Testing**: Mock all dependencies, focus on business logic

#### Infrastructure Services
- **Purpose**: Abstract external dependencies and system operations
- **Characteristics**: Stateless, focused on single external concern
- **Examples**: FileSystemService, UserInteractionService, ConfigurationService
- **Testing**: Test against real dependencies when possible

#### Utility Services
- **Purpose**: Provide common operations used across multiple contexts
- **Characteristics**: Pure functions, no external dependencies
- **Examples**: TemplateRenderer, PathResolver, DateFormatter
- **Testing**: Direct unit testing without mocks

## Implications

### Positive Implications
- **High Testability**: Each service can be tested in isolation with clear boundaries
- **Reusability**: Infrastructure services can be reused across multiple business operations
- **Maintainability**: Changes to external dependencies are isolated to specific services
- **Clear Architecture**: Service responsibilities are obvious and well-defined
- **Parallel Development**: Different services can be developed independently

### Concerns
- **Increased Complexity**: More classes and interfaces than coarse-grained approach
- **Potential Over-engineering**: May be excessive for simple operations
- **Coordination Overhead**: Business logic services must coordinate multiple dependencies
- **Testing Complexity**: More mock setup required for business logic tests

### Mitigation Strategies
- **Service Templates**: Provide standard templates for common service patterns
- **Documentation**: Clear guidelines on when to create new services
- **Refactoring Guidelines**: Rules for splitting or merging services as needs evolve

## Testing Strategy

### Service-Level Testing
```python
# Business Logic Service - Mock all dependencies
def test_adr_initializer():
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    initializer = AdrInitializer(file_system_service, user_interaction_service)

# Infrastructure Service - Test real behavior when possible
def test_file_system_service():
    service = FileSystemService()
    with tempfile.TemporaryDirectory() as tmpdir:
        service.create_directory(Path(tmpdir) / "test")
```

### Service Integration Testing
```python
# Test service integration without mocking
def test_services_integration():
    file_system_service = FileSystemService()
    user_interaction_service = Mock(spec=UserInteractionService)
    user_interaction_service.ask_confirmation.return_value = True
    
    initializer = AdrInitializer(file_system_service, user_interaction_service)
```

## Future Service Evolution

### Anticipated Services
As the application grows, expected new services include:

#### Business Logic Services
- **AdrCreator**: Handle new ADR creation workflow
- **AdrSearcher**: Implement ADR search and filtering
- **AdrValidator**: Validate ADR content and structure

#### Infrastructure Services
- **GitService**: Handle git operations for ADR versioning
- **ConfigurationService**: Manage application configuration
- **TemplateService**: Manage ADR templates and customization

#### Utility Services
- **MarkdownParser**: Parse and manipulate markdown content
- **AdrNumberGenerator**: Generate sequential ADR numbers
- **DateTimeService**: Handle date/time operations consistently

### Service Splitting Guidelines
**Consider splitting a service when:**
- It has multiple reasons to change (violates SRP)
- It becomes difficult to test due to multiple concerns
- Parts of the service are reused independently
- The service exceeds reasonable size (>200 lines typically)

### Service Merging Guidelines
**Consider merging services when:**
- They are always used together and never independently
- The boundary between them becomes artificial
- The overhead of coordination exceeds the benefits of separation

## Alternatives

### Coarse-Grained Services
- **Pros**: Fewer classes, simpler dependency management
- **Cons**: Harder to test, violates SRP, reduces reusability
- **Rejected**: Compromises testability and maintainability

### One Service Per File/Operation
- **Pros**: Ultimate separation of concerns
- **Cons**: Excessive granularity, coordination complexity
- **Rejected**: Over-engineering, difficult to manage

### Domain-Driven Service Boundaries
- **Pros**: Aligns with business domains, natural boundaries
- **Cons**: May not align with technical concerns, complex for CLI tools
- **Rejected**: Better suited for larger, domain-rich applications

### Functional Approach (No Services)
- **Pros**: Simple, direct function calls
- **Cons**: Difficult to test with external dependencies, poor separation
- **Rejected**: Doesn't support dependency injection and testing isolation

## Future Direction
- **Service Registry**: Consider service registry pattern if service count grows significantly
- **Service Documentation**: Maintain clear documentation of service responsibilities
- **Performance Monitoring**: Monitor service interaction patterns and performance
- **Refactoring Strategy**: Plan periodic service boundary evaluation and refactoring

## References
- [Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)
- [Clean Architecture Services](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [ADR-0015: Service Layer Architecture](./0015-service-layer-architecture-for-cli-commands.md)
- [ADR-0016: Dependency Injection Pattern](./0016-dependency-injection-pattern-for-service-composition.md)