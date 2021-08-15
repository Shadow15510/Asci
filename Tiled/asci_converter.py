def to_string(csv_filename, output_filename="world"):
    char_list = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "

    with open(csv_filename, "r") as file:
            data = [[int(char_id) for char_id in line.split(",")] for line in file.read().splitlines()]

    output = r""
    for line in data:
        for char_id in line:
            output += char_list[char_id]
        output += "\n"

    with open(f"{output_filename}.py", "w") as file:
        file.write(f"{output_filename}_map = r\"\"\"\n{output}\n\"\"\"")