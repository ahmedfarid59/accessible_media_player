# Quick Fix for UV Users

## The Error You're Seeing:
```
post() got an unexpected keyword argument 'proxies'
```

## Quick Fix (Using UV):

```cmd
uv pip install --upgrade youtube-search-python requests
```

That's it! UV will quickly update both packages to compatible versions.

## Alternative UV Commands:

### If that doesn't work, try specific versions:
```cmd
uv pip install youtube-search-python==1.6.6 requests==2.31.0
```

### Fresh reinstall with UV:
```cmd
uv pip uninstall youtube-search-python requests
uv pip install youtube-search-python requests
```

### Update all dependencies:
```cmd
uv pip install --upgrade -r requirements.txt
```

## Run Diagnostic:
```cmd
python diagnose_youtube_search.py
```

## Why UV is Better:

- **10-100x faster** than pip
- Better dependency resolution
- Faster package downloads
- More reliable conflict detection

## Test After Fix:

```python
python -c "from youtubesearchpython import VideosSearch; print('✓ Working!')"
```

## If Still Broken:

1. **Clear UV cache:**
   ```cmd
   uv cache clean
   ```

2. **Reinstall with UV:**
   ```cmd
   uv pip install --force-reinstall youtube-search-python requests
   ```

3. **Check UV version:**
   ```cmd
   uv --version
   ```

4. **Use UV sync (if you have pyproject.toml):**
   ```cmd
   uv sync
   ```

## All Documentation Updated:

All the documentation files now include UV commands alongside pip commands for your convenience.

---

**TL;DR for UV users:**
```cmd
uv pip install --upgrade youtube-search-python requests
```
