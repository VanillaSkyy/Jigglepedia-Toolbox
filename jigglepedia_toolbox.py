import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import tkinterdnd2
import webbrowser
import threading

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

FFMPEG_PATH = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))
FPS = 25
FRAME_PATTERN = "frame_%03d.png"
ICON_PATH = "app_icon.ico"

class ExporterApp(tkinterdnd2.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jigglepedia's Toolbox")
        self.geometry("420x300")
        self.resizable(False, False)

        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        self.folder_path = tk.StringVar()
        self.export_gif = tk.BooleanVar(value=True)
        self.export_mp4 = tk.BooleanVar(value=True)
        self.export_webm = tk.BooleanVar(value=False)

        self.mp4_crf = tk.IntVar(value=23)
        self.webm_crf = tk.IntVar(value=32)
        self.webm_bitrate = tk.StringVar(value="1M")

        self.build_ui()
        self.enable_drag_and_drop()

    def build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.tab_export = ttk.Frame(notebook)
        self.tab_gif = ttk.Frame(notebook)
        self.tab_mp4 = ttk.Frame(notebook)
        self.tab_webm = ttk.Frame(notebook)
        self.tab_about = ttk.Frame(notebook)

        notebook.add(self.tab_export, text="Export")
        notebook.add(self.tab_gif, text="GIF")
        notebook.add(self.tab_mp4, text="MP4")
        notebook.add(self.tab_webm, text="WebM")
        notebook.add(self.tab_about, text="About Me")

        self.build_export_tab()
        self.build_gif_tab()
        self.build_mp4_tab()
        self.build_webm_tab()
        self.build_about_tab()

    def build_export_tab(self):
        frame = self.tab_export

        ttk.Label(frame, text="Input Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Entry(frame, textvariable=self.folder_path, width=50).pack(padx=10)
        ttk.Button(frame, text="Browse...", command=self.browse_folder).pack(padx=10, pady=(5, 10))

        ttk.Checkbutton(frame, text="Export GIF", variable=self.export_gif).pack(anchor="w", padx=10)
        ttk.Checkbutton(frame, text="Export MP4", variable=self.export_mp4).pack(anchor="w", padx=10)
        ttk.Checkbutton(frame, text="Export WebM", variable=self.export_webm).pack(anchor="w", padx=10)

        ttk.Button(frame, text="Export", command=self.start_export).pack(pady=(15, 5))

        self.progress = tk.IntVar(value=0)
        self.progressbar = ttk.Progressbar(self.tab_export, maximum=100, variable=self.progress)
        self.progressbar.pack(fill="x", padx=10, pady=(5, 15))

    def build_gif_tab(self):
        ttk.Label(self.tab_gif, text="No settings available for GIF export.").pack(anchor="w", padx=10, pady=10)

    def build_mp4_tab(self):
        frame = self.tab_mp4
        ttk.Label(frame, text="Quality (CRF, lower = better, 18–28):").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Spinbox(frame, from_=15, to=35, textvariable=self.mp4_crf, width=10).pack(padx=10)

    def build_webm_tab(self):
        frame = self.tab_webm
        ttk.Label(frame, text="Quality (CRF, lower = better, 18–40):").pack(anchor="w", padx=10, pady=(10, 0))
        ttk.Spinbox(frame, from_=15, to=40, textvariable=self.webm_crf, width=10).pack(padx=10, pady=(0, 10))
        ttk.Label(frame, text="Bitrate (e.g. 1M, 500k):").pack(anchor="w", padx=10)
        ttk.Entry(frame, textvariable=self.webm_bitrate, width=15).pack(padx=10)

    def build_about_tab(self):
        tk.Label(self.tab_about, text="Jigglepedia's Toolbox\nMade by VanillaSkyy", font=("Segoe UI", 10)).pack(pady=(15, 5))
        link = tk.Label(self.tab_about, text="☕ Buy me a coffee", fg="blue", cursor="hand2", font=("Segoe UI", 10, "underline"))
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://ko-fi.com/vaniillaskyy"))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def enable_drag_and_drop(self):
        def drop(event):
            path = event.data.strip("{}")
            if os.path.isdir(path):
                self.folder_path.set(path)

        self.drop_target_register(tkinterdnd2.DND_FILES)
        self.dnd_bind('<<Drop>>', drop)

    def start_export(self):
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        self.progressbar.start()
        threading.Thread(target=self.export, daemon=True).start()


    def export(self):
        thread = threading.Thread(target=self.run_export, daemon=True)
        thread.start()

    def run_export(self):
        folder = self.folder_path.get()

        total = sum([self.export_gif.get(), self.export_mp4.get(), self.export_webm.get()])
        completed = 0

        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        if self.export_gif.get():
            self.progress.set(int((completed / total) * 100))
            self.generate_gif(folder, creationflags)
            completed += 1
        if self.export_mp4.get():
            self.progress.set(int((completed / total) * 100))
            self.generate_mp4(folder, creationflags)
            completed += 1
        if self.export_webm.get():
            self.progress.set(int((completed / total) * 100))
            self.generate_webm(folder, creationflags)
            completed += 1

        self.progress.set(100)
        self.progressbar.stop()
        messagebox.showinfo("Done", "Export complete!")
        os.startfile(folder)

    def generate_gif(self, folder, creationflags):
        input_pattern = os.path.join(folder, FRAME_PATTERN)
        palette_path = os.path.join(folder, "palette.png")
        output_path = os.path.join(folder, "output.gif")

        subprocess.run([
            FFMPEG_PATH, "-y",
            "-framerate", str(FPS),
            "-i", input_pattern,
            "-vf", "palettegen",
            palette_path
        ], cwd=folder, creationflags=creationflags)

        filters = f"fps={FPS},scale=iw:ih:flags=lanczos[x];[x][1:v]paletteuse"

        subprocess.run([
            FFMPEG_PATH, "-y",
            "-framerate", str(FPS),
            "-i", input_pattern,
            "-i", "palette.png",
            "-filter_complex", filters,
            "-loop", "0",
            output_path
        ], cwd=folder, creationflags=creationflags)

        if os.path.exists(palette_path):
            os.remove(palette_path)

    def generate_mp4(self, folder, creationflags):
        crf = self.mp4_crf.get()
        input_pattern = os.path.join(folder, FRAME_PATTERN)
        output_path = os.path.join(folder, "output.mp4")

        subprocess.run([
            FFMPEG_PATH, "-y",
            "-framerate", str(FPS),
            "-i", input_pattern,
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", "slow",
            "-pix_fmt", "yuv420p",
            output_path
        ], cwd=folder, creationflags=creationflags)

    def generate_webm(self, folder, creationflags):
        crf = self.webm_crf.get()
        bitrate = self.webm_bitrate.get()
        input_pattern = os.path.join(folder, FRAME_PATTERN)
        output_path = os.path.join(folder, "output.webm")

        subprocess.run([
            FFMPEG_PATH, "-y",
            "-framerate", str(FPS),
            "-i", input_pattern,
            "-c:v", "libvpx-vp9",
            "-crf", str(crf),
            "-b:v", bitrate,
            "-pix_fmt", "yuva420p",
            output_path
        ], cwd=folder, creationflags=creationflags)

if __name__ == "__main__":
    app = ExporterApp()
    app.mainloop()
    