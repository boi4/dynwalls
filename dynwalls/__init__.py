import os
import sys
from config import Config

PROGRAM_DESC = \
"""
dynwalls - Use Mac OS dynamic wallpapers on linux
""".strip()


if "XDG_DATA_HOME" in os.environ:
    DATA_DIR = os.environ.get("XDG_DATA_HOME") + "/dynwalls"
    SYSTEMD_DIR = os.environ.get("XDG_DATA_HOME") + "/systemd/user"
else:
    DATA_DIR = os.environ.get("HOME") + "/.local/share/dynwalls"
    SYSTEMD_DIR = os.environ.get("HOME") + "/.local/share/systemd/user"

try:
    if not os.path.isdir(DATA_DIR) and not os.path.islink(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.isdir(SYSTEMD_DIR) and not os.path.islink(SYSTEMD_DIR):
        os.makedirs(SYSTEMD_DIR)
except sys.OSError:
    print(f"Couldn't create data directory in {DATA_DIR}", file=sys.stderr)
    sys.exit(1)

config = Config(DATA_DIR)

WP_DIR = DATA_DIR + "/images"
PREFIX = "wallpaper"
EXTENSION = ".jpg"
