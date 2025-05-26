import os
import sys

# Add the app directory to Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Add the parent directory to Python path
parent_dir = os.path.dirname(app_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
