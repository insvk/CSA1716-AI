fruit(apple, red).
fruit(banana, yellow).
fruit(grape, purple).
fruit(orange, orange).
fruit(lemon, yellow).
fruit(strawberry, red).

find_fruit(Color, Fruit) :-
    fruit(Fruit, Color).
