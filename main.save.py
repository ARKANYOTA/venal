import math

import cv2
import os
import numpy as np
from colors import COLORS
from math import sqrt
import time


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


def boucle_screen(frame):
    txt_frame = ""
    for yi in range(len(frame)):
        for xi in range(len(frame[yi])):
            # if frame[yi][xi][0] != oldframe[yi][xi]] and frame[yi][xi][1] != oldframe[yi][xi][1] and frame[yi][xi][2] != oldframe[yi][xi][2]:
            # if old_frame[yi][xi] != get_closest_color(frame[yi][xi]):
            # txt_frame += f"\033[{get_closest_color(frame[yi][xi])}m\u2588"
            r, g, b = frame[yi][xi]
            txt_frame += f"\033[38;2;{r};{g};{b}m\u2588"
        txt_frame += "\n"
    return txt_frame


def print_screen(txt_frame, nb_frames, deltat):
    print("\033[0;0H" + txt_frame + "\033[0m" + "\033[0;0H" + str(nb_frames) + "fps: " + str(int(1 / (time.time() - deltat))))


def main():
    ecx = 0
    nb_frames = 0
    cap = read_video(VIDEO_FILE_NAME)
    ret, frame = get_frame(cap)
    while ret and ecx < 1000:
        ecx += 1
        deltat = time.time()
        nb_frames += 1
        ret, frame = get_frame(cap)
        txt_frame = boucle_screen(frame)

        print_screen(txt_frame, nb_frames, deltat)



if __name__ == "__main__":
    main()
    # print(colors.colors)
