import unittest
from commandline import TestCommandLine


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTests([TestCommandLine])
    return test_suite
