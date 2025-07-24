# Developer Guide

This guide is for developers who want to understand, modify, or extend the Splunk App Deployer.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Code Structure](#code-structure)
- [Core Components](#core-components)
- [Configuration System](#configuration-system)
- [Extending the Tool](#extending-the-tool)
- [Testing and Development](#testing-and-development)
- [Contributing](#contributing)
- [API Reference](#api-reference)

## 🏗️ Architecture Overview

### Design Philosophy

The Splunk App Deployer follows these principles:

- **Zero Dependencies**: Uses only Python standard library
- **Cross-Platform**: Works consistently across Linux, macOS, and Windows
- **User-Friendly**: Provides comprehensive guidance and clear feedback
- **Secure by Design**: Validates inputs and provides safe defaults
- **Extensible**: Modular design allows easy customization

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                  Main Script                   │
│              splunk_app_deployer.py             │
└─────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────┐  ┌──────▼──────┐  ┌─────▼─────┐
│DeploymentMgr│  │  OSConfig   │  │  Logger   │
│             │  │             │  │           │
└─────────────┘  └─────────────┘  └───────────┘
        │
        ▼
┌──────────────┐
│SplunkAppMgr  │
│              │
└──────────────┘
```

### Data Flow

1. **Initialization**: Parse arguments, detect OS, initialize components
2. **Discovery**: Scan source directory for valid Splunk apps
3. **Validation**: Check app structure and requirements
4. **Selection**: Interactive or automated app selection
5. **Backup**: Create timestamped backups of existing apps
6. **Deployment**: Copy apps with appropriate permissions
7. **Post-Processing**: Update versions, create git commits, restart handling

## 📂 Code Structure

### File Organization

```
splunk_app_deployer.py          # Main script (740+ lines)
├── Classes:
│   ├── Colors                  # ANSI color constants
│   ├── DeploymentLogger        # Centralized logging
│   ├── OSConfig                # OS detection and configuration
│   ├── SplunkAppManager        # App validation and management
│   └── DeploymentManager       # Main orchestration
├── Functions:
│   ├── show_help()             # Help text display
│   └── main()                  # Entry point
└── Constants:
    └── GLOBAL VARIABLES        # Selected apps storage
```

### Import Structure

```python
# Standard library only - no external dependencies
import os
import sys
import platform
import argparse
import subprocess
import tarfile
import configparser
import datetime
import re
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Tuple
```

## 🔧 Core Components

### 1. DeploymentLogger Class

**Purpose**: Centralized logging with colored output and file persistence

```python
class DeploymentLogger:
    def __init__(self, log_dir: Path):
        # Initialize logging to both console and file
        
    def log(self, message: str, level: str = "INFO"):
        # Log with timestamp and level
        
    def error(self, message: str):
        # Log error with red color
        
    def warning(self, message: str):
        # Log warning with yellow color
        
    def success(self, message: str):
        # Log success with green color
        
    def bold(self, message: str):
        # Log with bold formatting
```

**Key Features**:
- ANSI color support with fallback for unsupported terminals
- Timestamped file logging
- Multiple log levels (INFO, WARNING, ERROR, SUCCESS)
- Thread-safe operation

### 2. OSConfig Class

**Purpose**: Operating system detection and configuration

```python
class OSConfig:
    def __init__(self):
        self.os_type = self._detect_os()
        self.splunk_executable = self._get_splunk_executable()
        self.default_splunk_home = self._get_default_splunk_home()
        
    def _detect_os(self) -> str:
        # Returns 'Linux', 'macOS', or 'Windows'
        
    def get_backup_command(self) -> List[str]:
        # Returns OS-appropriate backup command
```

**Handled Differences**:
- Default Splunk installation paths
- Executable names (`splunk` vs `splunk.exe`)
- File permission handling
- Service management commands

### 3. SplunkAppManager Class

**Purpose**: App validation, version management, and structure checking

```python
class SplunkAppManager:
    def validate_app_structure(self, app_path: Path) -> bool:
        # Validates required files and directories
        
    def get_app_version(self, app_path: Path) -> str:
        # Extracts version from app.conf
        
    def update_app_version(self, app_path: Path, new_version: str):
        # Updates version in app.conf
        
    def discover_apps(self, source_dir: Path) -> List[Dict]:
        # Finds and validates all apps in directory
```

**Validation Checks**:
- Required directories: `default/`, `metadata/`
- Required files: `app.conf`, `default.meta`
- Valid app.conf format for version extraction
- Splunk app naming conventions

### 4. DeploymentManager Class

**Purpose**: Main orchestration and workflow management

```python
class DeploymentManager:
    def __init__(self, apps_source_dir: Optional[Path] = None):
        # Initialize all components
        
    def run(self, splunk_home: Path = None, 
            splunk_apps_dir: Path = None, 
            restart: bool = False):
        # Main deployment workflow
        
    def deploy_app(self, app_info: Dict, target_dir: Path) -> bool:
        # Deploy single app with validation
        
    def create_backup(self, app_path: Path) -> Path:
        # Create timestamped backup
        
    def restart_splunk(self, splunk_home: Path):
        # Handle Splunk restart with OS-specific commands
```

## ⚙️ Configuration System

### Environment Detection

The tool automatically detects and configures based on:

```python
# OS-specific defaults
DEFAULT_PATHS = {
    'Linux': '/opt/splunk',
    'macOS': '/Applications/Splunk', 
    'Windows': 'C:\\Program Files\\Splunk'
}

# Command variations
SPLUNK_EXECUTABLES = {
    'Linux': 'splunk',
    'macOS': 'splunk',
    'Windows': 'splunk.exe'
}
```

### Configuration Sources (Priority Order)

1. **Command Line Arguments**: `--splunk-home`, `--apps-source-dir`, etc.
2. **Interactive Prompts**: User input during execution
3. **Environment Detection**: OS-based defaults
4. **Hardcoded Defaults**: Fallback values

### Adding New Configuration Options

```python
# 1. Add to argument parser
parser.add_argument('--my-option', help='My new option')

# 2. Pass to DeploymentManager
deployment_manager.run(my_option=args.my_option)

# 3. Use in implementation
def run(self, my_option: str = None):
    if my_option:
        # Use custom value
    else:
        # Use default logic
```

## 🔌 Extending the Tool

### Adding New Operating Systems

1. **Update OS Detection**:
```python
def _detect_os(self) -> str:
    system = platform.system()
    if system == "Linux":
        return "Linux"
    elif system == "Darwin":
        return "macOS"
    elif system == "Windows":
        return "Windows"
    elif system == "FreeBSD":  # New OS
        return "FreeBSD"
    else:
        return "Unknown"
```

2. **Add OS-Specific Configuration**:
```python
def _get_default_splunk_home(self) -> str:
    defaults = {
        'Linux': '/opt/splunk',
        'macOS': '/Applications/Splunk',
        'Windows': 'C:\\Program Files\\Splunk',
        'FreeBSD': '/usr/local/splunk'  # New default
    }
    return defaults.get(self.os_type, '/opt/splunk')
```

### Adding New Validation Rules

```python
def validate_app_structure(self, app_path: Path) -> bool:
    """Extended validation with custom rules"""
    
    # Standard validation
    if not self._check_required_files(app_path):
        return False
        
    # Custom validation
    if not self._check_custom_requirements(app_path):
        return False
        
    return True

def _check_custom_requirements(self, app_path: Path) -> bool:
    """Add your custom validation logic here"""
    
    # Example: Check for specific file patterns
    if not (app_path / 'static' / 'appIcon.png').exists():
        self.logger.warning(f"No app icon found for {app_path.name}")
        
    # Example: Validate app naming convention
    if not re.match(r'^[a-z_][a-z0-9_]*$', app_path.name):
        self.logger.error(f"Invalid app name: {app_path.name}")
        return False
        
    return True
```

### Adding New Deployment Hooks

```python
class DeploymentManager:
    def deploy_app(self, app_info: Dict, target_dir: Path) -> bool:
        """Deploy with custom hooks"""
        
        # Pre-deployment hook
        if not self._pre_deploy_hook(app_info):
            return False
            
        # Standard deployment
        success = self._copy_app(app_info, target_dir)
        
        # Post-deployment hook
        if success:
            self._post_deploy_hook(app_info, target_dir)
            
        return success
    
    def _pre_deploy_hook(self, app_info: Dict) -> bool:
        """Override for custom pre-deployment logic"""
        # Example: Check disk space
        # Example: Validate dependencies
        # Example: Run custom tests
        return True
        
    def _post_deploy_hook(self, app_info: Dict, target_dir: Path):
        """Override for custom post-deployment logic"""
        # Example: Update configuration files
        # Example: Trigger external systems
        # Example: Send notifications
        pass
```

### Adding New Command Line Options

1. **Update Argument Parser**:
```python
def main():
    parser = argparse.ArgumentParser(description='Deploy Splunk apps')
    
    # Existing options...
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be deployed without doing it')
    parser.add_argument('--parallel', type=int, default=1,
                       help='Number of parallel deployments')
```

2. **Implement in DeploymentManager**:
```python
def run(self, dry_run: bool = False, parallel: int = 1):
    if dry_run:
        self.logger.info("DRY RUN MODE - No changes will be made")
        return self._simulate_deployment()
        
    if parallel > 1:
        return self._parallel_deployment(parallel)
```

## 🧪 Testing and Development

### Development Setup

```bash
# Clone and set up development environment
git clone https://github.com/MooseQuest/splunk_app_deployer.git
cd splunk_app_deployer

# Create test apps directory
mkdir -p test_apps/sample_app/{default,metadata}

# Create minimal test app
echo '[launcher]
version = 1.0.0
[package]
id = sample_app' > test_apps/sample_app/default/app.conf

echo '[]
access = read : [ * ], write : [ admin ]' > test_apps/sample_app/metadata/default.meta
```

### Manual Testing

```bash
# Test app discovery
python3 splunk_app_deployer.py --apps-source-dir test_apps --help

# Test validation
python3 splunk_app_deployer.py --apps-source-dir test_apps

# Test with different OS paths
python3 splunk_app_deployer.py --splunk-home /custom/path
```

### Code Quality Checks

```bash
# Syntax check
python3 -m py_compile splunk_app_deployer.py

# Import check
python3 -c "import splunk_app_deployer; print('✅ Import successful')"

# Basic functionality check
python3 splunk_app_deployer.py --help > /dev/null && echo "✅ Help works"
```

### Debugging

Enable debug logging by modifying the logger:

```python
# In DeploymentLogger.__init__
def __init__(self, log_dir: Path, debug: bool = False):
    self.debug_enabled = debug
    
def debug(self, message: str):
    if self.debug_enabled:
        self.log(f"DEBUG: {message}")
```

### Performance Profiling

```python
import time
import cProfile

# Add timing to methods
def deploy_app(self, app_info: Dict, target_dir: Path) -> bool:
    start_time = time.time()
    try:
        # ... deployment logic ...
        return True
    finally:
        elapsed = time.time() - start_time
        self.logger.debug(f"App deployment took {elapsed:.2f}s")

# Profile entire execution
if __name__ == "__main__":
    cProfile.run('main()', 'deployment_profile.prof')
```

## 🤝 Contributing

### Code Style Guidelines

- **Follow PEP 8** for Python style
- **Use type hints** for all function parameters and returns
- **Add docstrings** for all classes and public methods
- **Keep functions focused** - single responsibility principle
- **Use meaningful names** - self-documenting code

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/my-enhancement`
3. **Make changes** with appropriate tests
4. **Test thoroughly** on multiple platforms if possible
5. **Update documentation** as needed
6. **Submit pull request** with clear description

### Adding Features

When adding new features:

1. **Check compatibility** with zero-dependency requirement
2. **Ensure cross-platform** compatibility
3. **Add appropriate error handling**
4. **Update help text** and documentation
5. **Consider backward compatibility**

## 📚 API Reference

### Core Classes

#### DeploymentLogger

```python
class DeploymentLogger:
    """Centralized logging with colored output"""
    
    def __init__(self, log_dir: Path)
    def log(self, message: str, level: str = "INFO")
    def error(self, message: str)
    def warning(self, message: str) 
    def success(self, message: str)
    def bold(self, message: str)
```

#### OSConfig

```python
class OSConfig:
    """OS detection and configuration"""
    
    os_type: str                    # 'Linux', 'macOS', or 'Windows'
    splunk_executable: str          # OS-appropriate executable name
    default_splunk_home: str        # Default installation path
    
    def get_backup_command(self) -> List[str]
    def get_permission_command(self, path: Path) -> List[str]
```

#### SplunkAppManager

```python
class SplunkAppManager:
    """App validation and management"""
    
    def validate_app_structure(self, app_path: Path) -> bool
    def get_app_version(self, app_path: Path) -> str
    def update_app_version(self, app_path: Path, new_version: str)
    def discover_apps(self, source_dir: Path) -> List[Dict]
```

#### DeploymentManager

```python
class DeploymentManager:
    """Main deployment orchestration"""
    
    def __init__(self, apps_source_dir: Optional[Path] = None)
    def run(self, splunk_home: Path = None, 
            splunk_apps_dir: Path = None, 
            restart: bool = False)
    def deploy_app(self, app_info: Dict, target_dir: Path) -> bool
    def create_backup(self, app_path: Path) -> Path
    def restart_splunk(self, splunk_home: Path)
```

### Key Data Structures

```python
# App information dictionary
app_info = {
    'name': str,           # App directory name
    'path': Path,          # Full path to app
    'version': str,        # Current version from app.conf
    'valid': bool          # Validation status
}

# Global state
SELECTED_APPS: List[str] = []  # App names selected for deployment
```

### Error Handling Patterns

```python
try:
    # Operation that might fail
    result = risky_operation()
except SpecificException as e:
    self.logger.error(f"Specific error occurred: {e}")
    return False
except Exception as e:
    self.logger.error(f"Unexpected error: {e}")
    return False
else:
    self.logger.success("Operation completed successfully")
    return True
```

## 🔧 Customization Examples

### Custom Backup Strategy

```python
def create_backup(self, app_path: Path) -> Path:
    """Custom backup with compression and rotation"""
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{app_path.name}_backup_{timestamp}"
    
    # Custom backup location
    backup_dir = Path.home() / 'splunk_backups'
    backup_dir.mkdir(exist_ok=True)
    
    # Create backup with custom compression
    backup_path = backup_dir / f"{backup_name}.tar.xz"
    
    # Rotate old backups (keep last 5)
    self._rotate_backups(backup_dir, app_path.name, keep=5)
    
    return backup_path
```

### Custom Validation Rules

```python
def validate_app_structure(self, app_path: Path) -> bool:
    """Extended validation with organization standards"""
    
    # Standard validation
    if not super().validate_app_structure(app_path):
        return False
    
    # Custom: Check for required documentation
    if not (app_path / 'README.md').exists():
        self.logger.warning(f"Missing README.md in {app_path.name}")
    
    # Custom: Validate version format (semantic versioning)
    version = self.get_app_version(app_path)
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        self.logger.error(f"Invalid version format: {version}")
        return False
    
    # Custom: Check for test directory
    if not (app_path / 'tests').exists():
        self.logger.warning(f"No tests directory in {app_path.name}")
    
    return True
```

---

This developer guide provides the foundation for understanding and extending the Splunk App Deployer. For additional support, contact [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net) or open an issue on GitHub.
