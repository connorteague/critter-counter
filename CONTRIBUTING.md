# Contributing to Critter Counter

Thank you for contributing to this project! This guide will help you write code that's consistent with the project standards.

## Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length:** 88 characters (Black default)
- **Indentation:** 4 spaces (no tabs)
- **Quotes:** Use double quotes `"` for strings
- **Naming:**
  - `snake_case` for functions, methods, variables
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants

### Type Hints

Always use type hints:

```python
def add_entry(self, num_cattle: int = 1) -> None:
    """Add cattle to entry count."""
    pass

def get_counts(self) -> CountData:
    """Get current count data."""
    pass
```

### Docstrings

Use Google-style docstrings for all public functions and classes:

```python
def process_event(tag_id: str, rssi: float) -> Direction:
    """
    Process an RFID reading and determine direction.
    
    Args:
        tag_id: The EPC tag identifier (24 character hex string)
        rssi: Signal strength in dBm (typically -90 to -30)
        
    Returns:
        Direction enum (ENTRY, EXIT, or UNKNOWN)
        
    Raises:
        ValueError: If tag_id format is invalid
    """
    pass
```

### Comments

- Write comments for **why**, not **what**
- Good: `# Using RSSI trend because dual-antenna setup too expensive`
- Bad: `# Loop through tags`
- Keep comments up to date when code changes

## Testing

### Test Coverage

- Aim for >80% code coverage
- Every public method should have at least one test
- Test both success and failure cases

### Test Structure

```python
class TestCountManager:
    """Tests for CountManager class."""
    
    def test_add_entry_increments_count(self, temp_counts_file):
        """Test that add_entry increases the entry count."""
        # Arrange
        manager = CountManager()
        manager.PERSISTENCE_FILE = temp_counts_file
        
        # Act
        manager.add_entry(5)
        
        # Assert
        assert manager.counts.daily_entry == 5
```

### Running Tests

Before committing:

```bash
# Run all tests
pytest

# Check coverage
pytest --cov=src --cov-report=term

# Fix any linting issues
pylint src/
black src/
```

## Git Workflow

### Branch Naming

- Feature: `feature/count-manager`
- Bugfix: `bugfix/persistence-crash`
- Documentation: `docs/setup-guide`

### Commit Messages

Write clear commit messages:

```
Add CountManager with JSON persistence

- Implement add_entry() and add_exit() methods
- Add daily reset functionality
- Write unit tests with 90% coverage

Closes #123
```

Format:
1. First line: Brief summary (50 chars or less)
2. Blank line
3. Detailed description (if needed)
4. Reference issues

### Pull Request Process

1. Create branch: `git checkout -b feature/your-feature`
2. Write code and tests
3. Ensure tests pass: `pytest`
4. Commit changes: `git commit -m "Clear message"`
5. Push: `git push origin feature/your-feature`
6. Create pull request for Connor to review
7. Address feedback
8. Merge after approval

## Code Review Checklist

Before submitting code for review:

- [ ] All tests pass
- [ ] Code coverage >80%
- [ ] No linting errors
- [ ] Type hints on all functions
- [ ] Docstrings on public methods
- [ ] Comments explain complex logic
- [ ] No debugging print statements
- [ ] No commented-out code
- [ ] Updated documentation if needed

## File Organization

### Where Things Go

```
src/
  ├── config.py           # All configuration constants
  ├── count_manager.py    # Count logic
  ├── direction_detector.py
  └── ...

tests/
  ├── conftest.py         # Shared fixtures
  ├── test_count_manager.py
  └── ...

docs/
  ├── algorithm_notes.md  # Technical documentation
  └── ...
```

### Imports

Order imports:

1. Standard library
2. Third-party packages
3. Local modules

```python
# Standard library
import os
import json
from datetime import datetime
from typing import Optional, List

# Third-party (none yet in this project)

# Local
from config import DAILY_RESET_HOUR
from direction_detector import Direction
```

## Error Handling

### Fail Gracefully

```python
def load_counts(self) -> CountData:
    """Load counts from file."""
    try:
        with open(self.PERSISTENCE_FILE, 'r') as f:
            data = json.load(f)
            return CountData.from_dict(data)
    except FileNotFoundError:
        # File doesn't exist yet - normal on first run
        return CountData()
    except json.JSONDecodeError as e:
        # Corrupted file - log error and start fresh
        print(f"Warning: Corrupted counts file: {e}")
        return CountData()
```

### When to Raise Exceptions

Raise exceptions for:
- Invalid input (ValueError)
- Configuration errors
- Unrecoverable errors

Don't raise exceptions for:
- Expected conditions (file doesn't exist)
- Recoverable errors

## Performance Considerations

### This is NOT a performance-critical system

- Prioritize **readability** over micro-optimizations
- A few milliseconds don't matter for cattle passing through gate
- Do optimize for **power consumption** (that matters!)

### When Performance Matters

- Minimize display updates (power-hungry)
- Keep RFID scan time reasonable (<5 seconds)
- Use deep sleep when idle

## Questions?

If you're unsure about anything:

1. Check existing code for examples
2. Read `docs/code_example.py`
3. Ask Connor

## Thank You!

Your code will help protect cattle and wildlife in Botswana. Write it with care! 🐄🐆
