from os.path import basename, join
import shutil
from subprocess import call

from .control_flow import exit_with_error
from .name_constants import *


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
            '[0:v][0:s]overlay,scale=w=min(1280\,iw):h=min(720\,ih):force_original_aspect_ratio=decrease,'
            'scale=w=trunc(iw/2)*2:h=trunc(ih/2)*2[scaled]',
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
            '[0:v]scale=w=min(1280\,iw):h=min(720\,ih):force_original_aspect_ratio=decrease,'
            'scale=w=trunc(iw/2)*2:h=trunc(ih/2)*2[scaled]',
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
        call_parameters = None
        print('Unknown encoding profile: {0}'.format(encoding_profile))
        exit_with_error()

    call(call_parameters)
