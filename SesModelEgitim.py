import threading

from PyQt5.QtWidgets import QApplication
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder

from Fonksiyon import *

class Egitim:
    def KaydiBaslat(self):
        try:
            self.BilgilendirmeKutusu.setText("Kayıt Başladı.")
            QApplication.processEvents()

            icerik = self.Ad.text()

            dosya_yolu = os.path.abspath(icerik)
            duzeltilmis_yol = dosya_yolu.replace("\\", "/")
            self.Adres.setText(duzeltilmis_yol)

            if (len(icerik) > 0):
                samplerate = 44100  # Ses örnekleme oranı
                duration = 20 # Kaydetme süresi (saniye)
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

                thread1 = threading.Thread(target=Egitim.Islemler(self))
                thread1.start()
            else:
                self.BilgilendirmeKutusu.setText("Değeri Giriniz")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def DosyadanSec(self):
        try:
            self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
            QApplication.processEvents()  # Arayüzün güncellenmesi sağlanıyor

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav)", options=options)

            self.Adres.setText(file_path)
            thread2 = threading.Thread(target=Egitim.Islemler(self))
            thread2.start()
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def Islemler(self):
        thread3 = threading.Thread(target=Egitim.SesiParçala(self))
        thread3.start()
        thread4 = threading.Thread(target=Egitim.ModelEgit(self))
        thread4.start()

    def SesiParçala(self):
        try:
            if len(self.Ad.text())>0:
                chunk_length_ms = 2 * 1000

                input_file = f"{self.Adres.text()}/kayit.wav"
                output_folder = f"ModelSes/{self.Ad.text()}"

                audio = AudioSegment.from_file(input_file)

                # Create the output folder if it doesn't exist
                os.makedirs(output_folder, exist_ok=True)

                # Calculate the total number of chunks
                total_chunks = len(audio) // chunk_length_ms

                # Split the audio into chunks
                for i in range(total_chunks):
                    start_time = i * chunk_length_ms
                    end_time = min((i + 1) * chunk_length_ms, len(audio))  # Limit end time to audio length
                    chunk = audio[start_time:end_time]

                    # Save the chunk
                    chunk_name = os.path.join(output_folder, f"chunk_{i + 1}.wav")
                    chunk.export(chunk_name, format="wav")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)

    def ModelEgit(self):
        try:
            data_path = "ModelSes/"
            model_path = "model.pkl"
            features, labels = [], []

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
                            self.BilgilendirmeKutusu.setText(f"Hata: {e} - {audio_path}")

            features = np.array(features)
            labels = np.array(labels)

            # Etiketleri encode et
            le = LabelEncoder()
            y_encoded = le.fit_transform(labels)

            # Modeli eğit
            model = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=500, activation='relu', solver='adam')
            model.fit(features, y_encoded)

            # Modeli ve etiketleri kaydet
            joblib.dump((model, le), model_path)
            self.BilgilendirmeKutusu.setText("Model Eğitimi Tamamlandı.")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)
