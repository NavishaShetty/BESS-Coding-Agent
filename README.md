# BESS Coding Agent

## Overview
The **BESS Coding Agent Project** is designed to assist with analyzing Day-Ahead Market (DAM) prices and optimizing battery energy storage system (BESS) operations. This project leverages AI tools to determine optimal charge/discharge hours, simulate trading strategies, and summarize market data.

I also have a data_fetcher.py that can be used to fetch and store data unde the 'data' folder for whichever date we are interested in from the modo energy API. 

## Features
- **Optimal Charge/Discharge Hours**: Identifies the best hours to charge and discharge based on DAM prices.
- **BESS Trading Simulation**: Simulates charging and discharging operations to estimate profits.
- **Market Summary**: Provides statistical insights into DAM prices, including min, max, mean, and standard deviation.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/BESS-Coding-Agent.git
   cd BESS-Coding-Agent
2. Run the following command to install required packages
   ```bash
   pip install -r requirements.txt
3. Run the following command to see the agent in action.
   ```bash
   python energy_agent.py
