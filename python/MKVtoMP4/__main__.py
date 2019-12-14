import sys
from MKVtoMP4 import process_command_line


def entry_point():
    process_command_line(sys.argv)


if __name__ == "__main__":
    entry_point()
