import time
import cv2


class Template:
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
        time_after = time.strftime(" %H:%M ", time.gmtime(
            (Player.cap.get(cv2.CAP_PROP_FRAME_COUNT) - Player.cap.get(cv2.CAP_PROP_POS_FRAMES)) / Player.fps))
        Player.txt_frames[Globals.term_y - 5][19] = f"\033[0m{Template.top_left}"
        Player.txt_frames[Globals.term_y - 4][19] = f"\033[0m{Template.left}"
        Player.txt_frames[Globals.term_y - 3][19] = f"\033[0m{Template.bottom_left}"
        for y in range(Globals.term_x - 40):
            Player.txt_frames[Globals.term_y - 5][20 + y] = Template.top
            Player.txt_frames[Globals.term_y - 3][20 + y] = Template.bottom
        for y in range(Globals.term_x - 54):
            Player.txt_frames[Globals.term_y - 4][27 + y] = (
                Template.block if int(
                    Player.cap.get(cv2.CAP_PROP_POS_FRAMES) / Player.cap.get(cv2.CAP_PROP_FRAME_COUNT) * (
                                Globals.term_x - 54)) > y else Template.future
            )
        for y in range(len(time_before)):
            Player.txt_frames[Globals.term_y - 4][20 + y] = time_before[y]
        for y in range(len(time_after)):
            Player.txt_frames[Globals.term_y - 4][20 + Globals.term_x - 47 + y] = time_after[y]
        Player.txt_frames[Globals.term_y - 5][19 + Globals.term_x - 40] = Template.top_right
        Player.txt_frames[Globals.term_y - 4][19 + Globals.term_x - 40] = Template.right
        Player.txt_frames[Globals.term_y - 3][19 + Globals.term_x - 40] = Template.bottom_right

    def show_status(self) -> None:
        Player = self.Player
        Globals = Player.Globals

        start_y = int(Globals.term_y / 2 - 3)
        start_x1 = int(Globals.term_x / 2 - 4)
        start_x2 = start_x1 + 6
        for y in range(5):
            for x in range(2):
                Player.txt_frames[start_y + y][start_x1 + x] = f"\033[0m{Template.block}"
                Player.txt_frames[start_y + y][start_x2 + x] = f"\033[0m{Template.block}"

    def set_actulize(self) -> None:
        self.actu = True

    def set_pause(self) -> None:
        self.pause = not self.pause
        self.set_actulize()

    def set_status(self) -> None:
        self.status = not self.status
        self.set_actulize()

    def is_in_bar(self, x, y) -> bool:
        Player = self.Player
        Globals = Player.Globals
        if 20 <= x <= Globals.term_x - 20 and Globals.term_y - 5 <= y <= Globals.term_y - 3:
            return True
        return False

    def get_bar_pos(self) -> int:
        return int(self.Player.cap.get(cv2.CAP_PROP_POS_FRAMES) / self.Player.cap.get(cv2.CAP_PROP_FRAME_COUNT) * (
                    self.Player.Globals.term_x - 54))

    def goto_frame(self, frame) -> None:
        self.Player.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        self.set_actulize()

    def set_play(self) -> None:
        self.pause = False
        self.set_actulize()

    def is_play(self) -> bool:
        return not self.pause

    def is_pause(self) -> bool:
        return self.pause
