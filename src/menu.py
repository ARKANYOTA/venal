#  Menu
# \/
# [MenuItem|MenuItem|MenuItem|MenuItem]
#          |SubMenu |
#          |SubMenu |
#          |SubMenu > ScrollMenu|
#          |SubMenu |           |
#          |SubMenu |           |
#          |SubMenu |___________|
#          |SubMenu |
class ScrollMenu:
    def __init__(self, name: str, action: callable = None):
        self.name = name
        self.action = action


class SubMenu:
    def __init__(self, name: str, action: callable = None):
        self.name = name
        self.action = action
        self.scroll_menu_items: list[ScrollMenu] = []

    def add(self, scroll_menu_item: ScrollMenu):
        self.scroll_menu_items.append(scroll_menu_item)


class MenuItem:
    def __init__(self, text: str, action: callable = None, call_key: str = "") -> None:
        self.text = text
        self.action = action
        self.submenu_items: list[SubMenu] = []
        self.Menu: Menu = None
        self.call_key = call_key

    def add(self, submenu_item: SubMenu):
        self.submenu_items.append(submenu_item)

    def call_action(self):
        if self.action is not None:
            self.action()


class Menu:
    def __init__(self, player) -> None:
        self.player = player
        self.menu_items: list[MenuItem] = []
        self.is_active = False
        self.witch_menu_open = -1
        self.start()

    def add(self, menu_item: MenuItem):
        self.menu_items.append(menu_item)

    def start(self):
        media_menu = MenuItem("(M)edia", None, "M")
        open_file_menu = SubMenu("Open File", True)  # self.player.open_file)
        media_menu.add(open_file_menu)
        open_recent_menu = SubMenu("Open Recent")
        media_menu.add(open_recent_menu)
        self.add(media_menu)
        exit_menu = MenuItem("(E)xit", self.player.Globals.quit_player, "E")
        self.add(exit_menu)

    def show(self):
        text_frame = self.player.txt_frames

        first_line = ["\033[0m\033[30;107m "]
        for ind, i in enumerate(self.menu_items):
            first_line.append(" ")
            if self.witch_menu_open == ind:
                first_line.append("\033[31;107m" + i.text[0])
                for j in i.text[1:-1]:
                    first_line.append(j)
                first_line.append(i.text[-1]+"\033[30;107m")
            else:
                for j in i.text:
                    first_line.append(j)
            first_line.append(" ")
            first_line.append("|")

        for i in range(len(first_line)):
            text_frame[0][i] = first_line[i]

    def close_menu(self):
        self.witch_menu_open = -1
        self.is_active = False

    def match_key(self, key: str):
        for ind, i in enumerate(self.menu_items):
            if i.call_key == key:
                self.witch_menu_open = ind
        return None
