import pandas as pd
import json
import phoenix as px
from phoenix.otel import register
from energy_agent.energy_agent import EnergyAgent
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

session = px.launch_app(host="127.0.0.1", port=6006) # defaults: host=127.0.0.1, port=6006
tracer_provider = register(project_name="energy_agent_evaluation")
SmolagentsInstrumentor().instrument(tracer_provider=tracer_provider) 

agent = EnergyAgent()

# Multiple client requests for evaluation
client_requests = [
    ("What is the lowest price in the day for charging at settlement point LZ_WEST?", ["load_prices", "get_lowest_price"]),
    ("What is the highest price in the day for discharging at settlement point LZ_WEST?", ["load_prices", "get_highest_price"]),
    ("What would be the cycle profit if I charge during best charge window and discharge during best discharge window on an average at LZ_WEST?", ["load_prices", "get_cheapest_charge_window", "get_best_discharge_window", "get_cycle_profit"]),
    ("Which region has the highest energy demand?", None),
    ("What's the weather in California right now?", None),
    ("How many hours are there in the best charge window at HB_HOUSTON?", ["load_prices", "count_cheap_hours"]),
]

for request in client_requests:
    agent.run(request[0])

# To get all the traces from Phoenix as a dataframe of the different spans
spans = px.Client().get_spans_dataframe(project_name="energy_agent_evaluation")

# Processing the spans dataframe to get the tool calls performed by the agent for each request
agents = spans[spans['span_kind'] == 'AGENT'].copy()
agents['task'] = agents['attributes.input.value'].apply(
    lambda x: json.loads(x).get('task') if isinstance(x, str) else None)

tools = spans.loc[spans['span_kind'] == 'TOOL',["attributes.tool.name", "attributes.input.value", "context.trace_id"]].copy()

tools_per_task = agents[["name", "start_time", "task", "context.trace_id"]
                    ].merge(
                        tools,
                        on="context.trace_id",
                        how="left",
                    )

# Function to check if the tool calls match the expected tools for each request
def score_request(expected_tool, tool_calls):
    
    if expected_tool is None:
        return tool_calls == set(["final_answer"])
    elif isinstance(expected_tool, list):
        return any(tool in tool_calls for tool in expected_tool)
    else:
        return expected_tool in tool_calls

results = []
for request, expected_tool in client_requests:
    tool_calls = set(tools_per_task.loc[tools_per_task["task"] == request, "attributes.tool.name"].tolist())
    results.append(
        {
            "request": request,
            "tool_calls_performed": tool_calls,
            "is_correct": score_request(expected_tool, tool_calls)
        }
    )
results = pd.DataFrame(results)
results.to_csv("evaluation_results.csv", index=False)
print(results)

# Keep the session alive
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nStopping the Phoenix session...")