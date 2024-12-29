import unittest
from Main import SesTanima
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from unittest.mock import patch
import sys

class TestSesTanima(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.window = SesTanima()
        self.window.show()

    def tearDown(self):
        self.window.close()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit()

    def test_main_window1(self):
        def mock_get_open_file_name(*args, **kwargs):
            return "samet.wav", None

        with patch.object(QFileDialog, 'getOpenFileName', side_effect=mock_get_open_file_name):
            QTest.mouseClick(self.window.DosyadanSesButton, Qt.LeftButton)
        print("Test1 tamamlandı.")

    def test_main_window2(self):
        def mock_get_open_file_name(*args, **kwargs):
            return "samet.mp3", None

        with patch.object(QFileDialog, 'getOpenFileName', side_effect=mock_get_open_file_name):
            QTest.mouseClick(self.window.DosyadanSesButton, Qt.LeftButton)
        print("Test2 tamamlandı.")

    def test_main_window_cancel(self):
        def mock_get_open_file_name(*args, **kwargs):
            return "", None

        with patch.object(QFileDialog, 'getOpenFileName', side_effect=mock_get_open_file_name):
            QTest.mouseClick(self.window.DosyadanSesButton, Qt.LeftButton)
        print("Test Cancel tamamlandı.")

if __name__ == "__main__":
    unittest.main()
