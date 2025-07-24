# Installation Guide

This guide will help you install and set up Splunk App Deployer on your system.

## 📋 Prerequisites

### System Requirements

- **Python 3.6 or higher**
- **Splunk Enterprise 8.0 or higher**
- **Git** (optional, for version control integration)

### Platform Support

| Platform | Status | Tested Versions |
|----------|--------|-----------------|
| Linux | ✅ Full Support | Ubuntu 18.04+, CentOS 7+, RHEL 7+ |
| macOS | ✅ Full Support | macOS 10.14+, Big Sur, Monterey |
| Windows | ✅ Full Support | Windows 10+, Server 2016+ |

## 🚀 Installation Methods

### Method 1: Git Clone (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer

# Make executable
chmod +x splunk_app_deployer.py

# Test installation
python3 splunk_app_deployer.py --help
```

### Method 2: Direct Download

```bash
# Download the script directly
curl -O https://raw.githubusercontent.com/yourusername/splunk-app-deployer/main/splunk_app_deployer.py

# Make executable
chmod +x splunk_app_deployer.py

# Test installation
python3 splunk_app_deployer.py --help
```

### Method 3: Manual Download

1. Visit the [GitHub repository](https://github.com/yourusername/splunk-app-deployer)
2. Download the `splunk_app_deployer.py` file
3. Place it in your desired directory
4. Make it executable: `chmod +x splunk_app_deployer.py`

## 🔧 Platform-Specific Setup

### Linux Setup

#### Ubuntu/Debian
```bash
# Ensure Python 3.6+ is installed
sudo apt update
sudo apt install python3 python3-pip

# Verify version
python3 --version

# Install Splunk App Deployer
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer
chmod +x splunk_app_deployer.py
```

#### CentOS/RHEL/Fedora
```bash
# Ensure Python 3.6+ is installed
sudo yum install python3 python3-pip  # CentOS 7
# or
sudo dnf install python3 python3-pip  # CentOS 8+/Fedora

# Verify version
python3 --version

# Install Splunk App Deployer
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer
chmod +x splunk_app_deployer.py
```

### macOS Setup

#### Using Homebrew (Recommended)
```bash
# Install Python 3 if not already installed
brew install python3

# Verify version
python3 --version

# Install Splunk App Deployer
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer
chmod +x splunk_app_deployer.py
```

#### Using System Python
```bash
# macOS 10.15+ includes Python 3
python3 --version

# If Python 3 is not available, install from python.org
# Then proceed with installation
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer
chmod +x splunk_app_deployer.py
```

### Windows Setup

#### Using Git Bash (Recommended)
```bash
# Install Git for Windows (includes Git Bash)
# Download from: https://git-scm.com/download/win

# In Git Bash terminal:
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer

# Test (no chmod needed on Windows)
python splunk_app_deployer.py --help
```

#### Using PowerShell
```powershell
# Ensure Python 3.6+ is installed
python --version

# Clone repository
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer

# Test installation
python splunk_app_deployer.py --help
```

#### Using WSL (Windows Subsystem for Linux)
```bash
# In WSL terminal, follow Linux instructions
sudo apt update
sudo apt install python3 git
git clone https://github.com/yourusername/splunk-app-deployer.git
cd splunk-app-deployer
chmod +x splunk_app_deployer.py
```

## ✅ Verification

### Basic Functionality Test

```bash
# Test help system
python3 splunk_app_deployer.py --help

# Test OS detection
python3 splunk_app_deployer.py --help | grep "Detected"

# Test without Splunk (should show error about missing Splunk)
python3 splunk_app_deployer.py
```

### Expected Output

You should see:
```
SDS Multi-App Deployment Script (Python)

This script allows you to deploy one or more Splunk apps...

Usage:
  python3 splunk_app_deployer.py [OPTIONS]

Options:
  --splunk-home PATH      Path to Splunk installation directory
  --splunk-apps-dir PATH  Target apps directory
  --restart              Automatically restart Splunk after deployment
  --help, -h             Show this help message
```

## 🗂️ Directory Structure Setup

### For App Development

If you're developing Splunk apps, create this structure:
```bash
mkdir -p ~/splunk_apps/
cd ~/splunk_apps/

# Your app development directory
mkdir -p my_apps/
cd my_apps/

# Example app structure
mkdir -p my_splunk_app/{default,metadata,bin,static}
```

### For System-Wide Installation

```bash
# Option 1: User directory
mkdir -p ~/.local/bin
cp splunk_app_deployer.py ~/.local/bin/
# Add ~/.local/bin to PATH if not already

# Option 2: System-wide (requires sudo)
sudo cp splunk_app_deployer.py /usr/local/bin/
sudo chmod +x /usr/local/bin/splunk_app_deployer.py
```

## 🔐 Permissions Setup

### Linux/macOS

```bash
# Make script executable
chmod +x splunk_app_deployer.py

# If deploying to system Splunk installation
# Ensure your user can access Splunk directories
# Option 1: Add user to splunk group
sudo usermod -a -G splunk $USER

# Option 2: Use sudo when running the script
sudo python3 splunk_app_deployer.py --splunk-home /opt/splunk
```

### Windows

```cmd
# No special permissions needed for the script
# But you may need to run as Administrator for system directories

# Test with user permissions first
python splunk_app_deployer.py --help

# If needed, run PowerShell/Command Prompt as Administrator
```

## 🛠️ Troubleshooting Installation

### Common Issues

#### Python Version Error
```bash
# Error: Python 3.6+ required
python3 --version

# If version is too old, install newer Python
# Ubuntu/Debian:
sudo apt install python3.9

# macOS with Homebrew:
brew install python@3.9

# Windows: Download from python.org
```

#### Permission Denied
```bash
# Linux/macOS
chmod +x splunk_app_deployer.py

# If still fails, check file ownership
ls -la splunk_app_deployer.py
sudo chown $USER:$USER splunk_app_deployer.py
```

#### Git Not Found
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL
sudo yum install git

# macOS
brew install git

# Windows: Download from git-scm.com
```

#### Import Errors
```bash
# Test Python standard library availability
python3 -c "import os, sys, pathlib, subprocess, tarfile; print('✅ All imports successful')"

# If imports fail, Python installation may be incomplete
```

### Getting Help

If you encounter issues:

1. **Check Python version**: `python3 --version` (must be 3.6+)
2. **Test basic script**: `python3 splunk_app_deployer.py --help`
3. **Check file permissions**: `ls -la splunk_app_deployer.py`
4. **Verify Splunk installation** (if applicable)
5. **Open a GitHub issue** with your error details

## 🎯 Next Steps

After successful installation:

1. **Read the [User Guide](USER_GUIDE.md)** for usage instructions
2. **Check [Troubleshooting](TROUBLESHOOTING.md)** for common issues
3. **Review [Examples](../examples/)** for typical workflows
4. **Join [GitHub Discussions](https://github.com/yourusername/splunk-app-deployer/discussions)** for community support

## 📦 Package Managers (Future)

We're considering support for:
- **pip**: `pip install splunk-app-deployer`
- **homebrew**: `brew install splunk-app-deployer`
- **apt**: `apt install splunk-app-deployer`

Follow the repository for updates on package distribution! 