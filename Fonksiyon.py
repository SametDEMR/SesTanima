from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pydub import AudioSegment
import speech_recognition as Sr
import joblib
import librosa
from deep_translator import GoogleTranslator
import spacy
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')




from SesModelEgitim import *

class Fonksiyon(QWidget):
    def TiklananButonAlma(self):
        #TIKLANAN BUTONU ALMA
        clicked_button = self.sender()
        button_name = clicked_button.objectName()
        return button_name



    def SesleriAlma(self, button_name):
        try:
            file_path = None
            # Dosyadan ses almak için işlem başlatılıyor
            if button_name == "DosyadanSesButton":
                self.BilgilendirmeKutusu.setText("Lütfen Bekleyiniz, Ses Dosyası Alınıyor...")
                QApplication.processEvents()  # Arayüzün güncellenmesi sağlanıyor

                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getOpenFileName(
                    self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.wav *.mp3)", options=options
                )

            # Mikrofondan ses almak için işlem başlatılıyor
            elif button_name == "MikrofonSesButton":
                self.BilgilendirmeKutusu.setText("Ses Kaydediliyor. Lütfen Bekleyiniz...")
                QApplication.processEvents()  # Arayüzün güncellenmesi sağlanıyor

                samplerate = 44100  # Ses örnekleme oranı
                duration = 10  # Kaydetme süresi (saniye)
                file_path = 'kayit.wav'  # Kaydedilecek dosyanın adı ve formatı

                # Mikrofon üzerinden ses kaydı yapılıyor
                recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                sd.wait()  # Kaydın tamamlanmasını bekliyor

                # Kaydedilen ses dosyası belirtilen formata dönüştürülüp kaydediliyor
                write(file_path, samplerate, (recorded_audio * 32767).astype(np.int16))

            # Dosya yolunu kontrol etme işlemi
            if file_path:
                return file_path  # Dosya yolu döndürülüyor
            else:
                self.BilgilendirmeKutusu.setText("Dosya alınamadı.")
                return None

        except Exception as e:
            # Herhangi bir hata durumunda kullanıcı bilgilendiriliyor
            self.BilgilendirmeKutusu.setText(e)




    #SESİ UYGUN FORMATA DÖNÜŞTÜR VE KAYDET.
    def SesDönüstür(file_path):
        try:
            # Dosyanın uzantısını al ve küçük harfe çevir
            file_extension = os.path.splitext(file_path)[1].lower()

            # Eğer dosya zaten .wav uzantılıysa, olduğu gibi döndür
            if file_extension == ".wav":
                return file_path

            # Dosyayı belirtilen formata yükle
            audio = AudioSegment.from_file(file_path)

            # Başlangıç ve bitiş sürelerini milisaniye cinsinden tanımla
            start_time_ms = 0 * 1000  # Başlangıç zamanı (0 saniye)
            end_time_ms = start_time_ms + (10 * 1000)  # Bitiş zamanı (10 saniye)

            # Belirtilen süreye göre ses klibini kes
            clip = audio[start_time_ms:end_time_ms]

            # Yeni dosya yolunu .wav uzantısıyla ayarla
            file_path = os.path.splitext(file_path)[0] + ".wav"

            # Klipi .wav formatında dışa aktar
            clip.export(file_path, format="wav")

            # Yeni dosya yolunu döndür
            return file_path
        except Exception as e:
            # Hata durumunda hata mesajını yazdır ve None döndür
            print("Hata oluştu:", e)
            return None




    # SESİ APİ KULLANARAK METNE ÇEVİRME
    def SestenMetinYapma(self, file_path):
        recognizer = Sr.Recognizer()  # Ses tanıma için recognizer nesnesi oluşturuluyor
        try:
            # Ses dosyasını açıyoruz
            with Sr.AudioFile(file_path) as source:
                audio = recognizer.record(source)  # Ses dosyasını okuyup bir audio nesnesine dönüştürüyoruz

            # Google'ın API'si kullanılarak sesi metne çeviriyoruz
            metin = recognizer.recognize_google(audio, language='tr-TR')

            # Çıktı metnini bir dosyaya yazıyoruz
            with open("output.txt", "w", encoding="utf-8") as dosya:
                dosya.write(metin)

        # Ses anlaşılamazsa yapılacak işlem
        except Sr.UnknownValueError:
            with open("output.txt", "w", encoding="utf-8") as dosya:
                pass  # Eğer ses anlaşılmazsa boş bir dosya oluşturuluyor

        # API'den cevap alınamadığında yapılacak işlem
        except Sr.RequestError as e:
            self.BilgilendirmeKutusu.setText(f"Google API'den yanıt alınamadı; {e}")  # Hata mesajı gösteriliyor

        # Diğer hataları yakalama ve ekrana yazdırma
        except Exception as e:
            print("2")
            print(e)  # Hata mesajı konsola yazdırılıyor



    # SES TANIMA KISMINI BAŞLATAN FONKSİYON
    def SesleriAnalizEtme(self, button_name, file_path):
        try:
            # "output.txt" dosyasını aç ve içeriği oku
            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read().strip()  # Dosya içeriğini okuyup boşlukları temizle

            # Eğer dosya içeriği boş ise
            if len(metin) == 0:
                # Eğer buton "DosyadanSesButton" ise uygun mesaj göster
                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses Dosyasının İçeriği Boştur.")
                # Eğer buton "MikrofonSesButton" ise uygun mesaj göster
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Konuşma bulunmamaktadır.")
            else:
                # Sesin kime ait olduğunu belirlemek için ilgili fonksiyonu çağır
                Predictions = Fonksiyon.SesinKimeAitOlduğunuBulma(self, file_path)
                # Toplam kelime sayısını ekrana yazdır
                self.KacKelimeVar.setText(f"Toplam Sayılan Kelime Sayısı: {len(metin)}")

                # Butona göre bilgilendirme mesajını güncelle
                if button_name == "DosyadanSesButton":
                    self.BilgilendirmeKutusu.setText("Ses dosyasından ses tanıma tamamlandı.")
                elif button_name == "MikrofonSesButton":
                    self.BilgilendirmeKutusu.setText("Mikrofondan ses tanıma tamamlandı.")

                # Tahminleri döndür
                return Predictions
        except Exception as e:
            # Hata durumunda hatayı konsola yazdır
            print(e)
            print("3")



    # Sesin kime ait olduğunu bulma fonksiyonu
    def SesinKimeAitOlduğunuBulma(self, file_path):
        try:
            # Daha önce eğitilmiş SVM modeli yükleniyor
            model = joblib.load("SVM_linear_model.pkl")

            # Ses dosyasını yükle
            y, sr = librosa.load(file_path, sr=None)

            # 1 saniyelik segment uzunluğunu belirle (örnekleme frekansı kadar)
            segment_length = sr

            # Sonuçları saklamak için bir liste oluşturuluyor
            predictions = []

            # Sesi 1 saniyelik segmentlere böl ve her bir segmenti işle
            for i in range(0, len(y) // segment_length):
                start_sample = i * segment_length  # Segmentin başlangıç noktası
                end_sample = start_sample + segment_length  # Segmentin bitiş noktası

                # Eğer segmentin bitişi toplam uzunluğu aşarsa, segmenti sınırla
                if end_sample > len(y):
                    end_sample = len(y)

                # Segmenti al
                segment = y[start_sample:end_sample]

                # MFCC (Mel Frekans Kepstral Katsayıları) hesapla
                mfccs = np.mean(librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=13).T, axis=0)
                features = mfccs.reshape(1, -1)  # Özellikleri modelin kabul edeceği şekle getir

                # Model ile tahmin yap
                prediction = model.predict(features)
                predictions.append(prediction[0])  # Tahmin edilen sınıfı listeye ekle
                probabilities = model.decision_function(features)  # Tahmin olasılıklarını al

                # Eğer olasılık değeri belirli bir eşik değerin altındaysa
                if np.all(probabilities < 2.21):
                    # Ses eğitim fonksiyonuna yönlendirilir
                    okey = Egitim.SesModelEgitim(self, file_path)
                    return okey  # Eğitim sonucunu döndür
                else:
                    # Aksi durumda tahminleri döndür
                    return predictions
        except Exception as e:
            # Hata durumunda hatayı yazdır
            print(e)
            print("4")

    #METNE DÖNÜŞMÜŞ SESİN HAZIR KÜTÜPHANE KULLANARAK DUYGUSUNU BULMA
    def MetindenDuyguBulma(self):
        try:
            # "output.txt" dosyasını okuma işlemi
            with open("output.txt", "r", encoding="utf-8") as dosya:
                metin = dosya.read().strip()  # Dosyadaki metni okuyup baştaki ve sondaki boşlukları temizliyoruz

            # Eğer dosyada metin yoksa (boşsa) nötr duygu durumunu gösteriyoruz
            if not metin:
                self.DuyguDurumu.setText("Konuşan Kişinin Duygu Durumu: NÖTR")
                return

            try:
                # Metni Türkçeden İngilizceye çeviriyoruz
                ceviri_metni = GoogleTranslator(source='tr', target='en').translate(metin)

                # Çevrilen metin üzerinde duygu analizi yapıyoruz
                analyzer = SentimentIntensityAnalyzer()
                duygu = analyzer.polarity_scores(ceviri_metni)

                # Compound skora göre mutluluk ve mutsuzluk yüzdelerini hesaplıyoruz
                if duygu['compound'] < 0:
                    mutluluk = 0
                    mutsuzluk = 100
                else:
                    mutluluk = duygu['compound'] * 100
                    mutsuzluk = (1 - duygu['compound']) * 100

                # Hesaplanan değerleri kullanıcıya gösteriyoruz
                self.DuyguDurumu.setText(f"Metin: %{mutluluk:.2f} Mutlu %{mutsuzluk:.2f} Mutsuz")
            except Exception as e:
                # Herhangi bir hata oluşursa hatayı kullanıcıya gösteriyoruz
                self.DuyguDurumu.setText(f"Bir hata oluştu: {e}")
        except Exception as e:
            # Dosya okuma veya başka bir genel hata durumunda hatayı konsola yazdırıyoruz
            print(e)
            print("5")



    # METNE DÖNÜŞMÜŞ SESİN KONUSUNU BULMA
    def KonuBulma(self):
        # Dosya yolunu tanımla
        file_path = "output.txt"

        # SpaCy dil modeli yükleniyor (İngilizce için)
        nlp = spacy.load("en_core_web_sm")

        try:
            # Dosyadan metni oku
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # Metni SpaCy ile analiz et
            doc = nlp(text)

            # Konuları depolamak için bir liste oluştur
            topics = []

            # Metindeki varlıkları (entities) bul ve listeye ekle
            for ent in doc.ents:
                topics.append({
                    "text": ent.text,  # Bulunan varlık metni
                    "label": ent.label_  # Varlık etiketi (ör. kişi, yer, organizasyon)
                })

            # Eğer bir veya daha fazla konu bulunmuşsa
            if topics:
                for topic in topics:
                    # İlk bulunan konuyu arayüzde göster
                    self.Konu.setText(topic['text'])
            else:
                # Eğer konu bulunamazsa uygun bir mesaj göster
                self.Konu.setText("KONU ANLAŞILMADI.")

        # Dosya bulunamazsa hata mesajı ver
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found. Please check the path and try again.")
