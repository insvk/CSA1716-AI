fruits = [
    ("apple", "red"),
    ("banana", "yellow"),
    ("grape", "purple"),
    ("orange", "orange"),
    ("lemon", "yellow"),
    ("strawberry", "red")
]

def find_fruits_by_color(color):
    result = []
    for fruit, c in fruits:
        if c == color:
            result.append(fruit)
    return result

query_color = "red"
print(f"Fruits with color '{query_color}':", find_fruits_by_color(query_color))
