# ADR-0014: Use Simple Public Attributes for Dependencies

## Status
Accepted

## Date
2025-07-14

## Context
The project needs to establish patterns for class attribute access control, particularly for dependencies injected through constructor parameters. Different approaches exist for managing attribute visibility:

1. **Simple public attributes**: Direct access to attributes
2. **Private attributes with properties**: Use `_attribute` with property accessors
3. **Property-only interfaces**: Complex getter/setter patterns
4. **Name mangling**: Double underscore attributes

Key considerations include:
- Python idioms and conventions
- Code simplicity and readability
- Development velocity
- Maintenance overhead

## Decision
Use simple public attributes for constructor-injected dependencies. Avoid private attributes with property accessors for simple dependency injection.

## Rationale

### Python Idioms and PEP 8
- **"We're all consenting adults"**: Python philosophy trusts developers not to misuse interfaces
- **PEP 8 Guidance**: Use public attributes for simple cases, properties only when needed
- **Simpler is Better**: Following the Zen of Python principle
- **Community Standards**: Most Python codebases use simple public attributes

### Development Efficiency
- **Less Boilerplate**: No need to write property methods for simple access
- **Faster Development**: Direct attribute access is more straightforward
- **Easier Testing**: Simple attributes are easier to mock and verify
- **Reduced Complexity**: Less code to maintain and understand

### Practical Considerations
- **Dependency Injection**: Injected dependencies are typically not modified after construction
- **Type Safety**: Type hints provide sufficient documentation of expected types
- **IDE Support**: Modern IDEs understand type hints and provide appropriate warnings
- **Refactoring Safety**: Modern tools can safely refactor attribute access

### Implementation Example
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
- **Reduced Boilerplate**: Less code to write and maintain
- **Clearer Intent**: Simple attribute access is more readable
- **Faster Development**: No need to create property methods
- **Python Idiomatic**: Follows established Python conventions
- **Better Testing**: Easier to mock and verify in tests

### Concerns
- **Accidental Modification**: Attributes could be modified accidentally
- **No Access Control**: No protection against inappropriate access
- **Future Changes**: Adding validation later requires interface changes

### Mitigation Strategies
- **Type Hints**: Clear type annotations communicate expected usage
- **Code Review**: Team review process catches inappropriate usage
- **Testing**: Comprehensive tests verify correct behavior
- **Documentation**: Clear documentation of expected usage patterns

## Guidelines

### When to Use Simple Public Attributes
- **Constructor Dependencies**: All injected dependencies and services
- **Configuration Values**: Simple configuration parameters
- **Data Storage**: Basic data storage needs

### When to Consider Properties
- **Computed Values**: Values that need calculation on access
- **Validation Required**: When setter validation is genuinely needed
- **Lazy Loading**: When expensive operations should be deferred
- **Backward Compatibility**: When changing existing property interfaces

### Anti-Patterns to Avoid
```python
# Don't do this for simple dependencies
class BadExample:
    def __init__(self, service: Service) -> None:
        self._service = service
    
    @property
    def service(self) -> Service:
        return self._service
```

## Alternatives

### Private Attributes with Properties
- **Pros**: Encapsulation, protection against modification
- **Cons**: Unnecessary boilerplate, not Pythonic, slower development
- **Rejected**: Violates Python simplicity principles

### Frozen Dataclasses
- **Pros**: Enforced immutability
- **Cons**: Limited to data-only classes, overkill for service classes
- **Rejected**: Service classes need behavior, not just immutability

### Property-Only Interfaces
- **Pros**: Maximum control over access
- **Cons**: Complex implementation, unnecessary for dependency injection
- **Rejected**: Over-engineering for simple use cases

## Future Direction
- **Consistent Application**: Apply simple public attributes across all service classes
- **Code Review Guidelines**: Include in review checklist to ensure consistency
- **Refactoring**: Update existing private-attribute patterns to public attributes
- **Documentation**: Document this pattern in coding guidelines

## References
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/#designing-for-inheritance)
- [Effective Python - Item 44: Use Plain Attributes Instead of Setter/Getter Methods](https://effectivepython.com/)
- [Python's "We're All Consenting Adults" Philosophy](https://docs.python.org/3/tutorial/classes.html#private-variables)