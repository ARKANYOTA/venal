import os


class Globals:
    Player = None
    Args = None
    Mouse = None
    Menu = None
    Windows = None

    def __init__(self) -> None:
        self.term_x, self.term_y = os.get_terminal_size()

    def refresh(self) -> None:
        self.term_x, self.term_y = os.get_terminal_size()
        self.Player.init_txt_frame()
        self.Player.ProgressBar.set_actulize()

    def quit_player(self) -> None:
        self.Player.running = False
        if self.Player.Globals.Mouse.mouse_active:
            self.Player.Globals.Mouse.mouse_active = False
            self.Player.mouse_thread.join()


class App:
    Player = None

    def __init__(self) -> None:
        self.path = ""
