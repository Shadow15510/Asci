from random import randint
from mapset import *


class Screen:
    def __init__(self):
        self._data = [[" " for _ in range(21)] for _ in range(6)]

    def set_cell(self, x, y, value):
        self._data[y][x] = value
        
    def get_cell(self, x, y):
        return self._data[y][x]

    def load(self, value):
        for y, line in enumerate(value.splitlines()[1:]):
            for x, char in enumerate(line):
                self._data[y][x] = char

    def display(self):
        string = ""
        for line in self._data:
            print("".join(line))
        return input("> ")


class Asci:
    def __init__(self, stat=[0, 100, 1, True], opus_nb=1):
        # Load stats
        self.xp = stat[0]
        self.pv = stat[1]
        self.current_map = stat[2]
        self.outdoor = stat[3]
        
        # Initialize player's position
        self.x = 10
        self.y = 5

        # Misc initialisation
        self.screen = Screen()
        self.end = 100

    def new_map(self):
        self.x = 10
        self.y = 5
        self.current_map = randint(1, 7)

    def mainloop(self):
        key = key_buffer = 0
        while key != 9 and self.pv > 0 and self.xp < self.end:
            self.screen.load(get_map(self.current_map, self.outdoor))

            self.screen.set_cell(self.x, self.y, "@")
            key = convert(self.screen.display())
            self.screen.set_cell(self.x, self.y, " ")

            if not key: key = key_buffer
            self.keyboard_input(key)

    def keyboard_input(self, key):
        # Left
        if key == 1:
            if self.x - 1 < 0: self.new_map()
            else: self.x -= 1

        # Right
        if key == 3:
            if self.x + 1 > 21: self.new_map()
            else: self.x += 1

        # Up
        if key == 5:
            if self.y - 1 < 0: self.new_map()
            else: self.y -= 1

        # Down
        if key == 2:
            if self.y + 1 > 6: self.new_map()
            else: self.y += 1

        # Stat
        if key == 8:
            pass

        # Action
        if key == 7:
            pass

        # Quit
        if key == 9:
            pass


def convert(n):
    try: return int(n)
    except: return 0

if __name__ == "__main__":
    game = Asci()
    game.mainloop()
    