import customtkinter as ctk
from tkinter import messagebox

from server import start_server, stop_server, is_server_running

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Start remote-control server")
        w, h = 320, 140
        self.geometry(f"{w}x{h}")
        self.resizable(False, False)
        self._center_window(w, h)

        frame = ctk.CTkFrame(master=self, corner_radius=8)
        frame.pack(padx=16, pady=16, fill="both", expand=True)

        lbl = ctk.CTkLabel(master=frame, text="Port:", anchor="w")
        lbl.place(x=12, y=12)

        self.port_var = ctk.StringVar(value="8000")
        entry = ctk.CTkEntry(master=frame, textvariable=self.port_var, width=120)
        entry.place(x=12, y=40)

        start_btn = ctk.CTkButton(
            master=frame, text="Start", width=90, command=self.on_start
        )
        start_btn.place(x=190, y=36)

    def _center_window(self, width, height):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_start(self):
        port_str = self.port_var.get().strip()
        if not port_str.isdigit():
            messagebox.showerror("Error", "Port must be an integer")
            return
        port = int(port_str)
        if not (1 <= port <= 65535):
            messagebox.showerror("Error", "Port must be in range 1–65535")
            return
        server_started = False
        try:
            start_server(port)
            server_started = is_server_running()
        except Exception as e:
            messagebox.showerror("Error", str(e))
