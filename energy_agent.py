import pandas as pd
from smolagents import CodeAgent, OpenAIServerModel, GradioUI
from config.helper import get_openrouter_api_key
from tools.tools import optimal_charge_discharge_hours, simulate_bess_trading, market_summary

class EnergyAgent():
    def __init__(self):
        self.api_key=get_openrouter_api_key()
        self.model_id="qwen/qwen-2.5-72b-instruct:free"
        self.api_base="https://openrouter.ai/api/v1"

    def energy_agent(self):
        model = OpenAIServerModel(
            model_id="qwen/qwen-2.5-72b-instruct:free",   # name of the model to use
            api_base="https://openrouter.ai/api/v1",      # provider URL
            api_key=get_openrouter_api_key()              # API key for the provider
        )

        tools = [
            optimal_charge_discharge_hours,
            simulate_bess_trading,
            market_summary
        ]

        agent = CodeAgent(
            model=model,
            tools=tools
        )
        return agent
    
    def run(self, task: str):
        agent = self.energy_agent()
        response = agent.run(task=task)
        return response
    
    def start_ui(self):
        agent = self.energy_agent()
        GradioUI(agent).launch()

if __name__ == "__main__":
    energy_agent = EnergyAgent()

    # Example task to run
    energy_agent.run(task= "Given the DAM price data, what are the best hours to charge and discharge at LZ_WEST?")

    # Uncomment the line below to start the UI
    energy_agent.start_ui()