import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.exists(value):  # Se o valor já existe, não insere
            return False
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert(self.root, value)
        return True  # Retorna True se a inserção for bem-sucedida

    def _insert(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert(current.right, value)

    def exists(self, value):
        return self._exists(self.root, value)

    def _exists(self, current, value):
        if current is None:
            return False
        if current.value == value:
            return True
        elif value < current.value:
            return self._exists(current.left, value)
        else:
            return self._exists(current.right, value)

    def remove(self, value):
        if not self.exists(value):
            return False  # Retorna False se o valor não existir
        self.root = self._remove(self.root, value)
        return True  # Retorna True se a remoção for bem-sucedida

    def _remove(self, current, value):
        if current is None:
            return None

        if value < current.value:
            current.left = self._remove(current.left, value)
        elif value > current.value:
            current.right = self._remove(current.right, value)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            
            min_larger_node = self._get_min(current.right)
            current.value = min_larger_node.value
            current.right = self._remove(current.right, min_larger_node.value)

        return current

    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

class TreeGUI:
    def __init__(self, root):
        self.tree = BinaryTree()
        self.root = root
        self.root.title("Visualizador de Árvore Binária")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        # Criando um frame para alinhar os botões horizontalmente
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.insert_btn = tk.Button(self.button_frame, text="Inserir Valor", command=self.insert_value)
        self.insert_btn.pack(side=tk.LEFT, padx=5)

        self.remove_btn = tk.Button(self.button_frame, text="Remover Valor", command=self.remove_value)
        self.remove_btn.pack(side=tk.LEFT, padx=5)

        self.change_btn = tk.Button(self.button_frame, text="Alterar Valor", command=self.change_value)
        self.change_btn.pack(side=tk.LEFT, padx=5)

    def insert_value(self):
        value = simpledialog.askinteger("Inserir Valor", "Digite um número:")
        if value is not None:
            if not self.tree.insert(value):  # Se o valor já existir, exibe erro
                messagebox.showerror("Erro", f"O valor {value} já existe na árvore!")
            self.update_tree()

    def remove_value(self):
        value = simpledialog.askinteger("Remover Valor", "Digite um número para remover:")
        if value is not None:
            if not self.tree.remove(value):  # Se a remoção falhar, exibe erro
                messagebox.showerror("Erro", f"O valor {value} não existe na árvore!")
            self.update_tree()

    def change_value(self):
        value = simpledialog.askinteger("Alterar Valor", "Digite um número para alterar:")
        if value is not None:
            if not self.tree.remove(value):
                messagebox.showerror("Erro", f"O valor {value} não existe na árvore!")
            else:
                value2 = simpledialog.askinteger("Alterar Valor", "Digite um número para inserir no lugar:")
                while not self.tree.insert(value2):  # Se o valor já existir, exibe erro
                    messagebox.showerror("Erro", f"O valor {value2} já existe na árvore!")
                    value2 = simpledialog.askinteger("Alterar Valor", "Digite um número diferente:")
                self.update_tree()  

    def update_tree(self):
        self.canvas.delete("all")
        self.draw_tree(self.tree.root, 300, 50, 150)

    def draw_tree(self, node, x, y, spacing):
        if node:
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12))

            if node.left:
                self.canvas.create_line(x, y, x-spacing, y+50)
                self.draw_tree(node.left, x-spacing, y+50, spacing//2)

            if node.right:
                self.canvas.create_line(x, y, x+spacing, y+50)
                self.draw_tree(node.right, x+spacing, y+50, spacing//2)

if __name__ == "__main__":
    root = tk.Tk()
    gui = TreeGUI(root)
    root.mainloop()
