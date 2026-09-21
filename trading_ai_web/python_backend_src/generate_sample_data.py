#!/usr/bin/env python3

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data(num_candles=100, trend='uptrend', volatility=0.02):
    """
    Generate synthetic OHLC data for testing
    
    Args:
        num_candles: Number of candles to generate
        trend: 'uptrend', 'downtrend', or 'sideways'
        volatility: Price volatility (as decimal)
    """
    
    dates = pd.date_range(end=datetime.now(), periods=num_candles, freq='D')
    
    close_prices = [100]  # Starting price
    
    for i in range(1, num_candles):
        if trend == 'uptrend':
            daily_return = np.random.normal(0.001, volatility)
        elif trend == 'downtrend':
            daily_return = np.random.normal(-0.001, volatility)
        else:  # sideways
            daily_return = np.random.normal(0, volatility)
        
        new_close = close_prices[-1] * (1 + daily_return)
        close_prices.append(new_close)
    
    # Generate OHLC from close prices
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    
    for i, close in enumerate(close_prices):
        open_price = close_prices[i-1] if i > 0 else close * (1 + np.random.uniform(-0.01, 0.01))
        high = max(open_price, close) * (1 + np.abs(np.random.normal(0, volatility)))
        low = min(open_price, close) * (1 - np.abs(np.random.normal(0, volatility)))
        volume = np.random.uniform(1000000, 5000000)
        
        opens.append(open_price)
        highs.append(high)
        lows.append(low)
        closes.append(close)
        volumes.append(volume)
    
    data = pd.DataFrame({
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes,
        'Adj Close': closes
    }, index=dates)
    
    return data

def main():
    """Generate and save sample data files"""
    
    print("Generating sample data...")
    
    # Create data directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)
    
    # Generate different scenarios
    scenarios = [
        {'filename': '../data/sample_uptrend.csv', 'trend': 'uptrend', 'volatility': 0.015},
        {'filename': '../data/sample_downtrend.csv', 'trend': 'downtrend', 'volatility': 0.015},
        {'filename': '../data/sample_sideways.csv', 'trend': 'sideways', 'volatility': 0.02},
    ]
    
    for scenario in scenarios:
        data = generate_sample_data(
            num_candles=200,
            trend=scenario['trend'],
            volatility=scenario['volatility']
        )
        data.to_csv(scenario['filename'])
        print(f"✓ Generated {scenario['filename']}")
        print(f"  Trend: {scenario['trend']}")
        print(f"  Candles: {len(data)}")
        print(f"  Price Range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}\n")

if __name__ == "__main__":
    main()
