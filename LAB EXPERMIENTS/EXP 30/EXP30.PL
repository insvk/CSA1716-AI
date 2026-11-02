fact(croaks).
fact(eats_flies).

rule(frog, [croaks, eats_flies]).
rule(green, [frog]).

backward_chain(Goal) :-
    fact(Goal),
    format("Direct fact proven: ~w~n", [Goal]).
backward_chain(Goal) :-
    rule(Goal, SubGoals),
    format("To prove ~w, proving: ~w~n", [Goal, SubGoals]),
    prove_all(SubGoals).

prove_all([]).
prove_all([G | Rest]) :-
    backward_chain(G),
    prove_all(Rest).
