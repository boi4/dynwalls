from __init__ import PROGRAM_DESC

import argparse
import sys


class Args:
    """
    TODO: add action to help message string of subcommands
    """
    actions = {
        "setcmd" : ("<cmdstring>", "Configure which command to use for updating the wallpaper"),
        "use" : ("<heicfile>","Use HEIC file as the new dynamic wallpaper"),
        "enable" : ("","Enable and activate dynwalls"),
        "disable" : ("","Disable and stop dynwalls"),
        "update" : ("","Update wallpaper for current time (will be called automatically with systemd)"),
    }

    def __init__(self):
        usage = """dynwalls <action> [<args>]

Available actions:
   {}

    """.format("\n   ".join(f"{k:15} {args:20} {v}" for (k,(args,v)) in Args.actions.items()))

        self.cli = argparse.ArgumentParser(description=PROGRAM_DESC, usage=usage)
        self.cli.add_argument("action", choices=Args.actions, help="The action to perform")
        self.action = None
        self.subparser = None

    def parse(self):
        args = self.cli.parse_args(sys.argv[1:2])
        self.action = args.action
        self.subparser = argparse.ArgumentParser(description=Args.actions[self.action][1])

        getattr(self, args.action)()

        subargs = self.subparser.parse_args(sys.argv[2:])
        subargs.action = args.action
        return subargs

    # ============ SUBCOMMANDS PARSING =============
    def setcmd(self):
        self.subparser.add_argument(
            "cmdstring",
            help="The command to use for updating the wallpaper. If it contains one or multiple '{}' strings, they will "
                 "be replaced with the filename, otherwise the filename is put after the command."
        )

    def use(self):
        self.subparser.add_argument("heicfile", help="The HEIC file to use")

    def enable(self):
        pass

    def disable(self):
        pass

    def update(self):
        pass
