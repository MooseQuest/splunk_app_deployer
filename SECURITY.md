# Security Policy

## 🔒 **Reporting Security Vulnerabilities**

The security of Splunk App Deployer is important to us. If you believe you have found a security vulnerability, please report it responsibly.

### **How to Report**

**🚨 Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:
- **Security Email**: [security@moosequest.net](mailto:security@moosequest.net)
- **General Contact**: [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net)
- **Subject**: `[SECURITY] Splunk App Deployer - [Brief Description]`

### **What to Include**

Please include as much information as possible:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** and attack scenarios
4. **Affected versions** (if known)
5. **Proposed fix** (if you have one)
6. **Your contact information** for follow-up

### **Response Timeline**

- **Initial Response**: Within 48 hours of receiving your report
- **Status Update**: Within 7 days with preliminary assessment
- **Resolution**: Security fixes will be prioritized and released as soon as possible

## 🛡️ **Supported Versions**

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## 🔍 **Security Considerations**

### **What We Take Seriously**

- **Code injection** vulnerabilities
- **Path traversal** attacks
- **Privilege escalation** issues
- **Credential exposure** risks
- **Command injection** vulnerabilities
- **File system access** beyond intended scope

### **Known Security Features**

The Splunk App Deployer includes several security measures:

- ✅ **Input validation** for file paths and app names
- ✅ **Path sanitization** to prevent directory traversal
- ✅ **Read-only operations** for app discovery and validation
- ✅ **Explicit permission handling** for file operations
- ✅ **No external dependencies** (reduces attack surface)
- ✅ **No network communication** except for Git operations
- ✅ **Local-only operations** (no remote code execution)

### **Security Best Practices for Users**

1. **Run with minimal privileges** - Don't run as root/administrator unless necessary
2. **Validate app sources** - Only deploy apps from trusted sources
3. **Review app contents** - Inspect apps before deployment
4. **Use version control** - Track all changes through Git
5. **Regular updates** - Keep the deployer updated to the latest version
6. **Backup verification** - Ensure backups are created and valid
7. **Log monitoring** - Review deployment logs for suspicious activity

### **Deployment Environment Security**

- **Development**: Use isolated environments for testing
- **Production**: Limit access to deployment tools and Splunk directories
- **Credentials**: Use proper authentication for Git operations
- **Network**: Consider network isolation for sensitive deployments

## 🚫 **Out of Scope**

The following are generally considered out of scope for security reports:

- **Issues in third-party dependencies** (we use only Python standard library)
- **Social engineering attacks**
- **Physical access to systems**
- **Issues requiring physical access to the deployment machine**
- **Splunk security issues** (report those to Splunk directly)
- **Operating system vulnerabilities**

## 🔧 **Security Development Process**

### **Code Review**

- All changes undergo review before merging
- Security implications are considered for all modifications
- Input validation is required for user-provided data

### **Testing**

- Path traversal prevention is tested
- Input validation is verified
- File permission handling is validated
- Error handling prevents information disclosure

### **Dependencies**

- **Zero external dependencies** policy reduces attack surface
- Python standard library only
- No network dependencies for core functionality

## 📋 **Security Disclosure Policy**

### **Coordinated Disclosure**

We follow responsible disclosure practices:

1. **Private reporting** of vulnerabilities
2. **Collaborative investigation** with the reporter
3. **Coordinated public disclosure** after fixes are available
4. **Credit attribution** to security researchers (with permission)

### **Public Disclosure Timeline**

- **Immediate**: Critical vulnerabilities affecting data integrity
- **30 days**: High-severity vulnerabilities
- **90 days**: Medium and low-severity issues
- **Coordinated**: With reporter agreement when possible

### **Security Advisory Process**

For significant vulnerabilities, we will:

1. **Create a security advisory** on GitHub
2. **Notify users** through repository notifications
3. **Provide migration guidance** if needed
4. **Document the fix** in release notes

## 🏆 **Recognition**

### **Hall of Fame**

We maintain a security hall of fame for researchers who responsibly disclose vulnerabilities:

*No security issues have been reported yet. Be the first to help make Splunk App Deployer more secure!*

### **Acknowledgments**

- We appreciate responsible disclosure
- Security researchers will be credited (with permission)
- Significant findings may receive public recognition

## 📞 **Contact Information**

- **Primary Contact**: Kristerpher Henderson
- **Security Email**: [security@moosequest.net](mailto:security@moosequest.net)
- **General Contact**: [opensource-kris@moosequest.net](mailto:opensource-kris@moosequest.net)
- **GitHub**: [@MooseQuest](https://github.com/MooseQuest)
- **Response Time**: Within 48 hours

## 📚 **Additional Resources**

- **GitHub Security Features**: [Security Policy](https://github.com/MooseQuest/splunk_app_deployer/security/policy)
- **Splunk Security**: [Splunk Security Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Security)
- **Python Security**: [Python Security Guidelines](https://python.org/dev/security/)

---

**Last Updated**: July 24, 2025
**Version**: 1.1.2

Thank you for helping keep Splunk App Deployer secure! 🔒
