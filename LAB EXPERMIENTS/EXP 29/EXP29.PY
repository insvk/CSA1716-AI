facts = {"croaks", "eats_flies"}
rules = [
    ({"croaks", "eats_flies"}, "frog"),
    ({"frog"}, "green")
]

def forward_chaining(facts, rules):
    inferred = set(facts)
    changed = True
    while changed:
        changed = False
        for premises, conclusion in rules:
            if premises.issubset(inferred) and conclusion not in inferred:
                inferred.add(conclusion)
                print(f"Derived: {conclusion}")
                changed = True
    return inferred

print("Initial Facts:", facts)
final_facts = forward_chaining(facts, rules)
print("Final Derived Facts:", final_facts)
