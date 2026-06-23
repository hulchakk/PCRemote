import customtkinter as ctk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk

from server import start_server, stop_server, is_server_running
from utils import get_local_ip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Start remote-control server")
        self.geometry("360x240")
        self.resizable(False, False)
        self._center_window(360, 240)

        self.server_port = None
        self.qr_image = None
        self.qr_label = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_start_screen()

    def _center_window(self, width, height):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def build_start_screen(self):
        self.clear_window()
        self.geometry("360x240")
        self._center_window(360, 240)

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

    def build_running_screen(self, port: int):
        self.clear_window()
        self.geometry("420x420")
        self._center_window(420, 420)

        frame = ctk.CTkFrame(master=self, corner_radius=8)
        frame.pack(padx=16, pady=16, fill="both", expand=True)

        url = f"http://{get_local_ip()}:{port}"
        title = ctk.CTkLabel(frame, text=f"Server running on {url}")
        title.pack(pady=(12, 8))

        qr = qrcode.make(url).convert("RGB")
        qr = qr.resize((220, 220))
        self.qr_image = ImageTk.PhotoImage(qr)

        self.qr_label = ctk.CTkLabel(frame, text="", image=self.qr_image)
        self.qr_label.pack(pady=8)

        stop_btn = ctk.CTkButton(frame, text="Stop", command=self.on_stop)
        stop_btn.pack(pady=12)

    def on_start(self):
        port_str = self.port_var.get().strip()
        if not port_str.isdigit():
            messagebox.showerror("Error", "Port must be an integer")
            return

        port = int(port_str)
        if not (1 <= port <= 65535):
            messagebox.showerror("Error", "Port must be in range 1–65535")
            return

        try:
            start_server(port)
            if is_server_running():
                self.server_port = port
                self.build_running_screen(port)
            else:
                messagebox.showerror("Error", "Server failed to start")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_stop(self):
        try:
            stop_server()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.server_port = None
        self.build_start_screen()

    def on_close(self):
        try:
            stop_server()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
