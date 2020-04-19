#!/usr/bin/env python3
import sys
import os
import re
import datetime
import subprocess
import shlex

import args
import systemd
import heic

from pprint import pprint

from __init__ import DATA_DIR
from __init__ import WP_DIR
from __init__ import PREFIX
from __init__ import EXTENSION
from __init__ import config


class DynWalls:
    """
    Currently, this class only exists to make the getattr trick to work
    """

    def __init__(self):
        pass


    def act(self, actionname, args):
        getattr(self, actionname)(args)


    def get_timelist(self):
        timelist = []
        times = config.dyn_config['ti']
        for time in times:
            secs = int(float(time['t']) * 60*60*24)
            t = datetime.time(secs//(60*60), secs//60 % 60, secs % 60)
            timelist.append(t)
        return timelist

    # ===== SUBCOMMANDS ======
    def setcmd(self, arguments):
        config.wp_cmd = arguments.cmdstring
        print("Successfully updated wallpaper command.")

        # if hasattr(config, "dyn_config"):
        #     timelist = self.get_timelist()
        #     systemd.setup_units(timelist)

    def use(self, arguments):
        c = heic.get_wallpaper_config(arguments.heicfile)
        if "si" in c:
            print("Sun based wallpapers are not yet supported.", file=sys.stderr)
            sys.exit(1)
        times =  c['ti']
        times.sort(key=lambda x: x['t'])
        prev = -0.1
        for d in times:
            cur = float(d['t'])
            if not 0.0 <= cur <= 1.0:
                print("Warning: Invalid time specification found. Might skip some images.")
            if cur == prev:
                print("Warning: Ambigous time specifiation found. Might skip some images.")
            prev = cur

        # TODO: check if all image indizes are available in the heic file

        # clean up old images
        if os.path.isdir(WP_DIR):
            for f in os.listdir(WP_DIR):
                if re.match(f"^{PREFIX}-[\\d]+{EXTENSION}$", f):
                    os.remove(f"{WP_DIR}/{f}")

        heic.extract_images(arguments.heicfile,
                            outputdir=WP_DIR,
                            filename_prefix=PREFIX,
                            extension=EXTENSION)

        config.dyn_config = c

        # create units
        timelist = self.get_timelist()
        systemd.setup_units(timelist)
        # TODO: only update if enabled
        self.update({})



    def enable(self, arguments):
        if not hasattr(config, "dyn_config"):
            print("Error: Please set a wallpaper with the 'use' command first",file=sys.stderr)
            sys.exit(1)

        if not hasattr(config, "wp_cmd"):
            print("Error: Please specify a wallpaper setting command using 'setcmd' first.",file=sys.stderr)
            sys.exit(1)

        systemd.enable_timer()
        self.update({})


    def disable(self, arguments):
        # TODO: check if timer active at all
        systemd.disable_timer()


    def update(self, arguments):
        if not hasattr(config, "dyn_config"):
            print("Error: Please set a wallpaper with the 'use' command first",file=sys.stderr)
            sys.exit(1)

        if not hasattr(config, "wp_cmd"):
            print("Error: Please specify a wallpaper setting command using 'setcmd' first.",file=sys.stderr)
            sys.exit(1)

        times = config.dyn_config['ti']
        times.sort(key=lambda x: x['t'])
        using = times[0]
        now = datetime.datetime.now().time()
        nowsecs = now.hour * 60 * 60 + now.minute * 60 + now.second
        last_one = times[-1]
        for time in times:
            if float(time['t']) * 60*60*24 > nowsecs:
                if float(time['t']) * 60*60*24 - nowsecs < 10: # prevent floating errors or similar things
                    last_one = time
                break
            last_one = time
        index = last_one['i'] + 1 # plus one because heif-convert starts indexing at 1
        ext = EXTENSION[1:] if EXTENSION.startswith(".") else EXTENSION
        image_name = f"{WP_DIR}/{PREFIX}-{index}.{ext}"
        args = shlex.split(config.wp_cmd)
        if "{}" in args:
            args = [image_name if arg == "{}" else arg for arg in args]
        else:
            args += [image_name]
        subprocess.run(args)



def main():
    a = args.Args()

    arguments = a.parse()

    dw = DynWalls()
    dw.act(arguments.action, arguments)


if __name__ == "__main__":
    main()
