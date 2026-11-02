edge(a, b).
edge(a, c).
edge(b, d).
edge(b, e).
edge(c, f).
edge(c, g).
edge(f, goal).

h(a, 6).
h(b, 4).
h(c, 3).
h(d, 5).
h(e, 4).
h(f, 1).
h(g, 2).
h(goal, 0).

best_first_search(Goal, Goal, [Goal]).
best_first_search(Current, Goal, [Current | Path]) :-
    findall(Next, edge(Current, Next), Neighbors),
    best_neighbor(Neighbors, Best),
    best_first_search(Best, Goal, Path).

best_neighbor([X], X).
best_neighbor([H | T], Best) :-
    best_neighbor(T, RestBest),
    h(H, H1),
    h(RestBest, H2),
    (H1 =< H2 -> Best = H ; Best = RestBest).
