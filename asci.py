# Asci (1.9.0)
from math import floor, ceil


class Asci:
    def __init__(self, maps, entities, events_mapping, keys_mapping, behaviors=None, screen_width=21, screen_height=7):
        # Load maps and entities
        self.maps = [Map(*i) for i in maps]
        self.entities = {}
        entity_id = 0
        for i in entities:
            if not i[0]:
                i[0] = entity_id
                entity_id += 1

            if i[0] in self.entities: raise KeyError("'{}' is already a registered entities".format(i[0]))
            else: self.entities[i[0]] = Entity(*i)
        
        # Custom functions
        self._legend = list(events_mapping.keys())
        self._game_events_mapping = [events_mapping[i] for i in self._legend]
        self._game_keys_mapping = {key: keys_mapping[key] for key in keys_mapping if not key in (1, 2, 3, 5)}
        
        # Custom entities behavior
        self._behaviors = {"permanent": permanent, "stand by": stand_by, "follow": follow, "walk between": walk_between, "walk to": walk_to, "follow by player": follow_by_player}
        if behaviors:
            for i in behaviors: self._behaviors[i] = behaviors[i]

        # Screen initialisation
        self.screen = Screen(screen_width, screen_height)
        self.current_map = None

    def _looked_case(self, direction):
        if direction == 1: # Left
            return self.data[2] - 1, self.data[3]

        elif direction == 3: # Right
            return self.data[2] + 1, self.data[3]

        elif direction == 5: # Up
            return self.data[2], self.data[3] - 1

        elif direction == 2: # Down
            return self.data[2], self.data[3] + 1

        return self.data[2], self.data[3]

    def _cell_test(self, direction):
        if direction == 1:
            if self.data[2] - 1 < 0: return -1
            else: cell = self.screen.get_cell(self.data[2] - 1, self.data[3])
        if direction == 3:
            if self.data[2] + 1 >= self.map_width: return -1
            else: cell = self.screen.get_cell(self.data[2] + 1, self.data[3])
        if direction == 5:
            if self.data[3] - 1 < 0: return -1
            else: cell = self.screen.get_cell(self.data[2], self.data[3] - 1)
        if direction == 2:
            if self.data[3] + 1 >= self.map_height: return -1
            else: cell = self.screen.get_cell(self.data[2], self.data[3] + 1)

        cell_patterns = self._legend
        for pattern_index in range(len(cell_patterns)):
            if cell in cell_patterns[pattern_index]: return pattern_index

        return -1

    def _keyboard(self, key, interaction=True):
        # Interaction while moving
        if key in (1, 3, 5, 2):
            cell_test = self._cell_test(key)
            
            # Move
            if cell_test == len(self._legend) - 1:
                if key == 1: self.data[2] -= 1
                if key == 3: self.data[2] += 1
                if key == 5: self.data[3] -= 1
                if key == 2: self.data[3] += 1

            # Change map
            elif interaction and cell_test == len(self._legend) - 2:
                new_map, self.data[2], self.data[3] = self._get_map(key)
                if self.data[1] != new_map: self._change_map(new_map)

            # Interaction
            elif interaction and cell_test >= 0: self._interaction(key, cell_test)

        # Custom functions
        elif key in self._game_keys_mapping:
            self.screen.clear()
            self._game_keys_mapping[key](self.data, self.stat)

    def _get_map(self, direction):
        current_coords = self._looked_case(direction)

        for coords in self.current_map.coords:
            if coords[:2] == current_coords:
                return coords[2], coords[3], coords[4]

        return self.data[1], self.data[2], self.data[3]

    def _change_map(self, new_map):
        # Update map id and data
        old_map, self.data[1] = self.data[1], new_map
        self.current_map = self.maps[self.data[1]]
        self.current_map.entities = {}

        # Update entities
        for i in self.entities:
            entity = self.entities[i]
            if entity.map_id == old_map and entity.behavior == "follow":
                entity.pos_x = entity.pos_y = -1
                entity.map_id = new_map
            if entity.map_id == new_map: self.current_map.entities[i] = entity        
        
        # Update screen configuration
        self.screen.set_world(self.current_map.map_data)
        self.map_width, self.map_height = self.screen.get_map_size()

    def _interaction(self, direction, cell_content):
        x, y = self._looked_case(direction)
        data_copy = [self.data[0], self.data[1], x, y, self.data[4]]

        # Get the event
        event = self._game_events_mapping[cell_content](data_copy, self.stat, self.current_map.entities, self._get_entity_id(x, y))
        if type(event) == tuple:
            quest, event = event
        else:
            quest = "main"

        # data modification
        self.data[0] = data_copy[0]
        if self.data[1] != data_copy[1]:
            self._change_map(data_copy[1])

        if data_copy[2] != x: self.data[2] = data_copy[2]
        if data_copy[3] != y: self.data[3] = data_copy[3]

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

    def _get_entity_id(self, x, y):
        for entity in self.current_map.entities.values():
            if entity.pos_x == x and entity.pos_y == y:
                return entity.entity_id

    # Mainloop
    def mainloop(self, end_game, stat=None, data=None, routine=None, low_bar=None, player="@", door="^", walkable=" ", exit_key=9, multi_move="."):
        if exit_key in self._game_keys_mapping:
            raise ValueError("'{}' is already assigned to a function.".format(exit_key))

        # Load save ; data = [XP, map_id, x, y]
        if not stat or type(stat) != list: self.stat = [100]
        else: self.stat = stat

        if not data: self.data = [{"main": 0}, 0, 0, 0, 0]
        else: self.data = [data[0], data[1], data[2], data[3], 0]

        # Configuration
        self._legend.append(door)
        self._legend.append(walkable)
        self._change_map(self.data[1])
        self.screen.load_data(self.data)

        key = 0

        while key != exit_key and self.stat[0] > 0 and self.data[0]["main"] < end_game:
            # Update the map
            self.screen.set_screen()
            
            # Compute the player's and entities' positions
            data_copy = self.data[:]
            for entity in self.current_map.entities.values():
                self._behaviors[entity.behavior](entity, data_copy, self.stat, self.screen, walkable)
                if entity.map_id == self.data[1] and (0 <= entity.pos_x - self.data[2] + self.screen.pos_player[0] < self.screen.screen_width) and (0 <= entity.pos_y - self.data[3] + self.screen.pos_player[1] < self.screen.screen_height):
                    self.screen.set_cell(entity.pos_x, entity.pos_y, entity.symbol)

            self.screen.set_cell(self.data[2], self.data[3], player)
            
            # Display map, low bar, get the key and update key buffer
            if low_bar: bar = low_bar(self.data[:], self.stat[:])
            else: bar = None
            key = convert(self.screen.display(low_bar=bar))
            if not key: key = self.data[4]
            else: self.data[4] = key

            # Multi-move and key gestion
            if type(key) == str and key[0] == multi_move:
                key = key[1:]
                for k, r in get_multi_move(key):
                    for _ in range(r):
                        self._keyboard(k, False)
                        self.screen.set_screen()

                self.data[4] = k
            else:
                self._keyboard(key)
            
            # Launching the game routine
            if routine:
                data_copy = self.data[:]
                routine(data_copy, self.stat)

        if self.stat[0] <= 0: self.stat[0] = 100
        return self.stat, self.data[:-1]


# Classes used by Asci
class Screen:
    def __init__(self, screen_width=21, screen_height=7):
        # Screen configuration
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pos_player = (screen_width // 2, screen_height // 2)
        self._on_screen = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
        self._asci_data = []

    def load_data(self, data):
        self._asci_data = data

    def get_map_size(self):
        return self.map_width, self.map_height

    def set_world(self, world):
        self._world = [[char for char in line] for line in world.split("\n")[1:]]
        self.map_width = max([len(line) for line in self._world])
        self.map_height = len(self._world)

    def set_screen(self):
        x = self._asci_data[2] - self.pos_player[0] ; y = self._asci_data[3] - self.pos_player[1]
        for x_map in range(x, x + self.screen_width):
            for y_map in range(y, y + self.screen_height):
                self._on_screen[y_map - y][x_map - x] = " "
                if 0 <= x_map < self.map_width and 0 <= y_map < self.map_height:
                    try: self._on_screen[y_map - y][x_map - x] = self._world[y_map][x_map]
                    except: pass

    def display(self, return_input=True, low_bar=None):
        for line_no in range(len(self._on_screen)):
            line = "".join(self._on_screen[line_no])
            if line_no + 1 == self.screen_height and return_input:
                if not low_bar: line = line[:-6] + ">"
                else: line = low_bar + ">" 
                print(line, end="")
                return input()
            else:
                print(line)

    def clear(self):
        print("\n" * self.screen_height)

    def display_text(self, string):
        paragraphs = [i for i in text_formater(string, self.screen_width, self.screen_height) if i]
        nb_par = len(paragraphs)
        for index in range(nb_par):
            self.clear()
            print(paragraphs[index])
            if index + 1 == nb_par: return input(">")
            else: input()
    
    def set_cell(self, x, y, value):
        x = x - (self._asci_data[2] - self.pos_player[0])
        y = y - (self._asci_data[3] - self.pos_player[1])
        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
            self._on_screen[y][x] = value

    def get_cell(self, x, y):
        x = x - (self._asci_data[2] - self.pos_player[0])
        y = y - (self._asci_data[3] - self.pos_player[1])
        if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
            return self._on_screen[y][x]
        else: return " "


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
        self.entities = {}


class Entity:
    def __init__(self, entity_id, symbol, map_id, x, y, behavior, *args):
        self.entity_id = entity_id
        self.symbol = symbol
        self.map_id = map_id
        self.pos_x = x
        self.pos_y = y
        self.behavior = behavior
        self.args = list(args)

    def change_behavior(self, new_behavior):
        if self.behavior != "permanent": self.behavior = new_behavior

    def teleport(self, map_id, x, y):
        if self.behavio != "permanent": self.map_id, self.pos_x, self.pos_y = map_id, x, y


# Functions used by Asci
def convert(string, force_int=False):
    try: return int(string)
    except:
        if force_int: return 0
        else: return string


def text_formater(string, screen_width=21, screen_height=6):

    def line_formater(string, screen_width):
        string_result = ""        
        while len(string) > screen_width:
            stop_index = screen_width
            while stop_index > 0 and not string[stop_index].isspace(): stop_index -= 1
            if not stop_index: stop_index = screen_width

            string_result += string[:stop_index].strip() + "\n"
            string = string[stop_index:].strip()

        return string_result + string

    def paragraph_formater(lines, screen_height):
        paragraphs = ""
        while len(lines) >= screen_height:
            paragraphs += "\n".join(lines[:screen_height]) + "\n\n"
            lines = lines[screen_height:]

        return paragraphs + "\n".join(lines)

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


def get_multi_move(key):
    if "," in key:
        result = []
        for k in key.split(","):
            if "*" in k:
                k = k.split("*")
                result.append((convert(k[0]), convert(k[1])))
            else:
                result.append((convert(k), 1))

        return result
    
    elif "*" in key:
        key = key.split("*")
        return [(convert(key[0]), convert(key[1]))]
    
    else:
        return [(convert(k), 1) for k in key]


# Motions functions
def stand_by(entity, data, stat, screen, walkable):
    pass


def permanent(entity, data, stat, screen, walkable):
    pass


def follow(entity, data, stat, screen, walkable):
    if entity.pos_x == entity.pos_y == -1:
        entity.pos_x, entity.pos_y = data[2], data[3]

    elif data[4] in (1, 2, 3, 5):
        if entity.args: walkable += entity.args[0]
        cases = ((data[2] + 1, data[3]), (data[2], data[3] - 1), (data[2] - 1, data[3]), 0, (data[2], data[3] + 1))[data[4] - 1]
        if not (0 <= cases[0] < screen.map_width and 0 <= cases[1] < screen.map_height): entity.pos_x, entity.pos_y = data[2], data[3]
        elif screen.get_cell(cases[0], cases[1]) in walkable: entity.pos_x, entity.pos_y = cases


def walk_between(entity, data, stat, screen, walkable):
    frame = (entity.args[0] + 1) % len(entity.args[1])
    new_x, new_y = _walk_engine(entity, frame)
    if screen.get_cell(new_x, new_y) in walkable:
        entity.pos_x, entity.pos_y = new_x, new_y
    entity.args[0] = frame


def walk_to(entity, data, stat, screen, walkable):
    frame = entity.args[0]
    if len(entity.args[1]) == frame:
        entity.behavior = "stand by"
        entity.args = []
        return

    new_x, new_y = _walk_engine(entity, frame)
    
    if screen.get_cell(new_x, new_y) in walkable:
        entity.pos_x, entity.pos_y = new_x, new_y
    entity.args[0] += 1


def follow_by_player(entity, data, stat, screen, walkable):
    frame = entity.args[0]
    if len(entity.args[1]) == frame:
        entity.behavior = "stand by"
        entity.args = []
        return
        
    new_x, new_y = _walk_engine(entity, frame)

    if abs(data[2] - new_x) < 5 and abs(data[3] - new_y) < 3 and screen.get_cell(new_x, new_y) in walkable:
        entity.pos_x, entity.pos_y = new_x, new_y
        if (new_x, new_y) == entity.args[1][frame]: entity.args[0] += 1


def _walk_engine(entity, frame):
    delta_x, delta_y = list(map(lambda x,y: y - x, (entity.pos_x, entity.pos_y), entity.args[1][frame]))
    new_x = entity.pos_x
    new_y = entity.pos_y
    if delta_x: new_x += abs(delta_x) // delta_x
    if delta_y: new_y += abs(delta_y) // delta_y
    return new_x, new_y


# Extra functions
def print_text(text, min_value=0, max_value=0, default_value=0, screen_width=21, screen_height=7):
    paragraphs = [i for i in text_formater(text, screen_width, screen_height) if i]
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


def center(string, total_length, symbol):
    left = floor((total_length - len(string)) / 2)
    right = ceil((total_length - len(string)) / 2)

    return left * symbol + string + right * symbol


def enumerate(data):
    return [(i, data[i]) for i in range(len(data))]