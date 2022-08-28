from src.get_key import match_key
from src.menu import Menu
import cv2
import os
import time

from src.windows import Windows

if os.name != "nt":
    import tty
    import sys


def main(args, player):
    if os.name != "nt":
        tty.setcbreak(sys.stdin.fileno())
    player.Globals.Windows = Windows(player)
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
            if player.Globals.Windows.has_active_windows:
                player.Globals.Windows.show()
            player.print_frames()
            time_to_wait = 1 / args.fps - (time.time() - deltat)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
