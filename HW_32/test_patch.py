# -*- coding: utf-8 -*-
import unittest
import os
import mock


class TestOS(unittest.TestCase):
    @mock.patch('os.urandom', side_effect=lambda l: 'f' * l)
    def test_urandom(self, urandom_function):
        self.assertEqual(os.urandom(5), 'fffff')

    @mock.patch('os.listdir', return_value=['.', '..', 'settings.json'])
    def test_listdir(self, listdir_function=None):
        self.assertIn('settings.json', os.listdir('./'))
