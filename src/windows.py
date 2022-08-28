import os
import time

import cv2

from src.get_mouse import KeyEvent
from src.progress_bar import Template


class WindowsElement:
    def __init__(self, name: str, id: str, player, size: tuple = (30, 10)):
        self.name = name
        self.id = id
        self.size = size
        self.player = player
        if self.id == "file_open_windows":
            self.file_open_index = 0
            self.file_open_decalage = 0
            self.file_open_list = []
            self.path = os.getcwd()
            if self.path is None:
                self.path = "/" if os.name != "nt" else "C:\\"


    def show(self):
        player = self.player
        text_frames = player.txt_frames
        termx = player.Globals.term_x
        termy = player.Globals.term_y
        width = self.size[0]
        height = self.size[1]
        centerx = termx // 2
        centery = termy // 2
        top_left_x = centerx - (width // 2)
        top_left_y = centery - (height // 2)

        # clean inside
        for yi in range(height):
            for xi in range(width):
                text_frames[top_left_y + yi][top_left_x + xi] = " "
            text_frames = self.player.txt_frames

        # draw border
        # Vertical lines
        for yi in range(height - 2):
            text_frames[top_left_y + yi + 1][top_left_x] = "\033[0m" + Template.left
            text_frames[top_left_y + yi + 1][top_left_x + width - 1] = Template.right
        # Horizontal lines
        for xi in range(width - 2):
            text_frames[top_left_y][top_left_x + xi + 1] = Template.top
            text_frames[top_left_y + height - 1][top_left_x + xi + 1] = Template.bottom
        # Corners
        text_frames[top_left_y][top_left_x] = "\033[0m" + Template.top_left + "\033[30;107m"
        text_frames[top_left_y][top_left_x + width - 1] = Template.top_right
        text_frames[top_left_y + height - 1][top_left_x] = "\033[0m" + Template.bottom_left
        text_frames[top_left_y + height - 1][top_left_x + width - 1] = Template.bottom_right
        # Title
        for yi in range(len(self.name) - 1):
            text_frames[top_left_y][top_left_x + 1 + yi] = self.name[yi]
        text_frames[top_left_y][top_left_x + 1 + len(self.name) - 1] = self.name[-1] + "\033[0m"

        self.player.ProgressBar.set_actulize()

        # draw content
        if self.id == "file_open_windows":
            self.draw_file_open_window()
        elif self.id == "info_windows":
            self.draw_info_window()


    def draw_file_open_window(self):
        # path
        text_frames = self.player.txt_frames
        termx = self.player.Globals.term_x
        termy = self.player.Globals.term_y
        width = self.size[0]
        height = self.size[1]
        centerx = termx // 2
        centery = termy // 2
        top_left_x = centerx - (width // 2)
        top_left_y = centery - (height // 2)


        # draw path
        for xi in range(width - 2):
            text_frames[top_left_y+2][top_left_x + xi + 1] = Template.top
        for xi in range(len(self.path)):
            text_frames[top_left_y+1][top_left_x + xi + 1] = self.path[xi]

        # calcule file_open_decalage
        if self.file_open_index > self.size[1] - 7:
            self.file_open_decalage = self.file_open_index - (self.size[1] - 7)
        else:
            self.file_open_decalage = 0

        # list folders and files sort with folders first
        self.file_open_list = [".."] + os.listdir(self.path)
        self.file_open_list.sort(key=lambda x: os.path.isdir(os.path.join(self.path, x)), reverse=True)
        self.file_open_list = self.file_open_list[self.file_open_decalage:self.size[1] - 5+self.file_open_decalage]
        for i in range(len(self.file_open_list)):
            self.file_open_list[i] = ("\uf115 " if os.path.isdir(os.path.join(self.path, self.file_open_list[i])) else "\uf1c8 ") + self.file_open_list[i]


        for yi in range(height - 4):
            for xi in range(width - 2):
                text_frames[top_left_y+3+yi][top_left_x + xi + 1] = " "
        for yi in range(len(self.file_open_list)):
            if yi == self.file_open_index - self.file_open_decalage:
                text_frames[top_left_y+3+yi][top_left_x + 1] = "\033[34m "
            for xi in range(len(self.file_open_list[yi])):
                text_frames[top_left_y+3+yi][top_left_x + xi + 2] = self.file_open_list[yi][xi]
        self.player.ProgressBar.set_actulize()

    def draw_info_window(self):
        text_frames = self.player.txt_frames
        termx = self.player.Globals.term_x
        termy = self.player.Globals.term_y
        width = self.size[0]
        height = self.size[1]
        centerx = termx // 2
        centery = termy // 2
        top_left_x = centerx - (width // 2)
        top_left_y = centery - (height // 2)

        time_before = time.strftime(" %H:%M ", time.gmtime(self.player.cap.get(cv2.CAP_PROP_POS_FRAMES) / self.player.fps))
        time_after = time.strftime(" %H:%M ", time.gmtime((self.player.cap.get(cv2.CAP_PROP_FRAME_COUNT) - self.player.cap.get(cv2.CAP_PROP_POS_FRAMES)) / self.player.fps))
        duration = time.strftime(" %H:%M ", time.gmtime(self.player.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.player.fps))
        infos = {
           #  "Current Volume": self.player.Globals.current_volume,
           #  "Current Speed": self.player.Globals.current_speed,
           #  "Current Position": self.player.Globals.current_position,
           #  "Current Subtitle": self.player.Globals.current_subtitle,
            "Status": "Pause" if self.player.ProgressBar.pause else "Play",
            "Current File": self.player.App.path,
            "Current Time": time_before,
            "Time Left": time_after,
            "Duration": duration,
        }

        for yi, item in enumerate(infos.items()):
            text_to_draw = item[0] + ": " + item[1]
            for yii, it in enumerate(text_to_draw):
                text_frames[top_left_y+yi+1][top_left_x + yii + 1] = it
        self.player.ProgressBar.set_actulize()

    def __repr__(self):
        return self.name



class Windows:
    def __init__(self, player) -> None:
        self.has_active_windows = False
        self.windows_list: list[WindowsElement] = []
        self.active_windows = None
        self.player = player
        self.start()

    def start(self):
        player = self.player
        file_open_windows = WindowsElement("Open File", "file_open_windows", player, (90, 40))
        open_recent_windows = WindowsElement("Open recent", "open_recent_windows", player)
        info_windows = WindowsElement("Infos", "info_windows", player)
        help_windows = WindowsElement("Help", "help_windows", player)
        self.windows_list.append(file_open_windows)
        self.windows_list.append(open_recent_windows)
        self.windows_list.append(info_windows)
        self.windows_list.append(help_windows)

    def open_windows(self, windows_id: str):
        for windows in self.windows_list:
            if windows.id == windows_id:
                self.active_windows = windows
                self.has_active_windows = True
                return True
        return False

    def show(self):
        if self.has_active_windows:
            if self.player.Globals.term_x < self.active_windows.size[0]:
                return
            if self.player.Globals.term_y < self.active_windows.size[1]:
                return
            self.active_windows.show()

    def match_key(self, key: str):
        windows = self.active_windows
        if not windows:
            return False
        match key:
            case "esc" | "q":
                self.has_active_windows = False
                self.active_windows = None
                return True
            case "up" | "down" | "left" | "right":
                # overwrite this arrow keys if windows has active windows
                if windows.id == "file_open_windows":
                    if key == "up":
                        if windows.file_open_index > 0:
                            windows.file_open_index -= 1
                    elif key == "down":
                        if windows.file_open_index < len(os.listdir(windows.path)):
                            windows.file_open_index += 1
                            windows.player.ProgressBar.set_actulize()
                    self.player.ProgressBar.set_actulize()
                return True
            case "\n":
                if windows.id == "file_open_windows":
                    if windows.file_open_index == 0:
                        self.active_windows.path = os.path.dirname(self.active_windows.path)
                    else:  # TOVERIFY
                        if os.path.isdir(os.path.join(self.active_windows.path, windows.file_open_list[windows.file_open_index-windows.file_open_decalage][2:])):
                            self.active_windows.path = os.path.join(self.active_windows.path, windows.file_open_list[windows.file_open_index-windows.file_open_decalage][2:])
                        else:
                            self.active_windows.player.open_file(os.path.join(self.active_windows.path, windows.file_open_list[windows.file_open_index-windows.file_open_decalage][2:]))
                        windows.file_open_index = 0
                        windows.file_open_decalage = 0
                    self.player.ProgressBar.set_actulize()
                    return True
            case KeyEvent():
                self.match_mouse(key)
                return True
        return None

    def match_mouse(self, mouse_event):
        # Interact with menu
        pass
