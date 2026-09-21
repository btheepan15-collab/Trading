# Trading AI - Chart Analysis & P&L Prediction Tool

A powerful AI-driven trading analysis tool that analyzes price charts and generates profit/loss scenarios for informed trading decisions.

## Features

✅ **Technical Analysis**
- Moving Averages (20, 50, 200 period)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Average True Range (ATR)
- Support & Resistance Detection

✅ **AI-Powered Predictions**
- Multiple trading scenarios (Long, Short, No Trade)
- Profit/Loss probability calculations
- Expected value computation
- Risk/Reward ratio analysis
- Win probability estimation

✅ **Data Sources**
- Yahoo Finance (live market data)
- CSV file import
- Sample data generation

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python -c "import pandas, numpy, yfinance; print('All packages installed successfully!')"
```

## Quick Start

### Method 1: Analyze Live Stock Data

```bash
cd src
python trading_ai.py AAPL
```

Replace `AAPL` with any stock symbol or `BTC-USD` for cryptocurrency.

### Method 2: Analyze with CSV File

Create a CSV file with columns: `Open`, `High`, `Low`, `Close`, `Volume`

```bash
cd src
python trading_ai.py ../data/your_data.csv
```

### Method 3: Generate Sample Data & Analyze

```bash
cd src
python generate_sample_data.py
python trading_ai.py ../data/sample_uptrend.csv
```

## Configuration

Edit `config.json` to customize:

```json
{
  "position_size": 1.0,              // Units per trade
  "risk_reward_ratio": 2.0,          // Target RR ratio
  "confidence_threshold": 0.55,      // Minimum confidence
  "analysis_parameters": {
    "ma_periods": [20, 50, 200],     // Moving average periods
    "rsi_period": 14,                // RSI period
    "macd_fast": 12,                 // MACD fast EMA
    "macd_slow": 26,                 // MACD slow EMA
    "bollinger_period": 20,          // Bollinger Band period
    "atr_period": 14                 // ATR period
  }
}
```

## Output Interpretation

### Trend Analysis
- **STRONG UPTREND**: Price > MA20 > MA50 > MA200
- **UPTREND**: Price > MA20 > MA50
- **STRONG DOWNTREND**: Price < MA20 < MA50 < MA200
- **DOWNTREND**: Price < MA20 < MA50
- **SIDEWAYS**: No clear trend

### Indicators
- **RSI (0-100)**
  - < 30: Oversold (potential BUY)
  - 30-70: Neutral
  - > 70: Overbought (potential SELL)

- **MACD**: Trend strength and direction
  - Positive & Rising: Strong uptrend
  - Negative & Falling: Strong downtrend
  - Crossovers: Potential reversals

- **ATR**: Volatility measure
  - Higher = More volatile
  - Lower = Less volatile

### Trading Scenarios

Each scenario includes:
- **Entry Price**: Current market price
- **Stop Loss**: Loss exit point
- **Target Price**: Profit exit point
- **Risk**: Maximum loss if stop is hit
- **Reward**: Maximum profit if target is hit
- **Win Probability**: % chance of success (based on trend)
- **Expected Value**: Average profit/loss per trade

### Best Recommendation

The AI ranks all scenarios by Expected Value:
```
Expected Value = (Win% × Reward) - (Loss% × Risk)
```

Positive EV = Profitable over time
Negative EV = Avoid this trade

## Examples

### Example 1: Analyze Bitcoin

```bash
python trading_ai.py BTC-USD
```

Output includes:
- Current trend and strength
- Support/Resistance levels
- Technical indicators (RSI, MACD, ATR)
- 3 trading scenarios ranked by profitability
- Best recommended trade

### Example 2: Batch Analysis

Create `batch_analysis.py`:

```python
from trading_ai import TradingAI

ai = TradingAI()
symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']

for symbol in symbols:
    print(f"\n{'='*60}")
    print(f"Analyzing {symbol}")
    print('='*60)
    ai.run(symbol=symbol)
```

Run: `python batch_analysis.py`

### Example 3: Custom CSV Data

Prepare CSV with OHLCV data:

```
Date,Open,High,Low,Close,Volume
2024-01-01,100,105,99,104,1000000
2024-01-02,104,107,103,106,1200000
```

Run: `python trading_ai.py your_data.csv`

## API Usage

Use Trading AI in your own scripts:

```python
from trading_ai import TradingAI
from chart_analyzer import ChartAnalyzer
from pnl_predictor import PnLPredictor
import pandas as pd

# Initialize
ai = TradingAI('config.json')

# Get market data
data = ai.download_data('AAPL', period='3mo')

# Analyze chart
analysis = ai.analyze_chart(data)

# Get P&L predictions
current_price = analysis['latest_indicators']['Current_Price']
atr = analysis['latest_indicators']['ATR']

pnl_results = ai.predict_pnl(analysis, current_price, atr)

# Access best scenario
best_trade = pnl_results['best_scenario']
print(f"Entry: ${best_trade['entry_price']:.2f}")
print(f"Target: ${best_trade['target_price']:.2f}")
print(f"Expected Value: ${best_trade['expected_value']:.2f}")
```

## Data Files

### Input
- **CSV Format**: Open, High, Low, Close, Volume, Date
- **Live Data**: Yahoo Finance symbols (AAPL, BTC-USD, etc.)

### Output
- **JSON Report**: `trading_analysis_YYYYMMDD_HHMMSS.json`
  - Complete technical analysis
  - All scenarios with probabilities
  - Expected values and rankings

## Risk Disclaimer

⚠️ **IMPORTANT**
- This tool is for educational purposes only
- Not financial advice
- Past performance ≠ future results
- Always use stop losses in live trading
- Start with paper trading/backtesting
- Risk only what you can afford to lose
- Combine AI with your own analysis

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'yfinance'"
**Solution**: `pip install -r requirements.txt`

### Issue: "No data downloaded"
**Solution**: Check internet connection and symbol validity

### Issue: "CSV parsing error"
**Solution**: Ensure CSV has columns: Date, Open, High, Low, Close, Volume

### Issue: "ATR is NaN"
**Solution**: Need at least 14 candles of data for ATR calculation

## Performance Tips

1. **Use daily data** for swing trading analysis
2. **Use hourly data** for day trading
3. **Minimum 30 candles** for accurate indicators
4. **100+ candles** for best analysis quality
5. **Combine with manual analysis** for live trading

## File Structure

```
trading_ai/
├── src/
│   ├── trading_ai.py          # Main script
│   ├── chart_analyzer.py      # Technical analysis
│   ├── pnl_predictor.py       # P&L calculations
│   ├── generate_sample_data.py # Test data generator
│   └── __init__.py
├── data/                       # Data files
├── output/                     # Analysis results
├── config.json                 # Configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Advanced Features

### Custom Indicators
Edit `chart_analyzer.py` to add:
- Stochastic Oscillator
- CCI (Commodity Channel Index)
- Volume Profile
- Volume Weighted Average Price (VWAP)

### Machine Learning
Extend `pnl_predictor.py` with:
- Neural networks for prediction
- Random forest models
- Time series forecasting

### Real-time Monitoring
Add WebSocket support for:
- Live price updates
- Real-time alerts
- Automated trading signals

## Support & Updates

For issues or feature requests:
1. Check the troubleshooting section
2. Review your input data format
3. Verify all dependencies are installed

## License

Educational use only. See LICENSE file for details.

## Next Steps

1. ✅ Install requirements
2. ✅ Run sample analysis
3. ✅ Adjust configuration
4. ✅ Analyze your data
5. ✅ Backtest results
6. ✅ Paper trade
7. ✅ Live trade (with caution)

Happy trading! 📈
