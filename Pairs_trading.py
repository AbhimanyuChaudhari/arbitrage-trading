from config import ALPACA_CONFIG
from datetime import datetime
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import numpy as np
import pandas as pd  # Import pandas library
import statsmodels.api as sm
from scipy import stats
from lumibot.backtesting import YahooDataBacktesting

class PairsTradingStrategy(Strategy):
    def initialize(self, parameters=None):
        super().initialize(parameters)
        self.df = pd.DataFrame(columns=['Symbol', 'Price'])  # Create DataFrame with columns 'Symbol' and 'Price'
        self.window = 15
        self.z_score_threshold = 1.0
        self.entered_position = False
        self.stop_loss_threshold = 0.003
        self.take_profit_threshold = 0.05
        self.stop_loss_price = 0 
        self.take_profit_price = 0

    def on_trading_iteration(self):
        super().on_trading_iteration()
        pair = ['AAPL', 'MSFT']
        last_prices = self.get_last_prices(pair)
        for symbol, price in last_prices.items():
            self.df.loc[len(self.df)] = [symbol, price]  # Add new row to DataFrame
            
        apple_price = np.array(self.df[self.df['Symbol'] == 'AAPL']['Price'][-self.window:])
        msft_price = np.array(self.df[self.df['Symbol'] == 'MSFT']['Price'][-self.window:])
        
        if len(apple_price) < self.window or len(np.unique(apple_price)) == 1:
            return
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(apple_price, msft_price)
        expected_spread = slope * apple_price + intercept
        actual_spread = msft_price - apple_price
        z_score = (actual_spread[-1] - expected_spread[-1]) / np.std(actual_spread)
        
        if not self.entered_position:
            if z_score > self.z_score_threshold:
                order1 = self.create_order(pair[0], quantity=10, side='buy')
                order2 = self.create_order(pair[1], quantity=10, side='sell')
                self.submit_order(order1)
                self.submit_order(order2)
                self.entered_position = True
                self.log_message(f"Taking long position of {pair[0]} and going short on {pair[1]}")
                self.stop_loss_price = actual_spread[-1] * (1 - self.stop_loss_threshold)
                self.take_profit_price = actual_spread[-1] * (1 + self.stop_loss_threshold)
                self.log_message(f"Taking long position of {pair[0]} and going short on {pair[1]}")
            elif z_score < -self.z_score_threshold:
                order1 = self.create_order(pair[0], quantity=10, side='sell')
                order2 = self.create_order(pair[1], quantity=10, side='buy')
                self.submit_order(order1)
                self.submit_order(order2)
                self.entered_position = True
                self.stop_loss_price = actual_spread[-1] * (1 + self.stop_loss_threshold)
                self.take_profit_price = actual_spread[-1] * (1 - self.stop_loss_threshold)
                self.log_message(f"Taking long position of {pair[1]} and going short on {pair[0]}")
        else:
            if -self.z_score_threshold < z_score < self.z_score_threshold or actual_spread[-1] <= self.stop_loss_price or actual_spread[-1] >= self.take_profit_price:
                # Close the position when the spread returns to normal
                order1 = self.create_order(pair[0], quantity=10 if z_score > 0 else 1, side='sell' if z_score > 0 else 'buy')
                order2 = self.create_order(pair[1], quantity=10 if z_score < 0 else 1, side='sell' if z_score < 0 else 'buy')
                self.submit_order(order1)
                self.submit_order(order2)
                self.entered_position = False
                if z_score < -self.z_score_threshold:
                    self.log_message('Exiting position due to low z-score')
                elif actual_spread[-1] <= self.stop_loss_price:
                    self.log_message('Exiting position due to stop loss hit')
                elif actual_spread[-1] >= self.take_profit_price:
                    self.log_message('Exiting position due to take profit hit  ')
                self.log_message("Closing position")

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = PairsTradingStrategy(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()
    else:
        start = datetime(2023, 1, 1)
        end = datetime(2023, 1, 31)
        PairsTradingStrategy.backtest(
            YahooDataBacktesting,
            start,
            end
        )
