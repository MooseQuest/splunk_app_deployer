# Splunk App Deployer

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/MooseQuest/splunk_app_deployer)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Splunk](https://img.shields.io/badge/Splunk-8.0%2B-orange)](https://www.splunk.com/)

A modern Python tool for **local development and testing** of Splunk apps with interactive guidance, cross-platform support, and comprehensive validation.

> ⚠️ **Development Tool**: This tool is designed for local app development and testing environments. For production deployments, we recommend implementing proper CI/CD pipelines with automated testing, code review, and deployment approval processes.

## 🌟 Features

- 🐍 **Modern Python Implementation** - Clean, maintainable code with type hints
- 🌐 **Cross-Platform Support** - Works on Linux, macOS, and Windows
- 🎯 **Interactive App Selection** - Choose from available apps with version display
- 📚 **Informative Restart Prompts** - Understand why Splunk needs to restart
- 💾 **Automatic Backups** - Safe deployment with rollback capability
- ✅ **Structure Validation** - Ensures apps meet Splunk requirements
- 🔄 **Git Integration** - Optional commit creation with deployment summary
- 📝 **Comprehensive Logging** - Detailed logs for troubleshooting
- 🎨 **Colored Output** - Enhanced user experience with visual feedback
- 🛠️ **Flexible Options** - Command-line arguments or interactive mode

## 🚀 Quick Start

### Prerequisites

- Python 3.6+ 
- Splunk Enterprise 8.0+
- Git (optional, for version control integration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MooseQuest/splunk_app_deployer.git
   cd splunk_app_deployer
   ```

2. **Make the script executable:**
   ```bash
   chmod +x splunk_app_deployer.py
   ```

3. **Run your first deployment:**
   ```bash
   python3 splunk_app_deployer.py --help
   ```

### Basic Usage

```bash
# Interactive mode with OS-specific guidance
python3 splunk_app_deployer.py

# Quick deployment with automatic restart
python3 splunk_app_deployer.py --restart

# Specify custom Splunk installation
python3 splunk_app_deployer.py --splunk-home /opt/splunk --restart
```

## 📖 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions for all platforms
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage guide with examples and workflows
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Technical guide for extending and customizing the tool
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide for common issues

## 🎯 Use Cases

### 🔧 **Local Development & Testing** (Primary Use Case)

This tool is designed for **local development environments** where developers are:
- Building and testing Splunk apps locally
- Iterating on app configurations and dashboards
- Validating app structure and functionality
- Learning Splunk app development concepts

```bash
# Development workflow - multiple apps, restart once at the end
python3 splunk_app_deployer.py  # App 1, choose 'n' for restart
python3 splunk_app_deployer.py  # App 2, choose 'n' for restart
python3 splunk_app_deployer.py  # App 3, choose 'y' for restart
```

### 🧪 **Testing & Validation**

Suitable for controlled testing environments:
- Development Splunk instances
- Testing new app versions before production
- Validating app compatibility and functionality

```bash
# Testing deployment with validation
python3 splunk_app_deployer.py --splunk-home /opt/splunk-dev --restart
```

### ⚠️ **Production Deployments** (Not Recommended)

While this tool *can* be used for production, we **strongly recommend** implementing proper CI/CD pipelines for production deployments that include:

- **Automated Testing**: Unit tests, integration tests, and validation checks
- **Code Review**: Peer review and approval processes
- **Deployment Approval**: Manual approval gates for production changes
- **Rollback Capabilities**: Automated rollback on deployment failures
- **Monitoring & Alerting**: Deployment success/failure monitoring
- **Audit Logging**: Complete deployment audit trails

**Recommended Production Tools:**
- **GitLab CI/CD** or **GitHub Actions** for automation
- **Splunk REST API** for programmatic deployments
- **Ansible** or **Terraform** for infrastructure-as-code
- **Splunk Deployment Server** for large-scale app distribution
## 🖥️ Platform Support

| Platform | Status | Default Splunk Path | Notes |
|----------|--------|---------------------|-------|
| **Linux** | ✅ Full Support | `/opt/splunk` | Systemd integration |
| **macOS** | ✅ Full Support | `/Applications/Splunk` | Launchd integration |
| **Windows** | ✅ Full Support | `C:\Program Files\Splunk` | Services integration |

## 🔄 Restart Management

The tool includes comprehensive restart guidance that explains:

- **Why Splunk restart is required** (based on official documentation)
- **What happens during restart** (step-by-step process)
- **How to verify successful deployment** (validation checklist)
- **When NOT to restart** (timing considerations)
- **Manual restart options** (OS-specific commands)

## 📊 Command Line Options

```
Usage: python3 splunk_app_deployer.py [OPTIONS]

Options:
  --splunk-home PATH      Path to Splunk installation directory
  --splunk-apps-dir PATH  Target apps directory (default: SPLUNK_HOME/etc/apps)
  --restart              Automatically restart Splunk after deployment
  --help, -h             Show help message

Examples:
  python3 splunk_app_deployer.py                    # Full interactive mode
  python3 splunk_app_deployer.py --restart          # Interactive with auto-restart
  python3 splunk_app_deployer.py --splunk-home /opt/splunk --restart  # Fully automated
```

## 🏗️ Project Structure

```
splunk_app_deployer/
├── splunk_app_deployer.py     # Main deployment script
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── requirements.txt          # Python dependencies (none!)
├── docs/                     # Documentation
│   ├── INSTALLATION.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── ARCHITECTURE.md
├── examples/                 # Example configurations
│   ├── sample_app_structure/
│   └── deployment_scripts/
└── tests/                    # Test files (future)
    └── test_deployer.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Setup

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the linter:** `python -m flake8 splunk_app_deployer.py`
5. **Commit your changes:** `git commit -m 'Add amazing feature'`
6. **Push to the branch:** `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/MooseQuest/splunk_app_deployer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/MooseQuest/splunk_app_deployer/discussions)
- **General Contact:** [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net)

## 🙏 Acknowledgments

- **Splunk Inc.** for comprehensive documentation
- **Python Community** for excellent standard library
- **Open Source Contributors** who help improve this tool

## 📈 Roadmap

- [ ] **Unit Tests** - Comprehensive test coverage
- [ ] **Docker Support** - Containerized deployment scenarios
- [ ] **Cluster Deployment** - Search head cluster support
- [ ] **Web Interface** - Optional web-based UI
- [ ] **Configuration Validation** - Advanced app.conf validation
- [ ] **Performance Metrics** - Deployment timing and statistics

## ⭐ Show Your Support

If this project helps you, please consider giving it a star on GitHub! ⭐

---

**Made with ❤️ for the Splunk Community** 