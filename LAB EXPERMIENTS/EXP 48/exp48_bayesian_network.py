# Note: Requires pgmpy (pip install pgmpy)
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define Network Structure: Rain causes WetGrass
model = BayesianNetwork([('Rain', 'WetGrass')])

# Define Probabilities
# P(Rain): 20% True (1), 80% False (0)
cpd_rain = TabularCPD(variable='Rain', variable_card=2, values=[[0.8], [0.2]])

# P(WetGrass | Rain)
# Rain=0 (False): WetGrass=0 (90%), WetGrass=1 (10%)
# Rain=1 (True):  WetGrass=0 (20%), WetGrass=1 (80%)
cpd_wetgrass = TabularCPD(variable='WetGrass', variable_card=2, 
                          values=[[0.9, 0.2], 
                                  [0.1, 0.8]],
                          evidence=['Rain'], evidence_card=[2])

model.add_cpds(cpd_rain, cpd_wetgrass)

# Validate Model
assert model.check_model()

# Perform Inference
infer = VariableElimination(model)
print("Querying Probability of Rain given the Grass is Wet...")
prob = infer.query(variables=['Rain'], evidence={'WetGrass': 1})
print(prob)
