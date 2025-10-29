
import sys
import string
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QProgressBar, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AnalizadorSigma(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Analizador de Cadena - Alfabeto Σ")
        self.setGeometry(200, 150, 750, 550)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        # --- Título ---
        titulo = QLabel("🔠 Analizador de Cadena - Alfabeto Σ")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00e676; margin-bottom: 10px;")

        # --- Campo de entrada ---
        self.input_cadena = QLineEdit()
        self.input_cadena.setPlaceholderText("Escribe una cadena a analizar...")
        self.input_cadena.setFont(QFont("Consolas", 12))
        self.input_cadena.setStyleSheet(
            "background-color: #2b2b2b; color: white; padding: 6px; border-radius: 6px;"
        )

        # --- Botones ---
        self.boton_analizar = QPushButton("🔍 Analizar")
        self.boton_analizar.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.boton_analizar.setStyleSheet(
            "background-color: #00bfa5; color: black; padding: 8px; border-radius: 6px;"
        )
        self.boton_analizar.clicked.connect(self.analizar_cadena)

        self.boton_grafico = QPushButton("📊 Ver Gráfico")
        self.boton_grafico.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.boton_grafico.setStyleSheet(
            "background-color: #2196f3; color: white; padding: 8px; border-radius: 6px;"
        )
        self.boton_grafico.clicked.connect(self.mostrar_grafico)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.boton_analizar)
        botones_layout.addWidget(self.boton_grafico)

        # --- Área de resultados ---
        self.resultado_area = QTextEdit()
        self.resultado_area.setFont(QFont("Consolas", 11))
        self.resultado_area.setReadOnly(True)
        self.resultado_area.setStyleSheet(
            "background-color: #2b2b2b; color: white; padding: 10px; border-radius: 8px;"
        )

        # --- Barras de progreso ---
        self.barra_validos = QProgressBar()
        self.barra_validos.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 5px;
                text-align: center;
                background-color: #3c3c3c;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00e676;
            }
        """)

        self.barra_invalidos = QProgressBar()
        self.barra_invalidos.setStyleSheet("""
            QProgressBar {
                border: 1px solid #333;
                border-radius: 5px;
                text-align: center;
                background-color: #3c3c3c;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #ff1744;
            }
        """)

        # --- Contadores ---
        self.label_validos = QLabel("Válidos: 0")
        self.label_validos.setStyleSheet("color: #00e676; font-weight: bold;")

        self.label_invalidos = QLabel("Inválidos: 0")
        self.label_invalidos.setStyleSheet("color: #ff5252; font-weight: bold;")

        self.label_pureza = QLabel("Pureza: 0%")
        self.label_pureza.setStyleSheet("color: #03a9f4; font-weight: bold;")

        contadores_layout = QHBoxLayout()
        contadores_layout.addWidget(self.label_validos)
        contadores_layout.addWidget(self.label_invalidos)
        contadores_layout.addWidget(self.label_pureza)

        # --- Layout principal ---
        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.input_cadena)
        layout.addLayout(botones_layout)
        layout.addWidget(QLabel("📊 Barras de Simulación:"))
        layout.addWidget(self.barra_validos)
        layout.addWidget(self.barra_invalidos)
        layout.addLayout(contadores_layout)
        layout.addWidget(QLabel("🚦 Simulación de Caracteres:"))
        layout.addWidget(self.resultado_area)

        self.setLayout(layout)

        # Variables para gráfico
        self.conteo_validos = 0
        self.conteo_invalidos = 0

    def analizar_cadena(self):
        cadena = self.input_cadena.text()
        ALFABETO_VALIDO = set(string.ascii_lowercase + string.digits + 'ñ')

        if not cadena:
            self.resultado_area.setText("⚠️ No se ingresó ninguna cadena.")
            self.barra_validos.setValue(0)
            self.barra_invalidos.setValue(0)
            self.label_pureza.setText("Pureza: 0%")
            return

        self.conteo_validos = 0
        self.conteo_invalidos = 0
        resultado_html = ""

        for c in cadena:
            if c.lower() in ALFABETO_VALIDO:
                resultado_html += f"<span style='color:#00e676;'>{c}</span>"
                self.conteo_validos += 1
            else:
                resultado_html += f"<span style='color:#ff5252;'>{c}</span>"
                self.conteo_invalidos += 1

        total = len(cadena)
        porcentaje_validos = int((self.conteo_validos / total) * 100)
        porcentaje_invalidos = int((self.conteo_invalidos / total) * 100)

        pureza = round((self.conteo_validos / total) * 100, 2)

        # --- Mostrar resultados ---
        self.resultado_area.setHtml(resultado_html)
        self.label_validos.setText(f"Válidos: {self.conteo_validos}")
        self.label_invalidos.setText(f"Inválidos: {self.conteo_invalidos}")
        self.label_pureza.setText(f"Pureza: {pureza}%")
        self.barra_validos.setValue(porcentaje_validos)
        self.barra_invalidos.setValue(porcentaje_invalidos)

    def mostrar_grafico(self):
        if self.conteo_validos == 0 and self.conteo_invalidos == 0:
            return

        etiquetas = ['Válidos', 'Inválidos']
        valores = [self.conteo_validos, self.conteo_invalidos]
        colores = ['#00e676', '#ff5252']

        plt.figure(figsize=(5, 4))
        plt.bar(etiquetas, valores, color=colores)
        plt.title("Conteo de Caracteres - Alfabeto Σ")
        plt.ylabel("Cantidad")
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AnalizadorSigma()
    ventana.show()
    sys.exit(app.exec_())


