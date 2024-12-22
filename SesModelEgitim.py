import os
import joblib
import librosa
import pandas as pd
import soundfile as sf
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

from Islemler import *
from Fonksiyon import *

class Egitim():
    def SesModelEgitim(self, file_path):
        try:
            # "Sesler" ana klasörünü oluşturma
            base_dir = "Sesler"
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

            # Yeni klasör oluşturma işlemi için temel dizin adı
            save_dir = os.path.join(base_dir, "kisi")
            original_dir = save_dir
            counter = 1

            # Aynı isimde bir klasör varsa, benzersiz bir isim oluştur
            while os.path.exists(save_dir):
                save_dir = f"{original_dir}_{counter}"
                counter += 1

            # Klasörü oluştur
            os.makedirs(save_dir)

            # Ses dosyasını yükle ve 2 saniyelik segmentlere böl
            y, sr = librosa.load(file_path)  # Ses dosyasını yükle
            duration = librosa.get_duration(y=y, sr=sr)  # Ses dosyasının süresini al
            segment_length = 2  # Segment uzunluğu (saniye cinsinden)

            part_index = 1
            for start in range(0, int(duration), segment_length):
                end = min(start + segment_length, int(duration))  # Son segmentin sınırını kontrol et
                segment = y[start * sr: end * sr]  # Belirtilen aralığı kes
                part_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_part_{part_index}.wav"
                part_file_path = os.path.join(save_dir, part_file_name)
                sf.write(part_file_path, segment, sr)  # Kesiti WAV dosyası olarak kaydet
                part_index += 1

            # "Sesler" klasöründeki alt klasörleri tarayarak veri seti oluştur
            data_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
            labels = []  # Etiketler (klasör isimleri)
            features = []  # Özellikler (MFCC değerleri)

            for directory in data_dirs:
                folder_path = os.path.join(base_dir, directory)
                for file in os.listdir(folder_path):
                    if file.endswith(".wav"):
                        file_path = os.path.join(folder_path, file)
                        label = directory  # Klasör adını etiket olarak al
                        features.append(Egitim.OzellikCikarma(self, file_path))  # Özellik çıkar
                        labels.append(label)

            # Özellik ve etiketlerden oluşan veri setini hazırlama
            X = np.array(features)  # Özellikleri numpy dizisine çevir
            y = np.array(labels)  # Etiketleri numpy dizisine çevir

            # Veri setini DataFrame olarak oluştur ve CSV dosyasına kaydet
            data_df = pd.DataFrame(X)
            data_df['label'] = y
            data_csv_file = "veriseti.csv"
            data_df.to_csv(data_csv_file, index=False)

            # SVM modelini oluştur ve eğit
            model = SVC(kernel='linear', C=1.0, gamma='scale', random_state=42)
            model.fit(X, y)  # Modeli eğit

            # Eğitilen modeli dosyaya kaydet
            model_file_name = "SVM_linear_model.pkl"
            joblib.dump(model, model_file_name)

            # İşlem başarılı olduğunda 1 döndür
            okey = 1
            return okey

        except Exception as e:
            # Hata durumunda hatayı ekrana yazdır
            print("1")
            print(e)

    # Özellik çıkarma fonksiyonu (MFCC değerlerini hesaplar)
    def OzellikCikarma(self, file_path):
        # Ses dosyasını yükle (15 saniyelik kısmı işle)
        y, sr = librosa.load(file_path, duration=15)

        # MFCC özelliklerini hesapla ve ortalama değerini al
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
        return mfccs
