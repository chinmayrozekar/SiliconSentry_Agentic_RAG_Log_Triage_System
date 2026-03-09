import warnings
import sys

# Silence specific library warnings for a cleaner CLI experience
# MUST be done before importing libraries that trigger them
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")
warnings.filterwarnings("ignore", message="Unable to find acceptable character detection dependency")

# Optional: Silence InsecureRequestWarning if using unverified HTTPS anywhere
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
