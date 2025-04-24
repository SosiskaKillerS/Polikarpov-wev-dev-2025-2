import sys

# Add your project directory to the Python path
path = 'C:/Users/pesas/OneDrive/Desktop/Polikarpov-web-dev-2025-2'
if path not in sys.path:
    sys.path.append(path)

from app import app as application 