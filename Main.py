import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from Button import *
from TextArea import *
from Grafik import *
from MetinYerleri import *

class SesTanima(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SES TANIMA UYGULAMASI")
        self.setStyleSheet("background-color: #C0E0E0")
        self.setFixedSize(1200, 760)

        MetinYerleri.MetinYeri(self)
        Grafik.GrafikOlustur(self)
        ButonOlustur.Butonlar(self)
        MetinGirisiOlustur.MetinAlanlari(self)

        ShowHide.HepsiniGizle(self)
        ShowHide.Giris(self)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        SesTanimaSayfasi = SesTanima()
        SesTanimaSayfasi.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
