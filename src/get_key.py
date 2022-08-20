import os
from src.get_mouse import KeyEvent
import cv2

try:
    # POSIX system: Create and return a getch that manipulates the tty
    import termios, sys
    import tty, select

    # Read arrow keys correctly
    def get_key(player):
        Globals = player.Globals
        if Globals.Mouse.mouse_active:
            if Globals.Mouse.has_key():
                keyEvent: KeyEvent = Globals.Mouse.get_key()
                input_key = keyEvent.key
                match input_key:
                    case "\x1b[A":
                        return "up"
                    case "\x1b[B":
                        return "down"
                    case "\x1b[C":
                        return "right"
                    case "\x1b[D":
                        return "left"
                if keyEvent.click_state == "down" or keyEvent.click_state == "up":
                    # Mouse click
                    return keyEvent
                return input_key
            else:
                return "Empty"
        else:
            firstChar = sys.stdin.read(1)
            if firstChar == "\x1b":
                return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[sys.stdin.read(1) + sys.stdin.read(1)]
            else:
                return firstChar

except ImportError:
    # Non-POSIX: Return msvcrt's (Windows') getch
    from msvcrt import getch, kbhit

    # Read arrow keys correctly
    def get_key(player):
        firstChar = getch()
        if firstChar == b"\xe0":
            return {b"H": "up", b"P": "down", b"M": "right", b"K": "left"}[getch()]
        else:
            return firstChar.decode("utf-8")


def is_data():
    if os.name == "nt":
        return kbhit()
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def match_key(player):
    if not player.Globals.Mouse.mouse_active:
        if not is_data():
            return
    key = get_key(player)
    match key:
        case KeyEvent():
            match_mouse(key, player)
        case "up":
            player.video_add(10000)
        case "down":
            player.video_add(-1000)
        case "right":
            player.video_add(300)
        case "left":
            player.video_add(-300)
        case "r":
            print("\033[0;0H\033[2J")
            player.Globals.refresh()
        case " ":
            player.ProgressBar.set_pause()
        case "p":
            player.ProgressBar.set_status()


def mouse_press_on_bar(player, key: KeyEvent):
    mouse_pos: tuple[int, int]= key.mouse_pos
    if player.ProgressBar.status:
        if player.ProgressBar.is_in_bar(mouse_pos[0], mouse_pos[1]):
            goto_frame = (mouse_pos[0] - 27) * (player.cap.get(cv2.CAP_PROP_FRAME_COUNT)) // (player.Globals.term_x - 54)
            player.ProgressBar.goto_frame(goto_frame)

           # if mouse_pos[0] < player.ProgressBar.get_bar_pos() + 27:
           #     player.video_add(-300)
           # if mouse_pos[0] > player.ProgressBar.get_bar_pos() + 27:
           #     player.video_add(300)
            return True
    return False
def match_mouse(key: KeyEvent, player):
    if key.click_state == "down":
        if mouse_press_on_bar(player, key):
            return
        else:
            player.ProgressBar.set_pause()
            return
    return "mouse_event"