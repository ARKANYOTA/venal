import os

class Globals:
    Player = None
    Args = None
    Mouse = None

    def __init__(self) -> None:
        self.term_x, self.term_y = os.get_terminal_size()

    def refresh(self) -> None:
        self.term_x, self.term_y = os.get_terminal_size()
        self.Player.init_txt_frame()
        self.Player.ProgressBar.set_actulize()


class App:
    Player = None

    def __init__(self) -> None:
        self.path = ""
