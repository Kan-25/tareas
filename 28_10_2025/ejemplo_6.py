import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QProgressBar, QFrame
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class ComparadorCadenasGrafico(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # --- Configuración de ventana ---
        self.setWindowTitle("🔠 Comparador de Cadenas (Python + PyQt5)")
        self.setGeometry(250, 100, 800, 700)
        self.setStyleSheet("background-color: #EAF2F8;")

        # --- Logo superior ---
        logo = QLabel()
        pixmap = QPixmap("java_logo.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # --- Título principal ---
        titulo = QLabel("Comparador y Simulador de Cadenas")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #1B2631;")

        subtitulo = QLabel("💡 Ingrese dos cadenas y vea sus diferencias visualmente")
        subtitulo.setFont(QFont("Segoe UI", 11))
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("color: #2E4053; margin-bottom: 10px;")

        # --- Entradas de texto ---
        self.cadena1_input = QLineEdit()
        self.cadena2_input = QLineEdit()
        for campo in (self.cadena1_input, self.cadena2_input):
            campo.setFont(QFont("Consolas", 12))
            campo.setStyleSheet("padding: 6px; border-radius: 8px; border: 2px solid #5DADE2; background-color: white;")

        self.cadena1_input.setPlaceholderText("Ingrese la Cadena 1")
        self.cadena2_input.setPlaceholderText("Ingrese la Cadena 2")

        # --- Botón principal ---
        boton = QPushButton("🔍 Comparar Cadenas")
        boton.setFont(QFont("Segoe UI", 12, QFont.Bold))
        boton.setStyleSheet("""
            QPushButton {
                background-color: #2874A6; 
                color: white; 
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1F618D;
            }
        """)
        boton.clicked.connect(self.comparar)

        # --- Barras de longitud ---
        self.barra1 = QProgressBar()
        self.barra2 = QProgressBar()
        for barra in (self.barra1, self.barra2):
            barra.setTextVisible(True)
            barra.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #7FB3D5;
                    border-radius: 10px;
                    background-color: #EBF5FB;
                    height: 20px;
                }
                QProgressBar::chunk {
                    background-color: #2E86C1;
                    border-radius: 10px;
                }
            """)

        # --- Cuadros de identidad y orden ---
        self.identidad_label = QLabel("🟩 Identidad: ---")
        self.orden_label = QLabel("🟪 Orden: ---")
        for cuadro in (self.identidad_label, self.orden_label):
            cuadro.setFont(QFont("Segoe UI", 11, QFont.Bold))
            cuadro.setAlignment(Qt.AlignCenter)
            cuadro.setFixedHeight(40)
            cuadro.setFrameShape(QFrame.Panel)
            cuadro.setFrameShadow(QFrame.Raised)
            cuadro.setStyleSheet("background-color: #FDFEFE; border-radius: 8px; border: 2px solid #D5D8DC;")

        # --- Cuadro de resultados detallados ---
        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        self.resultado_texto.setFont(QFont("Consolas", 11))
        self.resultado_texto.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid #BFC9CA;")

        # --- Layout general ---
        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(QLabel("Cadena 1:"))
        layout.addWidget(self.cadena1_input)
        layout.addWidget(QLabel("Cadena 2:"))
        layout.addWidget(self.cadena2_input)
        layout.addWidget(boton)
        layout.addWidget(QLabel("📏 Longitud de las cadenas:"))
        layout.addWidget(self.barra1)
        layout.addWidget(self.barra2)
        layout.addWidget(QLabel("📊 Comparaciones Lógicas:"))
        layout.addWidget(self.identidad_label)
        layout.addWidget(self.orden_label)
        layout.addWidget(QLabel("🧠 Detalle del análisis:"))
        layout.addWidget(self.resultado_texto)
        self.setLayout(layout)

    def comparar(self):
        c1 = self.cadena1_input.text()
        c2 = self.cadena2_input.text()

        if not c1 or not c2:
            self.resultado_texto.setHtml("<b style='color:red;'>Por favor, ingrese ambas cadenas.</b>")
            return

        max_len = max(len(c1), len(c2), 1)
        self.barra1.setMaximum(max_len)
        self.barra2.setMaximum(max_len)
        self.barra1.setValue(len(c1))
        self.barra2.setValue(len(c2))

        salida = []
        salida.append(f"<h3>📋 RESULTADOS DE COMPARACIÓN</h3>")
        salida.append(f"<b>Cadena 1:</b> '{c1}' (Longitud: {len(c1)})<br>")
        salida.append(f"<b>Cadena 2:</b> '{c2}' (Longitud: {len(c2)})<br><hr>")

        # Identidad
        if c1 == c2:
            self.identidad_label.setText("🟩 Identidad: IDÉNTICAS")
            self.identidad_label.setStyleSheet("background-color: #ABEBC6; border: 2px solid #28B463; border-radius: 8px;")
            salida.append("<b style='color:green;'>✔ Las cadenas son IDÉNTICAS.</b><br>")
        else:
            self.identidad_label.setText("🟥 Identidad: NO IDÉNTICAS")
            self.identidad_label.setStyleSheet("background-color: #F5B7B1; border: 2px solid #CB4335; border-radius: 8px;")
            salida.append("<b style='color:red;'>✖ Las cadenas NO son idénticas.</b><br>")

        # Longitud
        if len(c1) == len(c2):
            salida.append("<b style='color:green;'>✔ Longitud equivalente.</b><br>")
        else:
            salida.append(f"<b style='color:orange;'>⚠ Diferencia de longitud: {abs(len(c1)-len(c2))} caracteres.</b><br>")

        # Orden lexicográfico
        if c1 == c2:
            orden_texto = "IGUALES en orden"
            color = "#D2B4DE"
        elif c1 > c2:
            orden_texto = "Cadena 1 es MAYOR (después alfabéticamente)"
            color = "#AED6F1"
        else:
            orden_texto = "Cadena 1 es MENOR (antes alfabéticamente)"
            color = "#FAD7A0"

        self.orden_label.setText(f"🟪 Orden: {orden_texto}")
        self.orden_label.setStyleSheet(f"background-color: {color}; border: 2px solid gray; border-radius: 8px;")
        salida.append(f"<b>{orden_texto}</b><br>")

        self.resultado_texto.setHtml("".join(salida))


# --- Programa principal ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ComparadorCadenasGrafico()
    ventana.show()
    sys.exit(app.exec_())

