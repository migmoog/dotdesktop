#!/usr/bin/python

## NOTE: this works, but can use more utils and ways to map
import sys
from os import getenv, chmod
from os.path import abspath, join
from desktop_parser import DesktopFile
from pathlib import Path
import argparse

def make_entry(file_name, exe_path, icon=None, categories="", name=""):
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
    if categories:
        entry_file.data["Categories"] = categories
    if icon:
        entry_file.data["Icon"] = icon
    entry_file.data["Name"] = name if name else file_name
    entry_file.data["Type"] = "Application"
    entry_file.data["Terminal"] = "false"

    return entry_file


def interactive(file_name = None):
    exe_path=Path( input("Path to exectuable: ") )
    if not exe_path.exists():
        raise FileNotFoundError()
    if file_name is None:
        file_name=exe_path.stem
    icon_path=Path(input("Path to icon: "))

    categories=input("Categories: " )
    return make_entry(file_name, exe_path, icon_path, categories)


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
    '--filename',
    help="Name of the .desktop file. Will use name of executable if not provided"
)
parser.add_argument(
    '-c',
    '--categories',
    help="List of categories for the \"Categories\" section"
)
parser.add_argument('--iv', action='store_true', help='do interactive filling')
parser.add_argument('-dbg', action='store_true', help=argparse.SUPPRESS)

def main():
    entry_file=None
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args(sys.argv[1:])
        filename = args.filename if args.filename else Path( args.executable ).stem
        if args.iv:
            entry_file = interactive(filename)
        else:
            categories=""
            if args.categories:
                categories=';'.join(args.categories)

            icon=None
            if args.icon:
                icon=abspath(args.icon)

            entry_file = make_entry(
                filename,
                abspath(args.executable),
                icon=icon,
                categories=categories
            )
        entry_file.dump(headings="[Desktop Entry]\n")
        chmod(str(entry_file.file_path), 0o775)

        if args.dbg:
            print(entry_file.file_path)

if __name__ == '__main__':
    main()
