#!/usr/bin/env python3
import os.path
import re
import subprocess
import sys

from PIL import Image  # needs python pillow installed

STATUSBAR_HEIGHT = 5  # in pixels
CONFIG_PATH = "~/.config/i3status-rust/config.toml"


# config values for i3status-rust

light_theme = {
    "idle_bg"            : "#00000000",
    "idle_fg"            : "#93a1a1ff",
    
    "info_bg"            : "#00000000",
    "info_fg"            : "#93a1a1ff",
    
    "good_bg"            : "#00000000",
    "good_fg"            : "#008800ff",
    
    "warning_bg"         : "#00000000",
    "warning_fg"         : "#963f00ff",
    
    "critical_bg"        : "#00000080",
    "critical_fg"        : "#ff0000ff",
    
    "separator"          : "| ",
    "separator_bg"       : "#00000000",
    "separator_fg"       : "#a9a9a9ff",
    
    "alternating_tint_bg": "#00000000",
    "alternating_tint_fg": "#000000ff",
}

dark_theme = {
    "idle_bg"             : "#00000000",
    "idle_fg"             : "#2a2a2aff",

    "info_bg"             : "#00000000",
    "info_fg"             : "#2a2a2aff",

    "good_bg"             : "#00000000",
    "good_fg"             : "#008800ff",

    "warning_bg"          : "#00000000",
    "warning_fg"          : "#963f00ff",

    "critical_bg"         : "#00000080",
    "critical_fg"         : "#880000ff",

    "separator"           : "| ",
    "separator_bg"        : "#00000000",
    "separator_fg"        : "#000000ff",

    "alternating_tint_bg" : "#00000000",
    "alternating_tint_fg" : "#000000ff",
}


def set_wallpaper(img_path):
    subprocess.run(["feh", "--bg-fill", "--no-fehbg", img_path])


def get_avg_luminance(img_path):
    im = Image.open(img_path)
    cropped = im.crop((0, 0, im.width, STATUSBAR_HEIGHT))

    # convert to grayscale
    if cropped.mode != "L":
        cropped = cropped.convert(mode="L")

    return cropped.resize((1,1), Image.ANTIALIAS).getpixel((0, 0)) / 255  # small trick


def reload_bar():
    subprocess.run(["pkill", "-f", "i3status-wrapper.py", "--signal", "SIGUSR1"])


def apply_theme(theme, theme_magic):
    with open(os.path.expanduser(CONFIG_PATH), "r") as f:
        content = f.read()

        # avoid reloading if theme already applied
        if theme_magic in content:
            return

    # set values
    for k,v in theme.items():
        content = re.sub(f"^{k}\\s*=.*$", f'{k}="{v}"', content, flags=re.M)

    # remove old theme magic string
    content = "\n".join(line for line in content.split("\n") if not line.startswith("#THEME"))

    # add theme magic string so, the script won't reload if same theme is applied
    content += "\n" + theme_magic

    with open(os.path.expanduser(CONFIG_PATH), "w") as f:
        f.write(content)

    reload_bar()


if len(sys.argv) != 2:
    exit(1)

image_path = os.path.expanduser(sys.argv[1])
set_wallpaper(image_path)

avg_lum = get_avg_luminance(image_path)

if avg_lum < 0.4:
    apply_theme(light_theme, "#THEME: light ajsdlfkjad")
else:
    apply_theme(dark_theme, "#THEME: dark gjalga")
