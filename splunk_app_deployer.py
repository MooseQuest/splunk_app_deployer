#!/usr/bin/env python3
"""
Multi-App Deployment Script for SDS Search Heads
Python version of deploy_app_to_dev.sh

Supports deployment of any app from the shcluster/apps/ directory with:
- Cross-platform support (Linux, macOS, Windows)
- Interactive app selection
- Version management
- Git integration
- Comprehensive validation and logging
"""

import os
import sys
import platform
import shutil
import subprocess
import tarfile
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import configparser


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


class DeploymentLogger:
    """Handle logging with colors and file output"""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _write_log(self, level: str, message: str, color: str = ""):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        
        # Print to console with color
        print(f"{color}{log_entry}{Colors.NC}")
        
        # Write to file without color
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry}\n")
    
    def log(self, message: str):
        self._write_log("INFO", message, Colors.BLUE)
    
    def success(self, message: str):
        self._write_log("SUCCESS", f"✅ {message}", Colors.GREEN)
    
    def warning(self, message: str):
        self._write_log("WARNING", f"⚠️  {message}", Colors.YELLOW)
    
    def error(self, message: str):
        self._write_log("ERROR", f"❌ {message}", Colors.RED)
    
    def info(self, message: str):
        self._write_log("INFO", f"ℹ️  {message}", Colors.CYAN)
    
    def bold(self, message: str):
        print(f"{Colors.BOLD}{message}{Colors.NC}")


class OSConfig:
    """OS-specific configuration and commands"""
    
    def __init__(self):
        self.os_type = self._detect_os()
        self._configure_settings()
    
    def _detect_os(self) -> str:
        """Detect the operating system"""
        system = platform.system().lower()
        if system == 'linux':
            return 'Linux'
        elif system == 'darwin':
            return 'macOS'
        elif system == 'windows':
            return 'Windows'
        else:
            return 'Unknown'
    
    def _configure_settings(self):
        """Configure OS-specific settings"""
        if self.os_type == 'Linux':
            self.default_splunk_home = Path('/opt/splunk')
            self.default_splunk_user = 'splunk'
            self.splunk_executable = 'splunk'
        elif self.os_type == 'macOS':
            self.default_splunk_home = Path('/Applications/Splunk')
            self.default_splunk_user = os.getenv('USER', 'splunk')
            self.splunk_executable = 'splunk'
        elif self.os_type == 'Windows':
            self.default_splunk_home = Path('C:/Program Files/Splunk')
            self.default_splunk_user = os.getenv('USERNAME', 'splunk')
            self.splunk_executable = 'splunk.exe'
        else:
            # Fallback to Linux defaults
            self.default_splunk_home = Path('/opt/splunk')
            self.default_splunk_user = 'splunk'
            self.splunk_executable = 'splunk'


class SplunkAppManager:
    """Manage Splunk app operations"""
    
    def __init__(self, apps_source_dir: Path, logger: DeploymentLogger):
        self.apps_source_dir = apps_source_dir
        self.logger = logger
    
    def list_available_apps(self) -> List[str]:
        """List all valid Splunk apps in the source directory"""
        apps = []
        
        if not self.apps_source_dir.exists():
            return apps
        
        for app_path in self.apps_source_dir.iterdir():
            if app_path.is_dir():
                app_conf_path = app_path / 'default' / 'app.conf'
                if app_conf_path.exists():
                    apps.append(app_path.name)
        
        return sorted(apps)
    
    def get_current_version(self, app_name: str) -> str:
        """Get the current version from app.conf"""
        app_conf_path = self.apps_source_dir / app_name / 'default' / 'app.conf'
        
        if not app_conf_path.exists():
            return "1.0.0"
        
        try:
            config = configparser.ConfigParser()
            config.read(app_conf_path)
            
            # Try launcher section first, then install section
            for section in ['launcher', 'install']:
                if config.has_section(section) and config.has_option(section, 'version'):
                    return config.get(section, 'version').strip('"')
            
            return "1.0.0"
        except Exception:
            return "1.0.0"
    
    def validate_app_structure(self, app_name: str) -> bool:
        """Validate that the app has required structure"""
        app_dir = self.apps_source_dir / app_name
        
        self.logger.log(f"Validating {app_name} app structure...")
        
        # Check required directories
        required_dirs = ['default', 'metadata']
        for dir_name in required_dirs:
            if not (app_dir / dir_name).exists():
                self.logger.error(f"Missing required directory: {app_dir / dir_name}")
                return False
        
        # Check required files
        required_files = ['default/app.conf', 'metadata/default.meta']
        for file_path in required_files:
            if not (app_dir / file_path).exists():
                self.logger.error(f"Missing required file: {app_dir / file_path}")
                return False
        
        self.logger.success(f"{app_name} app structure validation passed")
        return True
    
    def update_app_version(self, app_name: str, version: str) -> bool:
        """Update the version in app.conf"""
        app_conf_path = self.apps_source_dir / app_name / 'default' / 'app.conf'
        
        if not app_conf_path.exists():
            self.logger.error(f"App configuration file not found: {app_conf_path}")
            return False
        
        self.logger.log(f"Updating {app_name} version to {version}...")
        
        try:
            # Read the file
            config = configparser.ConfigParser()
            config.read(app_conf_path)
            
            # Update version in launcher section
            if not config.has_section('launcher'):
                config.add_section('launcher')
            config.set('launcher', 'version', version)
            
            # Update build number
            build_num = datetime.now().strftime('%Y%m%d%H%M')
            if not config.has_section('install'):
                config.add_section('install')
            config.set('install', 'build', build_num)
            
            # Update label to include version if it exists
            if config.has_option('launcher', 'label'):
                current_label = config.get('launcher', 'label')
                # Remove existing version info
                base_label = re.sub(r'\s+v\d+\.\d+\.\d+.*$', '', current_label)
                base_label = re.sub(r'\s*\([^)]*\)$', '', base_label).strip()
                config.set('launcher', 'label', f"{base_label} v{version}")
            
            # Write back to file
            with open(app_conf_path, 'w') as f:
                config.write(f)
            
            self.logger.success(f"{app_name} version updated to {version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update version: {e}")
            return False


class DeploymentManager:
    """Main deployment management class"""
    
    def __init__(self, apps_source_dir: Optional[Path] = None):
        self.script_dir = Path(__file__).parent
        # Default to looking for apps in current directory structure
        self.apps_source_dir = apps_source_dir or Path.cwd() / 'apps'
        self.deployment_log_dir = self.script_dir / 'logs'
        self.backup_dir = self.script_dir / 'backups'
        
        # Initialize components
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.deployment_log_dir / f'deployment_{timestamp}.log'
        self.logger = DeploymentLogger(log_file)
        self.os_config = OSConfig()
        self.app_manager = SplunkAppManager(self.apps_source_dir, self.logger)
        
        # Create necessary directories
        self.deployment_log_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.log(f"Detected operating system: {self.os_config.os_type}")
    
    def validate_environment(self) -> bool:
        """Validate the deployment environment"""
        self.logger.log("Validating deployment environment...")
        
        # Check if we're on Windows and warn about requirements
        if self.os_config.os_type == 'Windows':
            self.logger.warning("Windows detected - ensure you have proper permissions and tools")
        
        # Check for Git availability
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("Git not found - git integration will be disabled")
        
        self.logger.success("Environment validation passed")
        return True
    
    def prompt_for_splunk_home(self) -> Path:
        """Prompt user for Splunk home directory"""
        self.logger.bold("=== Splunk Home Detection ===")
        print(f"Detected OS: {Colors.CYAN}{self.os_config.os_type}{Colors.NC}")
        print(f"Default Splunk home for {self.os_config.os_type}: {Colors.YELLOW}{self.os_config.default_splunk_home}{Colors.NC}")
        print()
        
        splunk_input = input("Enter Splunk home path (or press Enter for default): ").strip()
        
        if not splunk_input:
            splunk_home = self.os_config.default_splunk_home
            self.logger.info(f"Using default Splunk home: {splunk_home}")
        else:
            splunk_home = Path(splunk_input)
        
        if not splunk_home.exists():
            self.logger.error(f"Splunk home directory does not exist: {splunk_home}")
            sys.exit(1)
        
        return splunk_home
    
    def select_apps_interactive(self) -> List[str]:
        """Interactive app selection"""
        available_apps = self.app_manager.list_available_apps()
        
        if not available_apps:
            self.logger.error(f"No apps found in {self.apps_source_dir}")
            sys.exit(1)
        
        self.logger.bold("=== Available Apps for Deployment ===")
        print()
        
        for i, app_name in enumerate(available_apps, 1):
            current_version = self.app_manager.get_current_version(app_name)
            print(f"  {Colors.CYAN}{i:2d}){Colors.NC} {app_name:<25} {Colors.YELLOW}(v{current_version}){Colors.NC}")
        
        print()
        selection = input(f"{Colors.BOLD}Enter app numbers to deploy (space-separated, or 'all'):{Colors.NC} ").strip()
        
        if not selection:
            self.logger.warning("No input received. Please enter a valid selection.")
            print("Valid options:")
            print("  - Enter app numbers: 1 3 5")
            print("  - Enter 'all' to select all apps")
            print(f"  - App numbers must be between 1 and {len(available_apps)}")
            sys.exit(1)
        
        self.logger.log(f"User selected: {selection}")
        
        selected_apps = []
        
        if selection.lower() == 'all':
            selected_apps = available_apps
            self.logger.info("Selected all apps for deployment")
        else:
            for num_str in selection.split():
                try:
                    num = int(num_str)
                    if 1 <= num <= len(available_apps):
                        app_name = available_apps[num - 1]
                        selected_apps.append(app_name)
                        self.logger.info(f"Selected app: {app_name}")
                    else:
                        self.logger.warning(f"Invalid selection: {num} (skipping)")
                except ValueError:
                    self.logger.warning(f"Invalid selection: {num_str} (skipping)")
        
        if not selected_apps:
            self.logger.error("No valid apps selected. Please run the script again and make a valid selection.")
            print()
            print("Valid options:")
            print("  - Enter app numbers: 1 3 5")
            print("  - Enter 'all' to select all apps")
            print(f"  - App numbers must be between 1 and {len(available_apps)}")
            sys.exit(1)
        
        return selected_apps
    
    def prompt_for_version(self, app_name: str, current_version: str) -> str:
        """Prompt for new version"""
        print()
        self.logger.bold(f"=== Version Configuration for {app_name} ===")
        print(f"Current version: {Colors.YELLOW}{current_version}{Colors.NC}")
        print()
        
        new_version = input("Enter new version (or press Enter to keep current): ").strip()
        
        if not new_version:
            return current_version
        
        # Basic version validation
        if re.match(r'^\d+\.\d+\.\d+$', new_version):
            return new_version
        else:
            self.logger.warning(f"Invalid version format. Using current version: {current_version}")
            return current_version
    
    def backup_existing_app(self, app_name: str, splunk_apps_dir: Path) -> bool:
        """Backup existing app if it exists"""
        app_path = splunk_apps_dir / app_name
        
        if not app_path.exists():
            self.logger.log(f"No existing {app_name} app found to backup")
            return True
        
        self.logger.log(f"Backing up existing {app_name} app...")
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"{app_name}_backup_{timestamp}.tar.gz"
            
            with tarfile.open(backup_path, 'w:gz') as tar:
                tar.add(app_path, arcname=app_name)
            
            self.logger.success(f"Backup created: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def deploy_app(self, app_name: str, target_dir: Path, version: str) -> bool:
        """Deploy a single app"""
        source_dir = self.apps_source_dir / app_name
        
        self.logger.log(f"Deploying {app_name} app (v{version})...")
        
        # Validate source app structure
        if not self.app_manager.validate_app_structure(app_name):
            self.logger.error(f"App structure validation failed for {app_name}")
            return False
        
        # Backup existing app
        if not self.backup_existing_app(app_name, target_dir.parent):
            self.logger.error(f"Backup failed for {app_name}")
            return False
        
        # Update version in source before copying
        if not self.app_manager.update_app_version(app_name, version):
            self.logger.error(f"Version update failed for {app_name}")
            return False
        
        try:
            # Remove existing app if it exists
            if target_dir.exists():
                self.logger.log(f"Removing existing {app_name} app...")
                shutil.rmtree(target_dir)
            
            # Copy new app
            self.logger.log(f"Copying {app_name} app to Splunk...")
            shutil.copytree(source_dir, target_dir)
            
            # Set proper permissions (skip on Windows)
            if self.os_config.os_type != 'Windows':
                self.logger.log(f"Setting permissions for {app_name} app...")
                self._set_app_permissions(target_dir)
            else:
                self.logger.log("Skipping permission setting on Windows")
            
            self.logger.success(f"{app_name} app deployed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to deploy {app_name}: {e}")
            return False
    
    def _set_app_permissions(self, app_dir: Path):
        """Set proper permissions for the app"""
        try:
            # Set directory permissions
            for root, dirs, files in os.walk(app_dir):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    file_path = os.path.join(root, f)
                    if file_path.endswith(('.py', '.sh')):
                        os.chmod(file_path, 0o755)
                    else:
                        os.chmod(file_path, 0o644)
        except Exception as e:
            self.logger.warning(f"Failed to set some permissions: {e}")
    
    def validate_deployment(self, app_name: str, target_dir: Path) -> bool:
        """Validate that deployment was successful"""
        self.logger.log(f"Validating {app_name} deployment...")
        
        if not target_dir.exists():
            self.logger.error(f"{app_name} app not found at target location")
            return False
        
        # Check key files
        key_files = ['default/app.conf', 'metadata/default.meta']
        for file_path in key_files:
            if not (target_dir / file_path).exists():
                self.logger.error(f"Key file missing: {target_dir / file_path}")
                return False
        
        self.logger.success(f"{app_name} deployment validation passed")
        return True
    
    def restart_splunk(self, splunk_home: Path) -> bool:
        """Restart Splunk service"""
        if not splunk_home or not splunk_home.exists():
            self.logger.warning("Splunk home not specified or invalid, skipping restart")
            return False
        
        self.logger.log("Restarting Splunk...")
        
        try:
            splunk_bin = splunk_home / 'bin' / self.os_config.splunk_executable
            
            if not splunk_bin.exists():
                # Try alternative locations
                if self.os_config.os_type == 'Windows':
                    alt_splunk_bin = splunk_home / 'bin' / 'splunk'
                    if alt_splunk_bin.exists():
                        splunk_bin = alt_splunk_bin
                
                if not splunk_bin.exists():
                    self.logger.error(f"Splunk executable not found in {splunk_home / 'bin'}")
                    return False
            
            self.logger.log(f"Using Splunk executable: {splunk_bin}")
            
            result = subprocess.run([str(splunk_bin), 'restart'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.logger.success("Splunk restarted successfully")
                return True
            else:
                self.logger.error(f"Splunk restart failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Splunk restart timed out")
            return False
        except Exception as e:
            self.logger.error(f"Failed to restart Splunk: {e}")
            return False
    
    def _interactive_restart_prompt(self, splunk_home: Path, deployed_apps: List[str]):
        """Interactive restart prompt with comprehensive information"""
        print()
        self.logger.bold("=== Splunk Restart Required ===")
        
        # Explain why restart is needed based on Splunk documentation
        print(f"{Colors.CYAN}📚 Why does Splunk need to restart?{Colors.NC}")
        print()
        print("According to Splunk documentation:")
        print(f"  • {Colors.YELLOW}New apps{Colors.NC} must be recognized by splunkd during startup")
        print(f"  • {Colors.YELLOW}Configuration changes{Colors.NC} (app.conf, props.conf, etc.) require restart")
        print(f"  • {Colors.YELLOW}Knowledge objects{Colors.NC} (dashboards, saved searches) need reloading")
        print(f"  • {Colors.YELLOW}Search-time configuration{Colors.NC} changes take effect after restart")
        print()
        
        # Show what was deployed
        print(f"{Colors.CYAN}📦 Apps deployed in this session:{Colors.NC}")
        for app in deployed_apps:
            print(f"  • {Colors.GREEN}{app}{Colors.NC}")
        print()
        
        # Show restart impact
        print(f"{Colors.CYAN}⚠️  Restart impact:{Colors.NC}")
        print(f"  • {Colors.YELLOW}Brief service interruption{Colors.NC} (typically 30s-2min)")
        print(f"  • {Colors.YELLOW}Active searches{Colors.NC} will be interrupted")
        print(f"  • {Colors.YELLOW}Users logged out{Colors.NC} of Splunk Web")
        print(f"  • {Colors.YELLOW}Scheduled searches{Colors.NC} may be delayed")
        print()
        
        # Show manual restart options
        print(f"{Colors.CYAN}🔧 Manual restart options:{Colors.NC}")
        if self.os_config.os_type == 'Windows':
            print(f"  • {Colors.BLUE}Command line:{Colors.NC} \"{splunk_home}\\bin\\{self.os_config.splunk_executable}\" restart")
            print(f"  • {Colors.BLUE}Services:{Colors.NC} Restart 'Splunkd' service from Services panel")
        else:
            print(f"  • {Colors.BLUE}Command line:{Colors.NC} {splunk_home}/bin/{self.os_config.splunk_executable} restart")
            if self.os_config.os_type == 'Linux':
                print(f"  • {Colors.BLUE}Systemd:{Colors.NC} sudo systemctl restart splunk")
            elif self.os_config.os_type == 'macOS':
                print(f"  • {Colors.BLUE}Launchd:{Colors.NC} sudo launchctl restart com.splunk.splunkd")
        print()
        
        # Interactive prompt
        print(f"{Colors.BOLD}Would you like to restart Splunk now?{Colors.NC}")
        print("  y/yes = Restart now (recommended)")
        print("  n/no  = Skip restart (manual restart required)")
        print("  i/info = Show more information about restart process")
        print()
        
        while True:
            choice = input("Choose [y/n/i]: ").strip().lower()
            
            if choice in ['y', 'yes']:
                print()
                self.logger.info("Starting Splunk restart...")
                self.restart_splunk(splunk_home)
                break
            elif choice in ['n', 'no']:
                print()
                self.logger.warning("Splunk restart skipped.")
                self.logger.info("🔧 Remember to restart Splunk manually to load the new apps:")
                if self.os_config.os_type == 'Windows':
                    self.logger.info(f"   \"{splunk_home}\\bin\\{self.os_config.splunk_executable}\" restart")
                else:
                    self.logger.info(f"   {splunk_home}/bin/{self.os_config.splunk_executable} restart")
                break
            elif choice in ['i', 'info']:
                self._show_restart_info()
            else:
                print(f"{Colors.YELLOW}⚠️  Please enter 'y' (yes), 'n' (no), or 'i' (info){Colors.NC}")
    
    def _show_restart_info(self):
        """Show detailed restart information"""
        print()
        self.logger.bold("=== Detailed Restart Information ===")
        print()
        
        print(f"{Colors.CYAN}📖 Splunk Documentation References:{Colors.NC}")
        print("  • 'Deploy an app in a single-instance deployment'")
        print("    - Apps must be restarted to be recognized by Splunk")
        print("  • 'Configuration file precedence'")
        print("    - Configuration changes require restart to take effect")
        print("  • 'About configuration files'")
        print("    - Search-time and index-time configurations need restart")
        print()
        
        print(f"{Colors.CYAN}🔄 What happens during restart:{Colors.NC}")
        print("  1. Splunkd service stops gracefully")
        print("  2. Configuration files are re-read")
        print("  3. Apps are discovered and loaded")
        print("  4. Knowledge objects are indexed")
        print("  5. Search processors are initialized")
        print("  6. Web server starts")
        print("  7. Services become available")
        print()
        
        print(f"{Colors.CYAN}⏱️  Typical restart timeline:{Colors.NC}")
        print("  • Small instance (1-5 apps): 30-60 seconds")
        print("  • Medium instance (10-50 apps): 1-2 minutes")
        print("  • Large instance (100+ apps): 2-5 minutes")
        print("  • Depends on: hardware, app complexity, data volume")
        print()
        
        print(f"{Colors.CYAN}✅ How to verify successful restart:{Colors.NC}")
        print("  1. Check Splunk Web loads without errors")
        print("  2. Verify new apps appear in 'Manage Apps'")
        print("  3. Test app functionality (dashboards, searches)")
        print("  4. Check splunkd.log for any errors")
        print("  5. Verify all expected services are running")
        print()
        
        print(f"{Colors.CYAN}🚨 When NOT to restart immediately:{Colors.NC}")
        print("  • During business hours (active users)")
        print("  • When critical searches are running")
        print("  • Before testing configuration changes")
        print("  • When deploying multiple apps (restart once at end)")
        print("  • In production without change window")
        print()

    def handle_git_operations(self, deployed_apps: List[str]) -> bool:
        """Handle git operations"""
        try:
            # Check if git is available
            subprocess.run(['git', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.info("Git not available - skipping git operations")
            return False
        
        print()
        self.logger.bold("=== Git Operations ===")
        git_commit = input("Do you want to commit the changes to git? (y/n): ").strip().lower()
        
        if git_commit in ['y', 'yes']:
            try:
                # Add app directories to git
                files_to_commit = []
                for app in deployed_apps:
                    files_to_commit.append(f"shcluster/apps/{app}/")
                files_to_commit.append("tools/deployment/deploy_app_to_dev.py")
                
                self.logger.log("Adding files to git...")
                subprocess.run(['git', 'add'] + files_to_commit, check=True)
                
                # Check if there are changes to commit
                result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                                      capture_output=True)
                
                if result.returncode != 0:  # There are changes
                    # Create commit message
                    app_list = ", ".join(deployed_apps)
                    
                    # Get summary of changes
                    summary_result = subprocess.run(['git', 'diff', '--cached', '--stat'], 
                                                  capture_output=True, text=True)
                    summary = summary_result.stdout.strip()
                    
                    commit_msg = f"""Deploy apps: {app_list}

Summary of changes:
{summary}

Deployed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                    
                    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                    self.logger.success(f"Git commit created for deployed apps: {app_list}")
                    return True
                else:
                    self.logger.info("No changes to commit")
                    return False
                    
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Git operation failed: {e}")
                return False
        else:
            self.logger.info("Skipping git commit")
            return False
    
    def show_deployment_summary(self, deployed_apps: List[str], app_versions: List[str], 
                              splunk_home: Path, splunk_apps_dir: Path):
        """Show deployment summary"""
        print()
        self.logger.bold("=== Deployment Summary ===")
        self.logger.success("Deployment completed successfully!")
        
        if deployed_apps:
            print()
            print("Deployed Apps:")
            for i, app in enumerate(deployed_apps):
                version = app_versions[i] if i < len(app_versions) else "unknown"
                print(f"  ✅ {Colors.CYAN}{app}{Colors.NC} {Colors.YELLOW}v{version}{Colors.NC}")
            
            print()
            print("=== Post-Deployment Instructions ===")
            print(f"1. Restart Splunk if not already done: {splunk_home}/bin/{self.os_config.splunk_executable} restart")
            print("2. Navigate to Splunk Web and verify apps are loaded")
            print("3. Check app versions in Manage Apps")
            print("4. Test app functionality")
            
            print()
            print("=== App Locations ===")
            for app in deployed_apps:
                print(f"  {app}: {splunk_apps_dir / app}")
        
        print()
        print("=== Logs and Backups ===")
        print(f"Deployment log: {self.logger.log_file}")
        print(f"Backup directory: {self.backup_dir}")
    
    def run(self, splunk_home: Optional[Path] = None, splunk_apps_dir: Optional[Path] = None, 
            restart: bool = False):
        """Main deployment workflow"""
        self.logger.bold("=== Splunk App Deployer ===")
        print()
        self.logger.log("Starting deployment process...")
        self.logger.log(f"Script dir: {self.script_dir}")
        self.logger.log(f"Apps source dir: {self.apps_source_dir}")
        
        # Validate environment
        if not self.validate_environment():
            self.logger.error("Environment validation failed")
            sys.exit(1)
        
        # Get Splunk home
        if not splunk_home:
            splunk_home = self.prompt_for_splunk_home()
        
        if not splunk_apps_dir:
            splunk_apps_dir = splunk_home / 'etc' / 'apps'
        
        self.logger.log(f"Splunk home: {splunk_home}")
        self.logger.log(f"Splunk apps dir: {splunk_apps_dir}")
        
        # Create splunk apps directory if it doesn't exist
        splunk_apps_dir.mkdir(parents=True, exist_ok=True)
        
        # Select apps to deploy
        selected_apps = self.select_apps_interactive()
        
        print()
        self.logger.bold("=== Selected Apps ===")
        for app in selected_apps:
            current_version = self.app_manager.get_current_version(app)
            print(f"  • {Colors.CYAN}{app}{Colors.NC} {Colors.YELLOW}(v{current_version}){Colors.NC}")
        
        print()
        proceed = input("Proceed with deployment? (y/n): ").strip().lower()
        
        if proceed not in ['y', 'yes']:
            self.logger.info("Deployment cancelled")
            return
        
        # Deploy each selected app
        deployed_apps = []
        app_versions = []
        
        for app in selected_apps:
            current_version = self.app_manager.get_current_version(app)
            new_version = self.prompt_for_version(app, current_version)
            
            target_dir = splunk_apps_dir / app
            
            if self.deploy_app(app, target_dir, new_version):
                if self.validate_deployment(app, target_dir):
                    deployed_apps.append(app)
                    app_versions.append(new_version)
                    self.logger.success(f"{app} v{new_version} deployed and validated")
                else:
                    self.logger.error(f"{app} deployment validation failed")
            else:
                self.logger.error(f"{app} deployment failed")
            
            print()
        
        # Restart Splunk if requested
        if restart:
            self.restart_splunk(splunk_home)
        else:
            self._interactive_restart_prompt(splunk_home, deployed_apps)
        
        # Handle git operations
        if deployed_apps:
            self.handle_git_operations(deployed_apps)
        
        # Show summary
        self.show_deployment_summary(deployed_apps, app_versions, splunk_home, splunk_apps_dir)


def show_help():
    """Show help information"""
    help_text = f"""
{Colors.BOLD}Splunk App Deployer{Colors.NC}

This script allows you to deploy one or more Splunk apps with interactive guidance and validation.

{Colors.BOLD}Usage:{Colors.NC}
  python3 splunk_app_deployer.py [OPTIONS]

{Colors.BOLD}Options:{Colors.NC}
  --splunk-home PATH      Path to Splunk installation directory (optional - will prompt)
  --splunk-apps-dir PATH  Target apps directory (default: SPLUNK_HOME/etc/apps)
  --apps-source-dir PATH  Source directory containing apps to deploy (default: ./apps)
  --restart              Automatically restart Splunk after deployment (skips interactive prompt)
  --help, -h             Show this help message

{Colors.BOLD}Features:{Colors.NC}
  • Cross-platform support (Linux, macOS, Windows)
  • OS-specific path detection and defaults
  • Interactive app selection from available apps
  • Version prompting with current version display
  • Automatic backup of existing apps
  • Structure validation
  • Git integration with commit prompting
  • Comprehensive logging

{Colors.BOLD}Examples:{Colors.NC}
  python3 deploy_app_to_dev.py                                    # Full interactive mode
  python3 deploy_app_to_dev.py --splunk-home /opt/splunk         # Linux/macOS with custom path
  python3 deploy_app_to_dev.py --restart                         # Interactive with auto-restart
  python3 deploy_app_to_dev.py --splunk-home "C:\\Program Files\\Splunk" --restart  # Windows, fully automated
"""
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Deploy Splunk apps', add_help=False)
    parser.add_argument('--splunk-home', type=Path, help='Splunk installation directory')
    parser.add_argument('--splunk-apps-dir', type=Path, help='Splunk apps directory')
    parser.add_argument('--apps-source-dir', type=Path, help='Source directory containing apps to deploy')
    parser.add_argument('--restart', action='store_true', help='Restart Splunk after deployment')
    parser.add_argument('--help', '-h', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return
    
    try:
        deployment_manager = DeploymentManager(apps_source_dir=args.apps_source_dir)
        deployment_manager.run(
            splunk_home=args.splunk_home,
            splunk_apps_dir=args.splunk_apps_dir,
            restart=args.restart
        )
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Deployment interrupted by user{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.NC}")
        sys.exit(1)


if __name__ == '__main__':
    main() 