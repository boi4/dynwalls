"""
Functions for installing and creating wallpaper systemd files
"""
import os
import subprocess
import sys

from __init__ import SYSTEMD_DIR


timerskeleton = \
"""
[Unit]
Description=Update Wallpaper at specific times

[Timer]
INSERTHERE
Persistent=true

[Install]
WantedBy=timers.target
""".strip()

servicetext = \
"""
[Unit]
Description=Update Dynamic Wallpaper

[Service]
ExecStart={} {} update
""".format(sys.executable,
           os.path.dirname(os.path.abspath(__file__)))

DEFAULT_TIMERNAME = "dynwalls.timer"

DEFAULT_TIMERFILE = SYSTEMD_DIR + "/" + DEFAULT_TIMERNAME
DEFAULT_SERVICEFILE = SYSTEMD_DIR + "/dynwalls.service"



def _create_timer(timelist, filename=DEFAULT_TIMERFILE):
    """
    timelist should be a list of datetime.time objects
    """
    conditions = ["OnCalendar=*-*-* {}".format(time.isoformat("seconds"))
                  for time in timelist]
    timertext = timerskeleton.replace("INSERTHERE","\n".join(conditions))
    with open(filename, "w+") as f:
        f.write(timertext)


def _create_service(filename=DEFAULT_SERVICEFILE):
    with open(filename, "w+") as f:
        f.write(servicetext)


def enable_timer(timername=DEFAULT_TIMERNAME):
    reload()
    args = ["systemctl", "--user", "enable", "--now", timername]
    subprocess.run(args)

def disable_timer(timername=DEFAULT_TIMERNAME):
    reload()
    args = ["systemctl", "--user", "disable", timername]
    subprocess.run(args)

def reload():
    args = ["systemctl", "--user", "daemon-reload"]
    subprocess.run(args)

def setup_units(timelist
                ,timerfile=DEFAULT_TIMERFILE
                ,servicefile=DEFAULT_SERVICEFILE
                ,unitdir=SYSTEMD_DIR):

    _create_timer(timelist, filename=timerfile)
    _create_service(filename=servicefile)
    reload()
