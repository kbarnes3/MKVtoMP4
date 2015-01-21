from argparse import ArgumentParser
from itertools import chain
from glob import glob
from os import remove
from os.path import basename, exists, join
import shutil
from subprocess import call

from powermanagement import long_running

MKV_EXTENSION = '.mkv'
MP4_EXTENSION = '.mp4'
MKV_SEARCH = '*' + MKV_EXTENSION
MP4_SEARCH = '*' + MP4_EXTENSION


def convert_videos(input_patterns, destination_directory, encoding_profile):
    for input_pattern in input_patterns:
        files = glob(input_pattern)

        if len(files) == 0:
            print('Warning: No files found matching ' + input_pattern)

        for input_file in files:
            output_file = generate_output_name(input_file, destination_directory)
            convert_video(input_file, output_file, encoding_profile)


def create_log_file(log_file):
    if not exists(log_file):
        f = open(log_file, 'w')
        f.close()


def mirror_videos(source_directory, destination_directory, log_directory, exclusions, only, encoding_profile):
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
        exit_with_error()
        return

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
        generate_output(input_file, output_file, encoding_profile)
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


def generate_output(input_file, output_file, encoding_profile):
    # If the input already has an extension of .mp4, just copy it directly
    if input_file.endswith(MP4_EXTENSION):
        copy_video(input_file, output_file)
    else:
        # Otherwise convert the file using FFmpeg
        convert_video(input_file, output_file, encoding_profile)


def copy_video(input_file, output_file):
    print('Copying ' + input_file + ' to ' + output_file)

    shutil.copyfile(input_file, output_file)


def convert_video(input_file, output_file, encoding_profile):
    print('Converting ' + input_file + ' to ' + output_file)

    if encoding_profile == 'video_passthrough':
        call_parameters = [
            'ffmpeg',
            '-i',
            input_file,
            '-y',
            '-c:v',
            'copy',
            '-c:a',
            'libfdk_aac',
            '-cutoff',
            '18000',
            '-b:a',
            '192k',
            '-ac',
            '2',
            output_file,
        ]

    elif encoding_profile == 'burn_in':
        call_parameters = [
            'ffmpeg',
            '-i',
            input_file,
            '-y',
            '-filter_complex',
            '[0:v][0:s]overlay[overlaid]',
            '-map',
            '[overlaid]',
            '-map',
            '0:a',
            '-c:v',
            'libx264',
            '-preset',
            'medium',
            '-crf',
            '22',
            '-c:a',
            'libfdk_aac',
            '-cutoff',
            '18000',
            '-b:a',
            '192k',
            '-ac',
            '2',
            output_file
        ]

    elif encoding_profile == '720p_burn_in':
        call_parameters = [
            'ffmpeg',
            '-i',
            input_file,
            '-y',
            '-filter_complex',
            '[0:v][0:s]overlay,scale=w=1280:h=720:force_original_aspect_ratio=decrease,scale=w=trunc(iw/2)*2:h=trunc(ih/2)*2[scaled]',
            '-map',
            '[scaled]',
            '-map',
            '0:a',
            '-c:v',
            'libx264',
            '-preset',
            'medium',
            '-crf',
            '22',
            '-c:a',
            'libfdk_aac',
            '-cutoff',
            '18000',
            '-b:a',
            '192k',
            '-ac',
            '2',
            output_file,
        ]

    elif encoding_profile == '720p':
        call_parameters = [
            'ffmpeg',
            '-i',
            input_file,
            '-y',
            '-filter_complex',
            '[0:v]scale=w=1280:h=720:force_original_aspect_ratio=decrease,scale=w=trunc(iw/2)*2:h=trunc(ih/2)*2[scaled]',
            '-map',
            '[scaled]',
            '-map',
            '0:a',
            '-c:v',
            'libx264',
            '-preset',
            'medium',
            '-crf',
            '22',
            '-c:a',
            'libfdk_aac',
            '-cutoff',
            '18000',
            '-b:a',
            '192k',
            '-ac',
            '2',
            output_file,
        ]

    else:
        print('Unknown encoding profile: {0}'.format(encoding_profile))
        exit_with_error()

    call(call_parameters)


def _files_mode(arguments):
    if len(arguments.paths) < 2:
        print('Files mode requires at least two paths')
        exit_with_error()
    convert_videos(arguments.paths[:-1], arguments.paths[-1], arguments.encoding_profile)


def _mirror_mode(arguments):
    if len(arguments.paths) < 2 or len(arguments.paths) > 3:
        print('Mirror mode can only take two or three paths')
        exit_with_error()

    # The first two paths are the source and destination directories
    source_directory = arguments.paths[0]
    destination_directory = arguments.paths[1]
    log_directory = arguments.paths[1]  # If there isn't a log directory specified, the destination acts like it
    if arguments.exclusions:
        exclusions = list(chain(*arguments.exclusions))
    else:
        exclusions = None
    if arguments.only:
        only = list(chain(*arguments.only))
    else:
        only = None

    if len(arguments.paths) == 3:
        log_directory = arguments.paths[2]

    mirror_videos(source_directory, destination_directory, log_directory, exclusions, only, arguments.encoding_profile)


def exit_with_error():
    sys.exit(1)


@long_running
def process_command_line(argv):
    parser = ArgumentParser()
    parser.add_argument('-files', action='store_true')
    parser.add_argument('-mir', action='store_true')
    parser.add_argument('paths', nargs='*')
    parser.add_argument('-not', action='append', dest='exclusions', nargs='*')
    parser.add_argument('-only', action='append', nargs='*')
    parser.add_argument('-encoding-profile', choices=['video_passthrough', 'burn_in', '720p_burn_in', '720p'], default='video_passthrough')

    arguments = parser.parse_args(argv[1:])

    if arguments.files and arguments.mir:
        print("Can't pass both -files and -mir")
        exit_with_error()

    if arguments.mir:
        _mirror_mode(arguments)
    else:
        _files_mode(arguments)


if __name__ == "__main__":
    import sys
    process_command_line(sys.argv)
