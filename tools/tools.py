import pandas as pd
from smolagents import tool

# Load your DataFrame ONCE (at the module level)
df = pd.read_csv("/Users/navisha/Desktop/PROJECTS/AI-Agents/BESS-Coding-Agent/data/dam_historical_prices_data.csv")

@tool
def optimal_charge_discharge_hours(settlement_point: str) -> tuple[float, float]:
    """
    Determines the best hours to charge and discharge based on DAM prices.

    Args:
        settlement_point (str): The name of the settlement point to filter the data.

    Returns:
        str: A formatted string showing the best hours to charge (lowest prices) and discharge (highest prices).
    """
    local_df = df[df['settlementPointName'] == settlement_point]
    lowest = local_df.nsmallest(2, 'settlementPointPrice')
    highest = local_df.nlargest(2, 'settlementPointPrice')
    # print(
    #     f"Best hours to CHARGE (lowest prices):\n{lowest[['hourEnding','settlementPointPrice']].to_string(index=False)}\n\n"
    #     f"Best hours to DISCHARGE (highest prices):\n{highest[['hourEnding','settlementPointPrice']].to_string(index=False)}"
    # )
    return (lowest[['hourEnding','settlementPointPrice']], highest[['hourEnding','settlementPointPrice']])

@tool
def simulate_bess_trading(settlement_point: str, bess_capacity_mwh: float = 1.0) -> str:
    """
    Simulates charging on the lowest-priced hours and discharging on the highest-priced hours, reporting profit.

    Args:
        settlement_point (str): The name of the settlement point to filter the data.
        bess_capacity_mwh (float): The capacity of the battery energy storage system in MWh. Default is 1.0.

    Returns:
        str: A formatted string showing charge hours, discharge hours, and estimated profit.
    """
    local_df = df[df['settlementPointName'] == settlement_point]
    charge_hours = local_df.nsmallest(2, 'settlementPointPrice')
    discharge_hours = local_df.nlargest(2, 'settlementPointPrice')
    revenue = discharge_hours['settlementPointPrice'].sum() * (bess_capacity_mwh / 2)
    cost = charge_hours['settlementPointPrice'].sum() * (bess_capacity_mwh / 2)
    profit = revenue - cost
    return (
        f"Charge hours:\n{charge_hours[['hourEnding','settlementPointPrice']].to_string(index=False)}\n\n"
        f"Discharge hours:\n{discharge_hours[['hourEnding','settlementPointPrice']].to_string(index=False)}\n\n"
        f"Estimated profit for {bess_capacity_mwh} MWh: ${profit:.2f}"
    )

@tool
def market_summary(settlement_point: str) -> str:
    """
    Provides a summary of DAM prices at a specific settlement point, including min, max, mean, and standard deviation.

    Args:
        settlement_point (str): The name of the settlement point to filter the data.

    Returns:
        str: A formatted string showing the market price summary.
    """
    local_df = df[df['settlementPointName'] == settlement_point]
    return (
        f"Market price summary for {settlement_point}:\n"
        f"Min: ${local_df['settlementPointPrice'].min():.2f}\n"
        f"Max: ${local_df['settlementPointPrice'].max():.2f}\n"
        f"Mean: ${local_df['settlementPointPrice'].mean():.2f}\n"
        f"Std Dev: ${local_df['settlementPointPrice'].std():.2f}"
    )
