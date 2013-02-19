from glob import glob
from os.path import basename, join
from subprocess import call

MKV_EXTENSION = '.mkv'
MP4_EXTENSION = '.mp4'


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


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' source_file [source_file]... destination_directory')
        sys.exit(1)

    # The last argument is the destination directory
    destination_directory = sys.argv[-1]

    # The first argument is the command name. Everything in between are the files to convert
    source_files = sys.argv[1:-1]

    convert_videos(source_files, destination_directory)
