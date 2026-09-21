#!/usr/bin/env python3

import pandas as pd
import json
import sys
from pathlib import Path
from chart_analyzer import ChartAnalyzer
from pnl_predictor import PnLPredictor
import yfinance as yf
from datetime import datetime, timedelta

class TradingAI:
    """Main Trading AI orchestrator"""
    
    def __init__(self, config_path: str = None):
        """Initialize Trading AI with optional config"""
        self.config = self.load_config(config_path) if config_path else self.get_default_config()
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Default configuration"""
        return {
            'position_size': 1.0,
            'risk_reward_ratio': 2.0,
            'lookback_days': 100,
            'confidence_threshold': 0.55
        }
    
    def download_data(self, symbol: str, period: str = '3mo') -> pd.DataFrame:
        """Download market data from Yahoo Finance"""
        try:
            print(f"Downloading data for {symbol}...")
            data = yf.download(symbol, period=period, progress=False)
            print(f"Downloaded {len(data)} bars of data")
            return data
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None
    
    def load_csv_data(self, csv_path: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
            print(f"Loaded {len(data)} bars from {csv_path}")
            return data
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def analyze_chart(self, data: pd.DataFrame) -> dict:
        """Analyze chart using technical analysis"""
        print("\n" + "="*60)
        print("RUNNING TECHNICAL ANALYSIS")
        print("="*60)
        
        analyzer = ChartAnalyzer(data)
        analysis = analyzer.run_full_analysis()
        
        print(f"Trend: {analysis['trend']['trend']}")
        print(f"Trend Strength: {analysis['trend']['strength']}")
        print(f"RSI: {analysis['latest_indicators']['RSI']:.2f}")
        print(f"MACD: {analysis['latest_indicators']['MACD']:.4f}")
        print(f"ATR: {analysis['latest_indicators']['ATR']:.4f}")
        
        return analysis
    
    def predict_pnl(self, analysis: dict, current_price: float, atr: float) -> dict:
        """Predict profit/loss scenarios"""
        print("\n" + "="*60)
        print("GENERATING P&L SCENARIOS")
        print("="*60)
        
        predictor = PnLPredictor(
            analysis,
            current_price,
            atr
        )
        
        scenarios = predictor.generate_scenarios(
            position_size=self.config['position_size'],
            risk_reward_ratio=self.config['risk_reward_ratio']
        )
        
        ranked_scenarios = predictor.rank_scenarios(scenarios)
        
        return {
            'scenarios': ranked_scenarios,
            'best_scenario': ranked_scenarios[0]
        }
    
    def format_output(self, analysis: dict, pnl_results: dict) -> str:
        """Format results for display"""
        output = []
        output.append("\n" + "="*60)
        output.append("TRADING AI ANALYSIS REPORT")
        output.append("="*60)
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Trend Analysis
        output.append("TREND ANALYSIS:")
        output.append(f"  Trend: {analysis['trend']['trend']}")
        output.append(f"  Strength: {analysis['trend']['strength']:.2f}\n")
        
        # Support & Resistance
        output.append("SUPPORT & RESISTANCE:")
        if analysis['support_resistance']['support_levels']:
            output.append(f"  Support Levels: {[f'{x:.2f}' for x in analysis['support_resistance']['support_levels']]}")
        if analysis['support_resistance']['resistance_levels']:
            output.append(f"  Resistance Levels: {[f'{x:.2f}' for x in analysis['support_resistance']['resistance_levels']]}\n")
        
        # Indicators
        output.append("INDICATORS:")
        output.append(f"  Price: ${analysis['latest_indicators']['Current_Price']:.2f}")
        output.append(f"  RSI: {analysis['latest_indicators']['RSI']:.2f}")
        output.append(f"  MACD: {analysis['latest_indicators']['MACD']:.4f}")
        output.append(f"  ATR: {analysis['latest_indicators']['ATR']:.4f}\n")
        
        # Best Scenario
        output.append("RECOMMENDED ACTION:")
        best = pnl_results['best_scenario']
        output.append(f"  Type: {best['type']}")
        output.append(f"  Entry: ${best['entry_price']:.2f}")
        output.append(f"  Stop Loss: ${best['stop_loss']:.2f}" if best['stop_loss'] else "  Stop Loss: N/A")
        output.append(f"  Target: ${best['target_price']:.2f}" if best['target_price'] else "  Target: N/A")
        output.append(f"  Risk: ${best['risk_per_trade']:.2f}")
        output.append(f"  Reward: ${best['reward_per_trade']:.2f}")
        output.append(f"  Risk/Reward Ratio: {best['risk_reward']:.2f}" if best['risk_reward'] > 0 else "  Risk/Reward Ratio: N/A")
        output.append(f"  Win Probability: {best['probability']*100:.1f}%")
        output.append(f"  Expected Value: ${best['expected_value']:.2f}\n")
        
        # All Scenarios
        output.append("ALL SCENARIOS (Ranked by Expected Value):")
        output.append("-" * 60)
        for scenario in pnl_results['scenarios']:
            output.append(f"\n{scenario['rank']}. {scenario['type']}")
            output.append(f"   Entry: ${scenario['entry_price']:.2f}")
            if scenario['stop_loss']:
                output.append(f"   Stop Loss: ${scenario['stop_loss']:.2f}")
            if scenario['target_price']:
                output.append(f"   Target: ${scenario['target_price']:.2f}")
            output.append(f"   Expected Value: ${scenario['expected_value']:.2f}")
            output.append(f"   Win Probability: {scenario['probability']*100:.1f}%")
        
        output.append("\n" + "="*60)
        return "\n".join(output)
    
    def run(self, symbol: str = None, csv_path: str = None):
        """Run complete analysis"""
        
        # Get data
        if csv_path:
            data = self.load_csv_data(csv_path)
        elif symbol:
            data = self.download_data(symbol)
        else:
            print("Please provide either a symbol or CSV path")
            return
        
        if data is None or len(data) == 0:
            print("Failed to load data")
            return
        
        # Run analysis
        analysis = self.analyze_chart(data)
        
        # Get current price and ATR
        current_price = analysis['latest_indicators']['Current_Price']
        atr = analysis['latest_indicators']['ATR']
        
        # Predict P&L
        pnl_results = self.predict_pnl(analysis, current_price, atr)
        
        # Format and display results
        report = self.format_output(analysis, pnl_results)
        print(report)
        
        # Save results to JSON
        output_file = f"trading_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis': self._make_serializable(analysis),
            'pnl_results': self._make_serializable(pnl_results)
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        return results
    
    def _make_serializable(self, obj):
        """Convert objects to JSON serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, (float, int)):
            return obj
        else:
            return str(obj)

if __name__ == "__main__":
    ai = TradingAI()
    
    # Example: Download and analyze Apple stock
    if len(sys.argv) > 1:
        symbol_or_path = sys.argv[1]
        if symbol_or_path.endswith('.csv'):
            ai.run(csv_path=symbol_or_path)
        else:
            ai.run(symbol=symbol_or_path)
    else:
        # Default to Bitcoin if no argument
        ai.run(symbol='BTC-USD')
