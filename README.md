# DynWalls - MacOS Wallpapers on Linux

This Python programs allows you to set Dynamic Wallpapers from MacOS (in the [HEIC](https://en.wikipedia.org/wiki/High_Efficiency_Image_File_Format) format) as your background.

## Features
 - Read HEIC file and set wallpaper
 - Update wallpaper at times specified in the HEIC file
 - Wallpaper updating command can be specified

### Missing Features
 - HEIC files using the sun position are currently not supported, but hopefully in the future


## Requirements
 - Systemd (For automatic updating)
 - exiftool
 - libheif (`libheif-examples` under Debian, Ubuntu, Pop!\_OS)
 - (optional) feh, if you want to use the example command below
 
Make sure that both `exiftool` and `heif-convert` (part of libheif) can be executed from your command line.
 
## Installation
Currently, the program is not available on pypi and has to be cloned manually.
After that you can use
```shell
python3 path/to/cloned/repo/dynwalls
```
to run the program.


## Usage
First, specify a command that will set your wallpaper given a jpg image:

```shell
dynwalls setcmd 'feh --bg-fill --no-fehbg {}'
```

The command you use depends on your system setup. If you're running GNOME, you will want to use:

```shell
dynwalls setcmd 'gsettings set org.gnome.desktop.background picture-uri {}'
```

In general, googling `How to set background image on command line with XYZ` where `XYZ` is your window manager/desktop environment should help.

Also, you can use a custom shellscript for more complicated setups, just make sure it is available in your PATH.


After you are done with the previous step, specify a dynamic wallpaper to use:

```shell
dynwalls use mojave.heic
```

This will install a systemd user service and a systemd timer which are not yet activated.

Sadly, wallpapers that use the sun position are not yet supported. The program will tell you if the passed picture is not supported.


Then, enable automatic updating of your wallpaper:

```shell
dynwalls enable
```

This will activate the systemd timer.


If you want to disable the automatic updating use:

```shell
dynwalls disable
```


## Troubleshooting
You can run 
```shell
journalctl --user -u dynamicwalls
```
to see possible error messages.


If you use a transparent status bar and are having contrast problems, take a look at [STATUS_BARS.md](./STATUS_BARS.md)
