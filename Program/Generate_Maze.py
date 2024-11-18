import random 
def generate_maze(n, m):
    # Use 0.3 (30%) probability for wall generation
    maze = [[' ' if random.random() > 0.3 else '#' for i in range(n)] for j in range(m)]
    
    rows = len(maze)
    cols = len(maze[0])

    # Root and Goal
    x1, y1 = random.randint(0, rows-1), random.randint(0, cols-1)
    while True:
        x2, y2 = random.randint(0, rows-1), random.randint(0, cols-1)
        if (x2, y2) != (x1, y1):
            break
    maze[x1][y1] = 'R'
    maze[x2][y2] = 'C'
    return maze, (x1,y1), (x2,y2)