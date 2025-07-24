# User Guide

This guide provides comprehensive instructions for using the Splunk App Deployer for local development and testing.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Interactive Mode](#interactive-mode)
- [Command Line Options](#command-line-options)
- [Deployment Workflow](#deployment-workflow)
- [Understanding Restart Options](#understanding-restart-options)
- [Working with Multiple Apps](#working-with-multiple-apps)
- [Best Practices](#best-practices)
- [Common Workflows](#common-workflows)

## 🚀 Getting Started

### Prerequisites

Before using the Splunk App Deployer, ensure you have:

- **Python 3.6+** installed
- **Splunk Enterprise 8.0+** running locally
- **Apps to deploy** in a structured format
- **Basic command line knowledge**

### First Run

```bash
# Navigate to the deployer directory
cd splunk_app_deployer

# Run in interactive mode
python3 splunk_app_deployer.py
```

On first run, the tool will:
1. Detect your operating system
2. Suggest default Splunk installation paths
3. Guide you through app selection
4. Explain restart requirements

## 💻 Basic Usage

### Interactive Mode (Recommended)

The easiest way to use the deployer:

```bash
python3 splunk_app_deployer.py
```

**What happens:**
1. **OS Detection**: Automatically detects Linux, macOS, or Windows
2. **Splunk Home**: Prompts for or detects Splunk installation directory
3. **App Discovery**: Scans for valid Splunk apps in the source directory
4. **App Selection**: Interactive menu to choose which apps to deploy
5. **Version Management**: Shows current versions and prompts for updates
6. **Validation**: Checks app structure before deployment
7. **Deployment**: Copies apps with proper permissions
8. **Restart Guidance**: Educational prompts about Splunk restart requirements

### Quick Deployment

For faster deployment when you know your setup:

```bash
# Deploy with automatic restart
python3 splunk_app_deployer.py --restart

# Specify custom Splunk location
python3 splunk_app_deployer.py --splunk-home /opt/splunk --restart
```

## 🎛️ Interactive Mode

### App Selection Process

When you run the tool interactively, you'll see:

```
Available apps:
1. my_security_app (v1.0.0)
2. dashboard_toolkit (v2.1.0)  
3. data_quality_checker (v1.5.0)

Select apps to deploy (comma-separated, e.g., 1,3): 1,2
```

**Tips:**
- Select multiple apps with commas: `1,2,3`
- See current versions before updating
- Apps are validated before selection

### Version Management

For each selected app:

```
Current version of my_security_app: 1.0.0
Enter new version (or press Enter to keep current): 1.1.0
```

**Version Guidelines:**
- Use semantic versioning (e.g., 1.0.0, 1.1.0, 2.0.0)
- Increment major version for breaking changes
- Increment minor version for new features
- Increment patch version for bug fixes

### Splunk Home Detection

The tool provides OS-specific defaults:

| OS | Default Path | Alternative Locations |
|----|--------------|---------------------|
| **Linux** | `/opt/splunk` | `/home/splunk/splunk` |
| **macOS** | `/Applications/Splunk` | `/Users/splunk/splunk` |
| **Windows** | `C:\Program Files\Splunk` | `C:\Splunk` |

You can override these by:
- Typing a custom path when prompted
- Using `--splunk-home` command line option

## ⚙️ Command Line Options

### Available Options

```bash
python3 splunk_app_deployer.py [OPTIONS]
```

| Option | Description | Example |
|--------|-------------|---------|
| `--splunk-home PATH` | Splunk installation directory | `--splunk-home /opt/splunk` |
| `--splunk-apps-dir PATH` | Target apps directory | `--splunk-apps-dir /opt/splunk/etc/apps` |
| `--apps-source-dir PATH` | Source directory with apps | `--apps-source-dir ./my_apps` |
| `--restart` | Automatically restart Splunk | `--restart` |
| `--help, -h` | Show help message | `--help` |

### Usage Examples

```bash
# Full interactive mode
python3 splunk_app_deployer.py

# Interactive with custom source directory  
python3 splunk_app_deployer.py --apps-source-dir /path/to/my/apps

# Automated deployment
python3 splunk_app_deployer.py \
  --splunk-home /opt/splunk \
  --apps-source-dir ./development_apps \
  --restart

# Development environment
python3 splunk_app_deployer.py \
  --splunk-home /Users/developer/splunk \
  --restart
```

## 🔄 Deployment Workflow

### Step-by-Step Process

1. **Environment Validation**
   - Checks Python version and dependencies
   - Validates source directory exists
   - Confirms apps directory structure

2. **App Discovery and Validation**
   - Scans source directory for valid Splunk apps
   - Validates required files (`app.conf`, `default.meta`)
   - Checks directory structure compliance

3. **Interactive Selection** 
   - Displays available apps with current versions
   - Allows multi-app selection
   - Prompts for version updates

4. **Pre-Deployment Checks**
   - Validates Splunk home directory
   - Checks target apps directory permissions
   - Creates backup directory if needed

5. **Backup Creation**
   - Creates timestamped tar.gz backups of existing apps
   - Stores backups in `backups/` directory
   - Provides rollback capability

6. **App Deployment**
   - Copies apps to Splunk apps directory
   - Sets appropriate file permissions
   - Updates version information

7. **Post-Deployment Validation**
   - Verifies successful app copy
   - Checks file permissions
   - Validates app structure in target

8. **Restart Management**
   - Explains why restart is needed
   - Provides restart options and guidance
   - Offers manual restart commands

## 🔄 Understanding Restart Options

### Why Restart is Required

When the restart prompt appears, you'll see detailed explanations:

**Splunk needs to restart because:**
- New apps must be recognized by splunkd during startup
- Configuration changes (app.conf, props.conf) require restart  
- Knowledge objects (dashboards, saved searches) need reloading
- Search-time configuration changes take effect after restart

### Restart Choices

```
Would you like to restart Splunk now?
  y/yes = Restart now (recommended)
  n/no  = Skip restart (manual restart required)
  i/info = Show more information about restart process
```

**When to choose each:**

- **Yes (y)**: Normal development workflow, single app deployment
- **No (n)**: Deploying multiple apps, want to restart once at the end
- **Info (i)**: Learn about the restart process and timing

### Manual Restart Commands

If you choose not to restart automatically:

**Linux/macOS:**
```bash
/opt/splunk/bin/splunk restart
# or with systemd
sudo systemctl restart splunk
```

**Windows:**
```cmd
"C:\Program Files\Splunk\bin\splunk.exe" restart
# or via Services panel
```

## 📱 Working with Multiple Apps

### Efficient Multi-App Deployment

**Strategy 1: Deploy All, Restart Once**
```bash
python3 splunk_app_deployer.py  # App 1, choose 'n' for restart
python3 splunk_app_deployer.py  # App 2, choose 'n' for restart  
python3 splunk_app_deployer.py  # App 3, choose 'y' for restart
```

**Strategy 2: Batch Selection**
```bash
# Select multiple apps in one session
python3 splunk_app_deployer.py
# When prompted: 1,2,3 (select all needed apps)
```

### Version Management for Multiple Apps

- **Consistent versioning**: Use same version scheme across related apps
- **Dependency tracking**: Note which apps depend on others
- **Testing order**: Deploy dependencies first, then dependent apps

## ✅ Best Practices

### Development Workflow

1. **Test Locally First**
   ```bash
   # Always test on local development Splunk first
   python3 splunk_app_deployer.py --splunk-home ~/splunk-dev
   ```

2. **Use Version Control**
   ```bash
   # Tool integrates with git for deployment tracking
   git add .
   git commit -m "Deploy my_app v1.1.0"
   ```

3. **Backup Before Major Changes**
   - Tool automatically creates backups
   - Keep backups for rollback capability
   - Test restore procedures

### App Structure Validation

Ensure your apps have the required structure:

```
my_app/
├── default/
│   ├── app.conf          # Required
│   └── ...
├── metadata/
│   └── default.meta      # Required  
├── bin/                  # Optional
├── static/               # Optional
└── README.md            # Recommended
```

### Security Considerations

- **Run with minimal privileges** - don't use root/administrator unless necessary
- **Validate app sources** - only deploy apps from trusted sources
- **Review app contents** - inspect apps before deployment
- **Monitor deployment logs** - check logs for suspicious activity

## 🔧 Common Workflows

### Daily Development

```bash
# Morning setup - deploy latest changes
cd splunk_app_deployer
python3 splunk_app_deployer.py --apps-source-dir ../my_development_apps

# Throughout the day - quick deployments
python3 splunk_app_deployer.py --restart
```

### Testing Environment Setup

```bash
# Set up clean testing environment
python3 splunk_app_deployer.py \
  --splunk-home /opt/splunk-test \
  --apps-source-dir ./test_apps \
  --restart
```

### Pre-Production Validation

```bash
# Deploy to staging environment
python3 splunk_app_deployer.py \
  --splunk-home /opt/splunk-staging \
  --apps-source-dir ./production_ready_apps \
  --restart

# Validate functionality before production CI/CD
```

### Rollback Procedure

If you need to rollback a deployment:

1. **Find the backup** in `backups/` directory
2. **Stop Splunk**
3. **Extract backup** to apps directory
4. **Restart Splunk**

```bash
# Example rollback
cd backups/
tar -xzf my_app_backup_20250124_143022.tar.gz -C /opt/splunk/etc/apps/
/opt/splunk/bin/splunk restart
```

## 📞 Getting Help

### Built-in Help

```bash
# Show all options
python3 splunk_app_deployer.py --help

# Interactive restart information
# Choose 'i' when prompted about restart
```

### Log Files

Check deployment logs in the `logs/` directory:
- `deployment_YYYYMMDD_HHMMSS.log` - Detailed deployment logs
- Look for errors, warnings, and status messages

### Support Channels

- **General Questions**: [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net)
- **GitHub Issues**: [Report bugs or request features](https://github.com/MooseQuest/splunk_app_deployer/issues)
- **GitHub Discussions**: [Community Q&A](https://github.com/MooseQuest/splunk_app_deployer/discussions)

## 🚀 Next Steps

After mastering the basics:

1. **Read the [Developer Guide](DEVELOPER_GUIDE.md)** for customization
2. **Check [Troubleshooting](TROUBLESHOOTING.md)** for common issues
3. **Explore [examples](../examples/)** for advanced usage patterns
4. **Set up CI/CD** for production deployments (see README production guidance)

---

**Happy Splunk app developing!** 🎯
