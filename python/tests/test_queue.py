from unittest.mock import call, patch

import MKVtoMP4.queue


basic_mkvs = [
    'Foo.S01E04.mkv',
    'Foo.S01E05.mkv',
    'Bar.S01E04.mkv',
    'Bar.S02E04.mkv',
]


def create_directory(tmpdir, name, file_names):
    directory = tmpdir.mkdir(name)
    for file_name in file_names:
        file = directory.join(file_name)
        file.write(None)

    assert len(directory.listdir()) == len(file_names)
    return directory


def create_empty_directory(tmpdir, name):
    return create_directory(tmpdir, name, [])


def create_basic_source_directory(tmpdir):
    return create_directory(tmpdir, 'source', basic_mkvs)


def create_empty_destination_directory(tmpdir):
    return create_empty_directory(tmpdir, 'destination')


def create_empty_queue_directory(tmpdir):
    return create_empty_directory(tmpdir, 'queue')


@patch('MKVtoMP4.queue.generate_output')
def test_empty_queue(mock_generate_output, tmpdir):
    source_directory = create_basic_source_directory(tmpdir)
    destination_directory = create_empty_destination_directory(tmpdir)
    queue_directory = create_empty_queue_directory(tmpdir)
    original_source_len = len(source_directory.listdir())

    MKVtoMP4.queue.process_queue(str(source_directory),
                           str(destination_directory),
                           str(queue_directory),
                           'video_passthrough')

    mock_generate_output.assert_not_called()
    assert len(source_directory.listdir()) == original_source_len
    assert len(destination_directory.listdir()) == 0
    assert len(queue_directory.listdir()) == 0


@patch('MKVtoMP4.queue.generate_output')
def test_complete_queue(mock_generate_output, tmpdir):
    source_directory = create_basic_source_directory(tmpdir)
    destination_directory = create_empty_destination_directory(tmpdir)
    file_name1 = 'Foo.S01E04.mkv'
    output_name1 = 'Foo.S01E04.mp4'
    file_name2 = 'Bar.S01E04.mkv'
    output_name2 = 'Bar.S01E04.mp4'
    queue_directory = create_directory(tmpdir, 'queue', [file_name1, file_name2])
    original_source_len = len(source_directory.listdir())

    source_name1 = str(source_directory.join(file_name1))
    destination_name1 = str(destination_directory.join(output_name1))
    source_name2 = str(source_directory.join(file_name2))
    destination_name2 = str(destination_directory.join(output_name2))

    MKVtoMP4.queue.process_queue(str(source_directory),
                           str(destination_directory),
                           str(queue_directory),
                           'video_passthrough')

    call1 = call(source_name1, destination_name1, 'video_passthrough')
    call2 = call(source_name2, destination_name2, 'video_passthrough')
    calls = [call1, call2]

    mock_generate_output.assert_has_calls(calls, any_order=True)

    assert len(source_directory.listdir()) == original_source_len
    assert len(destination_directory.listdir()) == 0
    assert len(queue_directory.listdir()) == 0


@patch('MKVtoMP4.queue.generate_output')
def test_partial_queue(mock_generate_output, tmpdir):
    source_directory = create_basic_source_directory(tmpdir)
    destination_directory = create_empty_destination_directory(tmpdir)
    file_name1 = 'Something.S01E04.mkv'
    file_name2 = 'Bar.S01E04.mkv'
    output_name2 = 'Bar.S01E04.mp4'
    queue_directory = create_directory(tmpdir, 'queue', [file_name1, file_name2])
    original_source_len = len(source_directory.listdir())

    source_name2 = str(source_directory.join(file_name2))
    destination_name2 = str(destination_directory.join(output_name2))

    MKVtoMP4.queue.process_queue(str(source_directory),
                           str(destination_directory),
                           str(queue_directory),
                           'video_passthrough')

    mock_generate_output.assert_called_once_with(source_name2, destination_name2, 'video_passthrough')

    assert len(source_directory.listdir()) == original_source_len
    assert len(destination_directory.listdir()) == 0
    assert queue_directory.join(file_name1).check(file=1)
    assert len(queue_directory.listdir()) == 1
