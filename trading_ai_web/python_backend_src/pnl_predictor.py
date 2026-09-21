import numpy as np
from typing import Dict, List

class PnLPredictor:
    """Predicts profit/loss scenarios based on technical analysis"""
    
    def __init__(self, analysis_results: Dict, current_price: float, atr: float = None):
        """
        Initialize with analysis results and current price
        """
        self.analysis = analysis_results
        self.current_price = current_price
        self.atr = atr if atr else current_price * 0.02
        
    def generate_scenarios(self, position_size: float = 1.0, risk_reward_ratio: float = 2.0):
        """
        Generate multiple trading scenarios
        
        Args:
            position_size: Position size (default 1 unit)
            risk_reward_ratio: Risk to reward ratio (default 2:1)
        """
        
        trend = self.analysis['trend']['trend']
        support = self.analysis['support_resistance']['support_levels']
        resistance = self.analysis['support_resistance']['resistance_levels']
        
        scenarios = []
        
        # Scenario 1: Long Position (Buy)
        if len(support) > 0:
            stop_loss = support[-1] if support else self.current_price - self.atr
        else:
            stop_loss = self.current_price - self.atr
            
        if len(resistance) > 0:
            target_price = resistance[0] if resistance else self.current_price + (self.atr * risk_reward_ratio)
        else:
            target_price = self.current_price + (self.atr * risk_reward_ratio)
        
        long_scenario = {
            'type': 'LONG',
            'entry_price': self.current_price,
            'stop_loss': stop_loss,
            'target_price': target_price,
            'risk_per_trade': abs(self.current_price - stop_loss) * position_size,
            'reward_per_trade': abs(target_price - self.current_price) * position_size,
            'risk_reward': abs(target_price - self.current_price) / abs(self.current_price - stop_loss) if stop_loss != self.current_price else 0,
            'position_size': position_size,
            'probability': self._calculate_win_probability('long', trend),
            'expected_value': self._calculate_expected_value('long', trend, stop_loss, target_price, position_size)
        }
        scenarios.append(long_scenario)
        
        # Scenario 2: Short Position (Sell)
        if len(resistance) > 0:
            short_stop_loss = resistance[0] if resistance else self.current_price + self.atr
        else:
            short_stop_loss = self.current_price + self.atr
            
        if len(support) > 0:
            short_target = support[-1] if support else self.current_price - (self.atr * risk_reward_ratio)
        else:
            short_target = self.current_price - (self.atr * risk_reward_ratio)
        
        short_scenario = {
            'type': 'SHORT',
            'entry_price': self.current_price,
            'stop_loss': short_stop_loss,
            'target_price': short_target,
            'risk_per_trade': abs(short_stop_loss - self.current_price) * position_size,
            'reward_per_trade': abs(self.current_price - short_target) * position_size,
            'risk_reward': abs(self.current_price - short_target) / abs(short_stop_loss - self.current_price) if short_stop_loss != self.current_price else 0,
            'position_size': position_size,
            'probability': self._calculate_win_probability('short', trend),
            'expected_value': self._calculate_expected_value('short', trend, short_stop_loss, short_target, position_size)
        }
        scenarios.append(short_scenario)
        
        # Scenario 3: No Trade (Wait)
        no_trade_scenario = {
            'type': 'NO_TRADE',
            'entry_price': self.current_price,
            'stop_loss': None,
            'target_price': None,
            'risk_per_trade': 0,
            'reward_per_trade': 0,
            'risk_reward': 0,
            'position_size': 0,
            'probability': 1.0,
            'expected_value': 0,
            'reason': 'Wait for better setup'
        }
        scenarios.append(no_trade_scenario)
        
        return scenarios
    
    def _calculate_win_probability(self, trade_type: str, trend: str) -> float:
        """Estimate win probability based on trend"""
        base_probability = 0.5
        
        if trade_type == 'long':
            if 'UPTREND' in trend:
                base_probability = 0.65 if 'STRONG' in trend else 0.58
            elif 'DOWNTREND' in trend:
                base_probability = 0.35 if 'STRONG' in trend else 0.42
        else:  # short
            if 'DOWNTREND' in trend:
                base_probability = 0.65 if 'STRONG' in trend else 0.58
            elif 'UPTREND' in trend:
                base_probability = 0.35 if 'STRONG' in trend else 0.42
        
        return base_probability
    
    def _calculate_expected_value(self, trade_type: str, trend: str, stop_loss: float, target: float, position_size: float) -> float:
        """Calculate expected value of the trade"""
        win_prob = self._calculate_win_probability(trade_type, trend)
        loss_prob = 1 - win_prob
        
        if trade_type == 'long':
            win_amount = (target - self.current_price) * position_size
            loss_amount = (self.current_price - stop_loss) * position_size
        else:  # short
            win_amount = (self.current_price - target) * position_size
            loss_amount = (stop_loss - self.current_price) * position_size
        
        expected_value = (win_prob * win_amount) - (loss_prob * loss_amount)
        return expected_value
    
    def rank_scenarios(self, scenarios: List[Dict]) -> List[Dict]:
        """Rank scenarios by expected value"""
        ranked = sorted(scenarios, key=lambda x: x['expected_value'], reverse=True)
        for i, scenario in enumerate(ranked):
            scenario['rank'] = i + 1
        return ranked
    
    def get_best_scenario(self, scenarios: List[Dict]) -> Dict:
        """Get the best scenario"""
        ranked = self.rank_scenarios(scenarios)
        return ranked[0]
