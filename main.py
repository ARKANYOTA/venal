import math

import cv2
import os
from colors import COLORS
from math import sqrt
import time
import asyncio
import argparse
import tqdm


# https://stackoverflow.com/questions/54242194/python-find-the-closest-color-to-a-color-from-giving-list-of-colors
def get_closest_color(rgb):
    r, g, b = rgb
    color_diff = math.inf
    closest_color = None
    for color in COLORS:
        cr, cg, cb = color[0]
        if sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2) < color_diff:
            color_diff = sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            closest_color = color[1]
    return closest_color


VIDEO_FILE_NAME = "a.mkv"
TERMINALX, TERMINALY = os.get_terminal_size()


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap


def get_frame(cap):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (TERMINALX, TERMINALY))
    return ret, frame


def boucle_screen(frame, txt_frame):
    for yi in range(len(frame)):
        for xi in range(len(frame[yi])):
            # if frame[yi][xi][0] != oldframe[yi][xi]] and frame[yi][xi][1] != oldframe[yi][xi][1] and frame[yi][xi][2] != oldframe[yi][xi][2]:
            # if old_frame[yi][xi] != get_closest_color(frame[yi][xi]):
            # txt_frame += f"\033[{get_closest_color(frame[yi][xi])}m\u2588"
            r, g, b = frame[yi][xi]
            txt_frame[yi][xi] = f"\033[38;2;{b};{g};{r}m\u2588"
    return txt_frame


def print_screen(txt_frame, nb_frames, deltat, TOTAL_FRAMES):
    print(f"\033[0;0H{''.join([''.join(i) for i in txt_frame])}")


def main():
    ecx = 0
    nb_frames = 0
    cap = read_video(args.path)
    TOTAL_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Wait, it's loading...")
    for i in tqdm.trange(args.startat):
        cap.grab()
    nb_frames = args.startat
    ret, frame = get_frame(cap)
    txt_frame = [[""] * TERMINALX for _ in range(TERMINALY)]
    while ret:  # and ecx < 1000:
        deltat = time.time()
        ecx += 1
        nb_frames += 1
        _, frame = get_frame(cap)
        txt_frame = boucle_screen(frame, txt_frame)

        print_screen(txt_frame, nb_frames, deltat, TOTAL_FRAMES)
        # Do 24 frame per second in take the time to print the screen
        time_to_wait = 1 / args.fps - (time.time() - deltat)
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        print(f"\033[0m\033[0;0H frames: {str(nb_frames)}/{TOTAL_FRAMES} fps: {1 / (time.time() - deltat):.2f} loose: {time_to_wait*1000:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vlc on terminal.')
    parser.add_argument('path', metavar='path', type=str, nargs="?", help='Path to video file.', const="a.mkv", default="a.mkv")
    parser.add_argument('startat', metavar='start-at', type=int, nargs="?", help='Start at frame.', const=0, default=0)
    parser.add_argument('fps', metavar='fps', type=int, help='FPS.', const=24, nargs='?', default=24)

    args = parser.parse_args()
    print(args.path)
    VIDEO_FILE_NAME = args.path[0]
    main()

    # print(colors.colors)
