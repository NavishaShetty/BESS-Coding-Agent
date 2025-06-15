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
            print(df)
            # parsing json and converting to dataframe
            result_df = pd.json_normalize(df['results'])
            return result_df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

    def get_available_regions(self):
        """Get list of available regions."""
        return ["ERCOT", "CAISO"]

if __name__ == "__main__":
    # Example usage
    fetcher = DataFetcher()
    start_date = "2024-05-31"
    end_date = "2025-05-31"

    #Add your base_url here
    #base_url = "https://api.modoenergy.com/pub/v1/us"
    base_url = "https://api.modoenergy.com/pub/v1/us/ercot/dam/historical-prices"    
    #base_url = "https://api.modoenergy.com/pub/v1/us/ercot/system/demand"
    
    data = fetcher.fetch_data(base_url, start_date, end_date)
    print(data.head())

    # Change the name of the csv file as per the data fetched
    data.to_csv("dam_historical_prices_data_may31_2025.csv", index=False)
    