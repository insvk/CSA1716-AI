symptom(john, fever).
symptom(john, cough).
symptom(john, headache).

symptom(mary, cough).
symptom(mary, sneezing).

disease(Patient, flu) :-
    symptom(Patient, fever),
    symptom(Patient, cough),
    symptom(Patient, headache).

disease(Patient, cold) :-
    symptom(Patient, cough),
    symptom(Patient, sneezing).

disease(Patient, measles) :-
    symptom(Patient, fever),
    symptom(Patient, rash).

disease(Patient, allergy) :-
    symptom(Patient, sneezing),
    symptom(Patient, rash).
