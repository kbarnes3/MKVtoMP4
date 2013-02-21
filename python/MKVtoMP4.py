from glob import glob
from os import remove
from os.path import basename, join
from subprocess import call

MKV_EXTENSION = '.mkv'
MP4_EXTENSION = '.mp4'
MKV_SEARCH = '*' + MKV_EXTENSION
MP4_SEARCH = '*' + MP4_EXTENSION
FILES_MODE = '-files'
MIRROR_MODE = '-mir'


def convert_videos(input_patterns, destination_directory):
    for input_pattern in input_patterns:
        files = glob(input_pattern)

        if len(files) == 0:
            print('Warning: No files found matching ' + input_pattern)

        for file in files:
            output_file = generate_output_name(file, destination_directory)
            convert_video(file, output_file)


def mirror_videos(source_directory, destination_directory):
    source_pattern = join(source_directory, MKV_SEARCH)
    source_glob = glob(source_pattern)
    destination_pattern = join(destination_directory, MP4_SEARCH)
    destination_glob = glob(destination_pattern)
    encode_list = []

    for source_file in source_glob:
        destination_file = generate_output_name(source_file, destination_directory)
        if destination_file in destination_glob:
            destination_glob.remove(destination_file)
        else:
            encode_job = (source_file, destination_file)
            encode_list.append(encode_job)

    for destination_file in destination_glob:
        print("Deleting " + destination_file)
        remove(destination_file)

    for input, output in encode_list:
        convert_video(input, output)


def generate_output_name(input_file, destination_directory):
    filename = basename(input_file)
    # Strip the extension if it is .mkv
    if filename.endswith(MKV_EXTENSION):
        filename = filename[:-len(MKV_EXTENSION)]

    filename += MP4_EXTENSION
    output_file = join(destination_directory, filename)
    return output_file


def convert_video(input_file, output_file):
    print('Converting ' + input_file + ' to ' + output_file)

    call(['ffmpeg',
          '-i',
          input_file,
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
        mirror_videos(sys.argv[2], sys.argv[3])
    elif sys.argv[1].lower() == FILES_MODE:
        _files_mode(2)
    elif sys.argv[1][0] == '-':
        print('Unknown option: ' + sys.argv[1])
        print_usage()
        sys.exit(1)
    else:
        _files_mode(1)
