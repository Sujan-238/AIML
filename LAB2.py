from collections import deque

# Social Network Graph
graph = {
    "Alice": ["Charlie", "David"],
    "Bob": ["Emma", "Fred"],
    "Charlie": ["Alice", "Emma"],
    "David": ["Alice", "Emma", "Fred"],
    "Emma": ["Bob", "Charlie", "David"],
    "Fred": ["Bob", "David"]
}

# Arrange neighbors alphabetically
for node in graph:
    graph[node].sort()


# Breadth First Search (BFS)
def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            visited.add(node)

            if node == goal:
                return path

            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


# Depth First Search (DFS)
def dfs(graph, start, goal):
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node not in visited:
            visited.add(node)

            if node == goal:
                return path

            # Reverse order so alphabetical neighbor is visited first
            for neighbor in reversed(graph[node]):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)

    return None


# Main Program
start = "Alice"
goal = "Bob"

bfs_path = bfs(graph, start, goal)
dfs_path = dfs(graph, start, goal)

print("=== Breadth First Search (BFS) ===")
print("Path:", " -> ".join(bfs_path))

print("\n=== Depth First Search (DFS) ===")
print("Path:", " -> ".join(dfs_path))