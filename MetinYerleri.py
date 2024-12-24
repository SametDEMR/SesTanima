import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MetinGirisiOlustur(QWidget):
    def MetinAlanlari(self):
        self.MetinGirisiAlanlari = []

        # METİN GİRİŞ ALANLARI OLUŞTURULUYOR
        text_fields_info = [
            {"bilgi": "Ad", "placeholder": "EĞİTİLMESİNİ İSTEDİĞİNİZ ADI GİRİNİZ.", "position": (390, 280, 420, 40)},
            {"bilgi": "Adres", "placeholder": "", "position": (390, 340, 420, 40)},
        ]

        for field_info in text_fields_info:
            bilgi = field_info["bilgi"]
            text_field = QLineEdit(self)
            text_field.setPlaceholderText(field_info["placeholder"])
            text_field.setGeometry(*field_info["position"])

            text_field.setObjectName(bilgi)

            # CSS EKLENDİ
            text_field.setStyleSheet("""
                QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #FFA500;
                    border-radius: 10px;
                    font-size: 16px;
                    padding: 5px;
                }
                QLineEdit:focus {
                    border-color: #FF8C00;
                }
            """)

            self.MetinGirisiAlanlari.append(text_field)
            setattr(self, bilgi, text_field)

            if bilgi == "Adres":
                text_field.setReadOnly(True)