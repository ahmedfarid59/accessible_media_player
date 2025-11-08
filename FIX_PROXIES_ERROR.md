# Fix for "post() got an unexpected keyword argument 'proxies'" Error

## The Problem

**Error Message:**
```
post() got an unexpected keyword argument 'proxies'
```

This error occurs when the `youtube-search-python` library has a version mismatch or compatibility issue with the `requests` library.

## Root Cause

The `youtube-search-python` library internally uses the `requests` library to make HTTP calls to YouTube. Different versions of these libraries may have incompatible function signatures. Specifically:

1. Older versions of `youtube-search-python` may call `requests.post()` with a `proxies` parameter
2. Some versions of `requests` or underlying HTTP libraries don't support this parameter
3. The function call fails before even reaching YouTube

## Solution

### Quick Fix (Recommended):

```cmd
pip install --upgrade youtube-search-python requests
```

This updates both libraries to compatible versions.

### If That Doesn't Work:

**Option 1: Install Specific Compatible Versions**
```cmd
pip uninstall youtube-search-python requests
pip install youtube-search-python==1.6.6 requests==2.31.0
```

**Option 2: Try Latest Development Version**
```cmd
pip install git+https://github.com/alexmercerind/youtube-search-python.git
pip install --upgrade requests
```

**Option 3: Reinstall Fresh**
```cmd
pip uninstall youtube-search-python requests
pip cache purge
pip install youtube-search-python requests
```

## Verification

After applying the fix, verify it works:

### Method 1: Run Diagnostic Tool
```cmd
python diagnose_youtube_search.py
```

### Method 2: Test Manually
```python
from youtubesearchpython import VideosSearch
search = VideosSearch('test', limit=1)
print(search.result())
```

If you see results without errors, it's fixed!

## Why This Happens

1. **Package Updates**: You or another program updated `requests` or `youtube-search-python` independently
2. **Multiple Python Versions**: Different Python installations with different package versions
3. **Virtual Environment**: Packages in venv are different from system packages
4. **Dependency Conflicts**: Another package required an incompatible version

## Check Your Current Versions

```cmd
pip show youtube-search-python
pip show requests
```

**Known Good Combinations:**
- `youtube-search-python==1.6.6` + `requests==2.31.0`
- `youtube-search-python==1.6.7` + `requests==2.32.0`
- Latest versions of both (usually works)

## Prevention

To prevent this in the future, pin versions in `requirements.txt`:

```txt
youtube-search-python==1.6.6
requests==2.31.0
```

Then install with:
```cmd
pip install -r requirements.txt
```

## Alternative: Use yt-dlp for Search

If youtube-search-python continues to cause issues, the app could be modified to use `yt-dlp` for searching instead. This is more stable but slower:

```python
# Instead of youtube-search-python
import yt_dlp

ydl_opts = {'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    result = ydl.extract_info(f"ytsearch:{query}", download=False)
```

## What The App Now Shows

With the improved error handling, when this error occurs, you'll see:

```
خطأ في توافق المكتبات. يرجى تحديث youtube-search-python:
pip install --upgrade youtube-search-python

تفاصيل الخطأ: post() got an unexpected keyword argument 'proxies'

هل تريد المحاولة مرة أخرى؟
```

The error message now includes the fix command directly!

## Still Not Working?

1. **Check Python version:**
   ```cmd
   python --version
   ```
   Need Python 3.7+

2. **Check for multiple Python installations:**
   ```cmd
   where python
   ```

3. **Use virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install youtube-search-python requests
   ```

4. **Check for conflicting packages:**
   ```cmd
   pip list | findstr -i "youtube requests http"
   ```

5. **View full error in console** - The app now prints full traceback

## Summary

This is a **library compatibility issue**, not a network or YouTube problem. The fix is simple:

```cmd
pip install --upgrade youtube-search-python requests
```

If that doesn't work, try the specific versions mentioned above.
