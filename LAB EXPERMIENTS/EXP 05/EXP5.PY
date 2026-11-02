from collections import deque

MISSIONARIES = 3
CANNIBALS = 3


def is_valid(state):
    m_left, c_left, boat = state
    m_right = MISSIONARIES - m_left
    c_right = CANNIBALS - c_left

    # Check left bank safety
    if m_left > 0 and c_left > m_left:
        return False
    # Check right bank safety
    if m_right > 0 and c_right > m_right:
        return False
    return True


def next_states(state):
    m_left, c_left, boat = state
    moves = []

    for m in range(3):
        for c in range(3):
            if m + c == 0 or m + c > 2:
                continue

            if boat == 1:  # boat on left
                nm = m_left - m
                nc = c_left - c
                if nm < 0 or nc < 0:
                    continue
                next_state = (nm, nc, 0)
            else:  # boat on right
                nm = m_left + m
                nc = c_left + c
                if nm > MISSIONARIES or nc > CANNIBALS:
                    continue
                next_state = (nm, nc, 1)

            if is_valid(next_state):
                moves.append(next_state)

    return moves


def solve():
    start = (MISSIONARIES, CANNIBALS, 1)  # (m_left, c_left, boat_on_left)
    goal = (0, 0, 0)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for nxt in next_states(state):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return None


path = solve()
if path is None:
    print("No solution found.")
else:
    print("Missionaries and Cannibals Solution:")
    for i, (m, c, boat) in enumerate(path, start=1):
        side = "Left" if boat == 1 else "Right"
        print(f"Step {i}: Missionaries={m}, Cannibals={c}, Boat={side}")
