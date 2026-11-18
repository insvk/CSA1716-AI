# pgmpy Bayesian-network example.
# Compatible with recent pgmpy versions.
try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
except ImportError:
    from pgmpy.models import BayesianNetwork

from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = BayesianNetwork([("Rain", "WetGrass")])

cpd_rain = TabularCPD(
    variable="Rain",
    variable_card=2,
    values=[[0.8], [0.2]],
    state_names={"Rain": ["False", "True"]},
)
cpd_wetgrass = TabularCPD(
    variable="WetGrass",
    variable_card=2,
    values=[[0.9, 0.2], [0.1, 0.8]],
    evidence=["Rain"],
    evidence_card=[2],
    state_names={"Rain": ["False", "True"], "WetGrass": ["False", "True"]},
)

model.add_cpds(cpd_rain, cpd_wetgrass)
if not model.check_model():
    raise ValueError("The Bayesian network CPDs are inconsistent.")

infer = VariableElimination(model)
result = infer.query(variables=["Rain"], evidence={"WetGrass": 1})
print("Probability of Rain given that the grass is wet:")
print(result)
