from argparse import ArgumentParser
from itertools import chain

from control_flow import exit_with_error
from files import convert_videos
from mirror import mirror_videos
from powermanagement import long_running
from output import convert_video, generate_output_name


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
