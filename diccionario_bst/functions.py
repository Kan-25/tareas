import os
# Importamos la clase DiccionarioBST desde el archivo bst
from bst import DiccionarioBST 

def cargar_diccionario(ruta_archivo):
    """Carga los pares palabra-traducción de un archivo y los inserta en un BST."""
    bst = DiccionarioBST()
    # Verifica que el archivo exista
    if not os.path.exists(ruta_archivo):
        return bst
        
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                # Esperamos formato 'palabra:traduccion'
                partes = linea.strip().split(':', 1)
                if len(partes) == 2:
                    palabra = partes[0].strip()
                    traduccion = partes[1].strip()
                    if palabra and traduccion:
                        bst.insertar_par(palabra, traduccion)
        return bst
    except Exception as e:
        print(f"Error al cargar el diccionario: {e}")
        return DiccionarioBST()


def exportar_inorder(bst, ruta_archivo):
    """Exporta el diccionario ordenado (InOrder) a un archivo."""
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            for palabra, traduccion in bst.inorder():
                f.write(f"{palabra}:{traduccion}\n")
    except Exception as e:
        print(f"Error al exportar diccionario: {e}")


def exportar_recorridos(bst, ruta_archivo):
    """Exporta los tres recorridos (InOrder, PreOrder, PostOrder) a un archivo."""
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write("=== RECORRIDOS DEL ÁRBOL BST ===\n\n")

            # InOrder
            f.write("--- Recorrido IN-ORDER ---\n")
            f.write(" ".join(palabra for palabra, _ in bst.inorder()) + "\n\n")

            # PreOrder
            f.write("--- Recorrido PRE-ORDER ---\n")
            f.write(" ".join(palabra for palabra, _ in bst.preorder()) + "\n\n")

            # PostOrder
            f.write("--- Recorrido POST-ORDER ---\n")
            f.write(" ".join(palabra for palabra, _ in bst.postorder()) + "\n")
    except Exception as e:
        print(f"Error al exportar recorridos: {e}")
