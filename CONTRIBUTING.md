# Contributing to iPhone Installment Store

Thank you for your interest in contributing to the iPhone Installment Store project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- A GitHub account

### Development Setup
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/iphone-store.git
   cd iphone-store
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Populate sample data:
   ```bash
   python manage.py populate_phones
   ```

## 🔧 Development Guidelines

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Django Best Practices
- Follow Django's [coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/)
- Use Django's built-in features when possible
- Write tests for new features
- Use Django's ORM efficiently
- Follow Django's security guidelines

### Git Workflow
1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Write tests for new functionality
4. Run tests:
   ```bash
   python manage.py test
   ```
5. Run linting:
   ```bash
   flake8 .
   ```
6. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request

### Commit Message Format
Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example:
```
feat: add card verification functionality

- Add card number validation
- Implement Luhn algorithm check
- Add card expiry date validation
- Include CVV validation
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test applications

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Use Django's test client for views

Example test:
```python
from django.test import TestCase
from django.urls import reverse
from applications.models import Application

class ApplicationTestCase(TestCase):
    def setUp(self):
        # Set up test data
        pass
    
    def test_application_creation(self):
        # Test application creation
        pass
```

## 📝 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Use Google-style docstrings
- Include parameter types and return values
- Add examples for complex functions

Example:
```python
def create_application(user, phone_data):
    """
    Create a new application for a user.
    
    Args:
        user (CustomUser): The user creating the application
        phone_data (dict): Phone selection data
        
    Returns:
        Application: The created application instance
        
    Raises:
        ValidationError: If phone data is invalid
    """
    pass
```

### README Updates
- Update README.md for new features
- Add installation instructions for new dependencies
- Update configuration examples
- Add usage examples

## 🔒 Security

### Security Guidelines
- Never commit sensitive data (passwords, API keys, etc.)
- Use environment variables for configuration
- Validate all user inputs
- Use Django's built-in security features
- Follow OWASP guidelines

### Security Checklist
- [ ] Input validation implemented
- [ ] SQL injection prevented
- [ ] XSS protection in place
- [ ] CSRF protection enabled
- [ ] File upload validation
- [ ] Authentication/authorization checks
- [ ] Sensitive data encrypted

## 🐛 Bug Reports

### Reporting Bugs
When reporting bugs, please include:
1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Detailed steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version, Django version
6. **Screenshots**: If applicable

### Bug Report Template
```markdown
**Bug Description**
Brief description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g. Windows 10]
- Python: [e.g. 3.11]
- Django: [e.g. 4.2.7]

**Additional Context**
Any other context about the problem
```

## 💡 Feature Requests

### Requesting Features
When requesting features, please include:
1. **Description**: Clear description of the feature
2. **Use case**: Why this feature is needed
3. **Implementation ideas**: How it might be implemented
4. **Mockups**: If applicable

### Feature Request Template
```markdown
**Feature Description**
Brief description of the feature

**Use Case**
Why this feature is needed

**Implementation Ideas**
How it might be implemented

**Mockups**
If applicable, include mockups or wireframes
```

## 📋 Pull Request Process

### Before Submitting
1. Ensure all tests pass
2. Run linting and fix any issues
3. Update documentation if needed
4. Test the feature manually
5. Ensure code follows style guidelines

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏷️ Release Process

### Versioning
We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written

## 📞 Getting Help

### Questions and Support
- Create an issue for questions
- Use GitHub Discussions for general questions
- Join our community chat (if available)

### Communication Channels
- GitHub Issues: For bugs and feature requests
- GitHub Discussions: For questions and discussions
- Email: For security issues

## 🎉 Recognition

### Contributors
All contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

### Contribution Levels
- **Contributor**: Any contribution
- **Maintainer**: Regular contributions and reviews
- **Core Team**: Project leadership and major decisions

Thank you for contributing to the iPhone Installment Store project! 🚀 