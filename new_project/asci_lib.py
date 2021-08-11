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
        self._data = [[" " for _ in range(21)] for _ in range(6)]
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

    def _new_map(self):
        self.x = 10
        self.y = 5
        self.current_map = randint(1, 7)
        print("Nouveau quartier :", self.current_map)

    def _cell_test(self, direction):
        # Left
        if direction == 1:
            if self.x - 1 < 0: return -1
            else: cell = self.screen.get_cell(self.x - 1, self.y)

        # Right
        if direction == 3:
            if self.x + 1 >= 21: return -1
            else: cell = self.screen.get_cell(self.x + 1, self.y)

        # Up
        if direction == 5:
            if self.y - 1 < 0: return -1
            else: cell = self.screen.get_cell(self.x, self.y - 1)

        # Down
        if direction == 2:
            if self.y + 1 >= 6: return -1
            else: cell = self.screen.get_cell(self.x, self.y + 1)

        cell_patterns = (" @", "^", "*", "$")
        for index, pattern in enumerate(cell_patterns):
            if cell in pattern: return index + 1

        return 0

    def mainloop(self):
        key = key_buffer = 0
        while key != 9 and self.pv > 0 and self.xp < self.end:
            self.screen.load(get_map(self.current_map, self.outdoor))

            self.screen.set_cell(self.x, self.y, "@")
            key = convert(self.screen.display())

            if not key: key = key_buffer
            else: key_buffer = key

            self.keyboard_input(key)

    def keyboard_input(self, key):
        # Left
        if key == 1:
            cell_test = self._cell_test(1)
            if cell_test == 1: self.x -= 1

        # Right
        if key == 3:
            cell_test = self._cell_test(3)
            if cell_test == 1: self.x += 1

        # Up
        if key == 5:
            cell_test = self._cell_test(5)
            if cell_test == 1: self.y -= 1

        # Down
        if key == 2:
            cell_test = self._cell_test(2)
            if cell_test == 1: self.y += 1

        if key in (1, 2, 3, 5):
            if cell_test < 0: self._new_map()

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

    