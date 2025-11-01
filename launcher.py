import subprocess
import sys
import time
import os

# Helper to find python executable
PYTHON = sys.executable

# Start ttsapi.py (backend)
ttsapi_proc = subprocess.Popen([PYTHON, 'ttsapi.py'])
print('Started ttsapi.py (backend)')

# Wait a bit to let backend start (adjust if needed)
time.sleep(5)

# Start frontend.py (frontend)
frontend_proc = subprocess.Popen([PYTHON, 'frontend.py'])
print('Started frontend.py (frontend)')

print('\nBoth backend and frontend are running.')
print('To stop, press Ctrl+C in this window.')

try:
    # Wait for both processes
    ttsapi_proc.wait()
    frontend_proc.wait()
except KeyboardInterrupt:
    print('\nShutting down...')
    ttsapi_proc.terminate()
    frontend_proc.terminate()
    ttsapi_proc.wait()
    frontend_proc.wait()
    print('Exited.')
