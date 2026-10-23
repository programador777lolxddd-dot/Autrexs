#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTREX · Reloj ASCII — Aroace Edition (definitiva)
--------------------------------------------------
Paleta de la bandera aroace: naranja · amarillo · blanco · azul claro · azul oscuro.

Uso:
    python autorex_clock.py
    python autorex_clock.py --tz Europe/Madrid
    python autorex_clock.py --no-color
    python autorex_clock.py --once

Controles:
    ESPACIO  → play / pausa cronómetro
    R        → reiniciar cronómetro
    Q / ESC  → salir
"""

import argparse
import calendar
import datetime
import os
import shutil
import sys
import time

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


# ═══════════════════════════════════════════════════════════════════════════
#  BANNER AUTREX  (ANSI Shadow)
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
#  Fuente de dígitos grandes
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


def big(text: str) -> list[str]:
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
#  PALETA AROACE — los 5 colores de la bandera + variantes seguras
# ═══════════════════════════════════════════════════════════════════════════
#  Bandera aroace:  naranja · amarillo · blanco · azul claro · azul oscuro
# ───────────────────────────────────────────────────────────────────────────
AROACE = {
    "orange":      (226, 140,   0),   # #E28C00  naranja aroace
    "yellow":      (236, 205,   0),   # #ECCD00  amarillo aroace
    "white":       (255, 255, 255),   # #FFFFFF  blanco
    "light_blue":  ( 98, 174, 208),   # #62AED0  azul claro aroace
    "dark_blue":   ( 27,  75, 138),   # #1B4B8A  azul oscuro aroace
    # variantes un poco más tenues para texto que debe leerse bien
    "soft_white":  (245, 245, 245),
    "warm_orange": (255, 165,  60),
    "deep_blue":   ( 40,  90, 160),
}


class Palette:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.flag = [
            AROACE["orange"],
            AROACE["yellow"],
            AROACE["white"],
            AROACE["light_blue"],
            AROACE["dark_blue"],
        ]


# ═══════════════════════════════════════════════════════════════════════════
#  Utilidades de color / alineación
# ═══════════════════════════════════════════════════════════════════════════
def center_line(text: str, width: int) -> str:
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text + " " * max(0, width - pad - len(text))


def fg(rgb) -> str:
    r, g, b = rgb
    return f"\033[38;2;{r};{g};{b}m"


def colorize_plain(text: str, rgb, width: int) -> str:
    return f"{fg(rgb)}{center_line(text, width)}\033[0m"


def lerp(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t))


def gradient_through(stops, n):
    """Devuelve n colores interpolando a través de una lista de stops."""
    if n <= 1:
        return [stops[0]]
    segs = len(stops) - 1
    out = []
    for i in range(n):
        pos = i / (n - 1) * segs
        seg = min(int(pos), segs - 1)
        t   = pos - seg
        out.append(lerp(stops[seg], stops[seg + 1], t))
    return out


def colorize_gradient(text: str, stops, width: int) -> str:
    """Gradiente horizontal que pasa por todos los `stops`."""
    pad  = max(0, (width - len(text)) // 2)
    tail = max(0, width - pad - len(text))
    colors = gradient_through(stops, len(text))
    parts = ["\033[0m" + " " * pad]
    for ch, rgb in zip(text, colors):
        parts.append(f"{fg(rgb)}{ch}")
    parts.append("\033[0m" + " " * tail)
    return "".join(parts)


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
            self.running = True

    def reset(self):
        self.elapsed = 0.0
        self.running = False
        self._t0     = None

    def value(self) -> float:
        if self.running:
            return self.elapsed + (time.monotonic() - self._t0)
        return self.elapsed


# ═══════════════════════════════════════════════════════════════════════════
#  Textos
# ═══════════════════════════════════════════════════════════════════════════
DIAS  = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def make_bar(pct: float, width: int = 28) -> str:
    pct   = max(0.0, min(100.0, pct))
    total = pct / 100.0 * width
    full  = int(total)
    frac  = total - full
    partials = " ▏▎▍▌▋▊▉"
    bar = "█" * full
    if full < width:
        bar += partials[int(frac * 7)]
        bar += " " * (width - full - 1)
    return bar


def colorize_bar_line(label: str, pct: float, stops, width: int) -> str:
    """Colorea la barra con gradiente y la etiqueta/porcentaje con el color
    del extremo correspondiente (izquierda = primer stop, derecha = último)."""
    bar   = make_bar(pct)
    left  = f"{label}   "
    right = f"  {pct:5.1f}%"
    pad   = max(0, (width - len(left) - len(bar) - len(right)) // 2)

    grad  = gradient_through(stops, len(bar))
    parts = ["\033[0m" + " " * pad]
    parts.append(f"{fg(stops[0])}{left}")
    for ch, rgb in zip(bar, grad):
        parts.append(f"{fg(rgb)}{ch}")
    parts.append(f"{fg(stops[-1])}{right}")
    tail = width - pad - len(left) - len(bar) - len(right)
    parts.append("\033[0m" + " " * max(0, tail))
    return "".join(parts)


# ═══════════════════════════════════════════════════════════════════════════
#  Construcción del frame
# ═══════════════════════════════════════════════════════════════════════════
def build_frame(now, tz_label, sw, C):
    W = shutil.get_terminal_size((100, 30)).columns
    L: list[str] = []
    on = C.enabled
    flag = C.flag

    # ── Banner: 5 colores de la bandera, uno por fila ─────────────────────
    if on:
        for i, row in enumerate(BANNER):
            L.append(colorize_plain(row, flag[i % len(flag)], W))
    else:
        for row in BANNER:
            L.append(center_line(row, W))

    L.append(center_line("", W))
    subtitle = "· aroace edition ·"
    L.append(colorize_plain(subtitle, AROACE["light_blue"], W)
             if on else center_line(subtitle, W))
    L.append(center_line("", W))

    # ── Hora grande: gradiente que recorre los 5 colores de la bandera ────
    for row in big(now.strftime("%H:%M:%S")):
        L.append(colorize_gradient(row, flag, W)
                 if on else center_line(row, W))
    L.append(center_line("", W))

    # ── Fecha (blanco suave) ──────────────────────────────────────────────
    fecha = f"{DIAS[now.weekday()]}, {now.day:02d} de {MESES[now.month-1]} de {now.year}"
    L.append(colorize_plain(fecha, AROACE["soft_white"], W)
             if on else center_line(fecha, W))
    L.append(center_line("", W))

    # ── Barras: día = naranja→amarillo, año = azul claro→azul oscuro ──────
    start_day  = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_pct    = (now - start_day).total_seconds() / 86400.0 * 100.0
    start_year = datetime.datetime(now.year,     1, 1, tzinfo=now.tzinfo)
    end_year   = datetime.datetime(now.year + 1, 1, 1, tzinfo=now.tzinfo)
    year_pct   = (now - start_year) / (end_year - start_year) * 100.0

    if on:
        L.append(colorize_bar_line("día", day_pct,
                                   [AROACE["orange"], AROACE["yellow"]], W))
        L.append(colorize_bar_line("año", year_pct,
                                   [AROACE["light_blue"], AROACE["dark_blue"]], W))
    else:
        L.append(center_line(f"día   {make_bar(day_pct)}  {day_pct:5.1f}%", W))
        L.append(center_line(f"año   {make_bar(year_pct)}  {year_pct:5.1f}%", W))
    L.append(center_line("", W))

    # ── Cronómetro (azul claro) ───────────────────────────────────────────
    sv   = sw.value()
    hh   = int(sv // 3600)
    mm   = int((sv % 3600) // 60)
    ss   = sv % 60
    flagtxt = "·" if sw.running else " "
    sw_line = (f"cronómetro {flagtxt} {hh:02d}:{mm:02d}:{ss:04.1f}    "
               f"espacio·play  r·reset")
    L.append(colorize_plain(sw_line, AROACE["light_blue"], W)
             if on else center_line(sw_line, W))
    L.append(center_line("", W))

    # ── Info (azul oscuro) + hint (naranja) ───────────────────────────────
    doy        = now.timetuple().tm_yday
    total_days = 366 if calendar.isleap(now.year) else 365
    iso_week   = now.isocalendar()[1]
    info = f"semana {iso_week:02d}  ·  día {doy:03d}/{total_days}  ·  {tz_label}"
    L.append(colorize_plain(info, AROACE["deep_blue"], W)
             if on else center_line(info, W))
    hint = "q · salir"
    L.append(colorize_plain(hint, AROACE["orange"], W)
             if on else center_line(hint, W))

    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════════════════
#  Teclado no bloqueante
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
    else:
        import select
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(description="AUTREX · reloj ASCII aroace")
    ap.add_argument("--tz", default=None, help="Zona horaria (ej. Europe/Madrid)")
    ap.add_argument("--no-color", action="store_true", help="Desactivar colores ANSI")
    ap.add_argument("--refresh", type=float, default=0.15, help="Segundos entre frames")
    ap.add_argument("--once", action="store_true", help="Imprime un frame y sale")
    args = ap.parse_args()

    if os.name == "nt":
        os.system("")

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

    C  = Palette(enabled=not args.no_color)
    sw = Stopwatch()

    if args.once:
        print(build_frame(datetime.datetime.now(tz), tz_label, sw, C))
        return

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
            frame = build_frame(now, tz_label, sw, C)

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