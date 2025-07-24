# Contributing to Splunk App Deployer

Thank you for your interest in contributing to Splunk App Deployer! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

We welcome contributions of all kinds:

- 🐛 **Bug Reports** - Help us identify and fix issues
- 💡 **Feature Requests** - Suggest new functionality
- 📝 **Documentation** - Improve our docs and examples
- 🔧 **Code Contributions** - Submit bug fixes and new features
- 🧪 **Testing** - Help us test on different platforms
- 💬 **Community Support** - Help other users in discussions

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer

# Add the original repository as upstream
git remote add upstream https://github.com/original/splunk-app-deployer.git
```

### 2. Set Up Development Environment

```bash
# Ensure you have Python 3.6+
python3 --version

# Make the script executable
chmod +x splunk_app_deployer.py

# Test the script
python3 splunk_app_deployer.py --help
```

### 3. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

## 📝 Development Guidelines

### Code Style

- **Follow PEP 8** Python style guidelines
- **Use type hints** for function parameters and return values
- **Add docstrings** for all classes and functions
- **Keep functions focused** - single responsibility principle
- **Use meaningful variable names** - clear and descriptive

### Code Quality

```bash
# Run basic linting (optional - we don't require external tools)
python3 -m py_compile splunk_app_deployer.py

# Check for basic syntax issues
python3 -c "import splunk_app_deployer; print('✅ Import successful')"
```

### Testing

- **Manual testing** on different platforms (Linux, macOS, Windows)
- **Test with different Splunk versions** (8.0+)
- **Verify cross-platform compatibility** for new features
- **Test both interactive and automated modes**

## 🐛 Bug Reports

When reporting bugs, please include:

### Required Information

1. **Environment Details:**
   ```
   - OS: (Linux/macOS/Windows + version)
   - Python version: (python3 --version)
   - Splunk version: (if applicable)
   ```

2. **Steps to Reproduce:**
   ```
   1. Command executed
   2. Expected behavior
   3. Actual behavior
   4. Error messages (if any)
   ```

3. **Additional Context:**
   - Log files (from logs/ directory)
   - Screenshots (if UI-related)
   - Configuration details

### Bug Report Template

```markdown
**Environment:**
- OS: Ubuntu 20.04
- Python: 3.8.10
- Splunk: 8.2.0

**Command Executed:**
```bash
python3 splunk_app_deployer.py --restart
```

**Expected Behavior:**
Script should restart Splunk after deployment

**Actual Behavior:**
Script hangs after showing restart prompt

**Error Messages:**
```
[2025-01-15 10:30:00] ❌ Timeout waiting for Splunk restart
```

**Additional Context:**
Using custom Splunk installation path
```

## 💡 Feature Requests

When suggesting features, please include:

- **Use Case:** Why is this feature needed?
- **Description:** What should the feature do?
- **Examples:** How would users interact with it?
- **Alternatives:** Are there existing workarounds?

## 🔧 Code Contributions

### Pull Request Process

1. **Update Documentation:**
   - Update README.md if needed
   - Add docstrings for new functions
   - Update help text for new options

2. **Test Your Changes:**
   - Test on your local platform
   - Verify existing functionality still works
   - Test both interactive and automated modes

3. **Commit Messages:**
   ```bash
   # Good commit messages
   git commit -m "Add support for custom app directories"
   git commit -m "Fix restart timeout on Windows"
   git commit -m "Improve error messages for invalid paths"
   
   # Follow conventional commit format (optional)
   git commit -m "feat: add batch deployment mode"
   git commit -m "fix: handle missing app.conf files gracefully"
   git commit -m "docs: update installation instructions"
   ```

4. **Submit Pull Request:**
   - Use descriptive title and description
   - Link to related issues
   - Explain what changed and why

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested on Linux
- [ ] Tested on macOS  
- [ ] Tested on Windows
- [ ] Tested interactive mode
- [ ] Tested automated mode

## Related Issues
Fixes #123, Closes #456
```

## 📚 Documentation Contributions

We welcome improvements to:

- **README.md** - Main project documentation
- **Code Comments** - Inline documentation
- **Examples** - Usage examples and tutorials
- **Troubleshooting** - Common issues and solutions

### Documentation Style

- **Use clear, simple language**
- **Provide code examples** where helpful
- **Include screenshots** for UI elements
- **Test all examples** before submitting

## 🌐 Platform-Specific Contributions

We especially welcome contributions that improve:

- **Windows compatibility** and testing
- **macOS-specific features** (launchd integration)
- **Linux distribution support** (systemd, init.d)
- **Cloud environment** compatibility

## 🚫 What We Don't Accept

- **Breaking changes** without strong justification
- **External dependencies** (we aim to use only Python standard library)
- **Platform-specific code** without fallbacks
- **Unsafe operations** (like automatic sudo/admin escalation)

## 📋 Review Process

1. **Automated Checks:** Basic syntax and import validation
2. **Manual Review:** Code quality, functionality, documentation
3. **Testing:** Platform compatibility verification
4. **Discussion:** Clarifications and suggestions
5. **Approval:** Merge when ready

## 💬 Community

- **Be respectful** and constructive in all interactions
- **Help others** learn and contribute
- **Share knowledge** and experiences
- **Follow** the [Code of Conduct](CODE_OF_CONDUCT.md)

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## 🎯 Current Priorities

Help us focus on these areas:

- [ ] **Unit Tests** - Automated testing framework
- [ ] **Docker Support** - Containerized deployment
- [ ] **Configuration Validation** - Enhanced app.conf checking
- [ ] **Performance Optimization** - Faster deployment for large apps
- [ ] **Error Handling** - Better error messages and recovery

## 📞 Questions?

- **GitHub Discussions** - For general questions and ideas
- **GitHub Issues** - For bug reports and feature requests
- **Pull Requests** - For code contributions

Thank you for contributing to Splunk App Deployer! 🙏 