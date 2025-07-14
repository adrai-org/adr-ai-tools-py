# ADR-0013: Test Data Strategy - Avoid Mocking Data Models

## Status
Accepted

## Date
2025-07-14

## Context
The project uses Pydantic models for data representation and needs to establish a comprehensive testing strategy for data models and test data creation. Different approaches exist for creating test data:

1. **Mock data models**: Replace model instances with mocks in tests
2. **Manual model creation**: Create actual model instances by hand
3. **Factory libraries**: Use libraries like polyfactory for automated test data generation
4. **Hybrid approaches**: Combine different strategies based on model complexity

Key considerations include:
- Test reliability and accuracy
- Development and maintenance overhead
- Model complexity and future growth
- Test data variety and edge case coverage
- Pydantic-specific mocking challenges

## Decision
- **Avoid mocking data models** in tests - use real Pydantic model instances
- **Start with manual creation** for simple models
- **Introduce polyfactory** when model complexity warrants automated generation

## Rationale

### Pydantic Mocking Complexity
Mocking Pydantic models requires complex workarounds due to their dynamic nature:
- **MagicMock Issues**: Standard mocking approaches fail with Pydantic's metaclass implementation
- **Spec Workarounds**: Requires intricate `spec` and `wraps` configurations
- **Maintenance Overhead**: Mock configurations become complex and fragile
- **Implementation Coupling**: Mocks must understand Pydantic's internal behavior

Given these complexities, the workarounds required for Pydantic mocking are **not justified** for our use case.

### Current State: Simple Models
Current models like `InitializationResult` are simple (2-3 fields):
```python
class InitializationResult(BaseModel):
    success: bool
    message: str
```
- **Manual creation is sufficient**: Easy to write and understand
- **Clear test intent**: Explicit values make test expectations obvious
- **No overhead**: No additional dependencies or setup required

### Anti-Pattern: Mocking Data Models
- **Mock-Reality Gap**: Mocks don't validate actual model behavior
- **Lost Validation**: Pydantic validation rules aren't tested
- **Maintenance Burden**: Mock configurations need updates when models change
- **Type Safety Loss**: Mocks don't provide real type checking benefits
- **Pydantic-Specific Issues**: Requires complex workarounds that add no value

### Future: Complex Models
As models grow (future ADR document models with 10+ fields):
```python
class AdrDocument(BaseModel):
    id: int
    title: str
    status: AdrStatus
    date: datetime
    context: str
    decision: str
    # ... many more fields
```
- **polyfactory becomes valuable**: Automated generation reduces boilerplate
- **Edge case testing**: Generate diverse test data automatically
- **Performance testing**: Create large datasets efficiently

## Implications

### Positive Implications
- **Higher Test Fidelity**: Tests exercise actual model validation and serialization
- **Reduced Maintenance**: No mock configurations to maintain
- **Clear Progression Path**: Natural evolution from simple to complex test data strategies
- **Validation Coverage**: Model validation is automatically tested
- **Avoided Complexity**: No need for Pydantic mocking workarounds

### Concerns
- **Test Coupling**: Tests become coupled to model implementation details
- **Future Complexity**: Manual creation may become burdensome for complex models
- **Dependency Growth**: Will eventually add polyfactory dependency

### Mitigation Strategies
- **Gradual Adoption**: Start simple, introduce polyfactory when needed
- **Clear Thresholds**: Define when to switch from manual to factory-based creation
- **Factory Patterns**: Develop reusable helper functions for common scenarios

## Implementation Strategy

### Phase 1: Current (Simple Models)
- Use manual model creation for models with ≤5 simple fields
- Create helper functions for commonly used model instances
- Use pytest fixtures for shared model instances

### Phase 2: Future (Complex Models)
- Introduce polyfactory when models have >5 fields or complex relationships
- Use factories for bulk data generation and edge case testing
- Maintain manual creation for specific test scenarios requiring explicit values

### Threshold Guidelines
**Use Manual Creation When:**
- Model has ≤5 simple fields
- Test requires specific, explicit values
- Model relationships are simple

**Use polyfactory When:**
- Model has >5 fields or complex nested structures
- Need to generate many instances for testing
- Testing edge cases and boundary conditions
- Performance testing with large datasets

## Alternatives

### Mock All Models
- **Pros**: Fast test execution, complete isolation
- **Cons**: Mock-reality gap, no validation testing, maintenance overhead, Pydantic-specific complexity
- **Rejected**: Loses validation testing benefits and requires complex workarounds

### Use polyfactory Immediately
- **Pros**: Consistent approach, future-ready
- **Cons**: Overkill for simple models, unnecessary complexity
- **Rejected**: Over-engineering for current simple models

### Hybrid Mocking Approach
- **Pros**: Flexibility per situation
- **Cons**: Inconsistent patterns, decision overhead, Pydantic mocking complexity
- **Rejected**: Creates inconsistent testing patterns and adds unnecessary complexity

## Future Direction
- **Monitor Model Complexity**: Track when models grow beyond manual creation threshold
- **polyfactory Introduction**: Add polyfactory when first complex model is introduced
- **Testing Utilities**: Develop helper functions for common model creation patterns
- **Performance Monitoring**: Monitor test execution time and optimize if needed

## References
- [Pydantic BaseModel Mocking Challenges](https://stackoverflow.com/questions/78638694/how-to-test-a-pydantic-basemodel-with-magicmock-spec-and-wraps)
- [polyfactory Documentation](https://polyfactory.litestar.dev/)
- [ADR-0005: pytest Testing Framework](./0005-adopt-pytest-for-testing-framework.md)
- [ADR-0012: Pydantic Data Models](./0012-adopt-pydantic-for-data-models.md)