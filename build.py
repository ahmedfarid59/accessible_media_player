"""
Build script for Accessible Media Player.

This script automates the entire build process:
1. Validates the environment and dependencies
2. Generates version_info.txt from __version__.py
3. Runs PyInstaller with the correct configuration
4. Validates the build output
5. Updates update_info.json with the new version

Usage:
    python build.py [--clean] [--test]

Options:
    --clean    Remove build artifacts before building
    --test     Skip creating distributable, just test the build
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

# Add source to path to import version
sys.path.insert(0, str(Path(__file__).parent / "source"))
from __version__ import __version__, __author__, __description__, __app_name__, __copyright__


# Build configuration
PROJECT_ROOT = Path(__file__).parent
SOURCE_DIR = PROJECT_ROOT / "source"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
SPEC_FILE = PROJECT_ROOT / "accessible_media_player.spec"
MAIN_SCRIPT = SOURCE_DIR / "accessible_media_player.py"
VERSION_INFO_FILE = SOURCE_DIR / "assets" / "version_info.txt"
UPDATE_INFO_FILE = PROJECT_ROOT / "update_info.json"

# Output executable name
EXE_NAME = f"accessible_media_player_{__version__}.exe"


def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70)


def check_dependencies():
    """Check if required tools and packages are installed."""
    print_header("Checking Dependencies")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check PyInstaller
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✓ PyInstaller {version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check if main script exists
    if not MAIN_SCRIPT.exists():
        print(f"❌ Main script not found: {MAIN_SCRIPT}")
        return False
    print(f"✓ Main script found: {MAIN_SCRIPT.name}")
    
    # Check for required directories
    required_dirs = [
        SOURCE_DIR / "plugins",
        SOURCE_DIR / "languages",
        SOURCE_DIR / "assets",
    ]
    for dir_path in required_dirs:
        if not dir_path.exists():
            print(f"❌ Required directory not found: {dir_path}")
            return False
        print(f"✓ {dir_path.relative_to(PROJECT_ROOT)}")
    
    return True


def generate_version_info():
    """Generate version_info.txt for PyInstaller from __version__.py."""
    print_header("Generating Version Info")
    
    version_parts = __version__.split('.')
    while len(version_parts) < 4:
        version_parts.append('0')
    
    version_tuple = ', '.join(version_parts)
    
    version_info_content = f"""# UTF-8
#
# For more details about fixed file info:
# See https://learn.microsoft.com/en-us/windows/win32/api/verrsrc/ns-verrsrc-vs_fixedfileinfo

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_tuple}),
    prodvers=({version_tuple}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{__author__}'),
        StringStruct(u'FileDescription', u'{__description__}'),
        StringStruct(u'FileVersion', u'{__version__}'),
        StringStruct(u'InternalName', u'accessible_media_player'),
        StringStruct(u'LegalCopyright', u'{__copyright__}'),
        StringStruct(u'OriginalFilename', u'accessible_media_player.exe'),
        StringStruct(u'ProductName', u'{__app_name__}'),
        StringStruct(u'ProductVersion', u'{__version__}')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    VERSION_INFO_FILE.parent.mkdir(parents=True, exist_ok=True)
    VERSION_INFO_FILE.write_text(version_info_content, encoding='utf-8')
    print(f"✓ Generated: {VERSION_INFO_FILE.relative_to(PROJECT_ROOT)}")
    print(f"  Version: {__version__}")


def clean_build():
    """Remove build artifacts."""
    print_header("Cleaning Build Artifacts")
    
    dirs_to_remove = [BUILD_DIR, DIST_DIR]
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✓ Removed: {dir_path.relative_to(PROJECT_ROOT)}")
        else:
            print(f"  Skip: {dir_path.relative_to(PROJECT_ROOT)} (doesn't exist)")


def run_pyinstaller():
    """Run PyInstaller to build the executable."""
    print_header("Running PyInstaller")
    
    if not SPEC_FILE.exists():
        print(f"❌ Spec file not found: {SPEC_FILE}")
        print("   Please ensure accessible_media_player.spec exists")
        return False
    
    try:
        # Run PyInstaller with the spec file
        cmd = [sys.executable, "-m", "PyInstaller", str(SPEC_FILE), "--clean", "--noconfirm"]
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True, capture_output=True, text=True)
        
        # Print relevant output
        if result.stdout:
            for line in result.stdout.splitlines():
                if any(keyword in line for keyword in ["WARNING", "ERROR", "Building", "completed"]):
                    print(f"  {line}")
        
        print("✓ PyInstaller completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed with error code {e.returncode}")
        if e.stderr:
            print("\nError output:")
            print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def validate_build():
    """Validate that the build was successful."""
    print_header("Validating Build")
    
    # Check for directory-based distribution
    exe_path = DIST_DIR / "accessible_media_player" / "accessible_media_player.exe"
    
    if not exe_path.exists():
        # Try old location
        exe_path = DIST_DIR / "accessible_media_player.exe"
        if not exe_path.exists():
            print(f"❌ Executable not found in:")
            print(f"   {DIST_DIR / 'accessible_media_player' / 'accessible_media_player.exe'}")
            print(f"   {DIST_DIR / 'accessible_media_player.exe'}")
            return False
    
    exe_size = exe_path.stat().st_size / (1024 * 1024)  # Convert to MB
    print(f"✓ Executable created: {exe_path.relative_to(PROJECT_ROOT)}")
    print(f"  Size: {exe_size:.2f} MB")
    
    # Check if it's suspiciously small
    if exe_size < 1:
        print(f"⚠️  Warning: Executable seems small ({exe_size:.2f} MB)")
        print("   This might indicate missing dependencies")
    
    return True


def rename_executable():
    """Rename the executable directory to include version number."""
    print_header("Finalizing Build")
    
    old_dir = DIST_DIR / "accessible_media_player"
    new_dir = DIST_DIR / f"accessible_media_player_{__version__}"
    
    if old_dir.exists():
        if new_dir.exists():
            shutil.rmtree(new_dir)
        old_dir.rename(new_dir)
        print(f"✓ Renamed distribution to: {new_dir.name}")
        exe_path = new_dir / "accessible_media_player.exe"
        return exe_path
    else:
        print(f"❌ Distribution folder not found: {old_dir}")
        return None


def update_update_info(exe_path):
    """Update update_info.json with new version information."""
    print_header("Updating Release Info")
    
    # GitHub release URL pattern
    github_url = f"https://github.com/ahmedfarid59/accessible_media_player/releases/download/v{__version__}/{exe_path.name}"
    
    update_info = {
        "version": __version__,
        "url": github_url
    }
    
    UPDATE_INFO_FILE.write_text(json.dumps(update_info, indent=2), encoding='utf-8')
    print(f"✓ Updated: {UPDATE_INFO_FILE.name}")
    print(f"  Version: {__version__}")
    print(f"  URL: {github_url}")
    print("\n⚠️  Remember to:")
    print(f"  1. Create a GitHub release with tag: v{__version__}")
    print(f"  2. Upload {exe_path.name} to the release")
    print(f"  3. Commit and push update_info.json")


def create_installer():
    """Create installer using Inno Setup."""
    print_header("Creating Installer")
    
    # Check if Inno Setup is installed
    inno_paths = [
        Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
    ]
    
    iscc = None
    for path in inno_paths:
        if path.exists():
            iscc = path
            break
    
    if not iscc:
        print("❌ Inno Setup not found")
        print("\nTo create installers, install Inno Setup from:")
        print("  https://jrsoftware.org/isdl.php")
        return False
    
    print(f"✓ Found Inno Setup: {iscc}")
    
    # Run Inno Setup compiler
    iss_file = PROJECT_ROOT / "installer.iss"
    if not iss_file.exists():
        print(f"❌ Installer script not found: {iss_file}")
        return False
    
    print(f"\nCompiling installer...")
    print(f"Script: {iss_file.name}")
    
    try:
        result = subprocess.run(
            [str(iscc), str(iss_file)],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        if result.returncode != 0:
            print(f"❌ Inno Setup compilation failed:")
            print(result.stdout)
            print(result.stderr)
            return False
        
        print("✓ Installer created successfully")
        
        # Find the created installer
        installer_dir = PROJECT_ROOT / "installer_output"
        if installer_dir.exists():
            installers = list(installer_dir.glob("*.exe"))
            if installers:
                print(f"\n✓ Installer: {installers[0]}")
                print(f"  Size: {installers[0].stat().st_size / (1024*1024):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating installer: {e}")
        return False


def main():
    """Main build process."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Accessible Media Player")
    parser.add_argument("--clean", action="store_true", help="Remove build artifacts before building")
    parser.add_argument("--test", action="store_true", help="Test build without creating release artifacts")
    parser.add_argument("--installer", action="store_true", help="Create installer using Inno Setup after building")
    args = parser.parse_args()
    
    print_header(f"Building {__app_name__} v{__version__}")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Build failed: Missing dependencies")
        return 1
    
    # Step 2: Clean if requested
    if args.clean:
        clean_build()
    
    # Step 3: Generate version info
    generate_version_info()
    
    # Step 4: Run PyInstaller
    if not run_pyinstaller():
        print("\n❌ Build failed: PyInstaller error")
        return 1
    
    # Step 5: Validate build
    if not validate_build():
        print("\n❌ Build failed: Validation error")
        return 1
    
    if args.test:
        print_header("Test Build Complete")
        print("✓ Build test successful")
        print(f"  Executable: {DIST_DIR / 'accessible_media_player.exe'}")
        print("\nTo create a release build, run without --test flag")
        return 0
    
    # Step 6: Rename executable with version
    exe_path = rename_executable()
    if not exe_path:
        print("\n❌ Build failed: Could not rename executable")
        return 1
    
    # Step 7: Update update_info.json
    update_update_info(exe_path)
    
    # Step 8: Create installer if requested
    if args.installer:
        if not create_installer():
            print("\n⚠️  Installer creation failed, but executable is ready")
    
    # Success!
    print_header("Build Complete! 🎉")
    print(f"✓ Executable: {exe_path}")
    print(f"✓ Version: {__version__}")
    print(f"\nNext steps:")
    print(f"  1. Test the executable: {exe_path}")
    print(f"  2. Create GitHub release: v{__version__}")
    print(f"  3. Upload {exe_path.name}")
    if args.installer:
        print(f"  4. Upload installer from installer_output/")
        print(f"  5. Commit and push changes")
    else:
        print(f"  4. Commit and push changes")
        print(f"\nTo create installer, run: python build.py --installer")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
