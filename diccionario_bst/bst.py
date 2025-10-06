# bst.py

class Nodo:
    """Representa un nodo en el Arbol Binario de Búsqueda (BST)."""
    def __init__(self, palabra, traduccion):
        # Aseguramos que la palabra se guarde en minúsculas para una búsqueda consistente
        self.palabra = palabra.lower()
        self.traduccion = traduccion
        self.izq = None
        self.der = None

class DiccionarioBST:
    """Implementa la estructura del Diccionario usando un BST."""
    def __init__(self):
        self.raiz = None

    def insertar_par(self, palabra, traduccion):
        palabra = palabra.lower()
        if self.raiz is None:
            self.raiz = Nodo(palabra, traduccion)
        else:
            self._insertar_recursivo(self.raiz, palabra, traduccion)

    def _insertar_recursivo(self, nodo, palabra, traduccion):
        if palabra < nodo.palabra:
            if nodo.izq is None:
                nodo.izq = Nodo(palabra, traduccion)
            else:
                self._insertar_recursivo(nodo.izq, palabra, traduccion)
        elif palabra > nodo.palabra:
            if nodo.der is None:
                nodo.der = Nodo(palabra, traduccion)
            else:
                self._insertar_recursivo(nodo.der, palabra, traduccion)
        else:
            # Reemplazar la traducción si la palabra ya existe (actualización)
            nodo.traduccion = traduccion

    def buscar_traduccion(self, palabra):
        palabra = palabra.lower()
        return self._buscar_recursivo(self.raiz, palabra)

    def _buscar_recursivo(self, nodo, palabra):
        if nodo is None:
            return None
        if palabra == nodo.palabra:
            return nodo.traduccion
        elif palabra < nodo.palabra:
            return self._buscar_recursivo(nodo.izq, palabra)
        else:
            return self._buscar_recursivo(nodo.der, palabra)
            
    # RECORRIDO IN-ORDER (PARA LA LISTA ORDENADA)
    def inorder(self):
        """Generador que devuelve (palabra, traduccion) en orden alfabético."""
        yield from self._inorder_recursivo(self.raiz)

    def _inorder_recursivo(self, nodo):
        if nodo is not None:
            yield from self._inorder_recursivo(nodo.izq)
            # Solo se devuelve el par (palabra, traduccion)
            yield nodo.palabra, nodo.traduccion 
            yield from self._inorder_recursivo(nodo.der)

    # --- Métodos de Eliminación ---

    def eliminar_palabra(self, palabra):
        palabra = palabra.lower()
        self.raiz = self._eliminar_recursivo(self.raiz, palabra)
        # El método recursivo devuelve el nuevo nodo raíz (o None)

    def _eliminar_recursivo(self, nodo, palabra):
        if nodo is None:
            return nodo

        if palabra < nodo.palabra:
            nodo.izq = self._eliminar_recursivo(nodo.izq, palabra)
        elif palabra > nodo.palabra:
            nodo.der = self._eliminar_recursivo(nodo.der, palabra)
        else:
            # Nodo encontrado

            # Caso 1: Cero o un hijo
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq

            # Caso 2: Dos hijos
            # Encontrar el sucesor in-order (el más pequeño en el sub-árbol derecho)
            sucesor = self._min_valor_nodo(nodo.der)
            
            # Copiar el contenido del sucesor al nodo actual
            nodo.palabra = sucesor.palabra
            nodo.traduccion = sucesor.traduccion

            # Eliminar el sucesor (que ahora está duplicado)
            nodo.der = self._eliminar_recursivo(nodo.der, sucesor.palabra)

        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    # --- Métodos de Recorrido Adicionales ---

    def preorder(self):
        yield from self._preorder_recursivo(self.raiz)

    def _preorder_recursivo(self, nodo):
        if nodo is not None:
            yield nodo.palabra, nodo.traduccion
            yield from self._preorder_recursivo(nodo.izq)
            yield from self._preorder_recursivo(nodo.der)

    def postorder(self):
        yield from self._postorder_recursivo(self.raiz)

    def _postorder_recursivo(self, nodo):
        if nodo is not None:
            yield from self._postorder_recursivo(nodo.izq)
            yield from self._postorder_recursivo(nodo.der)
            yield nodo.palabra, nodo.traduccion