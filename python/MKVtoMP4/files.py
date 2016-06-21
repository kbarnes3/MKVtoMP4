from glob import glob

from output import convert_video, generate_output_name


def convert_videos(input_patterns, destination_directory, encoding_profile):
    for input_pattern in input_patterns:
        files = glob(input_pattern)

        if len(files) == 0:
            print('Warning: No files found matching ' + input_pattern)

        for input_file in files:
            output_file = generate_output_name(input_file, destination_directory)
            convert_video(input_file, output_file, encoding_profile)
