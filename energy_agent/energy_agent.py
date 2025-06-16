import phoenix as px
from energy_agent.config import config
from phoenix.otel import register
from smolagents import CodeAgent, OpenAIServerModel, GradioUI
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from energy_agent.tools import load_prices, _extreme, get_highest_price, get_lowest_price, get_cheapest_charge_window, get_best_discharge_window, get_price_spread, get_cycle_profit, count_expensive_hours, count_cheap_hours

class EnergyAgent():
    def __init__(self):
        self.api_key=config.OPENROUTER_API_KEY 
        self.model_id=config.MODEL 
        self.api_base=config.OPENROUTER_API_BASE 

    def energy_agent(self):
        model = OpenAIServerModel(
            model_id=self.model_id,  
            api_base=self.api_base,   
            api_key=self.api_key        
        )

        tools = [
            load_prices,
            _extreme,
            get_highest_price,
            get_lowest_price,
            get_cheapest_charge_window,
            get_best_discharge_window,
            get_price_spread,
            get_cycle_profit,
            count_expensive_hours,
            count_cheap_hours   
        ]

        agent = CodeAgent(
            model=model,
            additional_authorized_imports=[
                "geopandas",
                "plotly",
                "plotly.express", 
                "plotly.express.colors",
                "shapely",
                "json",
                "pandas",
                "numpy",
            ],
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
    PROJECT_NAME = "energy_agent"

    # Launch Phoenix session and register tracer
    session = px.launch_app(host="127.0.0.1", port=6006) 
    tracer_provider = register(project_name=PROJECT_NAME)
    SmolagentsInstrumentor().instrument(tracer_provider=tracer_provider)

    # Initialize and start the Energy Agent UI
    agent = EnergyAgent()
    agent.start_ui()