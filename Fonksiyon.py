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
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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
                duration = 5  # Kaydetme süresi (saniye)
                file_path = 'kayit.wav'  # Kaydedilecek dosyanın adı ve formatı

                # Mikrofon üzerinden ses kaydı yapılıyor
                recorded_audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
                sd.wait()  # Kaydın tamamlanmasını bekliyor

                # Kaydedilen ses dosyası belirtilen formata dönüştürülüp kaydediliyor
                write(file_path, samplerate, (recorded_audio * 32767).astype(np.int16))

            QApplication.processEvents()
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
    def SesDönüstür(self, file_path):
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
            self.BilgilendirmeKutusu.setText(e)
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
            self.BilgilendirmeKutusu.setText(e)  # Hata mesajı konsola yazdırılıyor



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
            self.BilgilendirmeKutusu.setText(e)



    # Sesin kime ait olduğunu bulma fonksiyonu
    def SesinKimeAitOlduğunuBulma(self, file_path):
        try:
            # Modeli yükle
            model, label_encoder = joblib.load("model.pkl")

            # Ses dosyasını yükle
            y, sr = librosa.load(file_path)

            # Segment uzunluğu (1 saniye)
            segment_duration = sr  # 1 saniye için örnek sayısı
            total_duration = len(y)

            results = []

            # Ses dosyasını segmentlere ayır ve analiz et
            for start in range(0, total_duration, segment_duration):
                end = start + segment_duration
                if end > total_duration:
                    break

                segment = y[start:end]

                # MFCC özelliklerini çıkar
                mfcc = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=40)
                feature = np.mean(mfcc.T, axis=0)  # 2D'yi 1D'ye indirgeme

                # Tahmin yap
                prediction = model.predict([feature])
                predicted_label = label_encoder.inverse_transform(prediction)

                # Sonucu listeye ekle
                results.append(predicted_label[0])
            return results

        except Exception as e:
            # Hata durumunda hatayı yazdır
            self.BilgilendirmeKutusu.setText(e)
            return []

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
            self.BilgilendirmeKutusu.setText(e)



    # METNE DÖNÜŞMÜŞ SESİN KONUSUNU BULMA
    def KonuBulma(self):
        try:
            # Dosya yolunu tanımla
            file_path = "output.txt"
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            basliklar = {
                "TEKNOLOJİ": ["bilgisayar", "yazılım", "teknoloji", "internet", "yapay zeka", "robot", "kodlama"],
                "SPOR": ["futbol", "basketbol", "koşu", "antrenman", "maç", "şampiyon", "spor"],
                "SANAT": ["resim", "müzik", "heykel", "şiir", "tiyatro", "sanat", "sinema"],
                "GİYİM": ["elbise", "moda", "ayakkabı", "pantolon", "kazak", "çanta", "giyim"]
            }

            # Metni küçük harflere çevir
            metin = text.lower()

            # Skor tablosu
            skorlar = {"TEKNOLOJİ": 0, "SPOR": 0, "SANAT": 0, "GİYİM": 0}

            # Anahtar kelimelere göre skoru artır
            for baslik, anahtar_kelimeler in basliklar.items():
                for kelime in anahtar_kelimeler:
                    if kelime in metin:
                        skorlar[baslik] += 1

            # En yüksek skoru alan başlığı döndür
            en_uygun_baslik = max(skorlar, key=skorlar.get)
            self.Konu.setText(f"Konuşulan Konu:  {en_uygun_baslik}")
        except Exception as e:
            self.BilgilendirmeKutusu.setText(e)