"""
YouTube Search Diagnostic Tool
This script helps diagnose issues with YouTube search functionality
"""

import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

print("=" * 70)
print("YouTube Search Diagnostic Tool")
print("=" * 70)

# Test 1: Check if required modules are installed
print("\n[1/5] Checking installed packages...")
print("-" * 70)

try:
    import requests
    print(f"✓ requests: {requests.__version__}")
except ImportError as e:
    print(f"✗ requests: NOT INSTALLED - {e}")

try:
    import bs4
    print(f"✓ bs4 (BeautifulSoup): {bs4.__version__}")
except ImportError as e:
    print(f"✗ bs4: NOT INSTALLED - {e}")

try:
    from youtubesearchpython import VideosSearch
    print(f"✓ youtube-search-python: Installed")
except ImportError as e:
    print(f"✗ youtube-search-python: NOT INSTALLED - {e}")

# Test 2: Check internet connectivity
print("\n[2/5] Testing internet connectivity...")
print("-" * 70)

try:
    import requests
    response = requests.get("https://www.google.com", timeout=5)
    print(f"✓ Internet connection: OK (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Internet connection: FAILED - {e}")

# Test 3: Test YouTube access
print("\n[3/5] Testing YouTube access...")
print("-" * 70)

try:
    import requests
    response = requests.get("https://www.youtube.com", timeout=10)
    print(f"✓ YouTube access: OK (Status: {response.status_code})")
except Exception as e:
    print(f"✗ YouTube access: FAILED - {e}")

# Test 4: Test YouTube search API
print("\n[4/5] Testing YouTube search functionality...")
print("-" * 70)

try:
    from youtubesearchpython import VideosSearch
    print("Attempting search for 'python tutorial'...")
    search = VideosSearch('python tutorial', limit=5)
    results = search.result()
    
    if results and 'result' in results and len(results['result']) > 0:
        print(f"✓ YouTube search: OK - Found {len(results['result'])} results")
        print(f"  First result: {results['result'][0]['title']}")
    else:
        print("✗ YouTube search: FAILED - No results returned")
        print(f"  Response: {results}")
        
except Exception as e:
    print(f"✗ YouTube search: FAILED")
    print(f"  Error type: {type(e).__name__}")
    print(f"  Error message: {str(e)}")
    
    # Check for specific errors
    error_str = str(e)
    if "unexpected keyword argument 'proxies'" in error_str or "got an unexpected keyword argument" in error_str:
        print("\n  ⚠ KNOWN ISSUE: Library compatibility problem")
        print("  FIX: Run one of these commands:")
        print("       uv pip install --upgrade youtube-search-python requests")
        print("       OR")
        print("       pip install --upgrade youtube-search-python requests")
    
    import traceback
    print(f"\n  Full traceback:")
    print(traceback.format_exc())

# Test 5: Test custom search with filters
print("\n[5/5] Testing custom search with filters...")
print("-" * 70)

try:
    from youtubesearchpython import CustomSearch
    print("Attempting custom search with filter...")
    search = CustomSearch('music', "EgJAAQ", limit=2)
    results = search.result()
    
    if results and 'result' in results:
        print(f"✓ Custom search: OK - Found {len(results['result'])} results")
    else:
        print("✗ Custom search: FAILED")
        
except Exception as e:
    print(f"✗ Custom search: FAILED - {type(e).__name__}: {str(e)}")

# Summary and recommendations
print("\n" + "=" * 70)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 70)

print("""
If YouTube search is failing:

1. UPDATE PACKAGES (Most Common Fix):
   
   With uv (faster):
   uv pip install --upgrade youtube-search-python requests yt-dlp
   
   With pip:
   pip install --upgrade youtube-search-python requests yt-dlp

2. If you see "got an unexpected keyword argument 'proxies'":
   This is a library compatibility issue.
   
   FIX with uv:
   uv pip install --upgrade youtube-search-python requests
   
   FIX with pip:
   pip install --upgrade youtube-search-python requests
   
   Or install specific compatible versions:
   uv pip install youtube-search-python==1.6.6 requests==2.31.0
   (or with pip)

3. If that doesn't work, try installing a specific version:
   pip install youtube-search-python==1.6.6
   
4. Check if you're behind a proxy or firewall:
   - Corporate networks may block YouTube API access
   - Try using a VPN or different network

5. Clear Python cache:
   - Delete __pycache__ folders
   - Delete .pyc files

6. Alternative: Switch to yt-dlp for search:
   - Consider using yt-dlp's search functionality instead
   - More stable but slower

7. Check YouTube service status:
   - Visit: https://www.youtube.com
   - Check if YouTube is accessible from browser

For detailed error information, check the console output above.
""")

print("=" * 70)
print("Diagnostic complete!")
print("=" * 70)

input("\nPress Enter to exit...")
