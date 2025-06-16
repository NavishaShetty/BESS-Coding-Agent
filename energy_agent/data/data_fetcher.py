import pandas as pd
import requests

class DataFetcher:
    def __init__(self, api_key=None):
        """Initialize the DataFetcher"""
        self.headers = {
            "accept": "application/json"
        }

    def fetch_data(self, base_url, start_date, end_date):
        """Fetch Day-Ahead Market (DAM) bids data for a region and date range."""
        endpoint = base_url
        params = {
            "date_from": start_date,
            "date_to": end_date
        }
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
    
    def parse_json_to_dataframe(self, json_data):
        """Parse JSON data to a pandas DataFrame."""
        result_df = pd.json_normalize(json_data['results'])
        return result_df

if __name__ == "__main__":
    # Example usage
    get_data = DataFetcher()
    start_date = "2024-05-31"
    end_date = "2025-05-31"

    #Add your base_url here
    base_url = "https://api.modoenergy.com/pub/v1/us/ercot/dam/historical-prices"    
    
    raw_data = get_data.fetch_data(base_url, start_date, end_date)
    data = get_data.parse_json_to_dataframe(raw_data)

    print(data.head())

    # Change the name of the csv file as per the data fetched
    data.to_csv("dam_historical_prices_data_may31_2025.csv", index=False)
    