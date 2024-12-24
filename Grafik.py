import sys
import librosa
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPalette, QColor
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import Counter

class Grafik(QWidget):
    def GrafikOlustur(self):
        # İlk grafik için FigureCanvas oluştur
        self.figure1 = plt.Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setGeometry(20, 60, 1000, 240)  # İlk canvas boyutu ve konumu
        self.canvas1.setParent(self)  # Canvas'ı ana pencereye ekle
        self.canvas1.show()

        # İkinci grafik için FigureCanvas oluştur
        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setGeometry(20, 320, 1000, 240)  # İkinci canvas boyutu ve konumu
        self.canvas2.setParent(self)  # Canvas'ı ana pencereye ekle
        self.canvas2.show()

        # Pasta grafiği için FigureCanvas oluştur
        self.figure3 = plt.Figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.canvas3.setGeometry(960, 60, 240, 240)  # Pasta grafiği boyutu ve konumu
        self.canvas3.setParent(self)  # Canvas'ı ana pencereye ekle
        self.canvas3.show()

        # İlk başta grafik alanlarını temizle
        self.ax1 = self.figure1.add_subplot(111)  # İlk canvas için ilk subplot
        self.ax2 = self.figure2.add_subplot(111)  # İkinci canvas için ikinci subplot
        self.ax3 = self.figure3.add_subplot(111)  # Üçüncü canvas için ilk (ve tek) subplot

        # Renk ayarı
        self.figure1.patch.set_facecolor('#C0E0E0')
        self.figure2.patch.set_facecolor('#C0E0E0')
        self.figure3.patch.set_facecolor('#C0E0E0')

        # Grafik içi renk ayarı
        self.ax1.set_facecolor('#C0E0E0')
        self.ax2.set_facecolor('#C0E0E0')
        self.ax3.set_facecolor('#C0E0E0')

        self.ax3.axis('off')