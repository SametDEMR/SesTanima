from PyQt5.QtWidgets import QWidget
import threading
from Fonksiyon import *
from GrafikCizme import *
from ShowHide import *

class Islemler(QWidget):
    def Thread(self):
        # İşlemleri ayrı iş parçacığında çalıştır
        try:
            ShowHide.HepsiniGizle(self)
            ShowHide.CiktiKismi(self)
            thread = threading.Thread(target=Islemler.Islemler(self))
            thread.start()
        except Exception as e:
            print(e)

    def Islemler(self):
        # Ana işlem fonksiyonu
        ButtonName = Fonksiyon.TiklananButonAlma(self)
        FilePath = Fonksiyon.SesleriAlma(self, ButtonName)

        if FilePath:
            FilePath = Fonksiyon.SesDönüstür(FilePath)
            Fonksiyon.SestenMetinYapma(self, FilePath)
            Fonksiyon.KonuBulma(self)
            deneme = Fonksiyon.SesleriAnalizEtme(self, ButtonName, FilePath)

            if deneme == 1:
                self.BilgilendirmeKutusu.setText("Model Tekrar Eğitildi. Analiz Tekrar Yapılıyor.")
                deneme = Fonksiyon.SesleriAnalizEtme(self, ButtonName, FilePath)

            GrafikCizme.GrafikCiz(self, FilePath, deneme)
            Fonksiyon.MetindenDuyguBulma(self)
        else:
            ShowHide.HepsiniGizle(self)
            ShowHide.Giris(self)
