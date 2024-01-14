import heapq

class Node:
    def __init__(self, id, is_intersection):
        self.id = id
        self.is_intersection = is_intersection
        self.edges = {}
        
    def add_edge(self, child, weight):
        self.edges[child] = weight 
        
class Graph:
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, id, is_intersection):
        self.nodes[id] = Node(id, is_intersection)
        
    def add_edge(self, parent, child, weight):
        self.nodes[parent].add_edge(child, weight)
     
    def get_neighbors(self, node):
        return self.nodes[node].edges.items()
    
    def heuristic(self, node, goal):
        node_x, node_y = map(int, node.split(','))
        goal_x, goal_y = map(int, goal.split(','))
        return abs(node_x - goal_x) + abs(node_y - goal_y)

def add_nodes_from_grid(grid, graph):
    start_node = None
    destination_node = None

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is not None:
                node_id = f"{x},{y}"
                is_intersection = cell == 'I'
                graph.add_node(node_id, is_intersection)

                if cell == 'S':
                    start_node = node_id
                elif cell == 'D':
                    destination_node = node_id

    return start_node, destination_node

def add_edges_from_grid(grid, graph):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is not None:
                node_id = f"{x},{y}"
                if x < len(row) - 1 and grid[y][x+1] is not None:
                    graph.add_edge(node_id, f"{x+1},{y}", 1)
                if y < len(grid) - 1 and grid[y+1][x] is not None:
                    graph.add_edge(node_id, f"{x},{y+1}", 1)

def a_star_search(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = graph.heuristic(start, goal)
    came_from = {}

    while open_set:
        _, current_node = heapq.heappop(open_set)

        if current_node == goal:
            path = []
            travel_time = g_score[current_node]
            while current_node in came_from:
                path.insert(0, current_node)
                current_node = came_from[current_node]
            path.insert(0, start)  # Include start node in the path
            return path, travel_time

        for neighbor, weight in graph.get_neighbors(current_node):
            additional_time = 1 if graph.nodes[neighbor].is_intersection else 0
            temp_g_score = g_score[current_node] + weight + additional_time
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + graph.heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return [], 0

# Define the grid layout
grid = [
    ['S', 'R', 'I', 'R', 'R'],
    ['R', None, 'R', None, None],
    ['R', 'R', 'R', 'R', None],
    ['R', None, None, 'R', None],
    ['I', 'R', 'D', 'R', None]
]

# Initialize the graph
graph = Graph()

# Create the graph based on the grid
start_node, destination_node = add_nodes_from_grid(grid, graph)
add_edges_from_grid(grid, graph)

# Find the most efficient route and travel time using A* search
if start_node and destination_node:
    efficient_route, travel_time = a_star_search(graph, start_node, destination_node)

    # Print the efficient route and travel time
    if efficient_route:
        print("Most efficient route:", ' -> '.join(efficient_route))
        print("Travel time:", travel_time, "minutes")
    else:
        print("No route found.")
else:
    print("Start or destination node not defined in the grid.")