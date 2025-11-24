# Contributing to TextEditee

Thank you for your interest in contributing to TextEditee! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Basic understanding of vim/terminal editors
- Familiarity with Python development

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/yourusername/texteditee.git
   cd texteditee
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black mypy ruff
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Follow the existing code style
- Write clean, readable code
- Add comments only when necessary
- Follow DRY, KISS, and Clean Code principles

### 3. Write Tests

- Add tests for new features
- Ensure existing tests pass
- Aim for high code coverage

```bash
pytest tests/ -v --cov=src/texteditee
```

### 4. Format Code

```bash
black src/ tests/
```

### 5. Run Linters

```bash
ruff check src/
mypy src/
```

### 6. Commit Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Add feature: description of feature"
# or
git commit -m "Fix bug: description of bug fix"
```

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Prefer composition over inheritance

### Example

```python
from typing import Optional

class Buffer:
    def __init__(self, filename: str = ''):
        self.filename = filename
        self.modified = False

    def save(self, filename: Optional[str] = None) -> None:
        target = filename or self.filename
        if not target:
            raise ValueError("No filename specified")
        # Implementation...
```

## Architecture Guidelines

### Directory Structure

```
src/texteditee/
├── core/          # Core editor components
├── input/         # Input handling
├── ui/            # User interface
├── features/      # Editor features
├── fs/            # File system operations
└── config/        # Configuration
```

### Design Patterns

- **Command Pattern**: For undo/redo and key bindings
- **Strategy Pattern**: For different modes
- **Singleton Pattern**: For global state
- **Observer Pattern**: For buffer notifications

### Adding New Features

1. **Core Features** go in `core/`
2. **UI Components** go in `ui/`
3. **Editor Features** go in `features/`
4. **File Operations** go in `fs/`

## Testing

### Writing Tests

```python
import pytest
from texteditee.core.buffer import Buffer

class TestBuffer:
    def test_insert_char(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'a')
        assert buf.get_line(0) == 'a'
```

### Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_buffer.py

# With coverage
pytest tests/ --cov=src/texteditee

# Verbose output
pytest tests/ -v
```

## Documentation

### Code Documentation

- Use docstrings for classes and public methods
- Keep comments minimal and meaningful
- Update documentation when changing behavior

### User Documentation

- Update `README.md` for user-facing changes
- Update `docs/user_guide.md` for new features
- Update `CHANGELOG.md` for all changes

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass
- [ ] Code is formatted (black)
- [ ] Linters pass (ruff, mypy)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### PR Description

Include:

- What the PR does
- Why the change is needed
- How to test it
- Screenshots (if UI changes)

### Example PR Description

```markdown
## Description

Adds support for visual block mode

## Motivation

Users need to select rectangular blocks of text

## Changes

- Added visual block mode to mode manager
- Implemented block selection logic
- Added keybinding Ctrl+v

## Testing

1. Open file
2. Press Ctrl+v
3. Move cursor to select block
4. Press d to delete block

## Screenshots

[Add screenshots if applicable]
```

## Feature Requests

### Before Requesting

- Check existing issues
- Ensure it aligns with project goals
- Consider if it fits the vim philosophy

### Creating Feature Request

Use the issue template and include:

- Clear description
- Use case
- Expected behavior
- Alternative solutions considered

## Bug Reports

### Before Reporting

- Check existing issues
- Try to reproduce
- Gather information

### Creating Bug Report

Include:

- TextEditee version
- Operating system
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## Areas for Contribution

### Good First Issues

- Documentation improvements
- Test coverage
- Bug fixes
- Code cleanup

### Advanced Features

- Plugin system
- Advanced vim features
- Performance optimization
- Cross-platform improvements

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to TextEditee! 🎉
