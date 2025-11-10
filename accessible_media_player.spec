# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Accessible YouTube Downloader Pro.

This file defines how PyInstaller should build the executable, including:
- What files to include
- Where to find data files (plugins, translations, etc.)
- Executable metadata and configuration

Generated and maintained by build.py
"""

import sys
from pathlib import Path

# Import version info
sys.path.insert(0, 'source')
from __version__ import __version__, __app_name__

block_cipher = None

# Data files to include in the build
# Format: (source, destination)
datas = [
    ('source/plugins', 'plugins'),              # VLC plugins
    ('source/languages', 'languages'),          # Translation files
    ('source/assets', 'assets'),                # Icons, version info, etc.
    ('source/docs', 'docs'),                    # User documentation (legacy)
    ('USER_GUIDE.md', '.'),                     # Main user guide (markdown)
]

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'wx',
    'wx.html',
    'wx.lib.scrolledpanel',
    'wx.lib.agw',
    'vlc',
    'yt_dlp',
    'youtubesearchpython',
    'httpx',
    'sqlite3',
    'json',
    'urllib',
    'concurrent.futures',
    'markdown',
]

a = Analysis(
    ['source/accessible_media_player.py'],
    pathex=[],
    binaries=[
        ('source/nvdaControllerClient64.dll', '.'),
        ('source/nvdaControllerClient32.dll', '.'),
        ('source/libvlc.dll', '.'),
        ('source/libvlccore.dll', '.'),
    ],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'PyQt5',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='accessible_media_player',
    debug=False,  # Disable debug mode for production
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='source/assets/version_info.txt',  # Windows version info
    icon=None,  # Add icon path here if you have one: 'source/assets/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='accessible_media_player',
)
