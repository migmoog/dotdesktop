#!/usr/bin/python

## NOTE: this works, but can use more utils and ways to map
import sys
from os import getenv, chmod
from os.path import abspath, join, exists
from desktop_parser import DesktopFile
from pathlib import Path
import argparse

def make_entry(file_name, exe_path, **kwargs):
    home=getenv("HOME")
    if home is None:
        raise NotADirectoryError()
    path=join(home, ".local/share/applications")
    path=join(path, file_name+".desktop")
    entry_file=DesktopFile(
        file_path=path,
        load=False
    )

    entry_file.data["Exec"] = exe_path
    if kwargs["categories"]:
        entry_file.data["Categories"] = kwargs["categories"]
    if kwargs["icon"]:
        entry_file.data["Icon"] = kwargs["icon"]
    entry_file.data["Name"] = kwargs.get("name", file_name)
    entry_file.data["Type"] = "Application"
    entry_file.data["Terminal"] = "false"

    return entry_file


parser = argparse.ArgumentParser(
    prog="dotdesktop",
    description="Installs a desktop app via CLI",
)

parser.add_argument(
    '-e', '--executable',
    required=True,
    help="Path to exectuable file or command for \"Exec\""
)
parser.add_argument(
    '-n', '--name',
    help="Name of the entry",
)
parser.add_argument('-i', '--icon', help='Path to image file for "Icon"')
parser.add_argument(
    '-f', '--filename',
    help="Name of the .desktop file. Will use name of executable if not provided"
)
parser.add_argument(
    '-c',
    '--categories',
    help="List of categories for the \"Categories\" section"
)
parser.add_argument('-dbg', action='store_true', help=argparse.SUPPRESS)

def main():
    entry_file=None
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args(sys.argv[1:])
        filename = args.filename \
            if args.filename else \
            Path( args.executable ).stem

        categories=""
        if args.categories:
            categories=';'.join(args.categories)

        icon=None
        if args.icon:
            icon=abspath(args.icon)
            if not exists(icon):
                print(f"No file exists at {icon}")
                return 

        exe_path=abspath(args.executable)
        if not exists(exe_path):
            print(f"No executable at {exe_path}")
            return

        entry_file = make_entry(
            filename,
            exe_path,
            icon=icon,
            categories=categories,
            name=args.name if args.name else None
        )
        entry_file.dump(headings="[Desktop Entry]\n")
        chmod(str(entry_file.file_path), 0o775)

        if args.dbg:
            print(entry_file.file_path)

if __name__ == '__main__':
    main()
