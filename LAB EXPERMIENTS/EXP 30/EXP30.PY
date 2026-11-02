facts = {"croaks", "eats_flies"}
rules = {
    "green": [["frog"]],
    "frog": [["croaks", "eats_flies"]]
}

def backward_chain(goal, facts, rules, visited=None):
    if visited is None:
        visited = set()
    if goal in facts:
        return True
    if goal in visited or goal not in rules:
        return False
    visited.add(goal)
    for subgoals in rules[goal]:
        if all(backward_chain(sg, facts, rules, visited.copy()) for sg in subgoals):
            return True
    return False

query = "green"
result = backward_chain(query, facts, rules)
print(f"Query '{query}' satisfied:", result)
