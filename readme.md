# accessible_youtube_downloader_pro
an accessible youtube browser and downloader desktop application designed for nvda screan reader users

## Features
- YouTube search and browsing
- Video downloading from links
- Playing YouTube videos
- Managing favorite videos
- **NEW: Local media file playback with file format associations**

## Getting Started

### Installation

**With pip:**
```cmd
pip install -r requirements.txt
```

**With uv (faster):**
```cmd
uv pip install -r requirements.txt
```

### Running the Application
```cmd
python source\accessible_youtube_downloader_pro.py
```

## New Feature: File Associations
You can now associate video and audio file formats with the app's media player:
- Supported formats: MP4, AVI, MKV, WEBM, FLV, MP3, M4A, WAV, FLAC, OGG
- Open local files with Ctrl+O or from Windows Explorer
- Configure in Settings (Alt+S) → File Format Associations panel

For detailed instructions, see:
- [Quick Start Guide](QUICK_START.md)
- [File Associations Documentation](FILE_ASSOCIATIONS.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

## Recent Fixes

### YouTube Search Error Fix
If you're getting "Unable to get search results" error:

1. **For "proxies" error** (most common):
   
   **With uv:**
   ```cmd
   uv pip install --upgrade youtube-search-python requests
   ```
   
   **With pip:**
   ```cmd
   pip install --upgrade youtube-search-python requests
   ```

2. **General fix:**
   
   **With uv:**
   ```cmd
   uv pip install --upgrade youtube-search-python yt-dlp requests
   ```
   
   **With pip:**
   ```cmd
   pip install --upgrade youtube-search-python yt-dlp requests
   ```

3. **Run diagnostic:**
   ```cmd
   python diagnose_youtube_search.py
   ```

4. **See documentation:**
   - [UV Quick Fix](UV_QUICK_FIX.md) - **For UV users**
   - [Fix for Proxies Error](FIX_PROXIES_ERROR.md) - **For pip users**
   - [YouTube Search Fix Guide](YOUTUBE_SEARCH_FIX.md)
   - [LoadingDialog Fix](LOADINGDIALOG_FIX.md)
   - [Error Handling Improvements](ERROR_HANDLING_IMPROVEMENTS.md)

## Troubleshooting

### Logging System
The application now includes comprehensive logging to help trace issues:
- **Log location**: `%APPDATA%\accessible youtube downloader pro\logs\app_YYYYMMDD.log`
- **What's logged**: Searches, downloads, playback, errors, network issues
- **See**: [Logging Documentation](LOGGING.md) for detailed information

When reporting issues, check the log file for ERROR messages and include relevant lines.

# contributers
* Sulaiman Al Qusaimi, Oman
* Abdullah Zain Aldeen: Moroco
* Mustafa Elçiçek, Turkia