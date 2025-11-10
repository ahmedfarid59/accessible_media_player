# Building Accessible Media Player

**Developer Documentation**  
**Author: Ahmed Farid**

This document provides comprehensive instructions for developers who want to build, modify, or contribute to the Accessible Media Player application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Building the Executable](#building-the-executable)
- [Build Options](#build-options)
- [Testing the Build](#testing-the-build)
- [Troubleshooting](#troubleshooting)
- [Release Process](#release-process)

## Prerequisites

### Required Software

- **Python 3.8 or higher** (3.10+ recommended)
- **Git** (for version control)
- **PyInstaller** (for creating executables)

### Installing Dependencies

The project uses `uv` as the recommended package manager, but `pip` works too.

**With uv (recommended):**
```bash
# Install uv if you don't have it
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Install build tools
uv pip install pyinstaller
```

**With pip:**
```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro.git
   cd accessible_youtube_downloader_pro
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Run from source to test:**
   ```bash
   python source\accessible_youtube_downloader_pro.py
   ```

## Building the Executable

The project includes an automated build script that handles the entire build process.

### Basic Build

```bash
python build.py
```

This will:
1. Check all dependencies
2. Generate version info from `source/__version__.py`
3. Run PyInstaller with the configuration in `accessible_youtube_downloader_pro.spec`
4. Validate the build
5. Rename the executable with the version number
6. Update `update_info.json` with the new version

### Output

The build process creates:
- `dist/accessible_youtube_downloader_pro_X.Y.Z.exe` - The distributable executable
- `build/` - Temporary build files (can be deleted)

## Build Options

### Clean Build

Remove all previous build artifacts before building:
```bash
python build.py --clean
```

### Test Build

Build without creating the final distributable (useful for quick testing):
```bash
python build.py --test
```

This creates `dist/accessible_youtube_downloader_pro.exe` without renaming or updating version files.

## Testing the Build

After building, test the executable:

1. **Run the executable:**
   ```bash
   dist\accessible_youtube_downloader_pro_1.5.7.exe
   ```

2. **Test key features:**
   - YouTube search
   - Download a video
   - Play a video (local file)
   - Check favorites
   - Verify translations work
   - Test file associations (if configured)

3. **Check logs:**
   - Logs are written to `logs/app.log`
   - Look for any errors or warnings

## Troubleshooting

### Build Fails: "PyInstaller not found"

Install PyInstaller:
```bash
pip install pyinstaller
```

### Build Fails: "Missing dependencies"

Make sure all required packages are installed:
```bash
pip install -r requirements.txt
```

### Executable is Too Small

If the executable is smaller than expected (< 10 MB), PyInstaller may have missed dependencies. Check:
- That all data files are included (plugins, languages, assets)
- The spec file includes all required `hiddenimports`
- Run with `--clean` to rebuild from scratch

### Missing VLC Plugins

The VLC plugins folder (`source/plugins/`) must be present. If missing:
- The folder should be committed to the repository
- Ensure it's not excluded in `.gitignore`
- Check that the spec file includes it in `datas`

### Translation Files Not Included

Translation `.mo` files must be compiled before building:
- Check that `.mo` files exist in `source/languages/*/lc_messages/`
- The build process includes these automatically

### Version Mismatch

All version numbers come from `source/__version__.py`. If you see mismatches:
1. Edit `source/__version__.py`
2. Run `python build.py` again
3. The build script will update `version_info.txt` and `update_info.json` automatically

## Release Process

### 1. Update Version

Edit `source/__version__.py`:
```python
__version__ = "1.5.8"  # New version
```

### 2. Build

```bash
python build.py --clean
```

### 3. Test

Test the executable thoroughly:
```bash
dist\accessible_youtube_downloader_pro_1.5.8.exe
```

### 4. Create GitHub Release

1. Commit changes:
   ```bash
   git add source/__version__.py update_info.json
   git commit -m "Bump version to 1.5.8"
   ```

2. Create and push tag:
   ```bash
   git tag v1.5.8
   git push origin master --tags
   ```

3. Go to GitHub → Releases → Create new release
4. Select tag `v1.5.8`
5. Title: "Version 1.5.8"
6. Upload `dist/accessible_youtube_downloader_pro_1.5.8.exe`
7. Add release notes describing changes
8. Publish release

### 5. Update Repository

```bash
git push origin master
```

### 6. Verify Auto-Update

Users running older versions should see an update notification pointing to the new release.

## Project Structure

```
accessible_youtube_downloader_pro/
├── source/                          # Source code
│   ├── __version__.py              # Version info (single source of truth)
│   ├── accessible_youtube_downloader_pro.py  # Main entry point
│   ├── assets/                     # Icons, version_info.txt
│   ├── docs/                       # User documentation
│   ├── gui/                        # GUI components
│   ├── languages/                  # Translation files
│   └── plugins/                    # VLC plugins
├── build.py                        # Build automation script
├── accessible_youtube_downloader_pro.spec  # PyInstaller configuration
├── requirements.txt                # Python dependencies
├── update_info.json               # Auto-update configuration
└── README.md                      # User documentation
```

## Version Management

The project uses a single source of truth for version information:

- **Source:** `source/__version__.py`
- **Generated from source:**
  - `source/assets/version_info.txt` (Windows executable metadata)
  - `update_info.json` (auto-update configuration)

Never edit the generated files directly. Always update `__version__.py` and run the build script.

## Development Tips

### Running from Source

For development, run directly from source:
```bash
python source\accessible_youtube_downloader_pro.py
```

### Debugging Build Issues

Add debug output to PyInstaller:
```bash
pyinstaller accessible_youtube_downloader_pro.spec --debug=all
```

### Quick Iteration

Use test builds during development:
```bash
python build.py --test
```

This skips version updates and is faster.

## Contributing

We welcome contributions! Here's how to contribute:

### Reporting Issues

1. Check existing issues first
2. Provide detailed reproduction steps
3. Include error messages and logs
4. Specify your environment (OS, Python version)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

### Testing Checklist

Before submitting changes:
- [ ] Application runs without errors
- [ ] YouTube search works
- [ ] Downloads work (video and audio)
- [ ] Media player works
- [ ] NVDA announces correctly
- [ ] No regression in existing features
- [ ] Build process succeeds

## Getting Help

### Resources

- **Issues:** https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro/issues
- **Discussions:** https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro/discussions
- **Email:** Contact Ahmed Farid through GitHub

### Community

Join our community of developers and users:
- Report bugs and request features on GitHub Issues
- Share your modifications and improvements
- Help other users with troubleshooting

## License

**Copyright © 2024 Ahmed Farid**

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

You are free to:
- Use the software for any purpose
- Study and modify the source code
- Distribute copies
- Distribute modified versions

Under the conditions:
- Source code must be made available
- Modifications must be released under GPL-3.0
- Changes must be documented

See [LICENSE](LICENSE) file for full details.

## Acknowledgments

**Lead Developer:** Ahmed Farid

**Contributors:**
- Abdullah Zain Aldeen (Morocco) - Localization and testing
- Mustafa Elçiçek (Turkey) - Translation and accessibility testing

**Special Thanks:**
- The NVDA community for accessibility feedback
- VLC project for media player capabilities
- yt-dlp developers for download functionality
- All users who reported bugs and suggested features

---

**Happy Building! 🚀**

For questions or support, open an issue on GitHub or contact Ahmed Farid.
