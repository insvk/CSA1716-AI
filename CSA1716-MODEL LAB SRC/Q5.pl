CODING
% Course eligibility rules: eligible(Course, Math, Programming, English)
eligible(artificial_intelligence, Math, Prog, Eng) :-
    Math >= 80, Prog >= 80, Eng >= 60.

eligible(data_science, Math, Prog, Eng) :-
    Math >= 85, Prog >= 75, Eng >= 65.

eligible(computer_science, Math, Prog, Eng) :-
    Math >= 70, Prog >= 75, Eng >= 60.

eligible(software_engineering, Math, Prog, Eng) :-
    Math >= 65, Prog >= 75, Eng >= 65.

eligible(technical_communication, Math, Prog, Eng) :-
    Math >= 50, Prog >= 50, Eng >= 80.

% Check eligibility for a specific course
check_course(Course, Math, Prog, Eng) :-
    eligible(Course, Math, Prog, Eng), !,
    format('Status: ELIGIBLE for ~w.~n', [Course]).
check_course(Course, _, _, _) :-
    format('Status: NOT ELIGIBLE for ~w.~n', [Course]).

% Interactive Expert System to list all eligible courses
check_eligibility :-
    write('Enter Mathematics marks (0-100): '), read(Math),
    write('Enter Programming marks (0-100): '), read(Prog),
    write('Enter English marks (0-100): '),     read(Eng),
    findall(Course, eligible(Course, Math, Prog, Eng), Courses),
    ( Courses \= [] ->
        format('Eligible Courses: ~w~n', [Courses])
    ;
        write('Not eligible for any listed course.'), nl
    ).
