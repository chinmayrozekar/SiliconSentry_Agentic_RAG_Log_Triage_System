import warnings
import sys
import multiprocessing

# MUST be called at the very top for PyInstaller + Multiprocessing support
if __name__ == "__main__":
    multiprocessing.freeze_support()

# Silence specific library warnings for a cleaner CLI experience
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")
warnings.filterwarnings("ignore", message="Unable to find acceptable character detection dependency")

try:
    import requests
    from urllib3.exceptions import InsecureRequestWarning
    if hasattr(requests, 'packages'):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except Exception:
    pass

from src.cli import cli

if __name__ == "__main__":
    cli()
