# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Splunk App Deployer.

## 📋 Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Common Issues](#common-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Splunk-Related Issues](#splunk-related-issues)
- [App Structure Issues](#app-structure-issues)
- [Permission Problems](#permission-problems)
- [Getting Help](#getting-help)

## 🔍 Quick Diagnostics

### Basic Health Check

```bash
# Check Python version (should be 3.6+)
python3 --version

# Verify help system works
python3 splunk_app_deployer.py --help

# Check current directory structure
pwd && ls -la
```

### Environment Check

```bash
# Check if Splunk is running
ps aux | grep splunk

# Check Splunk installation paths
ls -la /opt/splunk              # Linux
ls -la /Applications/Splunk     # macOS
dir "C:\Program Files\Splunk"   # Windows
```

### Log Analysis

```bash
# View recent deployment logs
ls -lt logs/
tail -20 logs/deployment_*.log

# Search for errors
grep -i "error\|fail" logs/deployment_*.log
```

## ❗ Common Issues

### 1. "No apps found" Error

**Symptoms:** Script reports no valid apps in source directory

**Solutions:**

Check app structure:
```bash
# Verify required files exist
ls -la your_app/default/app.conf
ls -la your_app/metadata/default.meta
```

Create missing files:
```bash
# Minimal app.conf
cat > your_app/default/app.conf << 'EOF'
[launcher]
version = 1.0.0
[package]
id = your_app
[ui]
is_visible = true
label = Your App
EOF

# Minimal default.meta
cat > your_app/metadata/default.meta << 'EOF'
[]
access = read : [ * ], write : [ admin, power ]
export = system
EOF
```

### 2. Permission Denied Errors

**Linux/macOS Solutions:**
```bash
# Check current permissions
whoami && id

# Add user to splunk group
sudo usermod -a -G splunk $USER

# Or run with appropriate permissions
sudo python3 splunk_app_deployer.py
```

**Windows Solutions:**
```cmd
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"
python splunk_app_deployer.py
```

### 3. Splunk Not Found

**Find Splunk Installation:**
```bash
# Common Linux locations
ls -la /opt/splunk /home/splunk/splunk

# Common macOS locations  
ls -la /Applications/Splunk /Users/splunk/splunk

# Common Windows locations
dir "C:\Program Files\Splunk" "C:\Splunk"
```

**Specify Custom Path:**
```bash
python3 splunk_app_deployer.py --splunk-home /your/custom/path
```

### 4. Version Update Failures

**Check app.conf format:**
```bash
cat your_app/default/app.conf
# Should contain: [launcher] section with version = X.Y.Z
```

**Fix version format:**
```bash
# Use semantic versioning: 1.0.0, 1.2.3, 2.0.0
sed -i 's/version = .*/version = 1.0.0/' your_app/default/app.conf
```

### 5. Restart Failures

**Manual restart commands:**
```bash
# Linux/macOS
/opt/splunk/bin/splunk restart

# Windows
"C:\Program Files\Splunkin\splunk.exe" restart

# Check status
/opt/splunk/bin/splunk status
```

## 🖥️ Platform-Specific Issues

### Linux Issues

**SELinux Problems:**
```bash
# Check and temporarily disable
sestatus
sudo setenforce 0
```

**File System Permissions:**
```bash
# Check disk space and fix ownership
df -h
sudo chown -R splunk:splunk /opt/splunk
```

### macOS Issues

**Security/Gatekeeper:**
```bash
# Remove quarantine if present
xattr -d com.apple.quarantine splunk_app_deployer.py
```

**Python PATH:**
```bash
# Ensure Python is in PATH
export PATH="/usr/local/bin:$PATH"
which python3
```

### Windows Issues

**PowerShell Execution Policy:**
```powershell
# Check and set execution policy
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path Separators:**
```cmd
# Use forward slashes or escaped backslashes
python splunk_app_deployer.py --splunk-home "C:/Program Files/Splunk"
```

## 🎯 Splunk-Related Issues

### App Not Appearing in Splunk Web

**Check app status:**
```bash
/opt/splunk/bin/splunk display app your_app
/opt/splunk/bin/splunk enable app your_app
```

**Refresh Splunk:**
1. Go to **Settings > Server Settings > Server Settings**
2. Click **Refresh** next to "App and add-on management"
3. Or restart Splunk completely

### Knowledge Objects Missing

**Check permissions in metadata/default.meta:**
```bash
cat your_app/metadata/default.meta
# Should include proper export settings for views, savedsearches
```

**Validate XML syntax:**
```bash
# Check dashboard files
xmllint --noout your_app/default/data/ui/views/*.xml
```

## 📁 App Structure Issues

### Invalid Directory Structure

**Correct minimal structure:**
```
your_app/
├── default/
│   ├── app.conf          # Required
│   └── data/             # Optional
├── metadata/
│   └── default.meta      # Required  
├── bin/                  # Optional
└── static/               # Optional
```

**Fix structure:**
```bash
# Create missing directories
mkdir -p your_app/{default,metadata,bin,static}

# Move files to correct locations
mv your_app/*.conf your_app/default/
mv your_app/*.meta your_app/metadata/
```

## 🔐 Permission Problems

### File Ownership (Linux/macOS)

```bash
# Check current ownership
ls -la /opt/splunk/etc/apps/your_app

# Fix ownership
sudo chown -R splunk:splunk /opt/splunk/etc/apps/your_app

# Set proper permissions
sudo chmod -R 644 /opt/splunk/etc/apps/your_app
sudo chmod 755 /opt/splunk/etc/apps/your_app
```

### App Permissions in Splunk

1. **Settings > Apps > Manage Apps**
2. Find your app and click **Permissions**
3. Set appropriate sharing (App or Global)
4. Configure user access as needed

## 🆘 Getting Help

### Diagnostic Information to Collect

**System Information:**
```bash
# OS and Python version
uname -a                    # Linux/macOS
systeminfo | findstr OS    # Windows
python3 --version

# Splunk version
/opt/splunk/bin/splunk version
```

**Error Details:**
```bash
# Capture complete error output
python3 splunk_app_deployer.py 2>&1 | tee error_output.txt

# Recent deployment logs
tail -50 logs/deployment_*.log
```

### Support Channels

1. **Self-Help:**
   - Review this troubleshooting guide
   - Check [User Guide](USER_GUIDE.md) for usage help
   - Read [Developer Guide](DEVELOPER_GUIDE.md) for customization

2. **Community Support:**
   - [GitHub Issues](https://github.com/MooseQuest/splunk_app_deployer/issues) - Bug reports
   - [GitHub Discussions](https://github.com/MooseQuest/splunk_app_deployer/discussions) - Q&A

3. **Direct Contact:**
   - **General Questions**: [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net)
   - **Security Issues**: [security@moosequest.net](mailto:security@moosequest.net)

### Before Contacting Support

1. Review this guide for your specific issue
2. Check recent logs for error messages  
3. Verify basic setup (Python version, Splunk installation)
4. Test with a minimal example (single small app)
5. Collect diagnostic information listed above

**When contacting support, include:**
- Complete error messages
- System information (OS, Python, Splunk versions)
- Recent log files
- Steps to reproduce the issue
- What you've already tried

---

Most issues can be resolved with the information in this guide. For additional help, reach out through the support channels above! 🚀
