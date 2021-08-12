from random import randint
from mapset import *


class Screen:
    def __init__(self, screen_width=21, screen_height=6):
        self._data = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
        self.width = screen_width
        self.height = screen_height

    def set_cell(self, x, y, value):
        self._data[y][x] = value
        
    def get_cell(self, x, y):
        return self._data[y][x]

    def load(self, value):
        self._data = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for y, line in enumerate(value.split("\n")[1:]):
            for x, char in enumerate(line):
                self._data[y][x] = char

    def display(self):
        string = ""
        for line in self._data:
            print("".join(line))
        return input("> ")

    def display_text(self, string, final_input=True):
        for paragraph in text_formater(string):
            if paragraph:
                self.clear()
                print(paragraph)
                if final_input: input()

    def clear(self):
        print("\n" * (self.height))


class Asci:
    def __init__(self, stat="0.100.1.1", opus=1):
        # Load stats
        stat = [int(i) for i in stat.split(".")]
        self.xp = stat[0]
        self.pv = stat[1]
        self.current_map = stat[2]
        self.outdoor = stat[3]

        # Opus loading
        load_opus(opus)
        
        # Initialize player's position
        self.x = 10
        self.y = 5

        # Misc initialisation
        self.screen = Screen()
        self.end = event.end
        

    def _new_map(self):
        self.x = 10
        self.y = 5
        self.current_map = randint(1, 7)

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

    def _keyboard_input(self, key):
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

        # Stat
        if key == 8:
            places = ("Palais", "Thyel", "Medecins", "Foret", "Bibliotheque", "Plage", "Village", "Bois")
            print("* * Statistiques * *\nExperience .....: {0}\nPoints de vie ..: {1}\nQuartier actuel :\n... {2} ({3})\n* *              * * ".format(self.xp, self.pv, places[self.current_map - 1], self.current_map))
            input()

        # Teleportation
        if key == 15510 and self.xp > 28:
            self.screen.clear()
            qrt = convert(input("Numero du quartier :\n> "))
            if 0 < qrt < 9:
                self.current_map = qrt
                self.x = 10
                self.y = 5

        # Quit
        if key == 9:
            stat = (self.xp, self.pv, self.current_map, self.outdoor)
            self.screen.clear()
            print("Pour reprendre la\npartie, entrez :\nasci('{}')".format('.'.join([str(i) for i in stat])))

        # Interaction with map
        if key in (1, 2, 3, 5):
            # Exit the map
            if cell_test < 0:
                if self.outdoor:
                    self._new_map()
                else:
                    self.outdoor = 1
                    self.x = 10
                    self.y = 5

            # Door
            elif cell_test == 2:
                self.outdoor = 0
                self.x = 10
                self.y = 5

            # PnJ
            elif cell_test == 3:
                self._dialogue()

            # Fight
            elif cell_test == 4:
                self._fight()

    def _dialogue(self):
        xp, pv, text = event.get_dialogue(self.xp, self.pv, self.current_map, self.outdoor)
        self.xp += xp
        self.pv += pv

        self.screen.display_text(text)

    def _fight(self):
        enemy_pv = randint(50, 150)
        enemy_weapon = randint(10, 50)
        
        self.screen.clear()
        player_weapon = input("Code de l'arme :\n> ")
        player_weapon = convert(player_weapon)
        if player_weapon == 0:
            self.screen.display_text("Vous avez abandonne le combat.")
            return

        while self.pv > 0 and enemy_pv > 0:
            player_pa = player_weapon + randint(1, 25)
            enemy_pa = enemy_weapon + randint(1, 25)

            if player_pa > enemy_pa: enemy_pv -= player_pa
            else: self.pv -= enemy_pa

        if self.pv > 0:
            self.xp = event.get_interaction(self.xp, self.current_map)
            self.screen.display_text("Vous avez vaincu votre adversaire !")
        else:
            stat = (self.xp, 100, self.current_map, self.outdoor)
            self.screen.display_text("Vous avez perdu... Code de la dernière sauvegarde :\n'{}'".format('.'.join([str(i) for i in stat])), False)
        

    def mainloop(self):
        key = key_buffer = 0
        while key != 9 and self.pv > 0 and self.xp < self.end:
            self.screen.load(get_map(self.current_map, self.outdoor))

            self.screen.set_cell(self.x, self.y, "@")
            key = convert(self.screen.display())

            if not key: key = key_buffer
            else: key_buffer = key

            self._keyboard_input(key)


def convert(n):
    try: return int(n)
    except: return 0


def load_opus(opus):
    if opus == 1:
        import event_1 as e
    elif opus == 2:
        import event_2 as e
    elif opus == 3:
        import event_3 as e

    global event
    event = e


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


def enumerate(subscriptable):
    return [(i, subscriptable[i]) for i in range(len(subscriptable))]
