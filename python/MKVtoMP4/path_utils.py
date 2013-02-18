from os.path import basename, join

_mkvExtension = '.mkv'
_mp4Extension = '.mp4'


def hello_world(input_file, output_path):
    filename = basename(input_file)
    # Strip the extension if it is .mkv
    if filename.endswith(_mkvExtension):
        filename = filename[:-len(_mkvExtension)]

    filename += _mp4Extension
    output_file = join(output_path, filename)

    print(output_file)

