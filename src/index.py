from src.get_key import match_key
from src.menu import Menu
import cv2
import os
import time
if os.name != "nt":
    import tty, sys


def main(args, player):
    if os.name != "nt":
        tty.setcbreak(sys.stdin.fileno())
    player.Globals.Menu = Menu(player)

    while player.running:
        match_key(player)

        if not player.ProgressBar.pause or player.ProgressBar.actu:
            deltat = time.time()
            player.ProgressBar.actu = False

            player.screen_loop()
            if player.ProgressBar.status:
                player.ProgressBar.show()
            if player.Globals.Menu.is_active:
                player.Globals.Menu.show()
            if player.ProgressBar.pause:
                player.ProgressBar.show_status()
            player.print_frames()
            time_to_wait = 1 / args.fps - (time.time() - deltat)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            print(f"\033[0m\033[7;8H frames: {str(player.cap.get(cv2.CAP_PROP_POS_FRAMES))} fps: {1 / (time.time() - deltat):.2f}" f" loose: {time_to_wait * 1000:.2f}, {player.Globals.Menu.is_active}")
