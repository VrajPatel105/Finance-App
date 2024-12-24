import finnhub
''' import yfinance as yf

# Define the ticker symbol
ticker_symbol = "NVDA"

# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

# Fetch historical market data
historical_data = ticker.history(period="1d")  # data for the last year
print("Historical Data:")
print(historical_data)

# Fetch basic financials
financials = ticker.financials
print("\nFinancials:")
print(financials)

# Fetch stock actions like dividends and splits
actions = ticker.actions
print("\nStock Actions:")
print(actions) '''

'''from alpha_vantage.timeseries import TimeSeries
import time

# Initialize TimeSeries with your API key
ts = TimeSeries(key='NU3411A9YTCCUYS6')

# 1. Get Intraday Data (1min intervals)
def get_intraday_data(symbol):
    try:
        data, meta = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
        
        print(f"\nIntraday Data for {symbol}:")
        for timestamp, values in list(data.items())[:5]:  # Show last 5 entries
            print(f"Time: {timestamp}")
            print(f"Open: ${values['1. open']}")
            print(f"High: ${values['2. high']}")
            print(f"Low: ${values['3. low']}")
            print(f"Close: ${values['4. close']}")
            print(f"Volume: {values['5. volume']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"Error: {e}")

# 2. Continuous monitoring
def monitor_stock(symbol, interval=60):
    print(f"Starting monitoring for {symbol}")
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            data, meta = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
            latest = list(data.items())[0]  # Get most recent data point
            
            print(f"\nTime: {latest[0]}")
            print(f"Current Price: ${latest[1]['4. close']}")
            print(f"Volume: {latest[1]['5. volume']}")
            print("-" * 40)
            
            time.sleep(interval)  # Wait before next update (be mindful of API limits)
            
        except KeyboardInterrupt:
            print("\nStopping monitoring...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait if there's an error

# Usage examples:
# 1. Get one-time intraday data
get_intraday_data('AAPL')

# 2. Monitor continuously (uncomment to use)
# monitor_stock('AAPL', interval=60)  # Updates every 60 seconds'''



