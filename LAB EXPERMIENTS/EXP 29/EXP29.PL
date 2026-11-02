:- dynamic fact/1.

fact(croaks).
fact(eats_flies).

rule(frog, [croaks, eats_flies]).
rule(green, [frog]).

forward_chain :-
    rule(Conclusion, Premises),
    \+ fact(Conclusion),
    all_facts(Premises),
    assertz(fact(Conclusion)),
    format("Derived: ~w~n", [Conclusion]),
    forward_chain.
forward_chain :-
    write("Forward chaining finished."), nl.

all_facts([]).
all_facts([H | T]) :-
    fact(H),
    all_facts(T).
