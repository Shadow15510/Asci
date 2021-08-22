class Screen:
    def __init__(self, screen_width=21, screen_height=6):
        # Screen configuration
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._data = [[" " for _ in range(screen_width)] for _ in range(screen_height)]

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
                last_input = input(">")
        return last_input

    def get_cell(self, x, y):
        return self._data[y][x]

    def get_map_size(self):
        return self.map_width, self.map_height


class Asci:
    def __init__(self, maps, fn_events, fn_fight, fn_stat, fn_custom, screen_width=21, screen_height=6):
        # Load maps
        self.maps = maps

        # Custom functions
        self._game_event = fn_events
        self._game_fight = fn_fight
        self._game_stat = fn_stat
        self._game_custom = fn_custom

        # Screen initialisation
        self.screen = Screen(screen_width, screen_height)

    def _looked_case(self, direction):
        # Left
        if direction == 1:
            return self.data[2] + 9, self.data[3] + 3

        # Right
        elif direction == 3:
            return self.data[2] + 11, self.data[3] + 3

        # Up
        elif direction == 5:
            return self.data[2] + 10, self.data[3] + 2

        # Down
        elif direction == 2:
            return self.data[2] + 10, self.data[3] + 4

        return self.data[2] + 10, self.data[3] + 3

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

        cell_patterns = self.legend
        for pattern_index in range(len(cell_patterns)):
            if cell in cell_patterns[pattern_index]: return pattern_index + 1

        return cell == " "

    def _keyboard(self, key):
        # Interaction with map
        if key in (1, 3, 5, 2):
            cell_test = self._cell_test(key)
            
            # Enter house
            if cell_test == 2 or (self.data[1] and cell_test < 0):
                self.data[1], self.data[2], self.data[3] = self._get_map(key)
                if self.data[1]:
                    self.screen.set_world(self.maps[self.data[1]][0])
                else:
                    self.screen.set_world(self.maps[0])
                self.map_width, self.map_height = self.screen.get_map_size()

            # Talk
            elif cell_test == 3:
                self._talk(key)

            # Fight
            elif cell_test == 4:
                self._fight(key)

        # Left
        if key == 1 and cell_test == 1: self.data[2] -= 1
        # Right
        if key == 3 and cell_test == 1: self.data[2] += 1
        # Up
        if key == 5 and cell_test == 1: self.data[3] -= 1
        # Down
        if key == 2 and cell_test == 1: self.data[3] += 1

        # Stat
        if key == 7:
            self.screen.clear()
            self._game_stat(self.stat)
            input()

        # Custom display function
        elif key == 8:
            self.screen.clear()
            self._game_custom(self.data[0], self.data[1], self.data[2], self.data[3], self.stat)

        # Quit
        elif key == 9:
            self.screen.clear()

        # /!\ TEST /!\ #
        elif key == 4:
            print(self.data)
            input()
        # /!\ TEST /!\ #

    def _talk(self, direction):
        x, y = self._looked_case(direction)

        # Read the dialogue
        event = read_event(self.data[0], self._game_event(self.data[0], self.data[1], x, y, self.stat))

        # XP and stat modification
        self.data[0] += event.xp_earned
        for index in range(len(event.stat)):
            self.stat[index] += event.stat[index]

        answer_selected = convert(self.screen.display_text(event.text))

        if event.answer and (0 < answer_selected <= event.answer): self.data[0] += answer_selected

    def _fight(self, direction):
        x, y = self._looked_case(direction)

        # Run the fight
        if self._game_fight(self.data[0], self.data[1], x, y, self.stat):
            self._talk(direction)


    def _get_map(self, direction):
        x, y = self._looked_case(direction)
        current_map = self.data[1]

        if current_map:
            if (x, y) == self.maps[current_map][2]:
                return 0, self.maps[current_map][1][0] - 10, self.maps[current_map][1][1] - 3
        else:
            for index in range(1, len(self.maps)):
                if (x, y) == self.maps[index][1]:
                    return index, self.maps[index][2][0] - 10, self.maps[index][2][1] - 3

        return current_map, self.data[2], self.data[3]

    def mainloop(self, end_game, stat=None, data=[0, 0, 0, 0], legend=("@", "^", "*", "$")):
        # Load save ; data = [XP, map_id, x, y]
        self.data = data[:]
        if not stat or type(stat) != list:
            self.stat = [100]
        else:
            self.stat = stat

        # Load legend
        self.legend = legend[:]

        # Screen and map configuration
        if data[1]: self.screen.set_world(self.maps[data[1]][0])
        else: self.screen.set_world(self.maps[0])
        
        self.map_width, self.map_height = self.screen.get_map_size()

        key = key_buffer = 0

        while key != 9 and self.stat[0] > 0 and self.data[0] < end_game:
            self.screen.set_data(self.data[-2:])

            self.screen.set_cell(10, 3, self.legend[0][0])
            key = convert(self.screen.display())

            if not key: key = key_buffer
            else: key_buffer = key

            self._keyboard(key)

        if self.stat[0] <= 0: self.stat[0] = 100
        return self.stat, self.data


class Event:
    def __init__(self, xp_earned, text, answer=0, *stat):
        self.xp_earned = xp_earned
        self.text = text
        self.answer = answer
        self.stat = stat


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

    lines = []
    for line in string.split("\n"):
        for formated_line in line_formater(line, screen_width).split("\n"):
            lines.append(formated_line)

    return paragraph_formater(lines, screen_height).split("\n\n")


def read_event(xp, event):
    if type(event) == dict:
        if xp in event: event = event[xp]
        else: event = event["base"]

    if type(event) != list:
        raise TypeError("event is of type {} instead of list".format(type(event)))

    return Event(*event)
