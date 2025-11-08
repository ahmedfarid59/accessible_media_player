"""
Real-time log monitor for accessible_youtube_downloader_pro
"""
import os
import time
import sys

log_file = os.path.join(os.getenv('APPDATA'), 'accessible youtube downloader pro', 'logs', 'app_20251108.log')

print(f"Monitoring log file: {log_file}")
print("=" * 80)
print()

if not os.path.exists(log_file):
    print("ERROR: Log file not found!")
    sys.exit(1)

# Read existing content
with open(log_file, 'r', encoding='utf-8') as f:
    existing_content = f.read()
    print(existing_content)
    
print()
print("=" * 80)
print("Monitoring for new log entries (Ctrl+C to stop)...")
print("=" * 80)
print()

# Monitor for new lines
try:
    with open(log_file, 'r', encoding='utf-8') as f:
        # Seek to end
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if line:
                print(line.rstrip())
            else:
                time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")
