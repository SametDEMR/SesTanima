import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPalette, QColor

class MetinYerleri(QWidget):
    def MetinYeri(self):
        self.labels = []

        # UYARI-BİLGİLENDİRME MESAJ YERLERİ OLUŞTURULDU
        labels_info = [
            {"bilgi": "BilgilendirmeKutusu", "text": "Lütfen bir seçim yapınız.", "position": (0, 0, 1200, 40)},
            {"bilgi": "KonusulanKisiSirasi", "text": "", "position": (0, 580, 1200, 40)},
            {"bilgi": "DuyguDurumu", "text": "", "position": (20, 640, 1200, 40)},
            {"bilgi": "KacKelimeVar", "text": "", "position": (20, 700, 1200, 40)},
            {"bilgi": "Konu", "text": "", "position": (620, 700, 1200, 40)},
        ]

        for label_info in labels_info:
            bilgi = label_info["bilgi"]
            label = QLabel(label_info["text"], self)
            label.setGeometry(*label_info["position"])

            label.show()

            # CSS EKLENDİ
            label.setStyleSheet("""
                QLabel {
                    color: #333333;
                    font-family: "Arial", sans-serif; /* Yazı fontu */
                    font-size: 30px;
                }
            """)

            if bilgi == "BilgilendirmeKutusu" or bilgi == "KonusulanKisiSirasi":
                label.setAlignment(Qt.AlignCenter)

            self.labels.append(label)
            setattr(self, bilgi, label)