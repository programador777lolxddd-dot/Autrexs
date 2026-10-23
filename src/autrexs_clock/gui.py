"""A small graphical desktop clock for Autrexs."""
import time
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

BG = "#0b1020"
PANEL = "#111a2e"
FG = "#edf2ff"
MUTED = "#9ba9c8"
ACCENT = "#8172ff"


def launch_gui():
    root = tk.Tk()
    root.title("Autrexs — Clock Studio")
    root.geometry("540x470")
    root.minsize(440, 430)
    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=PANEL, foreground=FG, padding=(15, 9))
    style.map("TNotebook.Tab", background=[("selected", ACCENT)])
    style.configure("TButton", background=ACCENT, foreground="white", borderwidth=0, padding=8)
    style.configure("TEntry", fieldbackground="#202b43", foreground=FG, insertcolor=FG)

    tk.Label(root, text="AUTREXS", bg=BG, fg=FG, font=("Sans", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 0))
    tk.Label(root, text="CLOCK STUDIO  •  PYTHON EDITION", bg=BG, fg=MUTED, font=("Sans", 9, "bold")).pack(anchor="w", padx=25)
    clock = tk.Label(root, text="", bg=BG, fg=FG, font=("Sans", 42, "bold"))
    clock.pack(pady=(18, 0))
    date = tk.Label(root, text="", bg=BG, fg=MUTED, font=("Sans", 11))
    date.pack(pady=(0, 18))

    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True, padx=22, pady=(0, 20))
    timer_tab = tk.Frame(tabs, bg=PANEL)
    sw_tab = tk.Frame(tabs, bg=PANEL)
    tabs.add(timer_tab, text="Temporizador")
    tabs.add(sw_tab, text="Cronómetro")

    tk.Label(timer_tab, text="CUENTA ATRÁS", bg=PANEL, fg=MUTED).pack(pady=(20, 8))
    timer_display = tk.Label(timer_tab, text="00:00", bg=PANEL, fg=FG, font=("Sans", 32, "bold"))
    timer_display.pack()
    fields = tk.Frame(timer_tab, bg=PANEL)
    fields.pack(pady=10)
    mins = ttk.Entry(fields, width=6, justify="center")
    mins.insert(0, "1")
    mins.pack(side="left", padx=4)
    tk.Label(fields, text="min", bg=PANEL, fg=MUTED).pack(side="left")
    secs = ttk.Entry(fields, width=6, justify="center")
    secs.insert(0, "0")
    secs.pack(side="left", padx=4)
    tk.Label(fields, text="seg", bg=PANEL, fg=MUTED).pack(side="left")
    timer_state = {"deadline": 0.0, "running": False}

    def start_timer():
        try:
            total = int(mins.get()) * 60 + int(secs.get())
            if total <= 0 or int(mins.get()) < 0 or int(secs.get()) < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Tiempo no válido", "Introduce minutos y segundos válidos.")
            return
        timer_state["deadline"] = time.monotonic() + total
        timer_state["running"] = True

    def stop_timer():
        timer_state["running"] = False
        timer_display.config(text="00:00")

    controls = tk.Frame(timer_tab, bg=PANEL)
    controls.pack(pady=8)
    ttk.Button(controls, text="Iniciar", command=start_timer).pack(side="left", padx=4)
    ttk.Button(controls, text="Detener", command=stop_timer).pack(side="left", padx=4)

    tk.Label(sw_tab, text="CRONÓMETRO", bg=PANEL, fg=MUTED).pack(pady=(24, 8))
    sw_display = tk.Label(sw_tab, text="00:00.00", bg=PANEL, fg=FG, font=("Sans", 32, "bold"))
    sw_display.pack(pady=8)
    sw = {"running": False, "start": 0.0, "elapsed": 0.0}

    def start_sw():
        if not sw["running"]:
            sw["start"] = time.monotonic()
            sw["running"] = True

    def pause_sw():
        if sw["running"]:
            sw["elapsed"] += time.monotonic() - sw["start"]
            sw["running"] = False

    def reset_sw():
        sw.update(running=False, start=0.0, elapsed=0.0)
        sw_display.config(text="00:00.00")

    sw_controls = tk.Frame(sw_tab, bg=PANEL)
    sw_controls.pack(pady=12)
    ttk.Button(sw_controls, text="Iniciar", command=start_sw).pack(side="left", padx=4)
    ttk.Button(sw_controls, text="Pausar", command=pause_sw).pack(side="left", padx=4)
    ttk.Button(sw_controls, text="Reiniciar", command=reset_sw).pack(side="left", padx=4)
    tk.Label(root, text="Autrexs Python • local y sin cuenta", bg=BG, fg="#687797", font=("Sans", 8)).pack(pady=(0, 7))

    def tick():
        now = datetime.now()
        clock.config(text=now.strftime("%H:%M:%S"))
        date.config(text=now.strftime("%A, %d %B %Y"))
        if timer_state["running"]:
            remaining = max(0, timer_state["deadline"] - time.monotonic())
            total = int(remaining + 0.999)
            timer_display.config(text=f"{total // 60:02d}:{total % 60:02d}")
            if remaining <= 0:
                timer_state["running"] = False
                root.bell()
                messagebox.showinfo("Autrexs", "¡Tiempo terminado!")
        if sw["running"]:
            elapsed = sw["elapsed"] + time.monotonic() - sw["start"]
            centis = int(elapsed * 100)
            minutes, rest = divmod(centis, 6000)
            seconds, cs = divmod(rest, 100)
            sw_display.config(text=f"{minutes:02d}:{seconds:02d}.{cs:02d}")
        root.after(100, tick)

    tick()
    root.mainloop()
