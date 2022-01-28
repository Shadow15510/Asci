# Asci (1.7.0)

class Asci:
    def __init__(self, maps, events_mapping, keys_mapping, behaviors=None, screen_width=21, screen_height=6):
        # Load maps
        self.maps = [Map(*i) for i in maps]

        # Custom functions
        self._legend = list(events_mapping.keys())
        self._game_events_mapping = [events_mapping[i] for i in self._legend]
        self._game_keys_mapping = {key: keys_mapping[key] for key in keys_mapping if not key in (1, 2, 3, 5)}
        
        # Custom entities behavior
        self._behaviors = {"stand by": stand_by, "follow": follow, "walk": walk}
        if behaviors:
            for i in behaviors: self._behaviors[i] = behaviors[i]

        # Screen initialisation
        self.screen = Screen(screen_width, screen_height)
        self.current_map = None
        self.visible_entities = []

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
            else: cell = self.screen.get_cell(self.data[2: 4], self.data[2] - 1, self.data[3])
        if direction == 3:
            if self.data[2] + 1 >= self.map_width: return -1
            else: cell = self.screen.get_cell(self.data[2: 4], self.data[2] + 1, self.data[3])
        if direction == 5:
            if self.data[3] - 1 < 0: return -1
            else: cell = self.screen.get_cell(self.data[2: 4], self.data[2], self.data[3] - 1)
        if direction == 2:
            if self.data[3] + 1 >= self.map_height: return -1
            else: cell = self.screen.get_cell(self.data[2: 4], self.data[2], self.data[3] + 1)

        print(f"'{cell}'")
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
                self._change_map(new_map)

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
        # Update entities
        if self.current_map:
            for i in range(len(self.current_map.entities)):
                entity = self.current_map.entities[i]
                if entity.behavior == "follow":
                    self.maps[new_map].entities.append(entity)
                    self.maps[self.data[1]].entities.pop(i)

        # Update current map
        self.data[1] = new_map
        self.current_map = self.maps[self.data[1]]
        
        # Update screen configuration
        self.screen.set_world(self.current_map.map_data)
        self.map_width, self.map_height = self.screen.get_map_size()
        self._get_visible_entities()

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

    # Entities gestion
    def _get_visible_entities(self):
        self.visible_entities = {}
        for entity in self.current_map.entities:
            if (0 <= entity.pos_x - self.data[2] + 10 < self.screen.screen_width) and (0 <= entity.pos_y - self.data[3] + 3 < self.screen.screen_height):
                self.visible_entities[entity.entity_id] =  entity

    def _get_entity_id(self, x, y):
        for entity_id in self.visible_entities:
            entity = self.visible_entities[entity_id]
            if entity.pos_x == x and entity.pos_y == y:
                return entity_id

    def _run_entities_behaviors(self):
        for entity in self.current_map.entities:
            data_copy = get_data_copy(self.data)
            self._behaviors[entity.behavior](entity, data_copy, self.stat, self.screen, self.walkable)
        self._get_visible_entities()

    # Mainloop
    def mainloop(self, end_game, stat=None, data=None, routine=None, player="@", door="^", walkable=" ", exit_key=9, multi_move="."):
        if exit_key in self._game_keys_mapping:
            raise ValueError("'{}' is already assigned to a function.".format(exit_key))

        # Load save ; data = [XP, map_id, x, y]
        if not stat or type(stat) != list: self.stat = [100]
        else: self.stat = stat

        if not data: self.data = [{"main": 0}, 0, 0, 0, 0]
        else: self.data = [data[0], data[1], data[2], data[3], 0]

        # Configuration
        self.walkable = walkable
        self._legend.append(door)
        self._legend.append(walkable)
        self._change_map(data[1])

        key = 0

        while key != exit_key and self.stat[0] > 0 and self.data[0]["main"] < end_game:
            # Update the map
            self.screen.set_screen(self.data[2], self.data[3])
            
            # Compute the player's and entities' positions
            self.screen.set_cell(self.data[2] - 10, self.data[3] - 3, self.data[2], self.data[3], player)
            self._run_entities_behaviors()
            for entity in self.visible_entities.values():
                self.screen.set_cell(self.data[2] - 10, self.data[3] - 3, entity.pos_x, entity.pos_y, entity.symbol)
            
            # Display map and get the key
            key = convert(self.screen.display())

            if not key: key = self.data[4]
            else: self.data[4] = key

            if type(key) == str and key[0] == multi_move:
                for i in list(key[1:]):
                    self._keyboard(convert(i), False)
                    self.data[4] = convert(key[-1])
            else:
                self._keyboard(key)
            
            # Launching the game routine
            if routine:
                data_copy = get_data_copy(self.data)
                routine(data_copy, self.stat)

        if self.stat[0] <= 0: self.stat[0] = 100
        return self.stat, self.data[:-1]


# Classes used by Asci
class Screen:
    def __init__(self, screen_width=21, screen_height=6):
        # Screen configuration
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._on_screen = [[" " for _ in range(screen_width)] for _ in range(screen_height)]

    def get_map_size(self):
        return self.map_width, self.map_height

    def set_world(self, world):
        self._world = [[char for char in line] for line in world.split("\n")[1:]]
        self.map_width = max([len(line) for line in self._world])
        self.map_height = len(self._world)

    def set_screen(self, x, y):
        x -= 10 ; y -= 3
        for x_map in range(x, x + self.screen_width):
            for y_map in range(y, y + self.screen_height):
                self._on_screen[y_map - y][x_map - x] = " "
                if 0 <= x_map < self.map_width and 0 <= y_map < self.map_height:
                    try: self._on_screen[y_map - y][x_map - x] = self._world[y_map][x_map]
                    except: pass

    def display(self, return_input=True):
        for line in self._on_screen:
            print("".join(line))

        if return_input: return input(">")

    def clear(self):
        print("\n" * self.screen_height)

    def display_text(self, string):
        paragraphs = [i for i in text_formater(string) if i]
        nb_par = len(paragraphs)
        for index in range(nb_par):
            self.clear()
            print(paragraphs[index])
            if index + 1 == nb_par: return input(">")
            else: input()
    
    def set_cell(self, x_offset, y_offset, x, y, value):
        self._on_screen[y - y_offset][x - x_offset] = value

    def get_cell(self, offsets, x, y):
        x = x - (offsets[0] - 10)
        y = y - (offsets[1] - 3)
        if 0 <= x < self.screen_width and 0 <= y <= self.screen_height:
            return self._on_screen[y][x]
        else: return " "

class Event:
    def __init__(self, xp, text, answer=0, *stat):
        self.xp = xp
        self.text = text
        self.answer = answer
        self.stat = stat


class Map:
    def __init__(self, map_data, entities, *coords):
        self.map_data = map_data
        if entities: self.entities = [Entity(*i) for i in entities]
        else: self.entities = []
        self.coords = coords

class Entity:
    def __init__(self, entity_id, symbol, x, y, behavior, *args):
        self.entity_id = entity_id
        self.symbol = symbol
        self.pos_x = x
        self.pos_y = y
        self.behavior = behavior
        self.args = list(args)

    def change_behavior(self, new_behavior):
        self.behavior = new_behavior


# Functions used by Asci
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


def get_data_copy(data):
    return [data[0], data[1], data[2], data[3], data[4]]


# Extra functions
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


def stand_by(entity, data, stat, screen, walkable):
    pass

def follow(entity, data, stat, screen, walkable):
    if data[4] == 1 and screen.get_cell(data[2: 4], data[2] + 1, data[3]) in walkable: entity.pos_x, entity.pos_y = data[2] + 1, data[3]
    elif data[4] == 2 and screen.get_cell(data[2: 4], data[2], data[3] - 1) in walkable: entity.pos_x, entity.pos_y = data[2], data[3] - 1
    elif data[4] == 3 and screen.get_cell(data[2: 4], data[2] - 1, data[3]) in walkable: entity.pos_x, entity.pos_y = data[2] - 1, data[3]
    elif data[4] == 5 and screen.get_cell(data[2: 4], data[2], data[3] + 1) in walkable: entity.pos_x, entity.pos_y = data[2], data[3] + 1

def walk(entity, data, stat, screen, walkable):
    frame = (entity.args[0] + 1) % len(entity.args[1])
    new_x, new_y = entity.args[1][frame]
    print(new_x, new_y)
    if screen.get_cell(data[2: 4], new_x, new_y) in walkable:
        entity.pos_x, entity.pos_y = new_x, new_y
    entity.args[0] = frame
