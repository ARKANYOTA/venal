from src.index import main
import argparse, os
if os.name != "nt":
    import sys, termios

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vlc on terminal.")
    parser.add_argument("path", metavar="path", type=str, nargs="?", help="Path to video file.", const="a.mkv", default="a.mkv")
    parser.add_argument("startat", metavar="start-at", type=int, nargs="?", help="Start at frame.", const=0, default=0)
    parser.add_argument("fps", metavar="fps", type=int, help="FPS.", const=24, nargs="?", default=24)
    args = parser.parse_args()

    if os.name != "nt":
        old_settings = termios.tcgetattr(sys.stdin)
    try:
        main(args)
    finally:
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
