#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTREX · Reloj ASCII — Edición Pride (definitiva)
-------------------------------------------------
Te pregunta qué tema/bandera quieres y aplica esa paleta al reloj.

Uso:
    python autorex_clock.py                        # pregunta qué tema
    python autorex_clock.py --theme aroace         # sin preguntar
    python autorex_clock.py --random               # tema aleatorio
    python autorex_clock.py --list-themes          # ver todos
    python autorex_clock.py --once --theme trans   # 1 frame y sale
    python autorex_clock.py --tz Europe/Madrid

Controles en el reloj:
    ESPACIO  → play / pausa cronómetro
    R        → reiniciar cronómetro
    T        → siguiente tema
    Q / ESC  → salir
"""

import argparse
import calendar
import datetime
import os
import random
import shutil
import sys
import time

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


# ═══════════════════════════════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════════════════════════════
BANNER = r"""
 █████╗ ██╗   ██╗████████╗██████╗ ███████╗██╗  ██╗███████╗
██╔══██╗██║   ██║╚══██╔══╝██╔══██╗██╔════╝╚██╗██╔╝██╔════╝
███████║██║   ██║   ██║   ██████╔╝█████╗   ╚███╔╝ ███████╗
██╔══██║██║   ██║   ██║   ██╔══██╗██╔══╝   ██╔██╗ ╚════██║
██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗██╔╝ ██╗███████║
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
""".strip("\n").split("\n")
_BW = max(len(l) for l in BANNER)
BANNER = [l.ljust(_BW) for l in BANNER]


# ═══════════════════════════════════════════════════════════════════════════
#  Fuente de dígitos
# ═══════════════════════════════════════════════════════════════════════════
FONT = {
    "0": (" ███ ", "█   █", "█   █", "█   █", " ███ "),
    "1": ("  █  ", " ██  ", "  █  ", "  █  ", " ███ "),
    "2": (" ███ ", "█   █", "  ██ ", " █   ", "█████"),
    "3": ("████ ", "    █", " ███ ", "    █", "████ "),
    "4": ("█  █ ", "█  █ ", "█████", "   █ ", "   █ "),
    "5": ("█████", "█    ", "████ ", "    █", "████ "),
    "6": (" ███ ", "█    ", "████ ", "█   █", " ███ "),
    "7": ("█████", "   █ ", "  █  ", " █   ", "█    "),
    "8": (" ███ ", "█   █", " ███ ", "█   █", " ███ "),
    "9": (" ███ ", "█   █", " ████", "    █", " ███ "),
    ":": (" ", "█", " ", "█", " "),
    " ": ("     ",) * 5,
}

def big(text):
    rows = [""] * 5
    for i, ch in enumerate(text):
        g = FONT.get(ch, FONT[" "])
        for r in range(5):
            rows[r] += g[r]
        if i < len(text) - 1:
            for r in range(5):
                rows[r] += " "
    return rows


# ═══════════════════════════════════════════════════════════════════════════
#  TEMAS (banderas) — cualquier nombre sirve para --theme
# ═══════════════════════════════════════════════════════════════════════════
THEMES = {
    "aroace":      {"name": "Aroace",        "colors": [(226,140,0),(236,205,0),(255,255,255),(98,174,208),(27,75,138)]},
    "trans":       {"name": "Trans",         "colors": [(91,206,250),(245,169,184),(255,255,255),(245,169,184),(91,206,250)]},
    "bi":          {"name": "Bisexual",      "colors": [(214,2,112),(155,79,150),(0,56,168)]},
    "pan":         {"name": "Pansexual",     "colors": [(255,33,140),(255,216,0),(33,177,255)]},
    "lesbian":     {"name": "Lesbiana",      "colors": [(214,69,0),(255,140,70),(255,255,255),(213,91,140),(168,44,120)]},
    "gay":         {"name": "Gay / Rainbow", "colors": [(228,3,3),(255,140,0),(255,237,0),(0,128,38),(0,76,255),(115,41,130)]},
    "nonbinary":   {"name": "No binario",    "colors": [(252,244,52),(255,255,255),(156,89,209),(0,0,0)]},
    "genderfluid": {"name": "Género fluido", "colors": [(255,118,164),(255,255,255),(190,70,190),(0,0,0),(51,59,156)]},
    "agender":     {"name": "Agénero",       "colors": [(0,0,0),(188,188,188),(255,255,255),(184,226,140)]},
    "ace":         {"name": "Asexual",       "colors": [(0,0,0),(163,163,163),(255,255,255),(128,0,128)]},
    "aro":         {"name": "Aromántico",    "colors": [(59,190,80),(167,224,175),(255,255,255),(170,170,170),(0,0,0)]},
    "genderqueer": {"name": "Genderqueer",   "colors": [(182,152,255),(255,255,255),(90,158,80)]},
    "polysexual":  {"name": "Polisexual",    "colors": [(255,55,203),(0,144,120),(0,50,255)]},
    "omni":        {"name": "Omnisexual",    "colors": [(255,154,237),(255,232,145),(102,190,255),(105,76,202)]},
    "intersex":    {"name": "Intersex",      "colors": [(255,213,0),(120,44,175)]},
    "abrosexual":  {"name": "Abrosexual",    "colors": [(119,15,75),(239,113,181),(255,255,255),(239,113,181),(119,15,75)]},
    "demiboy":     {"name": "Demiboy",       "colors": [(126,126,126),(155,201,231),(255,255,255),(155,201,231),(126,126,126)]},
    "demigirl":    {"name": "Demigirl",      "colors": [(126,126,126),(245,169,184),(255,255,255),(245,169,184),(126,126,126)]},
}
THEME_KEYS    = list(THEMES.keys())
DEFAULT_THEME = "aroace"


# ═══════════════════════════════════════════════════════════════════════════
#  Utilidades de color
# ═══════════════════════════════════════════════════════════════════════════
def make_visible(rgb, min_lum=45):
    """Aclara colores demasiado oscuros para que se vean sobre fondo negro."""
    r, g, b = rgb
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if lum >= min_lum:
        return rgb
    if lum < 1:
        return (min_lum, min_lum, min_lum)
    scale = min_lum / lum
    return (min(255, int(r * scale)), min(255, int(g * scale)), min(255, int(b * scale)))

def fg(rgb):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def bg(rgb):
    return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

def lerp(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t))

def gradient_through(stops, n):
    if not stops:
        return [(255, 255, 255)] * max(1, n)
    if len(stops) == 1:
        return [stops[0]] * n
    segs = len(stops) - 1
    out = []
    for i in range(n):
        pos = i / max(1, n - 1) * segs
        seg = min(int(pos), segs - 1)
        t   = pos - seg
        out.append(lerp(stops[seg], stops[seg + 1], t))
    return out

def preview_blocks(colors, cell=2):
    return "".join(f"{bg(make_visible(c))}{' ' * cell}\033[0m" for c in colors)


# ═══════════════════════════════════════════════════════════════════════════
#  Alineación / colorizado
# ═══════════════════════════════════════════════════════════════════════════
def center_line(text, width):
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text + " " * max(0, width - pad - len(text))

def colorize_plain(text, rgb, width):
    return f"{fg(rgb)}{center_line(text, width)}\033[0m"

def colorize_gradient(text, stops, width):
    pad  = max(0, (width - len(text)) // 2)
    tail = max(0, width - pad - len(text))
    colors = gradient_through(stops, len(text))
    parts = ["\033[0m" + " " * pad]
    for ch, rgb in zip(text, colors):
        parts.append(f"{fg(rgb)}{ch}")
    parts.append("\033[0m" + " " * tail)
    return "".join(parts)

def center_strip(colors, width, cell=2):
    vis = cell * len(colors)
    pad = max(0, (width - vis) // 2)
    tail = max(0, width - pad - vis)
    strip = "".join(f"{bg(make_visible(c))}{' ' * cell}\033[0m" for c in colors)
    return " " * pad + strip + "\033[0m" + " " * tail


# ═══════════════════════════════════════════════════════════════════════════
#  Paleta derivada de un tema
# ═══════════════════════════════════════════════════════════════════════════
class Palette:
    def __init__(self, theme_key, enabled=True):
        self.enabled = enabled
        self.set_theme(theme_key)

    def set_theme(self, theme_key):
        theme = THEMES[theme_key]
        self.theme_key = theme_key
        self.name      = theme["name"]
        self.colors    = [make_visible(c) for c in theme["colors"]]
        n    = len(self.colors)
        half = (n + 1) // 2
        self.day_colors  = self.colors[:half]
        self.year_colors = self.colors[n - half:]
        if n >= 2:
            self.subtitle = self.colors[-2]
            self.sw_color = self.colors[-2]
        else:
            self.subtitle = self.colors[0]
            self.sw_color = self.colors[0]
        self.date_color = self.colors[n // 2]
        self.info_color = self.colors[-1]
        self.hint_color = self.colors[0]


# ═══════════════════════════════════════════════════════════════════════════
#  Cronómetro
# ═══════════════════════════════════════════════════════════════════════════
class Stopwatch:
    def __init__(self):
        self.elapsed = 0.0
        self.running = False
        self._t0     = None
    def toggle(self):
        if self.running:
            self.elapsed += time.monotonic() - self._t0
            self.running  = False
        else:
            self._t0     = time.monotonic()
            self.running  = True
    def reset(self):
        self.elapsed = 0.0
        self.running = False
        self._t0     = None
    def value(self):
        return self.elapsed + (time.monotonic() - self._t0) if self.running else self.elapsed


# ═══════════════════════════════════════════════════════════════════════════
#  Textos
# ═══════════════════════════════════════════════════════════════════════════
DIAS  = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def make_bar(pct, width=28):
    pct = max(0.0, min(100.0, pct))
    total = pct / 100.0 * width
    full  = int(total)
    frac  = total - full
    partials = " ▏▎▍▌▋▊▉"
    bar = "█" * full
    if full < width:
        bar += partials[int(frac * 7)]
        bar += " " * (width - full - 1)
    return bar

def colorize_bar_line(label, pct, stops, width):
    bar   = make_bar(pct)
    left  = f"{label}   "
    right = f"  {pct:5.1f}%"
    pad   = max(0, (width - len(left) - len(bar) - len(right)) // 2)
    grad  = gradient_through(stops, len(bar))
    parts = ["\033[0m" + " " * pad, f"{fg(stops[0])}{left}"]
    for ch, rgb in zip(bar, grad):
        parts.append(f"{fg(rgb)}{ch}")
    parts.append(f"{fg(stops[-1])}{right}")
    tail = max(0, width - pad - len(left) - len(bar) - len(right))
    parts.append("\033[0m" + " " * tail)
    return "".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
#  Frame
# ═══════════════════════════════════════════════════════════════════════════
def build_frame(now, tz_label, sw, C):
    W  = shutil.get_terminal_size((100, 30)).columns
    L  = []
    on = C.enabled

    # Banner
    if on:
        for i, row in enumerate(BANNER):
            L.append(colorize_plain(row, C.colors[i % len(C.colors)], W))
    else:
        for row in BANNER:
            L.append(center_line(row, W))

    L.append(center_line("", W))
    subtitle = f"· {C.name.lower()} edition ·"
    L.append(colorize_plain(subtitle, C.subtitle, W) if on else center_line(subtitle, W))
    if on:
        L.append(center_strip(C.colors, W))
    L.append(center_line("", W))

    # Hora
    for row in big(now.strftime("%H:%M:%S")):
        L.append(colorize_gradient(row, C.colors, W) if on else center_line(row, W))
    L.append(center_line("", W))

    # Fecha
    fecha = f"{DIAS[now.weekday()]}, {now.day:02d} de {MESES[now.month-1]} de {now.year}"
    L.append(colorize_plain(fecha, C.date_color, W) if on else center_line(fecha, W))
    L.append(center_line("", W))

    # Barras
    start_day  = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_pct    = (now - start_day).total_seconds() / 86400.0 * 100.0
    start_year = datetime.datetime(now.year, 1, 1, tzinfo=now.tzinfo)
    end_year   = datetime.datetime(now.year + 1, 1, 1, tzinfo=now.tzinfo)
    year_pct   = (now - start_year) / (end_year - start_year) * 100.0

    if on:
        L.append(colorize_bar_line("día", day_pct,  C.day_colors,  W))
        L.append(colorize_bar_line("año", year_pct, C.year_colors, W))
    else:
        L.append(center_line(f"día   {make_bar(day_pct)}  {day_pct:5.1f}%", W))
        L.append(center_line(f"año   {make_bar(year_pct)}  {year_pct:5.1f}%", W))
    L.append(center_line("", W))

    # Cronómetro
    sv   = sw.value()
    hh   = int(sv // 3600)
    mm   = int((sv % 3600) // 60)
    ss   = sv % 60
    flag = "·" if sw.running else " "
    sw_line = (f"cronómetro {flag} {hh:02d}:{mm:02d}:{ss:04.1f}    "
               f"espacio·play  r·reset  t·tema")
    L.append(colorize_plain(sw_line, C.sw_color, W) if on else center_line(sw_line, W))
    L.append(center_line("", W))

    # Info
    doy        = now.timetuple().tm_yday
    total_days = 366 if calendar.isleap(now.year) else 365
    iso_week   = now.isocalendar()[1]
    info = f"semana {iso_week:02d}  ·  día {doy:03d}/{total_days}  ·  {tz_label}"
    L.append(colorize_plain(info, C.info_color, W) if on else center_line(info, W))
    hint = "q · salir"
    L.append(colorize_plain(hint, C.hint_color, W) if on else center_line(hint, W))

    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════════════════
#  Selección de tema
# ═══════════════════════════════════════════════════════════════════════════
def resolve_theme(raw):
    if not raw:
        return None
    key = raw.strip().lower()
    if key in THEMES:
        return key
    for k, v in THEMES.items():
        if v["name"].lower() == key:
            return k
    return None

def show_theme_list():
    print()
    print("  🌈  Temas disponibles  🌈")
    print("  " + "─" * 66)
    for i, k in enumerate(THEME_KEYS, 1):
        t = THEMES[k]
        print(f"  {i:2d}. {t['name']:<16} {preview_blocks(t['colors'])}  ({k})")
    print()

def prompt_theme():
    show_theme_list()
    while True:
        try:
            raw = input(f"  Elige un tema [1-{len(THEME_KEYS)}] o nombre "
                        f"(Enter = {DEFAULT_THEME}): ").strip()
        except EOFError:
            return DEFAULT_THEME
        if not raw:
            return DEFAULT_THEME
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(THEME_KEYS):
                return THEME_KEYS[idx]
        else:
            k = resolve_theme(raw)
            if k:
                return k
        print("  ⚠  Opción no válida, intenta de nuevo.\n")


# ═══════════════════════════════════════════════════════════════════════════
#  Teclado
# ═══════════════════════════════════════════════════════════════════════════
def read_key():
    if os.name == "nt":
        import msvcrt
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("\x00", "\xe0"):
                msvcrt.getwch()
                return None
            return ch
        return None
    import select
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(description="AUTREX · reloj ASCII pride")
    ap.add_argument("--theme", default=None,
                    help="Tema (aroace, trans, bi, pan, gay, nonbinary, ...)")
    ap.add_argument("--random", action="store_true", help="Tema aleatorio")
    ap.add_argument("--list-themes", action="store_true", help="Lista los temas y sale")
    ap.add_argument("--tz", default=None, help="Zona horaria (ej. Europe/Madrid)")
    ap.add_argument("--no-color", action="store_true", help="Sin colores")
    ap.add_argument("--refresh", type=float, default=0.15, help="Segundos entre frames")
    ap.add_argument("--once", action="store_true", help="Imprime un frame y sale")
    args = ap.parse_args()

    if os.name == "nt":
        os.system("")

    if args.list_themes:
        show_theme_list()
        return

    # Resolver tema
    if args.theme:
        key = resolve_theme(args.theme)
        if not key:
            print(f"Tema desconocido: {args.theme}", file=sys.stderr)
            print("Usa --list-themes para ver los disponibles.", file=sys.stderr)
            sys.exit(1)
        theme_key = key
    elif args.random:
        theme_key = random.choice(THEME_KEYS)
        print(f"🎲 Tema aleatorio: {THEMES[theme_key]['name']}")
    elif args.once or args.no_color or not sys.stdin.isatty():
        theme_key = DEFAULT_THEME
    else:
        theme_key = prompt_theme()

    # Zona horaria
    tz, tz_label = None, "hora local"
    if args.tz:
        if ZoneInfo is None:
            print("zoneinfo no disponible (requiere Python 3.9+)", file=sys.stderr)
            sys.exit(1)
        try:
            tz = ZoneInfo(args.tz)
            tz_label = args.tz
        except Exception:
            print(f"Zona horaria inválida: {args.tz}", file=sys.stderr)
            sys.exit(1)

    palette = Palette(theme_key, enabled=not args.no_color)
    sw      = Stopwatch()

    if args.once:
        print(build_frame(datetime.datetime.now(tz), tz_label, sw, palette))
        return

    # Modo raw en Unix
    old_settings = None
    if os.name != "nt" and sys.stdin.isatty():
        import termios, tty
        try:
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except Exception:
            old_settings = None

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    first = True
    try:
        while True:
            now   = datetime.datetime.now(tz)
            frame = build_frame(now, tz_label, sw, palette)

            sys.stdout.write("\033[H\033[J" if first else "\033[H")
            sys.stdout.write(frame)
            sys.stdout.flush()
            first = False

            deadline = time.monotonic() + args.refresh
            while time.monotonic() < deadline:
                k = read_key()
                if k:
                    if k in ("q", "Q", "\x1b"):
                        return
                    elif k == " ":
                        sw.toggle()
                    elif k in ("r", "R"):
                        sw.reset()
                    elif k in ("t", "T"):
                        idx = THEME_KEYS.index(palette.theme_key)
                        palette.set_theme(THEME_KEYS[(idx + 1) % len(THEME_KEYS)])
                time.sleep(0.02)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\033[0m\n")
        sys.stdout.flush()
        if old_settings is not None:
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    main()
