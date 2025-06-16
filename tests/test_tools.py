import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.tools import (
    load_prices, _extreme, get_highest_price, get_lowest_price,
    get_cheapest_charge_window, get_best_discharge_window,
    get_price_spread, get_cycle_profit, count_expensive_hours,
    count_cheap_hours
)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'hourEnding': [1, 2, 3, 4],
        'settlementPointPrice': [20.5, 45.0, 15.0, 60.0]
    })

def test_load_prices():
    """Test load_prices function"""
    # Create a temporary CSV file for testing
    test_df = pd.DataFrame({
        'settlementPointName': ['HB_NORTH', 'HB_SOUTH'],
        'hourEnding': [1, 1],
        'settlementPointPrice': [25.0, 30.0]
    })
    test_path = 'test_prices.csv'
    test_df.to_csv(test_path, index=False)
    
    result = load_prices('HB_NORTH')
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['hourEnding', 'settlementPointPrice']
    
    # Cleanup
    os.remove(test_path)

def test_extreme(sample_data):
    # Test maximum
    max_result = _extreme(sample_data, 'max')
    assert max_result['hour'] == 4
    assert max_result['price'] == 60.0
    
    # Test minimum
    min_result = _extreme(sample_data, 'min')
    assert min_result['hour'] == 3
    assert min_result['price'] == 15.0

def test_get_highest_price(sample_data):
    """Test get_highest_price function"""
    result = get_highest_price(sample_data)
    assert result['hour'] == 4
    assert result['price'] == 60.0

def test_get_lowest_price(sample_data):
    """Test get_lowest_price function"""
    result = get_lowest_price(sample_data)
    assert result['hour'] == 3
    assert result['price'] == 15.0

def test_get_cheapest_charge_window(sample_data):
    """Test get_cheapest_charge_window function"""
    result = get_cheapest_charge_window(sample_data, cheap_threshold=25.0)
    assert result == [1, 3]

def test_get_best_discharge_window(sample_data):
    """Test get_best_discharge_window function"""
    result = get_best_discharge_window(sample_data, expensive_threshold=50.0)
    assert result == [4]

def test_get_price_spread(sample_data):
    """Test get_price_spread function"""
    result = get_price_spread(sample_data)
    assert result == 45.0  # 60.0 - 15.0 = 45.0

def test_get_cycle_profit():
    """Test get_cycle_profit function"""
    result = get_cycle_profit(
        battery_mwh=1.0,
        charge_eff=0.9,
        discharge_eff=0.9,
        lowest_price=15.0,
        highest_price=60.0
    )
    expected = round(1.0 * 0.9 * 60.0 - 1.0 / 0.9 * 15.0, 2)
    assert result == expected

def test_count_expensive_hours(sample_data):
    """Test count_expensive_hours function"""
    result = count_expensive_hours(sample_data, price_threshold=50.0)
    assert result == 1

def test_count_cheap_hours(sample_data):
    """Test count_cheap_hours function"""
    result = count_cheap_hours(sample_data, price_threshold=25.0)
    assert result == 2

def test_edge_cases():
    """Test edge cases"""
    # Empty DataFrame
    empty_df = pd.DataFrame(columns=['hourEnding', 'settlementPointPrice'])
    
    # Test with empty DataFrame
    assert get_price_spread(empty_df) == 0
    assert count_expensive_hours(empty_df) == 0
    assert count_cheap_hours(empty_df) == 0
    
    # Test with negative prices
    negative_df = pd.DataFrame({
        'hourEnding': [1],
        'settlementPointPrice': [-10.0]
    })
    assert get_lowest_price(negative_df)['price'] == -10.0