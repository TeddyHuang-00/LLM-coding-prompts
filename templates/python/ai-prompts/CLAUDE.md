# Python Project Configuration

## Language and Tooling
- Use Python 3.11+ with modern syntax and features
- Use Ruff exclusively for linting and formatting (never Black, isort, Flake8)
- Use mypy for strict type checking
- Use pytest for comprehensive testing
- Always import `from __future__ import annotations` at the top of every Python file

## Code Style
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
- Use pyproject.toml for all configuration

## Libraries and Dependencies
- Use Pydantic Settings for configuration management with type-safe validation
- Use pathlib instead of os.path for file operations
- Use dataclasses or Pydantic models for structured data, not plain dictionaries
- Use logging module for logging, not print statements
- Use enum.Enum for constants and enumerated values
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

## Testing
- Use pytest with fixtures and parametrized tests
- Write both unit tests and integration tests
- Test error conditions and edge cases
- Maintain comprehensive test coverage

## Quality Assurance
- Run `ruff format` to format code
- Run `ruff check --fix` to fix linting issues
- Run `mypy src/` for type checking
- Run `pytest` to run all tests
- Maintain zero linting warnings and type errors

## Modern Python Features
- Use match statements for pattern matching
- Use walrus operator for assignment expressions
- Use positional-only parameters where appropriate
- Use list comprehensions and generator expressions for data processing

## Performance and Security
- Use generators for large datasets
- Use appropriate data structures for the use case
- Validate all user inputs
- Use secure random number generation
- Follow secure coding practices for file operations

## Documentation
- Write clear, concise docstrings with examples
- Use type hints as primary documentation for parameters
- Include usage examples in docstrings
- Document error conditions and exceptions

## Build Commands
- `ruff format` - Format all Python code
- `ruff check --fix` - Lint and fix issues
- `mypy src/` - Type check source code
- `pytest` - Run test suite
- `python -m src.main` - Run the application