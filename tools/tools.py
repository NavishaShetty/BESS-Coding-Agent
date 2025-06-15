import pandas as pd
from smolagents import tool

from pathlib import Path
from typing import Dict, List, Tuple, Callable

# Load DataFrame
dam = pd.read_csv("/Users/navisha/Desktop/PROJECTS/AI-Agents/BESS-Coding-Agent/data/dam_historical_prices_data_may31_2025.csv")

# ------------------------------------loading & filtering data--------------------------------------
@tool
def load_prices(settlement_point: str) -> pd.DataFrame:
    """
    Returns a DataFrame filtered to one settlement point (node).

    Args:
        settlement_point (str): The name of the settlement point to filter the data.

    Returns:
        pd.DataFrame: A Dataframe with Columns: 
            - hourEnding (int 1‑24), 
            - settlementPointPrice (float).
    """
    df = (
        dam[dam["settlementPointName"] == settlement_point]
        .loc[:, ["hourEnding", "settlementPointPrice"]]
        .sort_values("hourEnding")
        .reset_index(drop=True)
    )
    return df

@tool
def _extreme(df: pd.DataFrame, kind: str = "max") -> Dict[str, float]:
    """
    Finds the extreme (maximum or minimum) settlement point price in the given DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing settlement point price data with columns:
            - "hourEnding" (int): The hour of the day (1‑24).
            - "settlementPointPrice" (float): The price at the settlement point.
        kind (str): Specifies whether to find the "max" or "min" price. Default is "max".

    Returns:
        Dict[str, float]: A dictionary containing:
            - "hour" (int): The hour corresponding to the extreme price.
            - "price" (float): The extreme price (rounded to 2 decimal places).
    """
    idx = df["settlementPointPrice"].idxmax() if kind == "max" else df["settlementPointPrice"].idxmin()
    row = df.loc[idx]
    return {"hour": int(row["hourEnding"]), "price": float(round(row["settlementPointPrice"], 2))}

@tool
def get_highest_price(df: pd.DataFrame) -> Dict[str, float]:
    """
    Highest hourly price.  
    Args:
        df: DataFrame with rows for a particular settlement point
    Returns
      ``{"hour": int, "price": float}``."""
    return _extreme(df, "max")

@tool
def get_lowest_price(df: pd.DataFrame) -> Dict[str, float]:
    """Lowest hourly price.  
    Args:
        df: DataFrame with rows for a particular settlement point
    Returns:
        ``{"hour": int, "price": float}``.
    """
    return _extreme(df, "min")

# -------------------------------charging & discharging windows--------------------------------------------
@tool
def _hours_where(df: pd.DataFrame, threshold: float) -> List[int]:
    """
    Filters the DataFrame based on a threshold applied to the settlement point price and returns a list of hours.

    Args:
        df (pd.DataFrame): A DataFrame with rows for a particular settlement point
        threshold: A threshold to check the price against. 

    Returns:
        List[int]: A list of hours (1 - 24) where the predicate condition is satisfied.
    """
    return df[df["settlementPointPrice"].apply(threshold)]["hourEnding"].astype(int).tolist()

@tool
def get_cheapest_charge_window(df: pd.DataFrame, cheap_threshold: float = 25.0) -> List[int]:
    """Return a list of hours where price ≤ `cheap_threshold` (USD/MWh).
    
    Args:
        df: DataFrame with rows for a particular settlement point
        cheap_threshold: Price threshold to identify cheap hours.
    Returns:
        List[int]: A list of hours (1 - 24) where the settlement point price is less than or equal to the specified threshold.
    """
    return _hours_where(df, lambda p: p <= cheap_threshold)

@tool
def get_best_discharge_window(df: pd.DataFrame, expensive_threshold: float = 50.0) -> List[int]:
    """Return a list of hours where price ≥ `expensive_threshold` (USD/MWh).
    Args:
        df: DataFrame with rows for a particular settlement point
        expensive_threshold: Price threshold to identify expensive hours.
    Returns:
        List[int]: A list of hours (1 - 24) where the settlement point price is greater than or equal to the specified threshold.
    """
    return _hours_where(df, lambda p: p >= expensive_threshold)


# ----------------------------------simple spread-----------------------------------------
@tool
def get_price_spread(df: pd.DataFrame) -> float:
    """Return (max - min) price for the day, rounded to 2 decimal points.
    Args:
        df: DataFrame with rows for a particular settlement point
    Returns:
        float: Price spread (USD/MWh)
    """
    hi = df["settlementPointPrice"].max()
    lo = df["settlementPointPrice"].min()
    return round(hi - lo, 2)

# ---------------------------------one cycle profit---------------------------------------
@tool
def get_cycle_profit(
    battery_mwh: float = 1.0,
    charge_eff: float = 1.0,
    discharge_eff: float = 1.0,
    lowest_price: float = None,
    highest_price: float = None,
) -> float:
    """Profit from a single cycle of charge to discharge.

    Picks the cheapest hour to buy and the most expensive hour to sell.

    Args:
        battery_mwh: Energy capacity.
        charge_eff: Charge efficiency (0 to 1) 
        discharge_eff: Discharge efficiency (0 to 1)
        lowest_price: provide the lowest price (USD/MWh). If not provided, it will be computed from the data.
        highest_price: provide the highest price (USD/MWh). If not provided, it will be computed from the data.
    
    Returns:
        float: Estimated profit in USD, rounded to 2 decimal points.
    """
    buy_cost = battery_mwh / charge_eff * lowest_price
    sell_revenue = battery_mwh * discharge_eff * highest_price
    return round(sell_revenue - buy_cost, 2)

# -----------------------------counting hours above / below thresholds-----------------------------------
@tool
def count_expensive_hours(df: pd.DataFrame, price_threshold: float = 50.0) -> int:
    """
    Number of hours with price ≥ `price_threshold`.

    Args:
        df: DataFrame with rows for a particular settlement point
        price_threshold: Price threshold to identify expensive hours.

    Returns:
        int: Count of hours where the settlement point price is greater than or equal to the specified threshold.
    """
    return int((df["settlementPointPrice"] >= price_threshold).sum())

@tool
def count_cheap_hours(df: pd.DataFrame, price_threshold: float = 25.0) -> int:
    """
    Number of hours with price ≤ `price_threshold`.
    Args:
        df: DataFrame with rows for a particular settlement point
        price_threshold: Price threshold to identify cheap hours.
    Returns:
        int: Count of hours where the settlement point price is less than or equal to the specified threshold.
    """
    return int((df["settlementPointPrice"] <= price_threshold).sum())