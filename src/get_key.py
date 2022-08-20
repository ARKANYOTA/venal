import os

try:
    # POSIX system: Create and return a getch that manipulates the tty
    import termios, sys
    import tty, select

    # Read arrow keys correctly
    def get_key():
        firstChar = sys.stdin.read(1)
        if firstChar == "\x1b":
            return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[sys.stdin.read(1) + sys.stdin.read(1)]
        else:
            return firstChar

except ImportError:
    # Non-POSIX: Return msvcrt's (Windows') getch
    from msvcrt import getch, kbhit

    # Read arrow keys correctly
    def get_key():
        firstChar = getch()
        if firstChar == b"\xe0":
            return {b"H": "up", b"P": "down", b"M": "right", b"K": "left"}[getch()]
        else:
            return firstChar.decode("utf-8")


def is_data():
    if os.name == "nt":
        return kbhit()
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def match_key(player):
    if not is_data():
        return
    match get_key():
        case "up":
            player.video_add(10000)
        case "down":
            player.video_add(-1000)
        case "right":
            player.video_add(300)
        case "left":
            player.video_add(-300)
        case "r":
            print("\033[0;0H\033[2J")
            player.Globals.refresh()
        case " ":
            player.ProgressBar.set_pause()
        case "p":
            player.ProgressBar.set_status()
