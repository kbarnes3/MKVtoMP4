import unittest
from mock import patch

import MKVtoMP4


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('MKVtoMP4.convert_videos')
    def test_convert_single_wildcard(self, mock_convert_videos):
        MKVtoMP4.process_command_line([
            'MKVtoMP4.py',
            'C:\\Input Videos\\*.mkv',
            'D:\\Output Videos',
        ])

        mock_convert_videos.assert_called_with(['C:\\Input Videos\\*.mkv'], 'D:\\Output Videos', 'video_passthrough')

    @patch('MKVtoMP4.convert_videos')
    def test_convert_multiple_files(self, mock_convert_videos):
        MKVtoMP4.process_command_line([
            'MKVtoMP4.py',
            'C:\\Input Videos\\Foo.S01E04.mkv',
            'C:\\Input Videos\\Foo.S01E05.mkv',
            'D:\\Output Videos',
        ])

        mock_convert_videos.assert_called_with(['C:\\Input Videos\\Foo.S01E04.mkv', 'C:\\Input Videos\\Foo.S01E05.mkv'],
                                               'D:\\Output Videos', 'video_passthrough')

    @patch('MKVtoMP4.mirror_videos')
    def test_mirror_videos(self, mock_mirror_videos):
        MKVtoMP4.process_command_line(([
            'MKVtoMP4.py',
            '-mir',
            'C:\\Input Videos',
            'D:\\Output Videos',
        ]))

        mock_mirror_videos.assert_called_with('C:\\Input Videos', 'D:\\Output Videos', 'D:\\Output Videos', None, None,
                                              'video_passthrough')

    @patch('MKVtoMP4.mirror_videos')
    def test_mirror_videos_exclusions(self, mock_mirror_videos):
        MKVtoMP4.process_command_line(([
            'MKVtoMP4.py',
            '-mir',
            'C:\\Input Stuff',
            'D:\\Mirror',
            '-not',
            'Boring*',
            '-not',
            'Slow*',
            '-not',
            'Long*',
        ]))

        mock_mirror_videos.assert_called_with('C:\\Input Stuff', 'D:\\Mirror', 'D:\\Mirror', [
            'Boring*', 'Slow*', 'Long*',
        ], None, 'video_passthrough')

    @patch('MKVtoMP4.mirror_videos')
    def test_mirror_videos_log_only(self, mock_mirror_videos):
        MKVtoMP4.process_command_line(([
            'MKVtoMP4.py',
            '-mir',
            'C:\\Input',
            'D:\\Output',
            'E:\\Logs',
            '-only',
            'Interesting*',
            '-only',
            'Fast*',
            '-only',
            'Short*',
        ]))

        mock_mirror_videos.assert_called_with('C:\\Input', 'D:\\Output', 'E:\\Logs', None, [
            'Interesting*', 'Fast*', 'Short*',
        ], 'video_passthrough')

    @patch('MKVtoMP4.mirror_videos')
    def test_mirror_videos_burn_in(self, mock_mirror_videos):
        MKVtoMP4.process_command_line(([
            'MKVtoMP4.py',
            '-mir',
            'C:\\Input Videos',
            'D:\\Output Videos',
            '-encoding-profile',
            'burn_in',
        ]))

        mock_mirror_videos.assert_called_with('C:\\Input Videos', 'D:\\Output Videos', 'D:\\Output Videos', None, None,
                                              'burn_in')

    @patch('MKVtoMP4.mirror_videos')
    def test_mirror_videos_720p_burn_in(self, mock_mirror_videos):
        MKVtoMP4.process_command_line(([
            'MKVtoMP4.py',
            '-mir',
            'C:\\Input Videos',
            'D:\\Output Videos',
            '-encoding-profile',
            '720p_burn_in',
        ]))

        mock_mirror_videos.assert_called_with('C:\\Input Videos', 'D:\\Output Videos', 'D:\\Output Videos', None, None,
                                              '720p_burn_in')
