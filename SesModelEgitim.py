from PyQt5.QtWidgets import QFileDialog, QApplication
from pydub import AudioSegment  # Pydub modülü ekleniyor
import os
import librosa
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import joblib
import sounddevice as sd
from scipy.io.wavfile import write

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import make_chunks
import os


import os
import librosa
import numpy as np
import pandas as pd  # Veri setini CSV olarak kaydetmek için pandas eklendi
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import joblib

import os
import librosa
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

from Fonksiyon import *

class Egitim:
    def KaydiBaslat(self):
        try:
            icerik = self.Ad.text()

            dosya_yolu = os.path.abspath(icerik)
            duzeltilmis_yol = dosya_yolu.replace("\\", "/")
            self.Adres.setText(duzeltilmis_yol)
            print(icerik)

            if (len(icerik) > 0):
                samplerate = 44100  # Ses örnekleme oranı
                duration = 15 # Kaydetme süresi (saniye)
                directory = icerik  # Klasör adı
                file_name = 'kayit.wav'  # Dosya adı

                # Klasör oluşturma (varsa mevcut klasörü korur)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Dosya yolunu oluştur
                file_path = os.path.join(directory, file_name)

                # Mikrofon üzerinden ses kaydı yapılıyor
                recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                sd.wait()  # Kaydın tamamlanmasını bekliyor

                # Kaydedilen ses dosyası belirtilen formata dönüştürülüp kaydediliyor
                write(file_path, samplerate, (recorded_audio * 32767).astype(np.int16))
                print(f"Ses kaydı başarıyla kaydedildi: {file_path}")
                
                Egitim.SesiParçala(self)
            else:
                print("değer gir")
        except Exception as e:
            print(e)

    def DosyadanSec(self):
        self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
        QApplication.processEvents()  # Arayüzün güncellenmesi sağlanıyor

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav)", options=options)

        self.Adres.setText(file_path)
        Egitim.SesiParçala(self)

    def SesiParçala(self):
        try:
            if len(self.Ad.text())>0:
                chunk_length_ms = 5 * 1000

                input_file = self.Adres.text()
                output_folder = f"/ModelSes/{self.Ad.text()}"
                # Ses dosyasını yükle
                audio = AudioSegment.from_file(input_file)

                # Çıktı klasörünü oluştur
                os.makedirs(output_folder, exist_ok=True)

                # Ses dosyasını belirli uzunluklarda parçalara ayır
                split_chunks = make_chunks(audio, chunk_length_ms)

                # Her bir parçayı kaydet
                for i, chunk in enumerate(split_chunks):
                    chunk_name = os.path.join(output_folder, f"chunk_{i + 1}.wav")
                    chunk.export(chunk_name, format="wav")
                    if (i == 40):
                        return

                print("Dosya kaydedildi. model eğitiliyor.")

                Egitim.ModelEgit(self)
        except Exception as e:
            print(e)
    def ModelEgit(self):
        try:
            data_path = "ModelSes/"
            model_path = "model.pkl"
            features, labels = [], []
            print("Veri seti işleniyor...")

            # Veri setini yükle ve özellik çıkar
            for person_folder in os.listdir(data_path):
                person_path = os.path.join(data_path, person_folder)
                if os.path.isdir(person_path):
                    for audio_file in os.listdir(person_path):
                        audio_path = os.path.join(person_path, audio_file)
                        try:
                            y, sr = librosa.load(audio_path, duration=2.5, offset=0.6)
                            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
                            feature = np.mean(mfcc.T, axis=0)
                            features.append(feature)
                            labels.append(person_folder)
                        except Exception as e:
                            print(f"Hata: {e} - {audio_path}")

            features = np.array(features)
            labels = np.array(labels)

            # Etiketleri encode et
            print("Etiketler encode ediliyor...")
            le = LabelEncoder()
            y_encoded = le.fit_transform(labels)

            # Modeli eğit
            print("Model eğitiliyor...")
            model = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=500, activation='relu', solver='adam')
            model.fit(features, y_encoded)

            # Modeli ve etiketleri kaydet
            print("Model kaydediliyor...")
            joblib.dump((model, le), model_path)
            print("Model başarıyla eğitildi ve kaydedildi.")
        except Exception as e:
            print(e)
