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
            self.BilgilendirmeKutusu.setText(e)

    def Islemler(self):
        try:
            # Ana işlem fonksiyonu
            ButtonName = Fonksiyon.TiklananButonAlma(self)
            FilePath = Fonksiyon.SesleriAlma(self, ButtonName)

            self.setEnabled(False)
            if FilePath:
                FilePath = Fonksiyon.SesDönüstür(self, FilePath)

                thread1 = threading.Thread(target=Fonksiyon.SestenMetinYapma(self, FilePath))
                thread1.start()

                thread2 = threading.Thread(target=Fonksiyon.KonuBulma(self))
                thread2.start()

                thread3 = threading.Thread(target=Fonksiyon.MetindenDuyguBulma(self))
                thread3.start()

                deneme = Fonksiyon.SesleriAnalizEtme(self, ButtonName, FilePath)
                if deneme == "okey":
                    self.BilgilendirmeKutusu.setText("Model Tekrar Eğitildi. Analiz Tekrar Yapılıyor.")
                    QApplication.processEvents()
                    deneme = Fonksiyon.SesleriAnalizEtme(self, ButtonName, FilePath)

                thread6 = threading.Thread(target=GrafikCizme.GrafikCiz(self, FilePath, deneme))
                thread6.start()

            else:
                ShowHide.HepsiniGizle(self)
                ShowHide.Giris(self)
            self.setEnabled(True)
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)