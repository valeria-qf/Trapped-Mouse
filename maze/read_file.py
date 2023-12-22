def read_file(filename):
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            line_clean = line.replace(' ', '')
            chars = list(line_clean.strip())
            maze.append(chars)
        return maze