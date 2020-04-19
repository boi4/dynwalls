import os
import sys
from config import Config

PROGRAM_DESC = \
"""
dynamicwalls - Use Mac OS dynamic wallpapers on linux
""".strip()


if "XDG_DATA_HOME" in os.environ:
    DATA_DIR = os.environ.get("XDG_DATA_HOME") + "/dynamicwalls/"
else:
    DATA_DIR = os.environ.get("HOME")+"/.local/share/dynamicwalls/"

if not os.path.isdir(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except sys.OSError:
        print(f"Couldn't create data directory in {DATA_DIR}", file=sys.stderr)
        sys.exit(1)

config = Config(DATA_DIR)

WP_DIR    = DATA_DIR+"/images"
PREFIX    = "wallpaper"
EXTENSION = ".jpg"
