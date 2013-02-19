from glob import glob
from os.path import basename, join
from subprocess import call

_mkvExtension = '.mkv'
_mp4Extension = '.mp4'


def convert_videos(input_pattern, output_path):
    files = glob(input_pattern)

    for file in files:
        filename = basename(file)
        # Strip the extension if it is .mkv
        if filename.endswith(_mkvExtension):
            filename = filename[:-len(_mkvExtension)]

        filename += _mp4Extension
        output_file = join(output_path, filename)

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
    convert_videos(sys.argv[1], sys.argv[2])
