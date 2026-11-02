import heapq

def best_first_search(graph, heuristics, start, goal):
    pq = [(heuristics[start], start, [start])]
    visited = set()
    while pq:
        h, current, path = heapq.heappop(pq)
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (heuristics.get(neighbor, float("inf")), neighbor, path + [neighbor]))
    return None

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [],
    "E": [],
    "F": ["Goal"],
    "G": [],
    "Goal": []
}

heuristics = {
    "A": 6,
    "B": 4,
    "C": 3,
    "D": 5,
    "E": 4,
    "F": 1,
    "G": 2,
    "Goal": 0
}

path = best_first_search(graph, heuristics, "A", "Goal")
print("Best First Search Path:", path)
