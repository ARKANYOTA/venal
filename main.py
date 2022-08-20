from src.application import Globals
from src.index import main
from src.player import Player
import threading
from src.get_mouse import Mouse, mouse_off, show_cursor, mouse_direct_off
import argparse, os
if os.name != "nt":
    import sys, termios

# TODO
# - Buffer
# - Sound  # https://www.geeksforgeeks.org/play-sound-in-python/
# - Mouse
# - (Menu)
#     - Selection de quelle video on veut lire dans le menu
#     - Sous titres
#     - Audio
#     - Quitter
# - Options
#     - Caméra args.path = 0
# - Sur la bar un appercu de la video
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vlc on terminal.")
    parser.add_argument("path", metavar="path", type=str, nargs="?", help="Path to video file.", const="a.mkv", default="a.mkv")
    parser.add_argument("startat", metavar="start-at", type=int, nargs="?", help="Start at frame.", const=0, default=0)
    parser.add_argument("fps", metavar="fps", type=int, help="FPS.", const=24, nargs="?", default=24)
    parser.add_argument("--mouse_active", metavar="False", type=bool, help="If you want mouse", const=False, nargs="?", default=False)
    args = parser.parse_args()

    if os.name != "nt":
        old_settings = termios.tcgetattr(sys.stdin)
    try:
        # start thread on main

        player = Player(args.path, args.startat)
        if args.mouse_active:
            player.Globals.Mouse = Mouse(args.mouse_active)
            mouse_thread = player.Globals.Mouse.start()
        else:
            player.Globals.Mouse = Mouse(False)
        main_thread = threading.Thread(target=main, args=(args, player))
        main_thread.start()
        main_thread.join()
        if args.mouse_active:
            player.Globals.Mouse.end()
    except KeyboardInterrupt:
        print("\nBye.")
    except BlockingIOError as e:
        print("\033[0m",show_cursor, mouse_off, mouse_direct_off)

        print(e)
        with open("error.log", "w") as f:
            f.write(str(e))
        exit(1)
    finally:
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

