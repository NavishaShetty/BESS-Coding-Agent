import os
from dotenv import load_dotenv, find_dotenv
import numpy as np
import pandas as pd

def load_env():
    _ = load_dotenv(find_dotenv())

def get_openrouter_api_key():
    load_env()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    return openrouter_api_key

def get_huggingface_token():
    load_env()
    hf_token = os.getenv("hf_token")
    return hf_token
