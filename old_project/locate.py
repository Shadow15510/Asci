class Screen:
    def _check(self, x, o, name):
        if not isinstance(x, int):
            raise TypeError("{} is not an int object".format(name))
        elif x < 1:
            raise ValueError("{} is lower than 1".format(name))
        if o is None:
            o = 0
        elif x > o and o:
            raise ValueError("{} is greater than the height of this object: {} > {}".
                format(name, x, o))

    def __init__(self, width=21, height=6, patern=" ", copy=None):
        if isinstance(copy, Screen):
            self._width = copy._width
            self._height = copy._height
            self._mat = copy._mat
        else:
            self._check(width, None, "width")
            self._check(height, None, "height")
            if not isinstance(patern, str):
                raise TypeError("patern is not a string")
            elif len(patern) > 1:
                raise ValueError("patern is too long (length = {})".format(len(patern)))
            self._width = width
            self._height = height
            self.fill(patern)

    def locate(self, x, y, string):
        self._check(x, self._width, "x")
        self._check(y, self._height, "y")
        string = str(string)
        i = -1
        for char in string:
            if i + x < self._width:
                self._mat[y - 1][x + i] = char
            i += 1

    def locate_v(self, x, y, string):
        self._check(x, self._width, "x")
        self._check(y, self._height, "y")
        string = str(string)
        i = -1
        for char in string:
            if i + y < self._height:
                self._mat[y + i][x - 1] = char
            i += 1

    def fill(self, patern=" "):
        self._mat = [[patern[0] for i in range(self._width)] for i in range(self._height)]

    def refresh(self, ask_for_input=True, endl="\n"):
        to_print = str()
        for line in self._mat:
            for cell in line:
                to_print += cell
            to_print += "\n"
        to_print = to_print[:-1]
        print(to_print)
        if ask_for_input:
            return input(">")
        else:
            print("", end=endl)
            return None

    def get_cell(self, x, y):
        self._check(x, self._width, "x")
        self._check(y, self._width, "y")
        return self._mat[y - 1][x - 1]

    def export(self):
        result = str()
        for line in self._mat:
            for cell in line:
                result += cell
        return result

    def load(self, string):
        if type(string) is not str:
            raise TypeError("string is not a string type")
        if len(string) != self._width * self._height:
            raise ValueError("string lenght isn't equal to {}".format(self._width * self._height))
        i = 0
        s = 0
        while i != self._height:
            self._mat[i] = list(string[s:s + self._width])
            i += 1
            s += self._width
    
    get_cell_content = get_cell # For retro-compability