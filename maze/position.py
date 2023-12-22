def position_mouse(maze_file):
    for row in range(len(maze_file)):
        for cell in range(len(maze_file[row])):
            if maze_file[row][cell] == 'm':
                return cell, row

def position_cheese(maze_file):
    for row in range(len(maze_file)):
        for cell in range(len(maze_file[row])):
            if maze_file[row][cell] == 'e':
                return cell, row
    return None, None
            
    
