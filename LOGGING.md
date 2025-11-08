# Logging System

## Overview

The application now includes comprehensive logging to help trace issues and debug problems.

## Log File Location

Logs are automatically saved to:
```
%APPDATA%\accessible youtube downloader pro\logs\app_YYYYMMDD.log
```

For example:
- `app_20240315.log` - logs from March 15, 2024
- `app_20240316.log` - logs from March 16, 2024

A new log file is created each day.

## What Gets Logged

The logging system tracks:

1. **Application startup** - Python environment, settings initialization
2. **YouTube searches** - Query parameters, result counts, errors
3. **Downloads** - URLs, formats, progress, completion status
4. **Media playback** - File opening, format detection, playback errors
5. **File associations** - Registry operations, success/failure
6. **Network errors** - Connection issues, API failures, library errors

## Log Levels

- **DEBUG**: Detailed technical information (function calls, parameters)
- **INFO**: Major operations (search started, download completed)
- **WARNING**: Unexpected but recoverable issues (no more results to load)
- **ERROR**: Failures that prevent operations (network errors, invalid URLs)

## How to Use Logs for Troubleshooting

### When YouTube Search Fails

1. Try the search that fails
2. Close the application
3. Open the log file: `%APPDATA%\accessible youtube downloader pro\logs\app_YYYYMMDD.log`
4. Search for "ERROR" or "youtube_browser"
5. Look for the error message near the timestamp of your search

Example log entry:
```
2024-03-15 14:23:45,123 - youtube_browser.search_handler - ERROR - __init__:67 - Failed to initialize search: TypeError: post() got an unexpected keyword argument 'proxies'
```

This tells you:
- **When**: 2024-03-15 at 14:23:45
- **Where**: search_handler.py, line 67, in __init__ method
- **What**: TypeError with 'proxies' argument
- **Solution**: Run `uv pip install --upgrade youtube-search-python requests`

### Sharing Logs

If you need help troubleshooting:

1. Reproduce the issue
2. Find your log file in `%APPDATA%\accessible youtube downloader pro\logs\`
3. Copy the relevant ERROR lines (include a few lines before/after for context)
4. Share with support or in issue reports

**Privacy Note**: Logs contain:
- YouTube search queries
- Video URLs
- Local file paths
- Settings values (no passwords)

Review logs before sharing if you have privacy concerns.

## Testing the Logging

To verify logging is working:

1. Run the application
2. Perform a YouTube search
3. Check the log file exists at the location above
4. Open the file and look for entries like:
   ```
   INFO - Initializing Search with query: 'test video'
   INFO - Found 20 results to parse
   ```

## Disabling Logs

Logs are essential for debugging. However, if you need to disable them:

Edit `source/logger_config.py` and change:
```python
level=logging.DEBUG
```
to:
```python
level=logging.CRITICAL  # Only log critical errors
```

Or remove the file handler entirely to stop saving logs to disk.

## Log Rotation

- Logs are rotated daily (new file each day)
- Old log files are kept indefinitely
- Manually delete old logs if disk space is a concern
- Each log file is typically 10-100 KB unless errors occur frequently
