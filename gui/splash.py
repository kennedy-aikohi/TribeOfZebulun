import customtkinter as ctk


class Splash(ctk.CTkToplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)

        self.on_close = on_close

        self.geometry("520x360")
        self.overrideredirect(True)
        self.title("Tribe Of Zebulun")

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both")

        # BIG SYMBOL
        ctk.CTkLabel(
            frame,
            text="✡",
            font=("Segoe UI Symbol", 90, "bold"),
            text_color="#FFD700"
        ).pack(pady=(30, 5))

        # APP NAME (BIGGEST)
        ctk.CTkLabel(
            frame,
            text="TRIBE OF ZEBULUN",
            font=("Segoe UI", 26, "bold")
        ).pack()

        # AUTHOR (NORMAL SIZE)
        ctk.CTkLabel(
            frame,
            text="Kennedy Aikohi",
            font=("Segoe UI", 16),
            text_color="#4DA6FF"
        ).pack(pady=(6, 0))

        ctk.CTkLabel(
            frame,
            text="linkedin.com/in/aikohikennedy\n"
                 "github.com/kennedy-aikohi",
            font=("Segoe UI", 12),
            text_color="#AAAAAA"
        ).pack(pady=(4, 0))

        self.after(2200, self.close)

    def close(self):
        self.destroy()
        self.on_close()
