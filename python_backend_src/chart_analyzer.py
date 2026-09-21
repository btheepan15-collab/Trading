import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import json

class ChartAnalyzer:
    """Analyzes trading charts and detects patterns for profit/loss scenarios"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLC data
        Expected columns: Open, High, Low, Close, Volume
        """
        self.data = data.copy()
        self.analysis_results = {}
        
    def calculate_moving_averages(self, periods=[20, 50, 200]):
        """Calculate moving averages"""
        for period in periods:
            self.data[f'MA_{period}'] = self.data['Close'].rolling(window=period).mean()
        return self.data
    
    def calculate_rsi(self, period=14):
        """Calculate Relative Strength Index"""
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.data['RSI'] = rsi
        return self.data
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        ema_fast = self.data['Close'].ewm(span=fast).mean()
        ema_slow = self.data['Close'].ewm(span=slow).mean()
        self.data['MACD'] = ema_fast - ema_slow
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=signal).mean()
        self.data['MACD_Hist'] = self.data['MACD'] - self.data['MACD_Signal']
        return self.data
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = self.data['Close'].rolling(window=period).mean()
        std = self.data['Close'].rolling(window=period).std()
        self.data['BB_Upper'] = sma + (std_dev * std)
        self.data['BB_Lower'] = sma - (std_dev * std)
        self.data['BB_Middle'] = sma
        return self.data
    
    def calculate_atr(self, period=14):
        """Calculate Average True Range"""
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        
        tr = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = tr.rolling(window=period).mean()
        self.data['ATR'] = atr
        return self.data
    
    def detect_support_resistance(self, window=5):
        """Detect support and resistance levels"""
        high_idx = self.data['High'].rolling(window=window*2+1, center=True).apply(lambda x: x.argmax()) == window
        low_idx = self.data['Low'].rolling(window=window*2+1, center=True).apply(lambda x: x.argmin()) == window
        
        resistance = self.data[high_idx]['High'].values
        support = self.data[low_idx]['Low'].values
        
        return {
            'support_levels': sorted(support[-5:]) if len(support) > 0 else [],
            'resistance_levels': sorted(resistance[-5:], reverse=True) if len(resistance) > 0 else []
        }
    
    def identify_trend(self):
        """Identify current trend"""
        self.calculate_moving_averages()
        
        current_price = self.data['Close'].iloc[-1]
        ma20 = self.data['MA_20'].iloc[-1]
        ma50 = self.data['MA_50'].iloc[-1]
        ma200 = self.data['MA_200'].iloc[-1]
        
        if current_price > ma20 > ma50 > ma200:
            trend = "STRONG UPTREND"
            strength = 0.95
        elif current_price > ma20 > ma50:
            trend = "UPTREND"
            strength = 0.75
        elif current_price < ma20 < ma50 < ma200:
            trend = "STRONG DOWNTREND"
            strength = -0.95
        elif current_price < ma20 < ma50:
            trend = "DOWNTREND"
            strength = -0.75
        else:
            trend = "SIDEWAYS"
            strength = 0
            
        return {'trend': trend, 'strength': strength}
    
    def run_full_analysis(self):
        """Run complete technical analysis"""
        self.calculate_moving_averages()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_atr()
        
        self.analysis_results = {
            'trend': self.identify_trend(),
            'support_resistance': self.detect_support_resistance(),
            'latest_indicators': {
                'RSI': float(self.data['RSI'].iloc[-1]) if not pd.isna(self.data['RSI'].iloc[-1]) else 0,
                'MACD': float(self.data['MACD'].iloc[-1]) if not pd.isna(self.data['MACD'].iloc[-1]) else 0,
                'MACD_Signal': float(self.data['MACD_Signal'].iloc[-1]) if not pd.isna(self.data['MACD_Signal'].iloc[-1]) else 0,
                'ATR': float(self.data['ATR'].iloc[-1]) if not pd.isna(self.data['ATR'].iloc[-1]) else 0,
                'Current_Price': float(self.data['Close'].iloc[-1])
            }
        }
        
        return self.analysis_results
    
    def get_analysis_data(self):
        """Return analyzed data"""
        return self.data
