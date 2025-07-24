# Sample Splunk App Structure

This directory contains an example of a properly structured Splunk app that can be deployed using the Splunk App Deployer.

## Directory Structure

```
my_sample_app/
├── default/
│   └── app.conf          # Required: App configuration
├── metadata/
│   └── default.meta      # Required: Permissions configuration
├── bin/                  # Optional: Scripts and executables
└── static/              # Optional: Static assets (CSS, JS, images)
```

## Required Files

### `default/app.conf`
- **Purpose**: Defines app metadata, version, and basic configuration
- **Required sections**: `[install]`, `[launcher]`, `[ui]`, `[package]`
- **Version field**: Used by the deployer for version tracking

### `metadata/default.meta` 
- **Purpose**: Defines permissions for the app and its objects
- **Required**: At minimum, application-level permissions
- **Format**: Splunk metadata configuration format

## Optional Directories

### `bin/`
- **Purpose**: Python scripts, shell scripts, and executables
- **Permissions**: Scripts automatically made executable during deployment
- **Examples**: Custom search commands, modular inputs

### `static/`
- **Purpose**: Static web assets
- **Examples**: CSS files, JavaScript, images, icons
- **Access**: Available via Splunk Web

### Other Common Directories
- `appserver/static/` - Alternative location for static assets
- `lookups/` - CSV lookup files
- `local/` - Local configuration overrides (usually empty in source)

## Usage with Splunk App Deployer

1. **Place your app** in a directory that the deployer can access
2. **Ensure required files** (`app.conf`, `default.meta`) exist
3. **Run the deployer** and select your app from the list
4. **Version tracking** happens automatically based on `app.conf`

## Validation

The Splunk App Deployer validates:
- ✅ Required directories exist (`default/`, `metadata/`)
- ✅ Required files exist (`default/app.conf`, `metadata/default.meta`)
- ✅ Valid app.conf format for version extraction
- ✅ Proper directory structure for Splunk compatibility

## Example Deployment

```bash
# From the directory containing your apps
python3 splunk_app_deployer.py

# Select your app from the interactive menu
# The deployer will:
# 1. Detect the app structure
# 2. Show current version (1.0.0 from app.conf)
# 3. Prompt for new version
# 4. Deploy with validation
```

## Best Practices

1. **Always use semantic versioning** (e.g., 1.0.0, 1.1.0, 2.0.0)
2. **Keep local/ directory empty** in source (runtime configurations only)
3. **Use meaningful app IDs** in the `[package]` section
4. **Set appropriate permissions** in default.meta
5. **Test apps** in development environment before production deployment

## Common Issues

- **Missing app.conf**: App won't be detected by the deployer
- **Missing default.meta**: Deployment will fail validation
- **Invalid version format**: Version prompting may not work correctly
- **Incorrect permissions**: App may not load properly in Splunk

For more information, see the main documentation in the [docs/](../../docs/) directory. 