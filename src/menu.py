#  Menu
#
# [MenuItem|MenuItem|MenuItem|MenuItem]
#          |SubMenu |
#          |SubMenu |
#          |SubMenu |
#          |SubMenu |
#          |SubMenu |
#          |SubMenu |
#          |SubMenu |
class MenuParent:
    def __init__(self, text: str, action: callable = None, call_key: str = None, condition: callable = None,
                 args: tuple = None) -> None:
        self.text = text
        self.action = action
        self.condition = condition  # if is return True, then not selectable
        self.menu_items = []
        self.args = args
        self.call_key = call_key
        self.size = 20

    def add(self, menu_item):
        self.menu_items.append(menu_item)

    def call_action(self):
        if self.action is None:
            return "ToSelect"
        if self.menu_items:
            return "ToSelect"
        if not self.condition_check():
            return "NoneSelectable"  # Do nothing
        self.action()

    def condition_check(self):
        if self.condition is None:
            return True
        return self.condition()


class SubMenu(MenuParent):
    def __init__(self, text: str, action: callable, call_key: str = None, condition: callable = None,
                 args: tuple = None) -> None:
        super().__init__(text, action, call_key, condition, args)


class MenuItem(MenuParent):
    def __init__(self, text: str, action: callable = None, call_key: str = None, condition: callable = None,
                 args: tuple = None) -> None:
        super().__init__(text, action, call_key, condition, args)


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
        open_file_menu = SubMenu("Open (F)ile", None, "F")  # self.player.open_file
        media_menu.add(open_file_menu)
        open_recent_menu = SubMenu("Open (R)ecent", None, "R")  # self.player.open_recent
        media_menu.add(open_recent_menu)
        self.add(media_menu)
        playback_menu = MenuItem("Play(B)ack", None, "B")
        playback_menu.add(
            MenuItem("(P)lay", self.player.ProgressBar.set_play, "P", condition=self.player.ProgressBar.is_pause))
        playback_menu.add(
            MenuItem("(P)ause", self.player.ProgressBar.set_pause, "P", condition=self.player.ProgressBar.is_play))
        self.add(playback_menu)

        audio_menu = MenuItem("(A)udio", None, "A")
        audio_menu.add(SubMenu("TODO", None))
        self.add(audio_menu)
        subtitle_menu = MenuItem("(S)ubtitle", None, "S")
        subtitle_menu.add(SubMenu("TODO", None))
        self.add(subtitle_menu)
        exit_menu = MenuItem("(E)xit", self.player.Globals.quit_player, "E")
        self.add(exit_menu)
        help_menu = MenuItem("(H)elp", None, "H")
        help_menu.add(SubMenu("TODO", None))
        help_menu.add(SubMenu("TODO", None))
        help_menu.add(SubMenu("TODO", None))
        help_menu.add(SubMenu("TODO", None))
        help_menu.add(SubMenu("TODO", None))
        self.add(help_menu)

    def show(self):
        text_frame = self.player.txt_frames

        # Fist line of the menu
        first_line = ["\033[0m\033[30;107m|"]
        for ind, i in enumerate(self.menu_items):
            if self.witch_menu_open == ind:
                first_line.append("\033[30;104m ")
            else:
                first_line.append(" ")
            for j in f"{i.text:<{i.size - 3}}":  # -3 because of " | "
                first_line.append(j)
            if self.witch_menu_open == ind:
                first_line.append(" \033[30;107m")
            else:
                first_line.append(" ")
            first_line.append("|")

        for i in range(len(first_line)):
            text_frame[0][i] = first_line[i]

        # Extand the menu if needed show SubMenus
        if self.witch_menu_open != -1:
            SubMenuToShow: MenuItem = self.menu_items[self.witch_menu_open]
            if SubMenuToShow.call_action() == "ToSelect":
                for ind, i in enumerate(SubMenuToShow.menu_items):
                    if i.condition_check():
                        text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open] = "\033[30;107m|"
                    else:
                        text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open] = "\033[97;100m|"
                    text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open + 1] = " "
                    for jnd, j in enumerate(f"{i.text:<{i.size}}"):
                        text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open + 2 + jnd] = j
                    text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open + 2 + i.size] = " "
                    text_frame[ind + 1][SubMenuToShow.size * self.witch_menu_open + 2 + i.size + 1] = "|\033[0m"
        self.player.ProgressBar.set_actulize()  # TODO Move this line

    def close_menu(self):
        self.witch_menu_open = -1
        self.is_active = False
        self.player.ProgressBar.set_actulize()

    def match_key(self, key: str):
        for ind, menu_item in enumerate(self.menu_items):
            if self.witch_menu_open == ind:
                if menu_item.call_key == key:
                    self.witch_menu_open = -1
                    self.player.ProgressBar.set_actulize()
                    return True
                else:
                    for submenu_item in menu_item.menu_items:
                        if submenu_item.condition_check():
                            if submenu_item.call_key == key:
                                submenu_item.call_action()
                                return True
            if menu_item.call_key == key:
                self.witch_menu_open = ind
                return True
        return None

    def mouse_press_in_menu(self, x: int, y: int):  # TOFIX / TODO
        # Check if the mouse is in first line of the menu
        if self.is_active:
            if y == 1:
                for ind, i in enumerate(self.menu_items):
                    if ind * i.size + 1 <= x <= ind * i.size + i.size + 1:
                        self.witch_menu_open = ind
                        return True
            else:
                if self.witch_menu_open != -1:
                    for ind, submenu_item in enumerate(self.menu_items[self.witch_menu_open].menu_items):
                        if y == ind + 2:
                            if submenu_item.size * self.witch_menu_open <= x <= submenu_item.size * self.witch_menu_open + 2 + submenu_item.size + 2:
                                submenu_item.call_action()
                                return True
        return False
