from glob import glob
from os import remove
from os.path import basename, exists, join
import shutil
from subprocess import call

MKV_EXTENSION = '.mkv'
MP4_EXTENSION = '.mp4'
MKV_SEARCH = '*' + MKV_EXTENSION
MP4_SEARCH = '*' + MP4_EXTENSION
FILES_MODE = '-files'
MIRROR_MODE = '-mir'
ONLY_FLAG = '-only'
NOT_FLAG = '-not'


def convert_videos(input_patterns, destination_directory):
    for input_pattern in input_patterns:
        files = glob(input_pattern)

        if len(files) == 0:
            print('Warning: No files found matching ' + input_pattern)

        for input_file in files:
            output_file = generate_output_name(input_file, destination_directory)
            convert_video(input_file, output_file)


def create_log_file(log_file):
    if not exists(log_file):
        f = open(log_file, 'w')
        f.close()


def mirror_videos(source_directory, destination_directory, log_directory, exclusions, only):
    source_pattern = join(source_directory, MKV_SEARCH)
    source_glob = glob(source_pattern)
    source_set = set(source_glob)
    destination_pattern = join(destination_directory, MP4_SEARCH)
    destination_glob = glob(destination_pattern)
    log_pattern = join(log_directory, MP4_SEARCH)
    log_glob = glob(log_pattern)
    encode_list = []

    if exclusions and only:
        print('mirror_videos was passed both exclusions and only')
        sys.exit(1)

    if exclusions:
        for exclusion in exclusions:
            exclusion_pattern = join(source_directory, exclusion)
            exclusion_glob = glob(exclusion_pattern)
            exclusion_set = set(exclusion_glob)

            source_set -= exclusion_set
    elif only:
        source_set = set()
        for pattern in only:
            only_pattern = join(source_directory, pattern)
            only_glob = glob(only_pattern)
            only_set = set(only_glob)

            source_set |= only_set

    for source_file in source_set:
        destination_file = generate_output_name(source_file, destination_directory)
        log_file = generate_output_name(source_file, log_directory)
        if log_file in log_glob:
            # We have a log of doing this conversion. We should make sure we keep the log
            # intact and not convert it again.
            log_glob.remove(log_file)
        elif destination_file in destination_glob:
            # We have the destination file, but not the log of doing it. Create the log.
            create_log_file(log_file)
        else:
            # We haven't converted this video yet. Queue it up
            encode_job = (source_file, destination_file, log_file)
            encode_list.append(encode_job)

    for log_file in log_glob:
        print("Deleting " + log_file)
        remove(log_file)

    for input_file, output_file, log_file in encode_list:
        generate_output(input_file, output_file)
        create_log_file(log_file)


def generate_output_name(input_file, destination_directory):
    filename = basename(input_file)
    # Preserve the name if the extension is .mp4
    if not filename.endswith(MP4_EXTENSION):
        # Strip the extension if it is .mkv
        if filename.endswith(MKV_EXTENSION):
            filename = filename[:-len(MKV_EXTENSION)]

        filename += MP4_EXTENSION
    output_file = join(destination_directory, filename)
    return output_file


def generate_output(input_file, output_file):
    # If the input already has an extension of .mp4, just copy it directly
    if input_file.endswith(MP4_EXTENSION):
        copy_video(input_file, output_file)
    else:
        # Otherwise convert the file using FFmpeg
        convert_video(input_file, output_file)


def copy_video(input_file, output_file):
    print('Copying ' + input_file + ' to ' + output_file)

    shutil.copyfile(input_file, output_file)


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
    print('Usage: ' + sys.argv[0] + ' -mir source_directory destination_directory log_directory [-only | -not pattern [pattern]...]')


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


def _mirror_mode():
    # The first two arguments are the source and destination directories
    source_directory = sys.argv[2]
    destination_directory = sys.argv[3]
    log_directory = sys.argv[3] # If there isn't a log directory specified, the destination acts like it
    exclusions = None
    only = None

    # The next parameter can either be -only, -not, or the log directory
    if len(sys.argv) >= 5:
        if sys.argv[4].lower() == ONLY_FLAG:
            # We have to have at least one 'only' pattern
            if len(sys.argv) < 6:
                print_usage()
                sys.exit(1)

            only = sys.argv[5:]

        elif sys.argv[4].lower() == NOT_FLAG:
            # We have to have at least one exclusion
            if len(sys.argv) < 6:
                print_usage()
                sys.exit(1)

            exclusions = sys.argv[5:]

        else:
            log_directory = sys.argv[4]

            # The next parameter can either be -only or -not
            if len(sys.argv) >= 6:
                if sys.argv[5].lower() == ONLY_FLAG:
                    # We have to have at least one 'only' pattern
                    if len(sys.argv) < 7:
                        print_usage()
                        sys.exit(1)

                    only = sys.argv[6:]

                elif sys.argv[5].lower() == NOT_FLAG:
                    # We have to have at least one exclusion
                    if len(sys.argv) < 7:
                        print_usage()
                        sys.exit(1)

                    exclusions = sys.argv[6:]

    mirror_videos(source_directory, destination_directory, log_directory, exclusions, only)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    # The first argument might be the mode to use, or it might be the first source file in files mode
    if sys.argv[1].lower() == MIRROR_MODE:
        _mirror_mode()
    elif sys.argv[1].lower() == FILES_MODE:
        _files_mode(2)
    elif sys.argv[1][0] == '-':
        print('Unknown option: ' + sys.argv[1])
        print_usage()
        sys.exit(1)
    else:
        _files_mode(1)
