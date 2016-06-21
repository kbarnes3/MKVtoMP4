from glob import glob
from os import remove
from os.path import exists, join

from control_flow import exit_with_error
from name_constants import *
from output import generate_output, generate_output_name


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


def create_log_file(log_file):
    if not exists(log_file):
        f = open(log_file, 'w')
        f.close()
