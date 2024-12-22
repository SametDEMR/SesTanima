import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from ShowHide import *
from Button import *
from TextArea import *
from Grafik import *

class SesTanima(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SES TANIMA, SESTEN DUYGU ANALİZİ, KONUŞULAN KONU TAHMİNLEME UYGULAMASI")
        self.setStyleSheet("background-color: #C0E0E0")
        self.setFixedSize(1200, 760)

        MetinYerleri.MetinYeri(self)
        Grafik.GrafikOlustur(self)
        ButonOlustur.Butonlar(self)
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
