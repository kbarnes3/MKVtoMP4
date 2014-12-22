import unittest
from mock import Mock

import MKVtoMP4


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        MKVtoMP4.exit_with_error = Mock()
        MKVtoMP4.print_usage = Mock()

    def tearDown(self):
        pass

    def test_no_arguments(self):
        MKVtoMP4.process_command_line(['MKVtoMP4.py'])
        self.assertTrue(MKVtoMP4.print_usage.called)
        self.assertTrue(MKVtoMP4.exit_with_error.called)
