# File Association Feature

## Overview
The Accessible YouTube Downloader Pro now includes functionality to associate local video and audio file formats with the application's media player. This allows you to open media files directly with the app from Windows File Explorer.

## Features Added

### 1. Settings Panel
A new panel has been added to the settings dialog (`الإعدادات`) called "ربط صيغ الملفات بالمشغل" (File Format Associations). This panel includes checkboxes for:

**Video Formats:**
- MP4
- AVI
- MKV
- WEBM
- FLV

**Audio Formats:**
- MP3
- M4A
- WAV
- FLAC
- OGG

### 2. How to Use

#### Associating File Formats:
1. Open the application
2. Go to Settings (Alt+S or through the main menu)
3. Scroll to the "File Format Associations" section
4. Check the boxes for the formats you want to open with this application
5. Click OK to save

The application will register itself in the Windows registry as the handler for the selected file types.

#### Opening Local Media Files:
There are three ways to open local media files:

1. **From the Application Menu:**
   - Press Ctrl+O or select "فتح ملف وسائط محلي" from the main menu
   - Browse and select a media file
   - The file will open in the built-in media player

2. **From Windows Explorer:**
   - If you've associated a format with the app, right-click a file
   - Select "Open with" → "Accessible YouTube Downloader Pro"
   - Or double-click the file if it's set as the default application

3. **Command Line:**
   - Run: `python accessible_youtube_downloader_pro.py "path\to\file.mp4"`

### 3. Technical Implementation

#### Files Modified:

1. **settings_handler.py**
   - Added default settings for file associations (assoc_mp4, assoc_avi, etc.)
   - Added `get_associated_formats()` function to retrieve current associations
   - Added `set_file_association(extension, enable)` function to register/unregister file types in Windows registry

2. **gui/settings_dialog.py**
   - Added file association panel with checkboxes for each format
   - Added `onFileAssocCheck()` method to track changes
   - Modified `onOk()` method to apply file associations when settings are saved

3. **accessible_youtube_downloader_pro.py**
   - Added "Open Local Media File" menu item (Ctrl+O)
   - Added `onOpenLocalFile()` method with file picker dialog
   - Added `openLocalMediaFile()` method to play local files
   - Added command-line argument handling for file associations

4. **media_player/media_gui.py**
   - Already supports playing local files through VLC (no changes needed)
   - The `can_download` parameter set to False for local files

### 4. Registry Entries
When you associate a file format, the application creates entries in:
```
HKEY_CURRENT_USER\Software\Classes\.{extension}
HKEY_CURRENT_USER\Software\Classes\AccessibleYouTubeDownloaderPro.{extension}
```

These entries allow Windows to recognize the application as a handler for those file types.

### 5. Notes
- File associations are stored per-user (HKEY_CURRENT_USER), not system-wide
- You can uncheck formats in settings to remove associations
- The media player uses VLC backend, so it supports all formats VLC can play
- Local files open with `can_download=False` to disable YouTube-specific features

## Keyboard Shortcuts
- **Ctrl+O** - Open local media file
- **Alt+S** - Open settings

## Troubleshooting

### File associations not working:
1. Make sure you've checked the format in settings and clicked OK
2. Try running the application as administrator
3. Check Windows' Default Apps settings

### Files not playing:
1. Ensure VLC is properly installed (python-vlc package)
2. Verify the file format is supported by VLC
3. Check that the file path doesn't contain special characters

## Future Enhancements
Possible improvements could include:
- Adding more format support
- Creating a "Set as default player" button
- Adding a recent files list
- Supporting playlists for local files
