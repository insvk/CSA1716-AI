knowledge_base = {
    "flu": {"fever", "cough", "headache"},
    "cold": {"cough", "sneezing"},
    "measles": {"fever", "rash"},
    "allergy": {"sneezing", "rash"}
}

def diagnose(patient_symptoms):
    results = []
    for disease, symptoms in knowledge_base.items():
        if symptoms.issubset(patient_symptoms):
            results.append(disease)
    return results

patient = {"fever", "cough", "headache"}
print("Patient Symptoms:", patient)
print("Diagnosed Disease:", diagnose(patient))
