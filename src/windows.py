from src.get_mouse import KeyEvent
from src.progress_bar import Template


class WindowsElement:
    def __init__(self, name: str, id: str, player):
        self.name = name
        self.id = id
        self.size = (30, 10)
        self.player = player

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
        for yi in range(height-2):
            text_frames[top_left_y + yi+1][top_left_x] = "\033[0m"+Template.left
            text_frames[top_left_y + yi+1][top_left_x + width - 1] = Template.right
        # Horizontal lines
        for xi in range(width-2):
            text_frames[top_left_y][top_left_x + xi+1] = Template.top
            text_frames[top_left_y + height - 1][top_left_x + xi+1] = Template.bottom
        # Corners
        text_frames[top_left_y][top_left_x] = "\033[0m"+Template.top_left+"\033[30;107m"
        text_frames[top_left_y][top_left_x + width - 1] = Template.top_right
        text_frames[top_left_y + height - 1][top_left_x] = "\033[0m"+Template.bottom_left
        text_frames[top_left_y + height - 1][top_left_x + width - 1] = Template.bottom_right
        # Title
        for yi in range(len(self.name)-1):
            text_frames[top_left_y][top_left_x + 1 + yi] = self.name[yi]
        text_frames[top_left_y][top_left_x + 1 + len(self.name)-1] = self.name[-1]+"\033[0m"

        self.player.ProgressBar.set_actulize()




        # draw content



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
        file_open_windows = WindowsElement("Open File", "file_open_windows", player)
        open_recent_windows = WindowsElement("Open recent", "open_recent_windows", player)
        help_windows = WindowsElement("Help", "help_windows", player)
        self.windows_list.append(file_open_windows)
        self.windows_list.append(open_recent_windows)
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
            self.active_windows.show()

    def match_key(self, key: str):
        match key:
            case "esc" | "q":
                self.has_active_windows = False
                self.active_windows = None
                return True
            case "up" | "down" | "left" | "right":
                # overwrite this arrow keys if windows has active windows
                return True
            case KeyEvent():
                self.match_mouse(key)
                return True
        return None

    def match_mouse(self, mouse_event):
        # Interact with menu
        pass