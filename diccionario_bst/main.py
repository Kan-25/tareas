# main.py

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QTabWidget, QGridLayout, QGroupBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

# py estén en la misma carpeta
from functions import cargar_diccionario, exportar_inorder, exportar_recorridos
# Se importa DiccionarioBST para una inicialización segura
from bst import DiccionarioBST 

DATA_PATH = os.path.join("data", "diccionario.txt")
OUTPUTS_DIR = "outputs"
# Asegurar que la carpeta 'outputs' exista
os.makedirs(OUTPUTS_DIR, exist_ok=True)


class DiccionarioGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📘 Diccionario Multilingüe (BST)")
        self.setGeometry(300, 150, 500, 600)

        # Configuración de color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#E0FFFF"))
        self.setPalette(palette)
        self.setFont(QFont("Arial", 10))

        # Cargar datos de forma segura
        loaded_bst = cargar_diccionario(DATA_PATH)
        # Aseguramos que self.bst sea un objeto válido de DiccionarioBST
        if isinstance(loaded_bst, DiccionarioBST):
             self.bst = loaded_bst
        else:
             self.bst = DiccionarioBST()

        main_layout = QVBoxLayout()
        
        # Título
        title = QLabel("Gestor de Diccionario Español ↔ Inglés")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #007BFF;")
        main_layout.addWidget(title)

        # Crear widget de pestañas
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", 11, QFont.Bold))
        
        self.tab_gestion = QWidget()
        self.tab_consulta = QWidget()

        self.tabs.addTab(self.tab_gestion, "📚 Gestión (Agregar/Eliminar)")
        self.tabs.addTab(self.tab_consulta, "🔍 Consulta y Exportación")
        
        self._setup_gestion_tab()
        self._setup_consulta_tab()
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Llama a actualizar_lista para que se muestre el diccionario
        self.actualizar_lista()

    # --- PESTAÑA DE GESTIÓN (AGREGAR/ELIMINAR) ---
    def _setup_gestion_tab(self):
        layout = QVBoxLayout(self.tab_gestion)

        # Grupo para agregar
        group_add = QGroupBox("Añadir / Reemplazar Palabra")
        add_layout = QGridLayout()
        
        add_layout.addWidget(QLabel("Palabra (Español):"), 0, 0)
        self.input_palabra = QLineEdit()
        self.input_palabra.setPlaceholderText("Ej: 'perro'")
        add_layout.addWidget(self.input_palabra, 0, 1)

        add_layout.addWidget(QLabel("Traducción (Inglés):"), 1, 0)
        self.input_traduccion = QLineEdit()
        self.input_traduccion.setPlaceholderText("Ej: 'dog'")
        add_layout.addWidget(self.input_traduccion, 1, 1)

        self.btn_agregar = QPushButton("➕ AGREGAR / REEMPLAZAR")
        self.btn_agregar.setStyleSheet("background-color: #28a745; color: white;")
        self.btn_agregar.clicked.connect(self.agregar_par)
        add_layout.addWidget(self.btn_agregar, 2, 0, 1, 2)
        
        group_add.setLayout(add_layout)
        layout.addWidget(group_add)

        # Grupo para eliminar
        group_del = QGroupBox("Eliminar Palabra")
        del_layout = QGridLayout()
        
        del_layout.addWidget(QLabel("Palabra a eliminar (usar campo de texto superior):"), 0, 0, 1, 2)
        
        self.btn_eliminar = QPushButton("❌ ELIMINAR")
        self.btn_eliminar.setStyleSheet("background-color: #dc3545; color: white;")
        self.btn_eliminar.clicked.connect(self.eliminar_palabra)
        del_layout.addWidget(self.btn_eliminar, 1, 0, 1, 2)
        
        group_del.setLayout(del_layout)
        layout.addWidget(group_del)
        
        layout.addStretch(1)

    # --- PESTAÑA DE CONSULTA Y EXPORTACIÓN ---
    def _setup_consulta_tab(self):
        layout = QVBoxLayout(self.tab_consulta)
        
        # 1. Búsqueda
        group_search = QGroupBox("Buscar Traducción")
        search_layout = QHBoxLayout()
        
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Escriba la palabra en Español y presione 'Enter' o el botón.")
        self.input_buscar.returnPressed.connect(self.buscar_palabra)
        search_layout.addWidget(self.input_buscar)

        self.btn_buscar = QPushButton("🔍 Buscar")
        self.btn_buscar.clicked.connect(self.buscar_palabra)
        search_layout.addWidget(self.btn_buscar)
        
        group_search.setLayout(search_layout)
        layout.addWidget(group_search)
        
        # 2. Lista de Diccionario (Inorder)
        layout.addWidget(QLabel("Diccionario Actual (Orden Alfabético):"))
        
        self.lista = QListWidget() 
        layout.addWidget(self.lista)
        
        # 3. Exportar
        self.btn_exportar = QPushButton("💾 EXPORTAR Diccionario y Recorridos")
        self.btn_exportar.setStyleSheet("background-color: #007BFF; color: white;")
        self.btn_exportar.clicked.connect(self.exportar_diccionario)
        layout.addWidget(self.btn_exportar)


    # --- MÉTODOS DE LA LÓGICA (Funciones del BST) ---
    
    # LA FUNCIÓN CORREGIDA QUE ELIMINA EL TEXTO MOLESTO
    def actualizar_lista(self):
        self.lista.clear()
        try:
            # Se asegura que SÓLO se usen los pares (palabra, traduccion)
            for palabra, traduccion in self.bst.inorder():
                self.lista.addItem(f"{palabra} = {traduccion}")
        except Exception as e:
            # En caso de error, muestra un mensaje útil en la GUI
            QMessageBox.critical(self, "Error al Cargar Lista", f"Ocurrió un error al cargar la lista. Revise bst.py. Error: {e}")


    def agregar_par(self):
        palabra = self.input_palabra.text().strip()
        traduccion = self.input_traduccion.text().strip()
        if not palabra or not traduccion:
            QMessageBox.warning(self, "Error", "Debe ingresar palabra y traducción para agregar.")
            return
        
        is_update = self.bst.buscar_traduccion(palabra) is not None
        self.bst.insertar_par(palabra, traduccion)
        
        msg = "reemplazada" if is_update else "agregada"
        QMessageBox.information(self, "Éxito", f"La palabra '{palabra}' ha sido {msg}.")
        
        self.input_palabra.clear()
        self.input_traduccion.clear()
        self.actualizar_lista()

    def buscar_palabra(self):
        palabra = self.input_buscar.text().strip()
        if not palabra:
            QMessageBox.information(self, "Búsqueda", "Ingrese una palabra para buscar.")
            return
        traduccion = self.bst.buscar_traduccion(palabra)
        if traduccion:
            QMessageBox.information(self, "Traducción encontrada", f"'{palabra.upper()}' se traduce como:\n{traduccion.upper()}")
        else:
            QMessageBox.information(self, "No encontrada", f"No se encontró traducción para '{palabra}'.")
        self.input_buscar.clear()

    def eliminar_palabra(self):
        palabra = self.input_palabra.text().strip()
        if not palabra:
            QMessageBox.warning(self, "Error", "Ingrese la palabra que desea eliminar en el campo de texto superior de 'Gestión'.")
            return
        
        if self.bst.buscar_traduccion(palabra):
            self.bst.eliminar_palabra(palabra)
            QMessageBox.information(self, "Eliminación exitosa", f"La palabra '{palabra}' ha sido eliminada del diccionario.")
        else:
            QMessageBox.warning(self, "Error de eliminación", f"La palabra '{palabra}' no se encontró en el diccionario.")
            
        self.input_palabra.clear()
        self.actualizar_lista()

    def exportar_diccionario(self):
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        exportar_inorder(self.bst, os.path.join(OUTPUTS_DIR, "diccionario_ordenado.txt"))
        exportar_recorridos(self.bst, os.path.join(OUTPUTS_DIR, "recorridos_diccionario.txt"))
        QMessageBox.information(self, "Exportado", f"Archivos guardados en la carpeta '{OUTPUTS_DIR}/'.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = DiccionarioGUI()
    ventana.show()
    sys.exit(app.exec_())