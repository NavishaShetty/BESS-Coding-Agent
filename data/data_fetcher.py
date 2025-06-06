import os
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path

class DataFetcher:
    def __init__(self, api_key=None):
        """Initialize the DataFetcher"""
        #self.base_url = "https://api.modoenergy.com/pub/v1/us"
        self.base_url = "https://api.modoenergy.com/pub/v1/us/ercot/dam/historical-prices"
        self.headers = {
            "accept": "application/json"
        }

    def fetch_dam_data(self, start_date, end_date):
        """Fetch Day-Ahead Market (DAM) bids data for a region and date range."""
        endpoint = self.base_url
        params = {
            "date_from": start_date,
            "date_to": end_date
        }
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            # parsing json and converting to dataframe
            result_df = pd.json_normalize(df['results'])
            return result_df
        except Exception as e:
            print(f"Error fetching DAM data: {e}")
            return pd.DataFrame()

    def get_available_regions(self):
        """Get list of available regions."""
        return ["ERCOT", "CAISO"]

if __name__ == "__main__":
    # Example usage
    fetcher = DataFetcher()
    start_date = "2025-05-31"
    end_date = "2025-05-31"
    dam_data = fetcher.fetch_dam_data(start_date, end_date)
    dam_data.to_csv("data/dam_historical_prices_data.csv", index=False)
    