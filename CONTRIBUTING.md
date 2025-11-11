# Contributing to TravelPurpose

Thank you for your interest in contributing to TravelPurpose! We welcome contributions from the community.

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. By participating, you agree to uphold this code.

## How to Contribute

### Reporting Issues

- Search existing issues before creating a new one
- Provide clear description and steps to reproduce
- Include relevant logs, error messages, and environment details
- Use issue templates when available

### Suggesting Features

- Check if the feature has already been requested
- Clearly describe the use case and benefits
- Consider backwards compatibility
- Provide examples of the desired API/behavior

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Make your changes** following our coding standards
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Run the test suite** and ensure all tests pass
6. **Submit a pull request** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Travel_Purpose-City_Tags.git
cd Travel_Purpose-City_Tags

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use Black for code formatting (line length: 100)
- Use Ruff for linting
- Add type hints where appropriate
- Write docstrings for all public functions/classes

### Code Organization

- Keep functions focused and concise
- Use meaningful variable and function names
- Add comments for complex logic
- Avoid magic numbers and strings

### Testing

- Write unit tests for all new functionality
- Aim for high test coverage (>80%)
- Use pytest fixtures for common setup
- Test edge cases and error conditions

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=travelpurpose --cov-report=term-missing
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings with examples
- Update type hints
- Create/update notebooks for complex features

## Adding New Data Sources

When adding new harvesters for travel platforms:

### Requirements

1. **Public Data Only**: Must use only publicly accessible data
2. **ToS Compliance**: Must comply with platform Terms of Service
3. **Robots.txt**: Must respect robots.txt directives
4. **Rate Limiting**: Implement appropriate rate limiting
5. **Error Handling**: Graceful degradation when source unavailable
6. **Attribution**: Proper source attribution in tags

### Implementation Guidelines

```python
from travelpurpose.utils.harvest import BaseHarvester, safe_harvest

class YourHarvester(BaseHarvester):
    """Harvester for YourPlatform public data."""

    BASE_URL = "https://yourplatform.com"

    @safe_harvest
    def get_city_tags(self, city_name: str, country: str = "") -> List[Dict]:
        """
        Get tags for a city.

        Args:
            city_name: City name
            country: Optional country

        Returns:
            List of tag dictionaries
        """
        # Implementation here
        pass
```

### Testing New Harvesters

```python
def test_your_harvester():
    """Test YourHarvester."""
    harvester = YourHarvester()
    tags = harvester.get_city_tags("Paris")

    assert isinstance(tags, list)
    # Add more assertions
```

## Extending the Ontology

To add new categories or subcategories:

1. Edit `travelpurpose/ontology/ontology.yaml`
2. Add appropriate tag mappings
3. Update documentation
4. Add tests for new mappings
5. Run pipeline to validate

## Commit Messages

Use clear, descriptive commit messages:

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

Example:
```
feat: add support for TripAdvisor public data

- Implement TripAdvisorHarvester
- Add tag mapping for reviews
- Update documentation
```

## Release Process

Maintainers follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

## Questions?

- Open a [Discussion](https://github.com/teyfikoz/Travel_Purpose-City_Tags/discussions)
- Check existing documentation
- Ask in pull request comments

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
