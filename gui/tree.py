import customtkinter as ctk
from tkinter import ttk


class PayloadTree(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill="both")

    def load(self, results):
        self.tree.delete(*self.tree.get_children())

        for i, node in enumerate(results):
            root = self.tree.insert(
                "", "end",
                text=f"Layer {node['depth']} | {node['size']} bytes"
            )

            for m in node.get("mitre", []):
                self.tree.insert(
                    root, "end",
                    text=f"{m['technique']} - {m['description']}"
                )
