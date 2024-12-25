import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import locale

from GrafikCizme import *

class ShowHide(QWidget):
    # Tüm bileşenleri gizleyen fonksiyon
    def HepsiniGizle(self):
        self.GeriButton.hide()
        self.MikrofonSesButton.hide()
        self.DosyadanSesButton.hide()

        self.SesEkleme.hide()
        self.SesSecme.hide()

        self.BilgilendirmeKutusu.hide()
        self.DuyguDurumu.hide()
        self.KacKelimeVar.hide()
        self.Konu.hide()

        self.Ad.hide()
        self.Adres.hide()
        self.KaydiBaslat.hide()

        self.canvas1.hide()
        self.canvas2.hide()
        self.canvas3.hide()

    # Giriş ekranındaki bileşenleri gösteren fonksiyon
    def Giris(self):
        self.MikrofonSesButton.show()
        self.DosyadanSesButton.show()

        self.SesEkleme.show()

    # Çıktı ekranındaki bileşenleri gösteren fonksiyon
    def CiktiKismi(self):
        self.ax3.axis('off')
        self.GeriButton.show()
        self.BilgilendirmeKutusu.show()
        self.DuyguDurumu.show()
        self.KacKelimeVar.show()
        self.Konu.show()
        self.canvas1.show()
        self.canvas2.show()
        self.canvas3.show()


    # Geri tuşuna basıldığında bileşenleri temizleyen ve giriş ekranına döndüren fonksiyon
    def Geri(self):
        GrafikCizme.GrafikTemizleme(self)
        ShowHide.HepsiniGizle(self)
        ShowHide.Giris(self)

    def ModeleSesEkleme(self):
        ShowHide.HepsiniGizle(self)

        self.GeriButton.show()
        self.Ad.show()
        self.Adres.show()
        self.KaydiBaslat.show()
        self.SesSecme.show()