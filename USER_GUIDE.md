# Accessible Media Player - User Guide

**Version 1.5.7**  
**Developed by: Ahmed Farid**

Welcome to Accessible Media Player, a fully accessible YouTube browser, downloader, and media player designed specifically for NVDA screen reader users.

---

## Credits and Acknowledgments

This application is based on the original **Accessible YouTube Downloader Pro** developed by **Sulaiman Al Qusaimi**. Ahmed Farid has enhanced and extended the original project with additional features, improvements, and ongoing maintenance.

**Original Developer:** Sulaiman Al Qusaimi  
**Original Repository:** https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro  
**Current Developer & Maintainer:** Ahmed Farid

We thank Sulaiman Al Qusaimi for creating the foundation of this accessible software that serves the blind and visually impaired community.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Main Features](#main-features)
3. [Using the Application](#using-the-application)
4. [Keyboard Shortcuts](#keyboard-shortcuts)
5. [Settings and Configuration](#settings-and-configuration)
6. [File Associations](#file-associations)
7. [Troubleshooting](#troubleshooting)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### Installation

1. **Download** the latest version from the [GitHub Releases page](https://github.com/ahmedfarid59/accessible_media_player/releases)
2. **Run** the installer or portable executable
3. The application can be installed or run as portable

### First Launch

When you first launch Accessible Media Player:

1. The main window will open with focus on the search field
2. NVDA will announce the interface elements
3. You can start searching for YouTube videos immediately

---

## Main Features

### 1. YouTube Search and Browsing
- **Search YouTube** directly from the app
- **Browse results** with detailed information
- **View video descriptions, comments, and related videos**
- **Navigate channels and playlists**

### 2. Video Downloading
- **Download videos** in multiple formats (MP4, WEBM, 3GP)
- **Audio-only downloads** (MP3, M4A, WEBM)
- **Choose quality** (High, Medium, Low)
- **Monitor progress** with accessible download dialogs

### 3. Media Playback
- **Play YouTube videos** directly in the app
- **Play local media files** (video and audio)
- **Full playback controls** (play, pause, stop, seek)
- **Volume control** with keyboard shortcuts

### 4. Favorites Management
- **Save favorite videos** for quick access
- **Organize playlists**
- **Quick launch** from favorites menu

### 5. Multi-Language Support
- English
- French
- Italian
- Turkish
- Arabic

---

## Using the Application

### Searching for Videos

1. **Press Alt+S** or focus on the search field
2. **Type your search query**
3. **Press Enter** to search
4. **Navigate results** with Up/Down arrow keys
5. **Press Enter** on a result to view details

### Downloading Videos

**Method 1: From Search Results**
1. Search for a video
2. Select the video from results
3. **Press Alt+D** or use the Download menu
4. Choose format and quality
5. Select download location
6. Monitor progress in the download dialog

**Method 2: From URL**
1. **Press Ctrl+L** to open Link dialog
2. Paste the YouTube URL
3. Click Download
4. Choose format, quality, and location

### Playing Videos

**YouTube Videos:**
1. Select a video from search results
2. **Press Alt+P** or use Play menu
3. Video plays in built-in player

**Local Files:**
1. **Press Ctrl+O** to open file browser
2. Select a video or audio file
3. File plays in built-in player

**Playback Controls:**
- **Space** - Play/Pause
- **Left/Right Arrow** - Seek backward/forward
- **Up/Down Arrow** - Volume up/down
- **M** - Mute/Unmute
- **Escape** - Close player

### Managing Favorites

**Adding to Favorites:**
1. Select a video from search results
2. **Press Ctrl+F** or use Favorites → Add
3. Video is saved for quick access

**Viewing Favorites:**
1. **Press Alt+F** or use Favorites menu
2. Browse saved videos
3. **Press Enter** to play or download

---

## Keyboard Shortcuts

### Main Window

| Shortcut | Action |
|----------|--------|
| **Alt+S** | Focus search field |
| **Enter** | Search / Select item |
| **Alt+D** | Download selected video |
| **Alt+P** | Play selected video |
| **Ctrl+L** | Open link dialog |
| **Ctrl+O** | Open local media file |
| **Ctrl+F** | Add to favorites |
| **Alt+F** | Open favorites |
| **Alt+E** | View description |
| **Alt+C** | View comments |
| **F5** | Refresh search results |
| **Ctrl+Q** | Quit application |

### Media Player

| Shortcut | Action |
|----------|--------|
| **Space** | Play/Pause |
| **Left Arrow** | Seek backward 5 seconds |
| **Right Arrow** | Seek forward 5 seconds |
| **Up Arrow** | Increase volume |
| **Down Arrow** | Decrease volume |
| **M** | Mute/Unmute |
| **Escape** | Close player |

### Download Dialog

| Shortcut | Action |
|----------|--------|
| **Tab** | Navigate fields |
| **Alt+F** | Choose format |
| **Alt+Q** | Choose quality |
| **Alt+L** | Choose location |
| **Enter** | Start download |
| **Escape** | Cancel |

---

## Settings and Configuration

Access settings with **Alt+T** → Settings

### General Settings

- **Download Location:** Default folder for downloads
- **Default Quality:** Auto-select video quality
- **Auto-Play:** Automatically play after download

### Interface Settings

- **Language:** Choose interface language
- **Font Size:** Adjust text size
- **Theme:** Light or dark mode

### File Format Associations

**Supported Formats:**
- **Video:** MP4, AVI, MKV, WEBM, FLV
- **Audio:** MP3, M4A, WAV, FLAC, OGG

**Setting Up Associations:**
1. Go to Settings → File Format Associations
2. Check formats you want to associate
3. Click Apply
4. Now you can open these files from Windows Explorer

**Removing Associations:**
1. Go to Settings → File Format Associations
2. Uncheck formats
3. Click Apply

---

## File Associations

### What are File Associations?

File associations allow you to **open video and audio files** directly with Accessible Media Player from Windows Explorer.

### How to Set Up

1. **Open Settings** (Alt+T → Settings)
2. Go to **File Format Associations** tab
3. **Check the formats** you want to associate (e.g., MP4, MP3)
4. Click **Apply**
5. Click **OK**

### How to Use

After setting up associations:

1. **Navigate to a video or audio file** in Windows Explorer
2. **Press Enter** or right-click → Open
3. File opens in Accessible Media Player automatically

### Removing Associations

1. Open Settings → File Format Associations
2. **Uncheck the formats**
3. Click Apply

---

## Troubleshooting

### YouTube Search Not Working

**Symptom:** "Unable to get search results" error

**Solution 1 - Update Dependencies:**
```cmd
pip install --upgrade youtube-search-python yt-dlp requests
```

**Solution 2 - Check Internet Connection:**
- Ensure you're connected to the internet
- Try opening YouTube in a browser

**Solution 3 - Check Logs:**
- Go to `%APPDATA%\Accessible Media Player\logs\`
- Open the latest log file
- Look for ERROR messages
- Report issues with log details

### Download Fails

**Possible Causes:**
- **Network issue** - Check your internet connection
- **Video restricted** - Some videos can't be downloaded (age-restricted, private)
- **Invalid URL** - Ensure the YouTube URL is correct

**Solutions:**
- Try downloading a different video
- Update dependencies (see above)
- Check if video plays in YouTube browser

### Video Won't Play

**Check:**
- **File format supported** - See supported formats above
- **VLC plugins** - Ensure plugins folder exists
- **File corrupted** - Try playing in another player

### NVDA Not Speaking

**Solutions:**
- Ensure NVDA is running
- Restart NVDA (NVDA+Q, then restart)
- Check NVDA speech settings
- Try restarting the application

### Application Crashes

**Steps:**
1. Check log file in `%APPDATA%\Accessible Media Player\logs\`
2. Note the error message
3. Report issue on GitHub with:
   - Error message from log
   - Steps to reproduce
   - Your Windows version

---

## Frequently Asked Questions

### Is this application free?

Yes! Accessible Media Player is completely free and open source.

### Do I need to install anything?

No installation required. Just download and run the executable.

### Can I use this without NVDA?

The application is optimized for NVDA but works with other screen readers and sighted users.

### Can I download playlists?

Yes! Use the playlist feature (Alt+L → Playlist URL) to download entire playlists.

### What video formats can I download?

- Video: MP4, WEBM, 3GP, FLV
- Audio: MP3, M4A, WEBM

### Can I convert videos to audio?

Yes! Choose "Audio Only" in the download format dropdown.

### How do I update the application?

The app checks for updates automatically. When an update is available:
1. You'll see a notification
2. Click "Download Update"
3. Replace the old executable with the new one

### Where are downloaded files saved?

Default location: `Downloads` folder

You can change this in Settings → Download Location

### Can I use this on multiple computers?

Yes! The application is portable. Copy the executable to any Windows computer.

### Is my download history saved?

The application saves:
- **Favorites** - Videos you explicitly save
- **Logs** - Activity logs for troubleshooting

Downloads are saved to your specified folder.

### How do I report bugs or request features?

Visit the [GitHub Issues page](https://github.com/ahmedfarid59/accessible_media_player/issues)

---

## Getting Help

### Resources

- **GitHub Repository:** https://github.com/ahmedfarid59/accessible_media_player
- **Issue Tracker:** https://github.com/ahmedfarid59/accessible_media_player/issues
- **Email Support:** Contact Ahmed Farid through GitHub

### Reporting Issues

When reporting issues, please include:

1. **Your Windows version**
2. **Application version** (Help → About)
3. **NVDA version** (if applicable)
4. **Steps to reproduce the problem**
5. **Error message** (from log file if available)
6. **Screenshots** (if helpful)

### Log Files

Logs are stored in:
```
%APPDATA%\Accessible Media Player\logs\app_YYYYMMDD.log
```

To access:
1. Press **Windows+R**
2. Type: `%APPDATA%\Accessible Media Player\logs`
3. Press Enter
4. Open the latest log file

---

## About

### Development Credits

**Current Developer & Maintainer:** Ahmed Farid  
**Original Developer:** Sulaiman Al Qusaimi (Accessible YouTube Downloader Pro)

Accessible Media Player is based on the original **Accessible YouTube Downloader Pro** created by **Sulaiman Al Qusaimi**. Ahmed Farid has taken over development, adding significant enhancements, new features, and ongoing improvements while maintaining the accessible foundation that Sulaiman built.

**Additional Contributors:**
- Abdullah Zain Aldeen (Morocco)
- Mustafa Elçiçek (Turkey)

### Version Information

**Version:** 1.5.7  
**License:** GNU General Public License v3.0  
**Copyright:** © 2024 Ahmed Farid  
**Original Work:** © Sulaiman Al Qusaimi

### Acknowledgments

Special thanks to **Sulaiman Al Qusaimi** for creating the original accessible YouTube downloader that serves the blind and visually impaired community. This project builds upon that excellent foundation.

**Original Project:** https://github.com/sulaiman-alqusaimi/accessible_youtube_downloader_pro

---

## Thank You!

Thank you for using Accessible Media Player. We hope this application makes YouTube more accessible for you!

If you find this application useful, please:
- ⭐ **Star the repository** on GitHub
- 📢 **Share with others** who might benefit
- 🐛 **Report bugs** to help us improve
- 💡 **Suggest features** for future versions

**Enjoy accessible YouTube browsing!**
