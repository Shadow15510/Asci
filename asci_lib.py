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
        paragraphs = [i for i in text_formater(string) if i]
        nb_par = len(paragraphs)
        for index in range(nb_par):
            self.clear()
            print(paragraphs[index])
            if index + 1 == nb_par: return input(">")
            else: input()

    def get_cell(self, x, y):
        return self._data[y][x]

    def get_map_size(self):
        return self.map_width, self.map_height


class Asci:
    def __init__(self, maps, events_mapping, keys_mapping, screen_width=21, screen_height=6):
        # Load maps
        self.maps = []
        for i in maps:
            if type(i) == str: self.maps.append(Map(i))
            else: self.maps.append(Map(*i))

        # Custom functions
        self.legend = list(events_mapping.keys())
        self._game_events_mapping = [events_mapping[i] for i in self.legend]
        self._game_keys_mapping = {key: keys_mapping[key] for key in keys_mapping if not key in (1, 2, 3, 5, 9)}

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
            if cell in cell_patterns[pattern_index]: return pattern_index

        return -1

    def _keyboard(self, key):
        # Interaction while moving
        if key in (1, 3, 5, 2):
            cell_test = self._cell_test(key)
            
            # Enter house
            if cell_test == len(self.legend) - 2: # or (self.data[1] and cell_test < 0):
                self.data[1], self.data[2], self.data[3] = self._get_map(key)
                self.screen.set_world(self.maps[self.data[1]].map_data)
                self.map_width, self.map_height = self.screen.get_map_size()

            # Move
            elif cell_test == len(self.legend) - 1:
                if key == 1: self.data[2] -= 1
                if key == 3: self.data[2] += 1
                if key == 5: self.data[3] -= 1
                if key == 2: self.data[3] += 1

            # Interaction
            elif cell_test >= 0: self._interaction(key, cell_test)

        # Custom functions
        elif key in self._game_keys_mapping:
            self.screen.clear()
            self._game_keys_mapping[key](self.data, self.stat)

        # Quit
        elif key == 9:
            self.screen.clear()

    def _interaction(self, direction, cell_content):
        x, y = self._looked_case(direction)
        fake_data = [self.data[0], self.data[1], x, y]

        # Get the event
        event = self._game_events_mapping[cell_content](fake_data, self.stat)
        event = read_event(self.data[0], event)

        # data modification
        self.data[0] = fake_data[0]
        self.data[1] = fake_data[1]
        if fake_data[2] != x: self.data[2] = fake_data[2]
        if fake_data[3] != y: self.data[3] = fake_data[3]

        # XP and stat modification
        self.data[0] += event.xp_earned
        for index, value in event.stat:
            self.stat[index] += value

        # Display and get answer
        if event.text:
            answer_selected = convert(self.screen.display_text(event.text))
            if event.answer and (0 < answer_selected <= event.answer): self.data[0] += answer_selected

    def _get_map(self, direction):
        x, y = self._looked_case(direction)
        current_map = self.data[1]

        if (x, y) == self.maps[current_map].coords_out:
            return self.maps[current_map].parent, self.maps[current_map].coords_in[0] - 10, self.maps[current_map].coords_in[1] - 3
        
        else:
            maps_available = [(i, self.maps[i]) for i in range(len(self.maps)) if self.maps[i].parent == current_map]

            for index, map_looked in maps_available:
                if (x, y) == map_looked.coords_in:
                    return index, map_looked.coords_out[0] - 10, map_looked.coords_out[1] - 3

        return current_map, self.data[2], self.data[3]

    def mainloop(self, end_game, stat=None, data=[0, 0, 0, 0], player="@", door="^", walkable=" "):
        # Load save ; data = [XP, map_id, x, y]
        self.data = data[:]
        if not stat or type(stat) != list: self.stat = [100]
        else: self.stat = stat

        self.legend.append(door)
        self.legend.append(walkable)

        # Screen and map configuration
        self.screen.set_world(self.maps[data[1]].map_data)
        self.map_width, self.map_height = self.screen.get_map_size()

        key = key_buffer = 0

        while key != 9 and self.stat[0] > 0 and self.data[0] < end_game:
            self.screen.set_data(self.data[-2:])

            self.screen.set_cell(10, 3, player)
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


class Map:
    def __init__(self, map_data, coords_in=None, coords_out=None, parent=None):
        self.map_data = map_data
        self.coords_in = coords_in
        self.coords_out = coords_out

        self.parent = parent


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
