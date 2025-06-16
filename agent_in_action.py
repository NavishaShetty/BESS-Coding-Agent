import phoenix as px
from phoenix.otel import register
from energy_agent import EnergyAgent
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

PROJECT_NAME = "energy_agent"

# Launch Phoenix session and register tracer
session = px.launch_app(host="127.0.0.1", port=6006) 
tracer_provider = register(project_name=PROJECT_NAME)
SmolagentsInstrumentor().instrument(tracer_provider=tracer_provider)

# Initialize and start the Energy Agent UI
agent = EnergyAgent()
agent.start_ui()

