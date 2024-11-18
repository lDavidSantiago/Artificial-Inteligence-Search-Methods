"""
David Santiago Velasco Triana
Cristian David Rivera Torres
Jhojan Stiven Castaño Jejen
"""
import random
from TreeClass import TreeNode
from collections import deque
from DrawTree import draw_tree
import matplotlib.pyplot as plt
import tkinter as tk
from Generate_Maze import generate_maze
from tkinter import messagebox
import heapq
expanded_edges = ([])
end_pos = None  # Global variable for end position




def show_alert(message):
    root = tk.Tk()
    root.withdraw()  
    messagebox.showinfo("Alert", message)
    root.destroy()    
# maze = [
#     # 0    1    2    3    4    5    6    7    8    9
#     [' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' '],  # 0
#     [' ', '#', ' ', '#', ' ', '#', ' ', '#', '#', ' '],  # 1
#     ['R', ' ', ' ', '#', ' ', ' ', ' ', '#', 'C', ' '],  # 2
#     [' ', '#', '#', '#', '#', ' ', ' ', '#', ' ', ' '],  # 3
#     [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' '],  # 4
#     ['#', '#', '#', ' ', '#', ' ', '#', '#', '#', ' '],  # 5
#     [' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],  # 6
#     [' ', '#', '#', '#', '#', '#', '#', ' ', '#', ' '],  # 7
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 8
#     [' ', '#', '#', '#', '#', '#', '#', '#', '#', ' '],  # 9
# ]



# Maze for testing UCS
maze = [
    # 0    1   2   3
    ['G', 'G',' ',' '],#0
    ['G', 'G',' ','C'],#1
    ['R', 'G',' ',' '],#2
    [' ', '#',' ','#'] #3
]
        # 0    1    2    3    4    5    6    7    8    9
test = [['#', '#', '#', ' ', ' ', ' ', ' ', 'G', ' ', ' '],#0
        ['R', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'C', ' '],#1
        [' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' '],#2
        ['#', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#'],#3
        [' ', ' ', ' ', '#', '#', '#', '#', ' ', ' ', ' '],#4
        ['#', ' ', '#', '#', ' ', '#', '#', ' ', ' ', '#'],#5
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],#6
        [' ', '#', ' ', ' ', '#', ' ', ' ', '#', '#', ' '],#7
        ['#', '#', ' ', ' ', ' ', '#', ' ', '#', ' ', ' '],#8
        [' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' '] #9
        ]

def moves(maze, x, y):
    moves = []
    if y > 0 and maze[x][y - 1] != '#':
        moves.append((x, y - 1))
    if x < len(maze) - 1 and maze[x + 1][y] != '#':
        moves.append((x + 1, y))
    if y < len(maze[0]) - 1 and maze[x][y + 1] != '#':
        moves.append((x, y + 1))
    if x > 0 and maze[x - 1][y] != '#':
        moves.append((x - 1, y))
    return moves

def explore_maze(node, maze):
    possible_moves = moves(maze, node.cords[0], node.cords[1])
    for mov in possible_moves: #Checks if move is same as parent so it doesn't go back
        if node.parent is None or mov != node.parent.cords:
            new_node = TreeNode(maze[mov[0]][mov[1]], mov)
            node.add_child(new_node)



#BFS
def bfs(nodes, maze, tupla, n):
    counter = 0
    n_expansion_reached = False
    queue = deque(nodes)
    nodes[0].cost = nodes[0].base_cost
    while queue and not n_expansion_reached:
        node = queue.popleft()
        if node.data == 'C':
            draw_tree(tupla, node.cords, "BFS")
            print("Meta Encontrada!")
            print(node.get_path_to_root())
            input()
            return True
        if not node.visited:
            node.visited = True
            explore_maze(node, maze)
            for child in node.children:
                new_cost = node.cost + child.base_cost
                child.parent = node
                child.cost = new_cost
                child.update_cost()
                print(f"Actualizando {child.cords}: costo = {child.cost}, nuevo padre = {child.parent.cords}")
                queue.append(child)
                tupla.append((node.cords, child.cords, child.cost))
                draw_tree(tupla, lambda x: x, "BFS")
                counter += 1
                if counter == n:
                    print("Expansion Limit Reached")
                    n_expansion_reached = True
                    return list(queue)
    show_alert("No se encontró solución.")
    return list(queue)
#DFS
def dfs(nodes, maze, tupla,n):
    counter = 0
    n_expansion_reached = False
    stack = []
    for node in nodes:
        stack.append(node)
    while stack and not n_expansion_reached:
        node = stack.pop()
        if node.data == 'C':
            draw_tree(tupla, node.cords, "DFS")
            print("Meta encontrada!")
            print(node.get_path_to_root())
            input()
            return True
        if not node.visited:
            node.visited = True
            explore_maze(node, maze)
            for child in reversed(node.children):
                new_cost = node.cost + child.base_cost
                child.parent = node
                child.cost = new_cost
                child.update_cost()
                stack.append(child)
                tupla.append((node.cords, child.cords, child.cost))
                draw_tree(tupla, lambda x: x, "DFS")
                counter += 1
                if counter == n:
                    print("Expansion Limit Reached")
                    n_expansion_reached = True
                    return list(stack)
    show_alert("No se encontró solución.")
    return list(stack)
#DFS con limite de expansion
def dfs_limit(nodes,maze,tupla,n,limit):
    counter = 0
    stack = []
    for node in nodes:
        stack.append(node)
    print("Limit: ",limit,"Nodo a evaluar",stack[0].cords)

    while stack:
        node = stack.pop()
        if node.data == 'C':
            print(node.cords)
            draw_tree(tupla,node.cords,"Depth First Search by Limit")
            print("Meta encontrada!")
            print(f"Ruta de camino a seguir: {node.get_path_to_root()}")
            input()
            return True
        if node.get_level() <limit:
            if not node.visited:
                node.visited = True
                explore_maze(node, maze)
                for child in reversed(node.children):
                    stack.append(child)
                for child in node.children:
                    tupla.append((node.cords, child.cords, child.cost))
                    print("Estoy en el nodo",node.cords)
                    draw_tree(tupla, lambda x: x,"Depth First Search by Limit")
                    counter += 1
                    if counter == n:
                        print("Expansion Limit Reached")
                        return list(stack)
        else:
            stack.append(node)
            print("Depht Limit Reached")
            print(f"En la profundidad {limit} devolvi los nodos {[node.cords for node in stack]}")
            return list(stack)
    show_alert("No se encontró solución.")
    return list(stack)
#Busqueda UCS
def ucs(nodes, maze, tupla, n):
    counter = 0
    priority_queue = []
    visited = set()
    # Initialize start node
    for node in nodes:
        node.cost = node.base_cost
        heapq.heappush(priority_queue, (node.cost, node))
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        # Skip if already visited
        if current_node.cords in visited:
            continue
        visited.add(current_node.cords)
        # Check if goal reached
        if current_node.data == 'C':
            draw_tree(tupla, current_node.cords, "UCS")
            print("Meta encontrada!")
            print(current_node.get_path_to_root())
            return True
        # Expand current node
        explore_maze(current_node, maze)
        # Process children
        for child in current_node.children:
            if child.cords not in visited:
                new_cost = current_node.cost + child.base_cost
                child.parent = current_node
                child.cost = new_cost
                heapq.heappush(priority_queue, (child.cost, child))
                tupla.append((current_node.cords, child.cords, child.cost))
                draw_tree(tupla, lambda x: x, "UCS")
                counter += 1
                if counter == n:
                    print("Expansion Limit Reached")
                    return [item[1] for item in priority_queue]
    
    show_alert("No se encontró solución.")
    return [item[1] for item in priority_queue]
#Busqueda Avara
def busqueda_avara(nodes, maze, tupla,n):
    counter = 0
    priority_queue = []
    for node in nodes:
            node.cost = node.base_cost
            heapq.heappush(priority_queue, (heuristic(node), node))
    while priority_queue:
        distance_to_goal, current_node = heapq.heappop(priority_queue)
        if current_node.data == 'C':
            draw_tree(tupla, current_node.cords, "Greedy")
            print("Meta encontrada!")
            print(current_node.get_path_to_root())
            return True

        explore_maze(current_node, maze)
        for child in current_node.children:
            child.parent = current_node
            heapq.heappush(priority_queue, (heuristic(child), child))
            tupla.append((current_node.cords, child.cords, heuristic(child)))
            draw_tree(tupla, lambda x: x, "Greedy")
            counter += 1
            if counter == n:
                print("Expansion Limit Reached")
                return [item[1] for item in priority_queue]
    show_alert("No se encontró solución.")
    return None
def iterative_deepening_search(nodes, maze, tupla, max_depth):
    left_nodes = dfs_limit(nodes, maze, tupla, 100, 1)
    print(left_nodes)
    for depth in range(0, max_depth + 1):
        print(f"Profundidad: {depth}")
        if left_nodes == True:
            return True
        left_nodes = dfs_limit(left_nodes, maze, tupla, 100, depth)
    print("No solution found within maximum depth")
    return left_nodes
# Función heurística (distancia Manhattan)
def set_end(new_end_pos):
    global end_pos
    end_pos = new_end_pos  # Set once
    return end_pos
def heuristic(node):
    global end_pos
    goal_x, goal_y = end_pos
    node_x, node_y = node.cords
    return abs(goal_x - node_x) + abs(goal_y - node_y)

def call_allfunctions(nodes, map, n):
    # Dictionary mapping functions to their names
    methods = {
        'DFS': lambda nodes, map, expanded_edges: dfs(nodes, map, expanded_edges, n),
        'BFS': lambda nodes, map, expanded_edges: bfs(nodes, map, expanded_edges, n),
        'UCS': lambda nodes, map, expanded_edges: ucs(nodes, map, expanded_edges, n),
        'Greedy': lambda nodes, map, expanded_edges: busqueda_avara(nodes, map, expanded_edges, n),
        'DFS Limited': lambda nodes, map, expanded_edges: dfs_limit(nodes, map, expanded_edges, n, 100),
        'Iterative Deepening': lambda nodes, map, expanded_edges: iterative_deepening_search(nodes, map, expanded_edges, n)
    }
    
    method_items = list(methods.items())
    
    while method_items:
        if nodes == True:
            print("A solution have been found")
            return True
        method_name, method_func = random.choice(method_items)
        print("Método ejecutado:", method_name)
        nodes = method_func(nodes, map, expanded_edges)
        method_items.remove((method_name, method_func))
        
    if(not method_items and nodes != True):
        print("No solution found")
        return False
if __name__ == "__main__":  
    n_map = int(input("Ingrese el tamaño del mapa n: ")) 
    m_map = int(input("Ingrese el tamaño del mapa m: "))
    map,start,end = generate_maze(n_map,m_map)
    raiz = TreeNode("R", start)
    node = [raiz]
    print("Este es el mapa que se genero")
    node[0].cost = node[0].base_cost
    plt.ion()
    call_allfunctions(node,map,10)
    plt.ioff()  
    plt.show()
