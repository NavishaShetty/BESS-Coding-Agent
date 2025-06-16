import phoenix as px
from phoenix.otel import register
from energy_agent import EnergyAgent
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

def main():
    PROJECT_NAME = "energy_agent"

    # Create an instance of the energy agent
    agent = EnergyAgent()

    # Launch Phoenix session and register tracer
    session = px.launch_app(host="127.0.0.1", port=6006) 
    tracer_provider = register(project_name=PROJECT_NAME)
    SmolagentsInstrumentor().instrument(tracer_provider=tracer_provider)
    
    # Replace with the task you want to the agent to perform
    agent.run(task = "What is the highest price for discharging at settlement point LZ_WEST?")

if __name__ == "__main__":
    main()