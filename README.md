# arbitrage-trading
This repository contains the code for a pairs trading strategy using Lumibot. The strategy is designed to trade two highly correlated stocks, Apple (AAPL) and Microsoft (MSFT), by exploiting statistical arbitrage opportunities.

Table of Contents
Introduction
Installation
Usage
Configuration
Strategy Explanation
Backtesting
Running the Strategy
License
Introduction
Pairs trading is a market-neutral trading strategy that involves taking long and short positions in two correlated securities. The strategy aims to profit from the relative price movements between the two securities.

This code uses the Lumibot framework to implement and backtest a pairs trading strategy. The strategy trades AAPL and MSFT based on the Z-score of the spread between their prices.

Installation
To run this strategy, you need to have Python installed along with the necessary libraries. You can install the required libraries using the following command:

bash
Copy code
pip install lumibot pandas numpy statsmodels scipy yfinance
Usage
You can use this code for both live trading and backtesting. For live trading, you need to have an Alpaca account and configure the ALPACA_CONFIG with your API keys.

Configuration
The ALPACA_CONFIG file should contain your Alpaca API credentials in the following format:

python
Copy code
ALPACA_CONFIG = {
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret',
    'BASE_URL': 'https://paper-api.alpaca.markets'
}
Strategy Explanation
The strategy operates as follows:

Initialization: Set up the strategy parameters, including the look-back window for price data and Z-score thresholds for entering and exiting trades.
Data Collection: Retrieve the latest prices for AAPL and MSFT.
Signal Generation:
Calculate the spread between the two stocks.
Perform a linear regression to determine the expected spread.
Compute the Z-score of the actual spread.
Trade Execution: Based on the Z-score:
Enter a long-short position if the Z-score exceeds a threshold.
Exit the position if the Z-score returns to normal or hit stop-loss/take-profit levels.
Key Parameters:
window: Look-back period for calculating the Z-score (default: 15).
z_score_threshold: Z-score threshold for entering trades (default: 1.0).
stop_loss_threshold: Stop-loss percentage (default: 0.003).
take_profit_threshold: Take-profit percentage (default: 0.05).
Backtesting
To backtest the strategy, you can use historical data from Yahoo Finance. Modify the start and end dates as required:

python
Copy code
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
Running the Strategy
To run the strategy for live trading, set the trade variable to True and ensure your Alpaca API keys are configured:

python
Copy code
if __name__ == "__main__":
    trade = True
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
License
This project is licensed under the MIT License. See the LICENSE file for details.
