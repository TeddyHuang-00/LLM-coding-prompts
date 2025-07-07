# Python Project Configuration

## Language and Version
- Use Python 3.11+ exclusively with modern syntax and features
- Always import `from __future__ import annotations` at the top of every Python file
- Use modern Python features: match statements, walrus operator, positional-only parameters

## Tooling and Development Environment
- Use Ruff for all linting and formatting (never Black, isort, Flake8, or other tools)
- Use mypy for static type checking with strict configuration
- Use pytest for testing with fixtures and parametrized tests
- Use pyproject.toml for all project configuration

## Code Style Standards
- Use double quotes for strings consistently
- Use 4-space indentation (no tabs)
- Use f-strings for string formatting, never % formatting or .format()
- Use descriptive variable names, avoid abbreviations
- Use type hints for all function parameters and return values
- Use modern collection types: dict, list, set (not Dict, List, Set from typing)

## Project Structure
- Follow src/ directory structure for source code
- Use absolute imports from src module, not relative imports
- Place tests in tests/ directory with test_ prefix
- Organize code into logical modules and packages

## Required Libraries
- **Pydantic Settings**: For configuration management with type-safe validation
- **pathlib**: For file operations instead of os.path
- **logging**: For logging instead of print statements
- **enum.Enum**: For constants and enumerated values
- **dataclasses**: For structured data representation

## Data Handling
- Use dataclasses or Pydantic models for structured data, not plain dictionaries
- Use list comprehensions and generator expressions for data processing
- Use type-safe patterns and avoid `Any` type annotations
- Use context managers (with statements) for resource management

## Error Handling
- Use proper exception handling with specific exception types
- Use environment variables for configuration with pydantic-settings
- Create custom exception classes for library code
- Follow patterns similar to anyhow for application error handling

## Async Programming
- Use async/await patterns for I/O operations with modern Python async syntax
- Use asyncio for concurrent operations
- Use proper async context managers for resources
- Handle async exceptions properly

## Testing Strategy
- Use pytest with comprehensive test coverage
- Use fixtures for test setup and teardown
- Use parametrized tests for multiple test cases
- Write both unit tests and integration tests
- Test error conditions and edge cases

## Quality Assurance Workflow
Before committing code, ALWAYS run these commands in order:
1. `ruff format` - Format code
2. `ruff check --fix` - Fix linting issues
3. `mypy src/` - Type checking
4. `pytest` - Run all tests

Maintain zero linting warnings and type errors. All tests must pass.

## Documentation
- Write clear, concise docstrings with examples
- Use type hints as primary documentation for parameters
- Include usage examples in docstrings
- Document error conditions and exceptions
- Use Google-style docstrings

## Performance Considerations
- Use generators for large datasets
- Use appropriate data structures for the use case
- Profile code when performance is critical
- Cache expensive operations when appropriate
- Use lazy evaluation where possible

## Security Practices
- Validate all user inputs
- Use secure random number generation
- Avoid eval() and exec() functions
- Follow secure coding practices for file operations
- Handle sensitive data appropriately

## Build Commands
- `ruff format` - Format all Python code
- `ruff check --fix` - Lint and fix issues
- `mypy src/` - Type check source code
- `pytest` - Run test suite
- `python -m src.main` - Run the application