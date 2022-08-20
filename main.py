import cv2
import os
import time
import argparse
import sys
import select


class GLOBALS:
    CAP = None
    TERMINALX, TERMINALY = os.get_terminal_size()
    TXT_FRAME = []


try:
    # POSIX system: Create and return a getch that manipulates the tty
    import termios
    import tty

    # Read arrow keys correctly
    def getKey():
        firstChar = sys.stdin.read(1)
        if firstChar == "\x1b":
            return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[sys.stdin.read(1) + sys.stdin.read(1)]
        else:
            return firstChar

except ImportError:
    # Non-POSIX: Return msvcrt's (Windows') getch
    from msvcrt import getch, kbhit

    # Read arrow keys correctly
    def getKey():
        firstChar = getch()
        if firstChar == b"\xe0":
            return {b"H": "up", b"P": "down", b"M": "right", b"K": "left"}[getch()]
        else:
            return firstChar.decode("utf-8")


def match_key():
    if not isData():
        return
    match getKey():
        case "up":
            GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) + 10000)
        case "down":
            GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) - 1000)
        case "right":
            GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) + 300)
        case "left":
            GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) - 300)
        case "r":
            print("\033[0;0H\033[2J")
            GLOBALS.TERMINALX, GLOBALS.TERMINALY = os.get_terminal_size()
            GLOBALS.TXT_FRAME = [[""] * GLOBALS.TERMINALX for _ in range(GLOBALS.TERMINALY)]


def get_frame():
    GLOBALS.CAP = cv2.VideoCapture(args.path)
    GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, args.startat)

    while GLOBALS.CAP.isOpened():
        ret, frame = GLOBALS.CAP.read()
        if frame is None:
            exit()
        frame = cv2.resize(frame, (GLOBALS.TERMINALX, GLOBALS.TERMINALY))
        if ret:
            yield frame
        else:
            break


def boucle_screen(frame):
    for yi in range(len(frame)):
        for xi in range(len(frame[yi])):
            r, g, b = frame[yi][xi]
            GLOBALS.TXT_FRAME[yi][xi] = f"\033[38;2;{b};{g};{r}m\u2588"


def print_screen(nb_frames, deltat):
    print(f"\033[0;0H{''.join([''.join(i) for i in GLOBALS.TXT_FRAME])}")


def isData():
    if os.name == "nt":
        return kbhit()
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def main():
    frames = get_frame()
    nb_frames = args.startat
    frame = next(frames)
    GLOBALS.TXT_FRAME = [[""] * GLOBALS.TERMINALX for _ in range(GLOBALS.TERMINALY)]

    if os.name != "nt":
        tty.setcbreak(sys.stdin.fileno())

    while True:
        match_key()

        deltat = time.time()
        nb_frames += 1
        frame = next(frames)
        boucle_screen(frame)

        print_screen(nb_frames, deltat)
        time_to_wait = 1 / args.fps - (time.time() - deltat)
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        print(f"\033[0m\033[0;0H frames: {str(GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES))} fps: {1 / (time.time() - deltat):.2f}" f" loose: {time_to_wait * 1000:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vlc on terminal.")
    parser.add_argument("path", metavar="path", type=str, nargs="?", help="Path to video file.", const="a.mkv", default="a.mkv")
    parser.add_argument("startat", metavar="start-at", type=int, nargs="?", help="Start at frame.", const=0, default=0)
    parser.add_argument("fps", metavar="fps", type=int, help="FPS.", const=24, nargs="?", default=24)
    args = parser.parse_args()

    if os.name != "nt":
        old_settings = termios.tcgetattr(sys.stdin)
    try:
        main()
    finally:
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
