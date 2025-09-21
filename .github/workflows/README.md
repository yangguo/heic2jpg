# GitHub Actions Workflow

This project uses GitHub Actions to automatically build and release Windows executables.

## Workflow Overview

The workflow is defined in `.github/workflows/build-release.yml` and performs the following steps:

1. Triggers on new tags (v* pattern) or manual dispatch
2. Sets up a Windows environment with Python
3. Installs project dependencies and PyInstaller
4. Builds the Windows executable using the provided spec file
5. Packages the executable into a ZIP file
6. Creates a GitHub Release and attaches the ZIP file

## Triggering the Workflow

### Automatic Trigger
The workflow automatically runs when you push a tag that starts with "v", for example:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Manual Trigger
You can also manually trigger the workflow from the GitHub Actions tab in your repository.

## Release Process

When the workflow runs, it will:

1. Build the Windows executable using PyInstaller
2. Package the executable and all required files into a ZIP archive
3. Create a new GitHub Release with the ZIP file attached
4. Generate release notes with installation instructions

## Customizing the Workflow

You can modify the workflow by editing `.github/workflows/build-release.yml`. Common customizations include:

- Changing the Python version
- Adding additional build steps
- Modifying the release notes template
- Adding multiple platform support