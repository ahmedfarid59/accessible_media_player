# Fix for LoadingDialog AttributeError

## The Problem

**Error Message:**
```
'LoadingDialog' object has no attribute 'res'
تفاصيل الخطأ: 'LoadingDialog' object has no attribute 'res'
```

## Root Cause

The `LoadingDialog` class was setting `self.res` inside the `run()` method (which runs in a separate thread). However:

1. If an exception occurred in the function being called, `self.res` was never set
2. The calling code immediately tried to access `.res` after the dialog closed
3. If the function failed, `.res` didn't exist, causing an AttributeError

## The Fix

### 1. Updated `activity_dialog.py`:
```python
# BEFORE:
class LoadingDialog(wx.Dialog):
    def __init__(self, parent, msg, function, *args, **kwargs):
        # ... no initialization of res
        
    def run(self):
        try:
            self.res = self.function(...)  # Only set if successful
        except Exception as e:
            raise e  # Error was raised but res never set

# AFTER:
class LoadingDialog(wx.Dialog):
    def __init__(self, parent, msg, function, *args, **kwargs):
        self.res = None  # Initialize to None
        self.error = None  # Store any error that occurs
        
    def run(self):
        try:
            self.res = self.function(...)
        except Exception as e:
            self.error = e  # Store error instead of raising
            # Don't raise - let caller check self.error
```

### 2. Updated `browser.py`:
```python
# BEFORE:
try:
    self.search = LoadingDialog(...).res  # Could fail if res doesn't exist
except Exception as e:
    # Handle error

# AFTER:
loading_dlg = LoadingDialog(...)

# Check if error occurred
if loading_dlg.error is not None:
    # Handle the error
    
# Check if result is valid
if loading_dlg.res is None:
    # Handle no results
    
self.search = loading_dlg.res  # Safe - we know res exists
```

## Benefits

1. **No more AttributeError** - `res` is always defined (even if None)
2. **Better error handling** - Errors are stored in `error` attribute
3. **More informative** - Can distinguish between:
   - Function failed (error is not None)
   - Function returned None (error is None, res is None)
   - Function succeeded (error is None, res has value)

## Testing

After this fix, you should see:
- No more "object has no attribute 'res'" errors
- Proper error messages showing the actual YouTube search error
- Better error details in the dialog

## Related Files Modified

1. `source/gui/activity_dialog.py` - LoadingDialog class
2. `source/youtube_browser/browser.py` - searchAction method
3. `source/languages/en/lc_messages/accessible_youtube_downloader.po` - Translations

## Next Steps

The YouTube search error you're seeing is now properly exposed. Run the diagnostic tool to see the actual error:

```cmd
python diagnose_youtube_search.py
```

This will tell you if it's:
- Outdated library (most common)
- YouTube API changes
- Network/firewall issues
- Package conflicts
