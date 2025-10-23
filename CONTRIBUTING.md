# Contributing to Tableau Python Automated Dashboard Generator

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Setup Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/tableau-python-automated-dashboard-generator.git
cd tableau-python-automated-dashboard-generator
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Install development dependencies
```

4. **Verify installation**

```bash
pytest tests/
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add docstrings to all functions and classes
- Update documentation if needed

### 3. Write Tests

- Add tests for all new features
- Ensure all tests pass: `pytest tests/`
- Maintain or improve code coverage

### 4. Run Code Quality Checks

```bash
# Format code
black src tests
isort src tests

# Lint code
flake8 src tests --max-line-length=100
pylint src --max-line-length=100

# Type checking (optional but recommended)
mypy src --ignore-missing-imports
```

### 5. Run Tests with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
```

Aim for >80% code coverage.

### 6. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of your feature"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots (if applicable)
- Test results

## 🎯 Code Style Guidelines

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://github.com/psf/black) for code formatting (line length: 100)
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 100 characters

### Documentation Style

- Use Google-style docstrings
- Include type hints where appropriate
- Document all parameters and return values

Example:

```python
def function_name(param1: str, param2: int) -> Dict:
    """
    Brief description of the function.

    Detailed description if needed.

    Parameters:
    -----------
    param1 : str
        Description of param1
    param2 : int
        Description of param2

    Returns:
    --------
    Dict : Description of return value

    Raises:
    -------
    ValueError : When param1 is empty
    """
    pass
```

### Testing Guidelines

- Write unit tests for all new functions
- Use descriptive test names: `test_function_name_should_do_something`
- Use pytest fixtures for common setup
- Mock external dependencies (Tableau Server API)

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Exact steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**:
   - Python version
   - Operating system
   - Package versions (`pip freeze`)
6. **Code snippets**: Minimal reproducible example
7. **Error messages**: Full error traceback

## 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

1. **Use case**: Why is this enhancement needed?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches you've thought about
4. **Additional context**: Screenshots, mockups, etc.

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows the project's style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] New code has tests (coverage >80%)
- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] Linting passes (flake8, pylint)
- [ ] Documentation is updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No unrelated changes are included

## 🔒 Security Issues

If you discover a security vulnerability, please email the maintainer directly instead of opening a public issue.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## 🙏 Thank You!

Your contributions help make this project better for everyone!
