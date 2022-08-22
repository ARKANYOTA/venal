from src.progress_bar import ProgressBar
from src.application import App, Globals

import cv2


class Player:
    cap: any = None
    fps: int = 0
    txt_frames: list[list[str]] = []
    running = True
    main_thread = None
    mouse_thread = None

    App: App = App()
    Globals: Globals = Globals()
    ProgressBar: ProgressBar = ProgressBar()

    def __init__(self, path: str, start: int = 0) -> None:
        self.App.path = path
        self.ProgressBar.Player = self
        self.Globals.Player = self

        self.init_txt_frame()
        self.p_start(start)

    def p_start(self, start: int):
        self.cap = cv2.VideoCapture(self.App.path)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self._get_frames = self.__get_frames()

    def __get_frames(self):
        while self.cap.isOpened():
            if self.ProgressBar.pause:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)
            ret, frame = self.cap.read()
            if not ret:
                self.Globals.quit_player()
            if frame is None:
                exit()
            frame = cv2.resize(frame, (self.Globals.term_x, self.Globals.term_y))
            if ret:
                yield frame
            else:
                break

    def screen_loop(self):
        frame = self.get_frame()
        for yi in range(len(frame)):
            for xi in range(len(frame[yi])):
                r, g, b = frame[yi][xi]
                self.txt_frames[yi][xi] = f"\033[38;2;{b};{g};{r}m\u2588"

    def video_add(self, frame: int):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) + frame)

    def init_txt_frame(self):
        self.txt_frames = [[""] * self.Globals.term_x for _ in range(self.Globals.term_y)]

    def get_frame(self):
        next_frame = next(self._get_frames)
        return next_frame

    def print_frames(self):
        try:
            print(f"\033[0;0H{''.join([''.join(i) for i in self.txt_frames])}\033[0;0H")
        except BlockingIOError:
            pass

