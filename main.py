import cv2
import os
import time
import argparse
import sys
import select
import tty
import termios




class GLOBALS:
    CAP = None

# get keys
TERMINALX, TERMINALY = os.get_terminal_size()

def get_frame():
    GLOBALS.CAP = cv2.VideoCapture(args.path)
    GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, args.startat)

    while GLOBALS.CAP.isOpened():
        ret, frame = GLOBALS.CAP.read()
        if frame is None:
            exit()
        frame = cv2.resize(frame, (TERMINALX, TERMINALY))
        if ret:
            yield frame
        else:
            break


def boucle_screen(frame, txt_frame):
    for yi in range(len(frame)):
        for xi in range(len(frame[yi])):
            r, g, b = frame[yi][xi]
            txt_frame[yi][xi] = f"\033[38;2;{b};{g};{r}m\u2588"
    return txt_frame


def print_screen(txt_frame, nb_frames, deltat):
    print(f"\033[0;0H{''.join([''.join(i) for i in txt_frame])}")


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
def main():
    frames = get_frame()
    nb_frames = args.startat
    frame = next(frames)
    txt_frame = [[""] * TERMINALX for _ in range(TERMINALY)]

    tty.setcbreak(sys.stdin.fileno())
    while True:
        if isData():
            c = sys.stdin.read(1)
            if c == "\x1b":
                d = sys.stdin.read(1)
                z = sys.stdin.read(1)
                if d == "[":
                    if z == 'A':
                        GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) - 300)
                    elif z == 'B':
                        GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) + 300)
                    elif z == 'C':
                        GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) + 10000)
                    elif z == 'D':
                        GLOBALS.CAP.set(cv2.CAP_PROP_POS_FRAMES, GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES) - 1000)
        deltat = time.time()
        nb_frames += 1
        frame = next(frames)
        txt_frame = boucle_screen(frame, txt_frame)

        print_screen(txt_frame, nb_frames, deltat)
        time_to_wait = 1 / args.fps - (time.time() - deltat)
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        print(f"\033[0m\033[0;0H frames: {str(GLOBALS.CAP.get(cv2.CAP_PROP_POS_FRAMES))} fps: {1 / (time.time() - deltat):.2f}"
              f" loose: {time_to_wait * 1000:.2f}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vlc on terminal.')
    parser.add_argument('path', metavar='path', type=str, nargs="?", help='Path to video file.', const="a.mkv",
                        default="a.mkv")
    parser.add_argument('startat', metavar='start-at', type=int, nargs="?", help='Start at frame.', const=0, default=0)
    parser.add_argument('fps', metavar='fps', type=int, help='FPS.', const=24, nargs='?', default=24)

    args = parser.parse_args()

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        main()
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


