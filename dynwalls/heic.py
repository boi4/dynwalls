"""
Functions for reading and extracting data from heic files
"""
import base64
import plistlib
import sys
import subprocess
import os


def get_exif(fname):
    """
    Sadly, pillow and exifread do not support heic yet
    """
    args = ["exiftool", fname]
    r = subprocess.run(args, stdout=subprocess.PIPE)
    output = r.stdout.decode("utf-8")
    return {line.split(":")[0].strip(): line.split(":")[1].strip() for line in output.split("\n")[:-1]}


def extract_images(fname, outputdir, filename_prefix, extension):
    """
    TODO: use pyheif
    """
    if extension.startswith("."):
        extension = extension[1:]
    if not os.path.isdir(outputdir):
        os.makedirs(outputdir)
    args = ["heif-convert", "-q", "100", fname, f"{outputdir}/{filename_prefix}.{extension}"]
    # TODO: check return code
    subprocess.run(args)


def get_wallpaper_config(fname):
    exif = get_exif(fname)

    if "H24" not in exif and "Solar" not in exif:
        print("Couldn't find time/solar info")
        sys.exit(0)

    if "Solar" in exif:
        data = exif["Solar"]
    else:
        data = exif["H24"]

    dec = base64.b64decode(data)
    config = plistlib.loads(dec)

    return config
