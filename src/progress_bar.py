from enum import Enum
import time
import cv2


class Template(Enum):
    top_left = "╭"
    top_right = "╮"
    bottom_left = "╰"
    bottom_right = "╯"
    top = "─"
    bottom = "─"
    left = "│"
    right = "│"
    block = "█"
    future = "┈"


class ProgressBar:
    Player = None

    def __init__(self) -> None:
        self.pause = False
        self.status = False
        self.actu = False

    def show(self) -> None:
        Player = self.Player
        Globals = Player.Globals

        time_before = time.strftime(" %H:%M ", time.gmtime(Player.cap.get(cv2.CAP_PROP_POS_FRAMES) / Player.fps))
        time_after = time.strftime(" %H:%M ", time.gmtime((Player.cap.get(cv2.CAP_PROP_FRAME_COUNT) - Player.cap.get(cv2.CAP_PROP_POS_FRAMES)) / Player.fps))
        Player.txt_frames[Globals.term_y - 5][19] = f"\033[0m{Template.top_left}"
        Player.txt_frames[Globals.term_y - 4][19] = f"\033[0m{Template.left}"
        Player.txt_frames[Globals.term_y - 3][19] = f"\033[0m{Template.bottom_left}"
        for y in range(Globals.term_x - 40):
            Player.txt_frames[Globals.term_y - 5][20 + y] = Template.top
            Player.txt_frames[Globals.term_y - 3][20 + y] = Template.bottom
        for y in range(Globals.term_x - 54):
            Player.txt_frames[Globals.term_y - 4][27 + y] = (
                Template.block if int(Player.cap.get(cv2.CAP_PROP_POS_FRAMES) / Player.cap.get(cv2.CAP_PROP_FRAME_COUNT) * (Globals.term_x - 54)) > y else Template.future
            )
        for y in range(len(time_before)):
            Player.txt_frames[Globals.term_y - 4][20 + y] = time_before[y]
        for y in range(len(time_after)):
            Player.txt_frames[Globals.term_y - 4][20 + Globals.term_x - 47 + y] = time_after[y]
        Player.txt_frames[Globals.term_y - 5][19 + Globals.term_x - 40] = Template.top_right
        Player.txt_frames[Globals.term_y - 4][19 + Globals.term_x - 40] = Template.right
        Player.txt_frames[Globals.term_y - 3][19 + Globals.term_x - 40] = Template.bottom_right

    def set_actulize(self) -> None:
        self.actu = True

    def set_pause(self) -> None:
        self.pause = not self.pause
        self.set_actulize()

    def set_status(self) -> None:
        self.status = not self.status
        self.set_actulize()
