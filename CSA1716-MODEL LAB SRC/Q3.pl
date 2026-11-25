% CNF Knowledge Base for the Happy Student Problem
% (1) Anyone passing history exams and winning the lottery is happy
kb_clause([not(pass(X, history)), not(win(X, lottery)), happy(X)]).

% (2) Anyone who studies or is lucky can pass all their exams
kb_clause([not(study(X)), pass(X, _)]).
kb_clause([not(lucky(X)), pass(X, _)]).

% (3) John did not study, but he is lucky
kb_clause([not(study(john))]).
kb_clause([lucky(john)]).

% (4) Anyone who is lucky wins the lottery
kb_clause([not(lucky(X)), win(X, lottery)]).

% Complementary literals
complement(not(P), P).
complement(P, not(P)) :- P \= not(_).

% Remove duplicate literals from a resolvent clause
remove_dups([], []).
remove_dups([H|T], R) :-
    member(X, T), X == H, !,
    remove_dups(T, R).
remove_dups([H|T], [H|R]) :-
    remove_dups(T, R).

% Single resolution step between current clause and a KB clause
resolve_step(Goal, NewGoal, UsedClause) :-
    select(Lit, Goal, RestGoal),
    kb_clause(UsedClause),
    select(CompLit, UsedClause, RestClause),
    complement(Lit, CompLit),
    append(RestGoal, RestClause, Combined),
    remove_dups(Combined, NewGoal).

% Resolution refutation loop (derives empty clause [])
refute([], _, []) :- !.
refute(Goal, Depth, [step(Goal, UsedClause, NewGoal)|Trace]) :-
    Depth > 0,
    resolve_step(Goal, NewGoal, UsedClause),
    D1 is Depth - 1,
    refute(NewGoal, D1, Trace).

% Display the resolution proof trace
print_trace([]).
print_trace([step(G, C, NG)|T]) :-
    format('Resolve ~w with ~w => ~w~n', [G, C, NG]),
    print_trace(T).

% Main query predicate
prove_happy(Person) :-
    NegGoal = [not(happy(Person))],
    format('Negated Goal: ~w~n', [NegGoal]),
    refute(NegGoal, 10, Trace), !,
    print_trace(Trace),
    format('Empty clause [] derived! Contradiction reached.~n', []),
    format('Therefore, ~w is happy (PROVED).~n', [Person]).
