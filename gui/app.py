import customtkinter as ctk
import threading
from tkinter import filedialog
import json

from core.file_loader import load_file
from core.decoders.recursive_engine import walk
from core.utils.tree import render_tree


class TribeOfZebulun(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("✡ Tribe Of Zebulun")
        self.geometry("1000x650")

        header = ctk.CTkFrame(self)
        header.pack(fill="x", pady=10)

        ctk.CTkLabel(
            header,
            text="✡",
            font=("Segoe UI Symbol", 52),
            text_color="#FFD700"
        ).pack(side="left", padx=20)

        title = ctk.CTkFrame(header, fg_color="transparent")
        title.pack(side="left")

        ctk.CTkLabel(
            title,
            text="TRIBE OF ZEBULUN",
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title,
            text="Author: Kennedy Aikohi",
            font=("Segoe UI", 16, "bold"),
            text_color="#4DA6FF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title,
            text="linkedin.com/in/aikohikennedy | github.com/kennedy-aikohi",
            font=("Segoe UI", 12),
            text_color="#AAAAAA"
        ).pack(anchor="w")

        controls = ctk.CTkFrame(self)
        controls.pack(fill="x", pady=8)

        ctk.CTkButton(controls, text="Upload", command=self.upload).pack(side="left", padx=8)
        ctk.CTkButton(controls, text="Analyze", command=self.start).pack(side="left", padx=8)
        ctk.CTkButton(controls, text="Cancel", command=self.cancel).pack(side="left", padx=8)
        ctk.CTkButton(controls, text="Clear", command=self.clear).pack(side="left", padx=8)
        ctk.CTkButton(controls, text="Save Results", command=self.save).pack(side="left", padx=8)

        self.show_strings = ctk.BooleanVar(value=False)
        self.show_intent = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(controls, text="Show Intent", variable=self.show_intent).pack(side="right", padx=12)
        ctk.CTkCheckBox(controls, text="Show Strings", variable=self.show_strings).pack(side="right", padx=12)

        self.output = ctk.CTkTextbox(self, wrap="word")
        self.output.pack(expand=True, fill="both", padx=10, pady=10)

        self.file_path = None
        self.running = False
        self.results = []

    def upload(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.output.insert("end", f"[+] Loaded: {self.file_path}\n")

    def start(self):
        if not self.file_path or self.running:
            return
        self.running = True
        self.output.insert("end", "[*] Analysis started...\n\n")
        threading.Thread(target=self.run, daemon=True).start()

    def cancel(self):
        self.running = False
        self.output.insert("end", "[!] Analysis cancelled\n")

    def clear(self):
        self.running = False
        self.file_path = None
        self.results = []
        self.output.delete("1.0", "end")
        self.output.insert("end", "[*] Ready for new analysis\n")

    def save(self):
        if not self.results:
            return
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=2)
            self.output.insert("end", f"[✓] Results saved: {path}\n")

    def run(self):
        try:
            data, _ = load_file(self.file_path)
            self.results = []
            walk(data, self.results, lambda: self.running)

            def render():
                self.output.insert("end", f"[✓] Decoded layers: {len(self.results)}\n\n")

                for i, layer in enumerate(self.results):
                    self.output.insert("end", "\n" + "═" * 80 + "\n")
                    self.output.insert(
                        "end",
                        f"LAYER {i} | DEPTH {layer['depth']} | {layer['decoder']}\n"
                    )
                    self.output.insert("end", "═" * 80 + "\n")

                    self.output.insert(
                        "end",
                        f"Size    : {layer['size']} bytes\n"
                        f"Entropy : {layer['entropy']}\n"
                        f"Score   : {layer['score']} / 100\n"
                    )

                    if layer.get("family"):
                        self.output.insert(
                            "end",
                            f"\n🚨 MALWARE FAMILY DETECTED\n"
                            f"Name   : {layer['family']}\n"
                        )

                    if layer.get("yara_desc"):
                        self.output.insert(
                            "end",
                            f"Sample : {layer['yara_desc']}\n"
                        )

                    if layer.get("yara"):
                        self.output.insert(
                            "end",
                            f"YARA   : {', '.join(layer['yara'])}\n"
                        )

                    if self.show_intent.get() and layer.get("intent"):
                        self.output.insert("end", "\n[Intent Indicators]\n")
                        for k, v in layer["intent"].items():
                            self.output.insert("end", f" • {k}: {', '.join(v)}\n")

                    self.output.insert("end", "\n[Preview]\n")
                    self.output.insert("end", layer.get("preview", "") + "\n")

                    if self.show_strings.get():
                        self.output.insert("end", "\n[Strings]\n")
                        for s in layer.get("strings", [])[:40]:
                            self.output.insert("end", s + "\n")

                self.output.insert("end", "\n[Payload Tree]\n")
                self.output.insert("end", render_tree(self.results) + "\n")

            self.after(0, render)

        finally:
            self.running = False
