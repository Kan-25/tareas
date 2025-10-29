# ✨ Verificador de Palíndromos Visual en PyQt5 con Gráfica
# Autor: David Flores

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PalindromoVisual(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔤 Verificador de Palíndromos Visual ✨")
        self.setGeometry(100, 100, 700, 600)

        # --- Fondo animado ---
        self.color_index = 0
        self.colores = [
            QColor("#E0FFFF"), QColor("#D8BFD8"),
            QColor("#FFFACD"), QColor("#F0E68C"),
            QColor("#E6E6FA"), QColor("#FFB6C1")
        ]

        self.timer = QTimer()
        self.timer.timeout.connect(self.cambiar_color_fondo)
        self.timer.start(1500)

        # --- Título ---
        self.label_titulo = QLabel("🌟 Verificador de Palíndromos 🌟", self)
        self.label_titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: #003366; margin-bottom: 5px;")

        # --- Campo de entrada ---
        self.input_cadena = QLineEdit(self)
        self.input_cadena.setPlaceholderText("🔹 Escribe una frase aquí...")
        self.input_cadena.setFont(QFont("Consolas", 14))
        self.input_cadena.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 3px solid #4682B4;
                border-radius: 12px;
                background-color: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 3px solid #1E90FF;
                background-color: #F0FFFF;
            }
        """)

        # --- Botones ---
        self.boton_verificar = QPushButton("🔍 Verificar", self)
        self.boton_verificar.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.boton_verificar.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.boton_verificar.clicked.connect(self.verificar_palindromo)

        self.boton_limpiar = QPushButton("🧹 Limpiar", self)
        self.boton_limpiar.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.boton_limpiar.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        self.boton_limpiar.clicked.connect(self.limpiar_campos)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.boton_verificar)
        botones_layout.addWidget(self.boton_limpiar)

        # --- Resultado ---
        self.resultado = QLabel("", self)
        self.resultado.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.resultado.setAlignment(Qt.AlignCenter)

        # --- Simulación ---
        self.texto_simulacion = QTextEdit(self)
        self.texto_simulacion.setReadOnly(True)
        self.texto_simulacion.setFont(QFont("Consolas", 11))
        self.texto_simulacion.setStyleSheet("""
            QTextEdit {
                background-color: #F8F8FF;
                border: 2px solid #B0C4DE;
                border-radius: 8px;
                padding: 6px;
                color: #222;
            }
        """)

        # --- Gráfica de coincidencias ---
        self.figura, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvas(self.figura)

        # --- Diseño general ---
        layout = QVBoxLayout()
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.input_cadena)
        layout.addLayout(botones_layout)
        layout.addWidget(self.resultado)
        layout.addWidget(QLabel("🔎 Simulación de lectura desde ambos extremos:"))
        layout.addWidget(self.texto_simulacion)
        layout.addWidget(QLabel("📊 Gráfica de coincidencias (1=igual, 0=diferente):"))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def cambiar_color_fondo(self):
        """Animación de fondo"""
        color = self.colores[self.color_index]
        gradiente = QLinearGradient(0, 0, 0, self.height())
        gradiente.setColorAt(0.0, color)
        gradiente.setColorAt(1.0, QColor("white"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradiente))
        self.setPalette(palette)
        self.color_index = (self.color_index + 1) % len(self.colores)

    def verificar_palindromo(self):
        texto_original = self.input_cadena.text().strip()
        if not texto_original:
            QMessageBox.warning(self, "⚠️ Advertencia", "Por favor ingresa una frase antes de verificar.")
            return

        # Normalizar cadena
        cadena = ''.join(filter(str.isalnum, texto_original)).lower()
        cadena_invertida = cadena[::-1]

        # --- Comparación bidireccional ---
        simulacion = ""
        coincidencias = []
        es_palindromo = True

        for i in range(len(cadena) // 2):
            izq, der = cadena[i], cadena[-(i + 1)]
            if izq == der:
                simulacion += f"<span style='color:green;'>✔️ {izq} ↔ {der}</span><br>"
                coincidencias.append(1)
            else:
                simulacion += f"<span style='color:red;'>❌ {izq} ≠ {der}</span><br>"
                coincidencias.append(0)
                es_palindromo = False

        # Resultado textual
        if es_palindromo:
            self.resultado.setText(f"✅ '{texto_original}' ES un palíndromo 💚")
            self.resultado.setStyleSheet("color: green; background-color: #E0FFE0; border-radius: 10px; padding: 8px;")
        else:
            self.resultado.setText(f"❌ '{texto_original}' NO es un palíndromo 💔")
            self.resultado.setStyleSheet("color: red; background-color: #FFE0E0; border-radius: 10px; padding: 8px;")

        simulacion += f"<br>🪞 <b>Original:</b> {cadena}<br>🔁 <b>Invertida:</b> {cadena_invertida}"
        self.texto_simulacion.setHtml(simulacion)

        # --- Mostrar gráfica ---
        self.ax.clear()
        self.ax.bar(range(1, len(coincidencias) + 1), coincidencias)
        self.ax.set_ylim(0, 1.2)
        self.ax.set_yticks([0, 1])
        self.ax.set_yticklabels(["No coincide", "Coincide"])
        self.ax.set_xlabel("Comparación (izq-der)")
        self.ax.set_title("Coincidencias de caracteres")
        self.ax.grid(True, linestyle="--", alpha=0.5)
        self.canvas.draw()

    def limpiar_campos(self):
        """Reinicia los campos"""
        self.input_cadena.clear()
        self.resultado.clear()
        self.texto_simulacion.clear()
        self.ax.clear()
        self.canvas.draw()

# --- Ejecución principal ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PalindromoVisual()
    ventana.show()
    sys.exit(app.exec_())

