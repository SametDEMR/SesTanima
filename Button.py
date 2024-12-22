import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import locale

from ShowHide import *
from Islemler import *

class ButonOlustur(QWidget):
    def Butonlar(self):
        self.AnaMenuButonlari = []
        self.selected_button = None

        # BUTONLAR OLUŞTURULUYOR
        buttons_info = [
            {"bilgi": "GeriButton", "text": "Geri", "position": (10, 10, 100, 40),"function": lambda: ShowHide.Geri(self)},
            {"bilgi": "MikrofonSesButton", "text": "MİKROFONDAN SES TANIMA", "position": (120, 310, 420, 40), "function": lambda: Islemler.Thread(self)},
            {"bilgi": "DosyadanSesButton", "text": "SES DOSYASINDAN SES TANIMA", "position": (660, 310, 420, 40), "function": lambda: Islemler.Thread(self)}
        ]

        for button_info in buttons_info:
            bilgi = button_info["bilgi"]
            button = QPushButton(button_info["text"], self)
            button.setGeometry(*button_info["position"])
            button.clicked.connect(button_info["function"])

            button.setObjectName(bilgi)

            #CSS EKLENDİ
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFA500;
                    border-radius: 20px;
                    color: #333333;
                    font-size: 20px;
                    padding: 0px 0px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
            """)

            self.AnaMenuButonlari.append(button)
            setattr(self, bilgi, button)
