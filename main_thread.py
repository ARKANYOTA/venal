import math
import cv2
import os
import numpy as np
import time

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from multiprocessing.pool import ThreadPool
from queue import Queue

import asyncio


VIDEO_FILE_NAME = "a.mkv"
TERMINALX, TERMINALY = os.get_terminal_size()


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


def print_screen(txt_frame, nb_frames, deltat):
    print("\033[0;0H" + txt_frame + "\033[0m" + "\033[0;0H" + str(nb_frames) + "fps: " + str(int(1 / (time.time() - deltat))))


def get_frame_generator():
    cap, max_frames = read_video(VIDEO_FILE_NAME)
    yield max_frames
    for i in range(max_frames):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (TERMINALX, TERMINALY))
        yield frame, i


def boucle_screen(frame):
    txt_frame = ""
    for yi in range(len(frame)):
        for xi in range(len(frame[yi])):
            r, g, b = frame[yi][xi]
            txt_frame += f"\033[38;2;{r};{g};{b}m\u2588"
        txt_frame += "\n"
    return txt_frame



async def get_all_frames(all_frames, get_frame, max_frames):
    with tqdm(total=max_frames, desc="Threading #1 get All frames") as pbar:
        for [frame, _] in get_frame:
            all_frames.put(frame)
            pbar.update(1)


async  def resolve_all_frames(all_frames, all_resolved, get_frame, max_frames):
    with tqdm(total=max_frames, desc="Threading #2 resolve All frames") as pbar:
        for i in range(max_frames):
            nxt = all_frames.get(block=True)
            all_resolved.put(boucle_screen(nxt))
            pbar.update(1)


def main():
    get_frame = get_frame_generator()
    max_frames = next(get_frame)
    print(f"x: {TERMINALX} y: {TERMINALY} | {max_frames}")

    all_frames = Queue()
    all_resolved = Queue()
    tasks = []

    tasks.append(get_all_frames(all_frames, get_frame, max_frames))
    tasks.append(resolve_all_frames(all_frames, all_resolved, get_frame, max_frames))

    asyncio.run(asyncio.gather(*tasks))

    # pool_frames = ThreadPool(processes=os.cpu_count())

    # worker1 = pool_frames.apply_async(get_all_frames, args=(all_frames, get_frame, max_frames))
    # worker2 = pool_frames.apply_async(resolve_all_frames, args=(all_frames, all_resolved, get_frame, max_frames))

    # worker1.wait()
    # worker2.wait()
    print("all_resolved")

    # with tqdm(total=max_frames, desc="Threading") as pbar:
    #     all_frames = [fr for fr in tqdm(get_frame, desc="All Frames")]
    #     pool = ThreadPool(10)
    #     threads = []
    #     for i in tqdm(range(max_frames), desc="Set in threads", leave=False):
    #         thread = pool.apply_async(boucle_screen, args=(all_frames[i], pbar))
    #         threads.append(thread)
    #     for thread in threads:
    #         thread.wait()
    #         txt_frame = thread.get()
    #     pool.close()
    #     pool.join()


if __name__ == "__main__":
    main()
