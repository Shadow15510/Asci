from random import randint

class Screen:
    def __init__(self, world, screen_width=21, screen_height=6):
        # Screen configuration
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._data = [[" " for _ in range(screen_width)] for _ in range(screen_height)]

        # Load map data
        self.set_world(world)


    def clear_data(self):
        self._data = [[" " for _ in range(self.screen_width)] for _ in range(self.screen_height)]

    def clear(self):
        print("\n" * self.screen_height)

    def set_world(self, world):
        self._world = [[char for char in line] for line in world.split("\n")[1:]]
        self.map_width = max([len(line) for line in self._world])
        self.map_height = len(self._world)

    def set_data(self, coords):
        x, y = coords
        for x_map in range(x, x + self.screen_width):
            for y_map in range(y, y + self.screen_height):
                self._data[y_map - y][x_map - x] = " "
                if 0 <= x_map < self.map_width and 0 <= y_map < self.map_height:
                    try: self._data[y_map - y][x_map - x] = self._world[y_map][x_map]
                    except: pass

    def set_cell(self, x, y, value):
        self._data[y][x] = value

    def display(self, return_input=True):
        for line in self._data:
            print("".join(line))

        if return_input: return input(">")

    def display_text(self, string):
        for paragraph in text_formater(string):
            if paragraph:
                self.clear()
                print(paragraph)
                return input(">")

    def get_cell(self, x, y):
        return self._data[y][x]

    def get_map_size(self):
        return self.map_width, self.map_height


class Asci:
    def __init__(self, maps, fn_dialogue, end_game, stat, data=[0, 100, 0, 0, 0], screen_width=21, screen_height=6):
        # Load save ; data = [XP, PV, map_id, x, y]
        self.data = data
        self.stat = stat

        # Load data
        self.maps = maps
        self.end_game = end_game

        # Custom functions
        self.get_dialogue = fn_dialogue

        # Screen configuration
        self.screen = Screen(maps[data[2]], screen_width, screen_height)
        self.map_width, self.map_height = self.screen.get_map_size()

    def _looked_case(self, direction):
        # Left
        if direction == 1:
            return self.data[3] + 9, self.data[4] + 3

        # Right
        elif direction == 3:
            return self.data[3] + 11, self.data[4] + 3

        # Up
        elif direction == 5:
            return self.data[3] + 10, self.data[4] + 2

        # Down
        elif direction == 2:
            return self.data[3] + 10, self.data[4] + 4

        return self.data[3] + 10, self.data[4] + 3

    def _cell_test(self, direction):
        if direction == 1:
            if self.data[-2] + 9 < 0: return -1
            else: cell = self.screen.get_cell(9, 3)
        if direction == 3:
            if self.data[-2] + 11 >= self.map_width: return -1
            else: cell = self.screen.get_cell(11, 3)
        if direction == 5:
            if self.data[-1] + 2 < 0: return -1
            else: cell = self.screen.get_cell(10, 2)
        if direction == 2:
            if self.data[-1] + 4 >= self.map_height: return -1
            else: cell = self.screen.get_cell(10, 4)

        cell_patterns = (" @", "^", "*", "$")
        for pattern_index in range(len(cell_patterns)):
            if cell in cell_patterns[pattern_index]: return pattern_index + 1

        return 0

    def _keyboard(self, key):
        # Interaction with map
        if key in (1, 3, 5, 2):
            cell_test = self._cell_test(key)
            
            # Enter house
            if cell_test == 2 or (self.data[2] and cell_test < 0):
                self.data[2], self.data[3], self.data[4] = self._get_map(key)
                if self.data[2]:
                    self.screen.set_world(self.maps[self.data[2]][0])
                else:
                    self.screen.set_world(self.maps[0])

            # PnJ
            elif cell_test == 3:
                self._chatting(key)

            # Fight
            elif cell_test == 4:
                pass

        # Left
        if key == 1 and cell_test == 1: self.data[3] -= 1
        # Right
        if key == 3 and cell_test == 1: self.data[3] += 1
        # Up
        if key == 5 and cell_test == 1: self.data[4] -= 1
        # Down
        if key == 2 and cell_test == 1: self.data[4] += 1

        # Stat
        if key == 8:
            self.screen.clear()
            print("<*> Statistiques <*>\nExperience ...: {0}\nPoints de vie : {1}\n<*> ------------ <*>".format(self.data[0], self.data[1]))
            input()

        # Quit
        if key == 9:
            self.screen.clear()
            print(self.stat, self.data)

        # /!\ TEST /!\ #
        if key == 7:
            print(self.data[-2:])
            input()
        # /!\ TEST /!\ #

    def _chatting(self, direction):
        x, y = self._looked_case(direction)

        # Read the dialogue
        dialogue = self.get_dialogue(self.data[0], self.data[1], self.data[2], x, y, self.stat)
        if type(dialogue) == dict:
            if self.data[0] in dialogue: dialogue = dialogue[self.data[0]]
            else: dialogue = dialogue["base"]
        
        # XP and PV modification
        self.data[0] += dialogue[0]
        self.data[1] += dialogue[1]

        # Stat modification
        for index in range(len(dialogue[4:])):
            stat[index] += dialogue[4 + index]

        answer_selected = self.screen.display_text(dialogue[2])
        if dialogue[3]: self.data[0] += convert(answer_selected)

    def _get_map(self, direction):
        x, y = self._looked_case(direction)
        current_map = self.data[2]

        if current_map:
            if (x, y) == self.maps[current_map][2]:
                return 0, self.maps[current_map][1][0] - 10, self.maps[current_map][1][1] - 3
        else:
            for index in range(1, len(self.maps)):
                if (x, y) == self.maps[index][1]:
                    return index, self.maps[index][2][0] - 10, self.maps[index][2][1] - 3

        return current_map, self.data[3], self.data[4]

    def mainloop(self):
        key = key_buffer = 0
        while key != 9 and self.data[1] > 0 and self.data[0] < self.end_game:
            self.screen.clear_data()
            self.screen.set_data(self.data[-2:])

            self.screen.set_cell(10, 3, "@")
            key = convert(self.screen.display())

            if not key: key = key_buffer
            else: key_buffer = key

            self._keyboard(key)


def convert(string):
    try: return int(string)
    except: return 0


def text_formater(string, screen_width=21, screen_height=6):

    def line_formater(string, screen_width):
        if len(string) <= screen_width: return string

        stop_index = screen_width
        while stop_index > 0 and not string[stop_index].isspace(): stop_index -= 1
        if not stop_index: stop_index = screen_width
    
        return string[:stop_index] + "\n" + line_formater(string[stop_index + 1:], screen_width)

    def paragraph_formater(lines, screen_height):
        if len(lines) < screen_height: return "\n".join(lines)

        return "\n".join(lines[:screen_height]) + "\n\n" + paragraph_formater(lines[screen_height:], screen_height)

    lines = line_formater(string, screen_width).split("\n")
    return paragraph_formater(lines, screen_height).split("\n\n")
