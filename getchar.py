import sys
import tty
import termios


# class for checking keyboard input
class Getchar:
    def __init__(self):
        pass

    def getch(self):
        settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key


# Example usage
if __name__ == "__main__":
    getchar = Getchar()
    while True:
        key = getchar.getch()
        if key:
            print("You pressed:", key)
