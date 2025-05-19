# backend/config.py

import os

# Base path to vinyl recordings
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RECORDINGS_DIR = os.path.join(BASE_DIR, 'data', 'Recordings')
