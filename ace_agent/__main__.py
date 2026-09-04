import argparse
import ctypes
import os
import sys


# Set Windows DPI awareness before PySide6 is imported. This keeps the
# screenshot coordinate system aligned with the desktop UI as closely as
# possible and avoids Qt selecting an incompatible DPI context later.
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

from .config import Settings
from .ui import run_gui
from .cli import run_cli


parser = argparse.ArgumentParser(description="ACE Python multilingual computer-use agent")
parser.add_argument("--cli", action="store_true", help="run terminal interface")
args = parser.parse_args()
settings = Settings.from_env()

if args.cli:
    run_cli(settings)
else:
    run_gui(settings)
