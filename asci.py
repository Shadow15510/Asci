# Asci (version 1.6.3)

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
        self.maps = [Map(*i) for i in maps]

        # Custom functions
        self.legend = list(events_mapping.keys())
        self._game_events_mapping = [events_mapping[i] for i in self.legend]
        self._game_keys_mapping = {key: keys_mapping[key] for key in keys_mapping if not key in (1, 2, 3, 5)}

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

    def _keyboard(self, key, interaction=True):
        # Interaction while moving
        if key in (1, 3, 5, 2):
            cell_test = self._cell_test(key)
            
            # Move
            if cell_test == len(self.legend) - 1:
                if key == 1: self.data[2] -= 1
                if key == 3: self.data[2] += 1
                if key == 5: self.data[3] -= 1
                if key == 2: self.data[3] += 1            
            
            # Change map
            elif interaction and cell_test == len(self.legend) - 2: # or (self.data[1] and cell_test < 0):
                self.data[1], self.data[2], self.data[3] = self._get_map(key)
                self.screen.set_world(self.maps[self.data[1]].map_data)
                self.map_width, self.map_height = self.screen.get_map_size()


            # Interaction
            elif interaction and cell_test >= 0: self._interaction(key, cell_test)

        # Custom functions
        elif key in self._game_keys_mapping:
            self.screen.clear()
            self._game_keys_mapping[key](self.data, self.stat)

    def _interaction(self, direction, cell_content):
        x, y = self._looked_case(direction)
        data_copy = [self.data[0], self.data[1], x, y]

        # Get the event
        event = self._game_events_mapping[cell_content](data_copy, self.stat)
        if type(event) == tuple:
            quest, event = event
        else:
            quest = "main"

        # data modification
        self.data[0] = data_copy[0]
        if self.data[1] != data_copy[1]:
            self.data[1] = data_copy[1]
            self.screen.set_world(self.maps[self.data[1]].map_data)
            self.map_width, self.map_height = self.screen.get_map_size()

        if data_copy[2] != x: self.data[2] = data_copy[2] - 10
        if data_copy[3] != y: self.data[3] = data_copy[3] - 3

        if not event: return 
        event = read_event(self.data, event, quest)

        # XP and stat modification
        self.data[0][quest] += event.xp
        for index, value in event.stat:
            self.stat[index] += value

        # Display and get answer
        if event.text:
            answer_selected = convert(self.screen.display_text(event.text), True)
            if event.answer and (0 < answer_selected <= event.answer):
                self.data[0][quest] += answer_selected
                self._interaction(direction, cell_content)

    def _get_map(self, direction):
        current_coords = self._looked_case(direction)
        current_map = self.data[1]

        for coords in self.maps[current_map].coords:
            if coords[:2] == current_coords:
                return coords[2], coords[3] - 10, coords[4] - 3

        return current_map, self.data[2], self.data[3]

    def mainloop(self, end_game, stat=None, data=None, routine=None, player="@", door="^", walkable=" ", exit_key=9, multi_move="."):
        if exit_key in self._game_keys_mapping:
            raise ValueError("'{}' is already assigned to a function.".format(exit_key))

        # Load save ; data = [XP, map_id, x, y]
        if not stat or type(stat) != list: self.stat = [100]
        else: self.stat = stat

        if not data: self.data = [{"main": 0}, 0, 0, 0]
        else: self.data = [data[0], data[1], data[2] - 10, data[3] - 3]

        self.legend.append(door)
        self.legend.append(walkable)

        # Screen and map configuration
        self.screen.set_world(self.maps[self.data[1]].map_data)
        self.map_width, self.map_height = self.screen.get_map_size()

        key = key_buffer = 0

        while key != exit_key and self.stat[0] > 0 and self.data[0]["main"] < end_game:
            self.screen.set_data(self.data[-2:])

            self.screen.set_cell(10, 3, player)
            key = convert(self.screen.display())

            if not key: key = key_buffer
            else: key_buffer = key

            if type(key) == str and key[0] == multi_move:
                for i in list(key[1:]):
                    self._keyboard(convert(i), False)
            else:
                self._keyboard(key)
            
            # Launching the game routine
            if routine: routine(self.data, self.stat)

        if self.stat[0] <= 0: self.stat[0] = 100
        self.data[2] += 10
        self.data[3] += 3
        return self.stat, self.data


class Event:
    def __init__(self, xp, text, answer=0, *stat):
        self.xp = xp
        self.text = text
        self.answer = answer
        self.stat = stat


class Map:
    def __init__(self, map_data, *coords):
        self.map_data = map_data
        self.coords = coords


def convert(string, force_int=False):
    try: return int(string)
    except:
        if force_int: return 0
        else: return string


def text_formater(string, screen_width=21, screen_height=6):

    def line_formater(string, screen_width):
        if len(string) <= screen_width: return string

        stop_index = screen_width
        while stop_index > 0 and not string[stop_index].isspace(): stop_index -= 1
        if not stop_index: stop_index = screen_width
    
        return string[:stop_index].strip() + "\n" + line_formater(string[stop_index:].strip(), screen_width)

    def paragraph_formater(lines, screen_height):
        if len(lines) < screen_height: return "\n".join(lines)

        return "\n".join(lines[:screen_height]) + "\n\n" + paragraph_formater(lines[screen_height:], screen_height)

    lines = []
    for line in string.split("\n"):
        for formated_line in line_formater(line, screen_width).split("\n"):
            lines.append(formated_line)

    return paragraph_formater(lines, screen_height).split("\n\n")


def read_event(data, event, quest):
    if not quest in data[0]:
        data[0][quest] = 0
    
    if type(event) == dict:
        if data[0][quest] in event: event = event[data[0][quest]]
        else: event = event["base"]

    if type(event) != list:
        raise TypeError("event is of type {} instead of list".format(type(event)))

    return Event(*event)


def print_text(text, min_value=0, max_value=0, default_value=0):
    paragraphs = [i for i in text_formater(text) if i]
    nb = len(paragraphs)
    for index in range(nb):
        print("\n" * 7)
        print(paragraphs[index])

        if index + 1 == nb and (min_value or max_value or default_value) and min_value <= max_value:
            result = input(">")
            try: result = int(result)
            except: result = default_value
            if not (min_value <= result <= max_value): result = default_value

            return result

        else: input()
