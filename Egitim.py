import os
import librosa
import numpy as np
import pandas as pd  # Veri setini CSV olarak kaydetmek için pandas eklendi
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import joblib

class Egitim():
    def SesModelEgitim(self):
        data_dir = os.getcwd()  # Geçerli çalışma dizini
        data_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
        labels = []
        features = []

        for directory in data_dirs:
            folder_path = os.path.join(data_dir, directory)
            for file in os.listdir(folder_path):
                if file.endswith(".wav"):
                    file_path = os.path.join(folder_path, file)
                    label = directory  # Klasör adını etiket olarak alıyor
                    features.append(Egitim.extract_features(file_path))
                    labels.append(label)

        # 3. Veri Setini Hazırlama
        X = np.array(features)
        y = np.array(labels)

        # Veri setini DataFrame olarak oluşturma
        data_df = pd.DataFrame(X)
        data_df['label'] = y

        # DataFrame'i CSV olarak kaydetme
        data_csv_file = "veriseti.csv"
        data_df.to_csv(data_csv_file, index=False)
        print(f"Veri seti CSV dosyası olarak kaydedildi: {data_csv_file}")

        # 4. KNN Modeli
        knn_model = KNeighborsClassifier(n_neighbors=5)  # K=5 komşu kullanılıyor

        # 5. Çapraz Doğrulama
        cv_scores = cross_val_score(knn_model, X, y, cv=5)
        print("KNN Cross Validation Scores:", cv_scores)
        print("Mean CV Accuracy:", np.mean(cv_scores))

        # 6. Modeli Eğitme
        knn_model.fit(X, y)

        # 7. Modeli Kaydetme
        model_file_name = "KNN_model.pkl"
        joblib.dump(knn_model, model_file_name)
        print(f"Model kaydedildi: {model_file_name}")

    def extract_features(file_path):
        y, sr = librosa.load(file_path, duration=15)
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
        return mfccs