import os
import sys
import math
import random
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # Look for icons relative to current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return repo_root

class DiscoDancer:
    def __init__(self, canvas, img_path, name, x, y):
        self.canvas = canvas
        self.name = name
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.phase = random.uniform(0, math.pi * 2)
        self.dance_style = random.choice(['bounce', 'sway', 'circle', 'pulse'])
        self.hue_offset = random.uniform(0, 360)

        try:
            self.orig_img = Image.open(img_path).convert("RGBA")
        except Exception:
            self.orig_img = Image.new("RGBA", (120, 120), (255, 0, 255, 255))

        self.orig_img = self.orig_img.resize((90, 90), Image.Resampling.LANCZOS)
        self.current_tk_img = ImageTk.PhotoImage(self.orig_img)

        self.shadow_id = canvas.create_oval(x - 35, y + 45, x + 35, y + 60, fill="#11052C", outline="")
        self.image_id = canvas.create_image(x, y, image=self.current_tk_img)
        self.text_id = canvas.create_text(x, y + 65, text=name.replace('_', ' ').title(),
                                         fill="#00ffff", font=("Segoe UI", 10, "bold"))
        self.spotlight_id = canvas.create_polygon(x, y - 250, x - 45, y + 40, x + 45, y + 40,
                                                  fill="", outline="")

    def update(self, t, bpm_factor, intensity, strobe):
        dance_t = t * bpm_factor * 4.0 + self.phase

        off_x = 0
        off_y = 0
        scale = 1.0

        if self.dance_style == 'bounce':
            off_y = -abs(math.sin(dance_t)) * 35.0 * intensity
            off_x = math.sin(dance_t * 0.5) * 15.0 * intensity
        elif self.dance_style == 'sway':
            off_x = math.sin(dance_t) * 30.0 * intensity
            off_y = -abs(math.cos(dance_t * 2.0)) * 15.0 * intensity
        elif self.dance_style == 'circle':
            off_x = math.cos(dance_t) * 25.0 * intensity
            off_y = math.sin(dance_t) * 25.0 * intensity
        elif self.dance_style == 'pulse':
            scale = 1.0 + math.sin(dance_t * 2.0) * 0.25 * intensity
            off_y = -abs(math.sin(dance_t)) * 20.0 * intensity

        cur_x = self.base_x + off_x
        cur_y = self.base_y + off_y
        self.x = cur_x
        self.y = cur_y

        self.canvas.coords(self.image_id, cur_x, cur_y)
        self.canvas.coords(self.text_id, cur_x, cur_y + 55 * scale)

        shadow_w = max(10, 40 - abs(off_y) * 0.5)
        self.canvas.coords(self.shadow_id, cur_x - shadow_w, self.base_y + 50, cur_x + shadow_w, self.base_y + 62)

        if strobe and random.random() < 0.4:
            spot_color = "#ffffff"
        else:
            hue = (t * 50 + self.hue_offset) % 360
            spot_color = f"#{int(127 + 127*math.sin(math.radians(hue))):02x}{int(127 + 127*math.sin(math.radians(hue+120))):02x}{int(127 + 127*math.sin(math.radians(hue+240))):02x}"

        self.canvas.coords(self.spotlight_id, cur_x, 50, cur_x - 50, cur_y + 40, cur_x + 50, cur_y + 40)
        self.canvas.itemconfig(self.spotlight_id, fill=spot_color if random.random() < 0.3 else "")


class DiscoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DiscoMode - Windows Icon Dance Party!")
        self.geometry("1100x750")
        self.configure(bg="#08020f")

        base_dir = get_base_dir()
        icon_path = os.path.join(base_dir, "icons", "discomode.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        title_frame = tk.Frame(self, bg="#08020f")
        title_frame.pack(fill="x", pady=10)

        self.title_lbl = tk.Label(title_frame, text="🕺 DISCO MODE - THE ULTIMATE ICON DANCE FLOOR 💃",
                                  font=("Impact", 24, "bold"), fg="#ff00a0", bg="#08020f")
        self.title_lbl.pack()

        controls = tk.Frame(self, bg="#12072b", bd=2, relief="ridge")
        controls.pack(fill="x", padx=20, pady=5)

        tk.Label(controls, text="BPM / Speed:", font=("Segoe UI", 10, "bold"), fg="#00ffff", bg="#12072b").pack(side="left", padx=10, pady=5)
        self.bpm_slider = ttk.Scale(controls, from_=0.5, to=3.0, value=1.2)
        self.bpm_slider.pack(side="left", padx=10)

        tk.Label(controls, text="Intensity:", font=("Segoe UI", 10, "bold"), fg="#ff00ff", bg="#12072b").pack(side="left", padx=10, pady=5)
        self.intensity_slider = ttk.Scale(controls, from_=0.2, to=2.0, value=1.0)
        self.intensity_slider.pack(side="left", padx=10)

        self.strobe_var = tk.BooleanVar(value=True)
        self.strobe_chk = tk.Checkbutton(controls, text="Strobe Flashes", variable=self.strobe_var,
                                         font=("Segoe UI", 10, "bold"), fg="#ffff00", bg="#12072b",
                                         selectcolor="#08020f", activebackground="#12072b")
        self.strobe_chk.pack(side="left", padx=15)

        self.party_btn = tk.Button(controls, text="🔥 EXTRA PARTY HYPE 🔥", font=("Segoe UI", 10, "bold"),
                                   fg="#ffffff", bg="#e60073", activebackground="#ff0080",
                                   command=self.hype_mode)
        self.party_btn.pack(side="right", padx=15, pady=5)

        self.canvas = tk.Canvas(self, bg="#0d041a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        icon_names = [
            "text_editor", "settings", "file_explorer", "media_player", "web_browser",
            "calculator", "security", "terminal", "task_manager", "photo_viewer",
            "timeline_explorer", "discomode", "gamegetlink", "linkmydevice", "find_this_id_ip"
        ]

        self.dancers = []
        cols = 5
        start_y = 180
        row_height = 160

        for idx, name in enumerate(icon_names):
            r = idx // cols
            c = idx % cols

            x = 120 + c * 200
            y = start_y + r * row_height

            img_file = os.path.join(base_dir, "icons", f"{name}.png")
            dancer = DiscoDancer(self.canvas, img_file, name, x, y)
            self.dancers.append(dancer)

        self.disco_ball_x = 520
        self.disco_ball_y = 60
        self.disco_ball_r = 45
        self.ball_wire = self.canvas.create_line(520, 0, 520, 60, fill="#ffffff", width=3)
        self.disco_ball = self.canvas.create_ellipse(475, 15, 565, 105, fill="#e0e5ff", outline="#ffffff", width=3)

        self.lasers = []
        for _ in range(8):
            lid = self.canvas.create_line(520, 60, 0, 0, fill="#ff00ff", width=3)
            self.lasers.append(lid)

        self.eq_bars = []
        for i in range(16):
            bx = 100 + i * 55
            bar = self.canvas.create_rectangle(bx, 680, bx + 35, 710, fill="#00ffff", outline="")
            self.eq_bars.append(bar)

        self.start_time = time.time()
        self.animate()

    def hype_mode(self):
        self.bpm_slider.set(2.5)
        self.intensity_slider.set(1.8)
        self.strobe_var.set(True)

    def animate(self):
        t = time.time() - self.start_time
        bpm = self.bpm_slider.get()
        intensity = self.intensity_slider.get()
        strobe = self.strobe_var.get()

        hue = (t * 120) % 360
        r_c = int(127 + 127 * math.sin(math.radians(hue)))
        g_c = int(127 + 127 * math.sin(math.radians(hue + 120)))
        b_c = int(127 + 127 * math.sin(math.radians(hue + 240)))
        title_col = f"#{r_c:02x}{g_c:02x}{b_c:02x}"
        self.title_lbl.config(fg=title_col)

        beat = (t * bpm * 4.0)
        bg_val = int(8 + 15 * abs(math.sin(beat)))
        if strobe and random.random() < 0.15:
            self.canvas.config(bg="#3a005c")
        else:
            self.canvas.config(bg=f"#{bg_val:02x}041a")

        for idx, lid in enumerate(self.lasers):
            angle = (t * bpm * 3.0 + idx * (2 * math.pi / 8))
            lx = 520 + math.cos(angle) * 700
            ly = 60 + math.sin(angle) * 600
            col = ["#ff00a0", "#00ffff", "#ffff00", "#00ff66", "#ff6600"][idx % 5]
            self.canvas.coords(lid, 520, 60, lx, ly)
            self.canvas.itemconfig(lid, fill=col)

        for idx, bar in enumerate(self.eq_bars):
            bx = 100 + idx * 55
            h = 10 + abs(math.sin(t * bpm * 6.0 + idx * 0.5)) * 60 * intensity
            col = ["#00ffff", "#ff00a0", "#ffff00", "#00ff66"][idx % 4]
            self.canvas.coords(bar, bx, 700 - h, bx + 35, 700)
            self.canvas.itemconfig(bar, fill=col)

        for dancer in self.dancers:
            dancer.update(t, bpm, intensity, strobe)

        self.after(30, self.animate)

if __name__ == "__main__":
    app = DiscoApp()
    app.mainloop()
