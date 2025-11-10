# Accessible Media Player

**Version 1.5.7**  
**Author: Ahmed Farid**

An accessible YouTube browser, downloader, and media player desktop application designed specifically for NVDA screen reader users.

---

## ✨ Features

- 🔍 **YouTube Search & Browse** - Search and explore YouTube content
- ⬇️ **Video Downloads** - Download videos in multiple formats and qualities
- ▶️ **Media Playback** - Play YouTube videos and local media files
- ⭐ **Favorites Management** - Save and organize favorite videos
- 🎵 **Audio Extraction** - Download audio-only from videos
- 📁 **File Associations** - Associate video/audio formats with the player
- 🌍 **Multi-Language** - English, French, Italian, Turkish, Arabic
- ♿ **Fully Accessible** - Optimized for NVDA screen reader

---

## 📥 For Users

### Quick Start

1. **Download** the latest version from [GitHub Releases](https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro/releases)
2. **Run** the executable - **no installation required!**
3. **Start searching** for YouTube videos

### 📖 Documentation

- **[User Guide](USER_GUIDE.md)** - Complete guide with features, shortcuts, and troubleshooting
- **[Quick Start](QUICK_START.md)** - Get started quickly
- **[File Associations](FILE_ASSOCIATIONS.md)** - Set up file format associations
- **[Troubleshooting](YOUTUBE_SEARCH_FIX.md)** - Fix common issues

### 💻 Running from Source

If you prefer to run from source:

**With uv (recommended):**
```cmd
uv pip install -r requirements.txt
python source\accessible_media_player.py
```

**With pip:**
```cmd
pip install -r requirements.txt
python source\accessible_media_player.py
```

---

## 🔧 Troubleshooting

### YouTube Search Issues

If you're getting "Unable to get search results" error:

**Quick Fix:**
```cmd
pip install --upgrade youtube-search-python yt-dlp requests
```

**For detailed solutions, see:**
- [YouTube Search Fix Guide](YOUTUBE_SEARCH_FIX.md)
- [User Guide - Troubleshooting](USER_GUIDE.md#troubleshooting)

### Logs

The application includes comprehensive logging:
- **Location:** `%APPDATA%\accessible youtube downloader pro\logs\app_YYYYMMDD.log`
- **What's logged:** Searches, downloads, playback, errors
- **See:** [Logging Documentation](LOGGING.md)

When reporting issues, include relevant ERROR messages from the log file.

---

## 👨‍💻 For Developers

Want to build, modify, or contribute? See our developer documentation:

**[BUILDING.md](BUILDING.md)** - Complete developer guide:
- Development environment setup
- Building executables with PyInstaller
- Creating installers with Inno Setup
- Testing and debugging
- Release process
- Contributing guidelines

**Quick Build:**
```cmd
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python build.py --clean

# Build with installer
python build.py --clean --installer
```

---

## Author
**Ahmed Farid** - Lead Developer

## Contributors
* Abdullah Zain Aldeen, Morocco
* Mustafa Elçiçek, Turkey

## License
Copyright © 2024 Ahmed Farid

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
See [LICENSE](LICENSE) file for details.