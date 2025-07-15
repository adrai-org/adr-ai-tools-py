# ADR-0016: Dependency Injection Pattern for Service Composition

## Status
Accepted

## Date
2025-07-14

## Context
The service-oriented architecture requires a strategy for managing dependencies between services and composing them into functional units. The application needs to balance simplicity with flexibility while maintaining testability and adherence to SOLID principles.

Key considerations include:
- Dependency management complexity
- Testing isolation and mock injection
- Service lifecycle management
- Configuration and flexibility
- Development simplicity vs. advanced features

## Decision
Adopt Constructor Injection with Manual Wiring for service composition, avoiding heavyweight DI containers for the current scope.

## Rationale

### Constructor Injection Benefits
- **Explicit Dependencies**: All dependencies are clearly visible in the constructor
- **Compile-time Safety**: Missing dependencies are caught at object creation time
- **Immutable Dependencies**: Dependencies are set once and cannot be changed
- **Test Friendly**: Easy to inject mocks and test doubles

### Manual Wiring Advantages
- **Simplicity**: No additional frameworks or configuration files required
- **Transparency**: Dependency graph is explicit and traceable in code
- **Zero Learning Curve**: Standard Python patterns, no special knowledge required
- **Minimal Overhead**: No runtime reflection or complex initialization logic

### Current Implementation Pattern
```python
# CLI Layer - Manual composition
@app.command()
def init() -> None:
    # Dependency injection - create service instances
    file_system_service = FileSystemService()
    user_interaction_service = UserInteractionService()
    initializer = AdrInitializer(file_system_service, user_interaction_service)
    
    # Execute business logic
    result = initializer.initialize()
```

### Service Layer Pattern
```python
class AdrInitializer:
    def __init__(
        self,
        file_system_service: FileSystemService,
        user_interaction_service: UserInteractionService,
    ) -> None:
        self.file_system_service = file_system_service
        self.user_interaction_service = user_interaction_service
```

## Implications

### Positive Implications
- **Simplicity**: Easy to understand and implement without additional frameworks
- **Testability**: Simple to inject mocks for unit testing
- **Transparency**: Clear dependency relationships visible in code
- **Performance**: No runtime overhead from DI containers
- **Flexibility**: Can easily change composition logic as needed

### Concerns
- **Repetitive Code**: Manual wiring may become repetitive as services grow
- **Configuration Management**: No centralized configuration for dependencies
- **Lifecycle Management**: Manual management of service lifecycles
- **Cross-cutting Concerns**: No built-in support for aspects like logging or caching

### Mitigation Strategies
- **Factory Functions**: Create factory functions for common service compositions
- **Service Builders**: Implement builder patterns for complex service graphs
- **Configuration Objects**: Use configuration objects for parameterized services
- **Future Migration Path**: Can evolve to DI containers if complexity grows

## Testing Strategy

### Unit Testing with Mocks
```python
def test_initialization_success():
    # Arrange - inject mocks
    file_system_service = Mock(spec=FileSystemService)
    user_interaction_service = Mock(spec=UserInteractionService)
    initializer = AdrInitializer(file_system_service, user_interaction_service)
    
    # Act & Assert
    result = initializer.initialize()
    assert result.success
```

### CLI Testing with Mocked Services
```python
def test_cli_command(mocker):
    # Mock the service classes
    mock_initializer_class = mocker.patch("adraitools.cli.AdrInitializer")
    mock_initializer = mock_initializer_class.return_value
    
    # Test CLI behavior
    result = runner.invoke(app, ["init"])
```

## Future Evolution Path

### Phase 1: Current (Manual Wiring)
- Suitable for simple service graphs
- Direct instantiation in CLI commands
- Manual composition for each command

### Phase 2: Factory Functions (If Needed)
```python
def create_adr_services() -> AdrServices:
    file_system_service = FileSystemService()
    user_interaction_service = UserInteractionService()
    return AdrServices(file_system_service, user_interaction_service)
```

### Phase 3: DI Container (If Complexity Grows)
- Consider lightweight containers like `dependency-injector` or `punq`
- Only if service graph becomes complex (>10 services)
- Maintain backward compatibility with current patterns

## Alternatives

### Dependency Injection Containers
- **Pros**: Automatic wiring, configuration management, lifecycle control
- **Cons**: Additional complexity, learning curve, framework dependency
- **Rejected**: Over-engineering for current scope, can revisit later

### Service Locator Pattern
- **Pros**: Centralized service access, dynamic service resolution
- **Cons**: Hidden dependencies, anti-pattern for testing, tight coupling
- **Rejected**: Violates dependency inversion principle

### Factory Pattern for All Services
- **Pros**: Centralized creation logic, consistent instantiation
- **Cons**: Additional abstraction layer, may be premature optimization
- **Rejected**: Can be added later if needed, not required now

### Singleton Services
- **Pros**: Reduced object creation, shared state management
- **Cons**: Hidden dependencies, difficult testing, global state issues
- **Rejected**: Violates dependency injection principles

## Guidelines

### Service Design Principles
- **Stateless Services**: Prefer stateless services for easier testing and reuse
- **Interface Segregation**: Keep service interfaces focused and minimal
- **Dependency Inversion**: Depend on abstractions when beneficial
- **Constructor Injection**: Always use constructor injection for dependencies

### Testing Guidelines
- **Mock Externals**: Mock file system, user interaction, and external services
- **Test Business Logic**: Focus unit tests on business logic in service layer
- **Integration Tests**: Test service integration with real dependencies when needed

## Future Direction
- **Monitor Complexity**: Track service dependency growth and complexity
- **Factory Evolution**: Introduce factory functions when repetition becomes problematic
- **Configuration Strategy**: Develop configuration patterns as needs emerge
- **Container Evaluation**: Evaluate DI containers if service graph becomes unwieldy

## References
- [Dependency Injection Principles](https://martinfowler.com/articles/injection.html)
- [SOLID Principles - Dependency Inversion](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
- [ADR-0015: Service Layer Architecture](./0015-service-layer-architecture-for-cli-commands.md)
- [ADR-0013: Test Data Strategy](./0013-test-data-strategy-avoid-mocking-data-models.md)