from glob import glob
from os.path import basename, join
from subprocess import call

MKV_EXTENSION = '.mkv'
MP4_EXTENSION = '.mp4'
FILES_MODE = '-files'
MIRROR_MODE = '-mir'


def convert_videos(input_patterns, destination_directory):
    for input_pattern in input_patterns:
        files = glob(input_pattern)

        if len(files) == 0:
            print('Warning: No files found matching ' + input_pattern)

        for file in files:
            filename = basename(file)
            # Strip the extension if it is .mkv
            if filename.endswith(MKV_EXTENSION):
                filename = filename[:-len(MKV_EXTENSION)]

            filename += MP4_EXTENSION
            output_file = join(destination_directory, filename)

            print('Converting ' + file + ' to ' + output_file)

            call(['ffmpeg',
                  '-i',
                  file,
                  '-c:v',
                  'copy',
                  '-c:a',
                  'aac',
                  '-cutoff',
                  '15000',
                  '-b:a',
                  '192k',
                  '-ac',
                  '2',
                  '-strict',
                  '-2',
                  output_file])


def print_usage():
    print('Usage: ' + sys.argv[0] + ' [-files] source_file [source_file]... destination_directory')
    print('Usage: ' + sys.argv[0] + ' -mir source_directory destination_directory')


def _files_mode(first_file):
    # We need at least one file and one directory from sys.argv, so the length needs to be
    # at least 2 greater than first_file
    if len(sys.argv) < first_file + 2:
        print_usage()
        sys.exit(1)

    # The last argument is the destination directory
    destination_directory = sys.argv[-1]

    # The file names start at sys.argv[first_file].
    source_files = sys.argv[first_file:-1]

    convert_videos(source_files, destination_directory)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    # The first argument might be the mode to use, or it might be the first source file in files mode
    if sys.argv[1].lower() == MIRROR_MODE:
        pass
    elif sys.argv[1].lower() == FILES_MODE:
        _files_mode(2)
    elif sys.argv[1][0] == '-':
        print('Unknown option: ' + sys.argv[1])
        print_usage()
        sys.exit(1)
    else:
        _files_mode(1)
