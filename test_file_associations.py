"""
Test script for file association functionality
This script tests the file association features without running the full GUI
"""

import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

from settings_handler import config_get, set_file_association, get_associated_formats

def test_file_associations():
    print("=" * 60)
    print("File Association Test Script")
    print("=" * 60)
    
    # Test 1: Check current associations
    print("\nTest 1: Current file associations")
    print("-" * 40)
    formats = ["mp4", "avi", "mkv", "webm", "flv", "mp3", "m4a", "wav", "flac", "ogg"]
    for fmt in formats:
        status = config_get(f"assoc_{fmt}")
        print(f"  {fmt.upper()}: {'✓ Associated' if status else '✗ Not associated'}")
    
    # Test 2: Get associated formats
    print("\nTest 2: Get associated formats function")
    print("-" * 40)
    associated = get_associated_formats()
    if associated:
        print(f"  Associated formats: {', '.join(associated)}")
    else:
        print("  No formats currently associated")
    
    # Test 3: Demonstrate association (without actually doing it)
    print("\nTest 3: File association functions available")
    print("-" * 40)
    print("  ✓ set_file_association(extension, enable=True)")
    print("  ✓ get_associated_formats()")
    print("  ✓ config_get(f'assoc_{extension}')")
    
    # Test 4: Show what happens when you associate
    print("\nTest 4: What happens during association")
    print("-" * 40)
    print("  When you check a format in settings and click OK:")
    print("  1. set_file_association(extension, True) is called")
    print("  2. Registry keys are created:")
    print("     - HKCU\\Software\\Classes\\.{ext}")
    print("     - HKCU\\Software\\Classes\\AccessibleYouTubeDownloaderPro.{ext}")
    print("  3. Config file is updated with assoc_{ext} = True")
    
    print("\nTest 5: Command-line file opening")
    print("-" * 40)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"  File argument detected: {file_path}")
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[1][1:].lower()
            print(f"  File extension: {ext}")
            print(f"  File exists: ✓")
            if ext in formats:
                is_associated = config_get(f"assoc_{ext}")
                print(f"  Format associated: {'✓' if is_associated else '✗'}")
        else:
            print(f"  File exists: ✗")
    else:
        print("  No file argument provided")
        print("  Usage: python test_file_associations.py path\\to\\file.mp4")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_file_associations()
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
