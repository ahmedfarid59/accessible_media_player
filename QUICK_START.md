# Quick Start Guide: File Associations

## For Users

### Step 1: Run the Application
```cmd
cd d:\code\accessible_youtube_downloader_pro
python source\accessible_youtube_downloader_pro.py
```

### Step 2: Configure File Associations
1. Press **Alt+S** to open Settings
2. Navigate to the "File Format Associations" section (last section)
3. Check the formats you want to associate:
   - For videos: Check MP4, AVI, MKV, WEBM, FLV
   - For audio: Check MP3, M4A, WAV, FLAC, OGG
4. Press **Tab** to OK button and press **Enter**

### Step 3: Open Local Media Files

**Option A: From the Application**
- Press **Ctrl+O**
- Select a media file
- File plays in the built-in player

**Option B: From Windows Explorer**
- Right-click any associated file (e.g., .mp4)
- Select "Open with" → "Accessible YouTube Downloader Pro"
- Or set as default and just double-click

**Option C: From Command Line**
```cmd
python source\accessible_youtube_downloader_pro.py "C:\Videos\movie.mp4"
```

## For Developers

### Testing the Implementation

1. **Test configuration reading:**
```cmd
python test_file_associations.py
```

2. **Test with a sample file:**
```cmd
python test_file_associations.py "C:\sample.mp4"
```

3. **Manually test file association:**
```python
from settings_handler import set_file_association, config_get

# Associate MP4
set_file_association("mp4", True)
print(config_get("assoc_mp4"))  # Should print: True

# Unassociate MP4
set_file_association("mp4", False)
print(config_get("assoc_mp4"))  # Should print: False
```

### Registry Check

After associating a format, check the registry:
```cmd
reg query "HKCU\Software\Classes\.mp4"
reg query "HKCU\Software\Classes\AccessibleYouTubeDownloaderPro.mp4"
```

## Troubleshooting

### Issue: File associations not working
**Solution:** Run the application, go to Settings, uncheck and re-check the format, click OK.

### Issue: "Module not found" errors
**Solution:** Install dependencies:
```cmd
pip install -r requirements.txt
```

### Issue: Files won't play
**Solution:** Make sure VLC is installed:
```cmd
pip install python-vlc
```

### Issue: Can't find the settings panel
**Solution:** The file association panel is at the bottom of the settings dialog. Scroll down or press Tab multiple times.

## Features at a Glance

| Feature | Keyboard Shortcut |
|---------|-------------------|
| Open Settings | Alt+S |
| Open Local File | Ctrl+O |
| Search YouTube | Ctrl+F |
| Download from Link | Ctrl+D |
| Play YouTube Link | Ctrl+Y |
| Favorites | Ctrl+Shift+F |
| Open Download Folder | Ctrl+P |
| Exit | Ctrl+W |

## Supported Formats

**Video Formats:**
- MP4 (MPEG-4 Part 14)
- AVI (Audio Video Interleave)
- MKV (Matroska Video)
- WEBM (Web Media)
- FLV (Flash Video)

**Audio Formats:**
- MP3 (MPEG Audio Layer 3)
- M4A (MPEG-4 Audio)
- WAV (Waveform Audio)
- FLAC (Free Lossless Audio Codec)
- OGG (Ogg Vorbis)

## Notes

- File associations are user-specific (no admin rights required)
- You can associate/unassociate formats at any time
- The app uses VLC backend, so any VLC-supported format should work
- Local files open without download options (YouTube features disabled)
