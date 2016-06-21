from os import listdir, remove
from os.path import exists, join

from output import generate_output, generate_output_name


def process_queue(source_directory, destination_directory, queue_directory, encoding_profile):
    queue = listdir(queue_directory)
    for queued_name in queue:
        source_file = join(source_directory, queued_name)
        if exists(source_file):
            destination_file = generate_output_name(source_file, destination_directory)
            generate_output(source_file, destination_file, encoding_profile)
            queued_file = join(queue_directory, queued_name)
            remove(queued_file)
        else:
            print("Warning: {0} does not exist".format(source_file))
