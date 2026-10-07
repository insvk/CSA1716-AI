import heapq

def manhattan(state):
    return sum(abs(i // 3 - (val - 1) // 3) + abs(i % 3 - (val - 1) % 3)
               for i, val in enumerate(state) if val)

def solve_8_puzzle(start):
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    queue = [(manhattan(start), 0, start, [])]
    visited = set()
    
    while queue:
        _, g, current, path = heapq.heappop(queue)
        
        if current == goal:
            return path + [current]
            
        if current in visited:
            continue
            
        visited.add(current)
        idx = current.index(0)
        r, c = idx // 3, idx % 3
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= r + dr < 3 and 0 <= c + dc < 3:
                new_idx = (r + dr) * 3 + (c + dc)
                new_state = list(current)
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                new_state = tuple(new_state)
                
                if new_state not in visited:
                    heapq.heappush(queue, (g + 1 + manhattan(new_state), g + 1, new_state, path + [current]))
    return None

if __name__ == "__main__":
    start_state = (1, 2, 3, 4, 0, 5, 6, 7, 8)
    solution = solve_8_puzzle(start_state)
    
    if solution:
        for step in solution:
            for i in range(0, 9, 3):
                print(step[i:i+3])
            print("-" * 10)
    else:
        print("No solution exists")

        
