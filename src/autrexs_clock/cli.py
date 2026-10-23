"""Command-line entry point for Autrexs."""

import argparse
import time

from . import __version__
from .core import format_duration, get_current_time, monotonic_seconds


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="autrexs",
        description="Autrexs: reloj gráfico, cronómetro y temporizador.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    clock = commands.add_parser("now", help="mostrar la hora local en la terminal")
    clock.add_argument("--12h", dest="twelve_hour", action="store_true", help="usar formato de 12 horas")
    clock.add_argument("--no-seconds", action="store_true", help="ocultar los segundos")
    timer = commands.add_parser("count", help="contar una duración en segundos en la terminal")
    timer.add_argument("seconds", type=float, help="duración en segundos (0 o más)")
    args = parser.parse_args()

    if args.command is None:
        from .gui import launch_gui
        launch_gui()
    elif args.command == "now":
        print(get_current_time(seconds=not args.no_seconds, twelve_hour=args.twelve_hour))
    elif args.command == "count":
        if args.seconds < 0:
            parser.error("seconds debe ser 0 o un número positivo")
        start = monotonic_seconds()
        try:
            while True:
                elapsed = monotonic_seconds() - start
                remaining = max(0.0, args.seconds - elapsed)
                print(f"\rRestante: {format_duration(remaining)}", end="", flush=True)
                if remaining <= 0:
                    break
                time.sleep(min(0.05, remaining))
            print("\n¡Tiempo terminado!")
        except KeyboardInterrupt:
            print("\nCuenta atrás cancelada.")


if __name__ == "__main__":
    main()
