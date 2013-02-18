from MKVtoMP4 import *

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' source_file [source_file]... destination_directory')
        sys.exit(1)
    hello_world(sys.argv[1], sys.argv[2])
