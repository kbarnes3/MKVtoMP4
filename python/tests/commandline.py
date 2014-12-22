import unittest
from mock import patch

import MKVtoMP4


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('MKVtoMP4.exit_with_error')
    @patch('MKVtoMP4.print_usage')
    def test_no_arguments(self, mock_print_usage, mock_exit_with_error):
        MKVtoMP4.process_command_line(['MKVtoMP4.py'])
        self.assertTrue(mock_print_usage.called)
        self.assertTrue(mock_exit_with_error.called)

    @patch('MKVtoMP4.convert_videos')
    def test_convert_single_wildcard(self, mock_convert_videos):

        MKVtoMP4.process_command_line([
            'MKVtoMP4.py',
            'C:\\Input Videos\\*.mkv',
            'D:\\Output Videos',
        ])

        mock_convert_videos.assert_called_with(['C:\\Input Videos\\*.mkv'], 'D:\\Output Videos')
