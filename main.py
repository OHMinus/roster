import sys
import datetime
import cui
import core
import withGui
import os

def main():
    
    if(index_of(sys.argv, "-h") != -1 or index_of(sys.argv, "--help") != -1):
        print_help()
        sys.exit(1)

    if (index_of(sys.argv, "-c") != -1 or index_of(sys.argv, "--cui") != -1):
        if len(sys.argv) == 4:
            cui.Main(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            cui.Main(sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) > 5:
            print("Usage: roster.exe -c [input_dir] [output_file] [output_file_encoding]")
            sys.exit(1)
    else:
        withGui.StartGUI()

def index_of(array:list, target):
    i = 0
    for item in array:
        if item == target:
            return i
        i = i + 1
    return -1


def print_help():
    print("Usage: roster.exe [options] [input_dir] [output_file] [output_file_encoding]")
    print("List the data of application files as csv format.")
    print("Options:")
    print("  -h, --help      Show this help message and exit")
    print("  -c, --cui       Run in CUI mode (default is GUI)")


if __name__ == "__main__":
    if "nt" in os.name:
        sys.setdefaultencoding('cp932')
    main()
