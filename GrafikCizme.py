from collections import Counter

import librosa
import numpy as np

from TextArea import *

class GrafikCizme():
    def GrafikCiz(self, file_path, predictions):
        try:
            # Ses dosyasını yükle
            y, sr = librosa.load(file_path)

            # Ses dalgasını çiz
            librosa.display.waveshow(y, sr=sr, ax=self.ax1)
            self.ax1.set_title('Dalga Formu')
            self.ax1.set_ylabel('Amplitüd')

            # Spektrogram hesapla ve çiz
            D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log', cmap='viridis', ax=self.ax2)
            self.ax2.set_title('Spektrogram')
            self.ax2.set_ylabel('Frekans (log)')
            self.figure2.colorbar(self.ax2.collections[0], ax=self.ax2, format='%+2.0f dB')

            # Çizimleri güncelle
            self.canvas1.draw()
            self.canvas2.draw()

            # Tahminlerin dağılımını hesapla
            eleman_sayilari = Counter(predictions)
            adlar = list(eleman_sayilari.keys())
            sayılar = list(eleman_sayilari.values())

            # Pasta grafiği çiz
            ax = self.figure3.add_subplot(111)
            ax.clear()
            ax.pie(sayılar, labels=adlar, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            self.canvas3.draw()
        except Exception as e:
            # Hata mesajını göster
            print(e)

    def GrafikTemizleme(self):
        try:
            # Bilgi alanlarını temizle
            self.BilgilendirmeKutusu.setText("")
            self.DuyguDurumu.setText("")
            self.KacKelimeVar.setText("")
            self.Konu.setText("")

            # Grafiklerin içeriğini temizle
            self.figure1.clear()
            self.figure2.clear()
            self.figure3.clear()

            # Yeni grafik alanları oluştur
            self.ax1 = self.figure1.add_subplot(111)
            self.ax2 = self.figure2.add_subplot(111)
            self.ax3 = self.figure3.add_subplot(111)

            # Arka plan rengini ayarla
            self.ax1.set_facecolor('#C0E0E0')
            self.ax2.set_facecolor('#C0E0E0')
            self.ax3.set_facecolor('#C0E0E0')

            # Çizimleri güncelle
            self.canvas1.draw()
            self.canvas2.draw()
            self.canvas3.draw()
        except Exception as e:
            # Hata mesajını göster
            print(e)
