import yfinance as yf
import pandas as pd
import json
import requests
import concurrent.futures
import math

# Fetch S&P 500 tickers
def get_sp500_tickers():
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
    response = requests.get(url)
    lines = response.text.split('\n')
    tickers = {}
    for line in lines[1:]:
        if line.strip():
            parts = line.split(',')
            symbol = parts[0].strip('"')
            name = parts[1].strip('"')
            tickers[symbol] = name
    return tickers

def calculate_momentum(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1y')
        if len(data) < 250:
            return None
        price_12m_ago = data.iloc[0]['Close']
        price_1m_ago = data.iloc[-30]['Close']  # Approx 1 month ago
        current_price = data.iloc[-1]['Close']
        if math.isnan(price_12m_ago) or math.isnan(price_1m_ago) or math.isnan(current_price):
            return None
        momentum = ((price_1m_ago - price_12m_ago) / price_12m_ago) * 100
        return {
            'symbol': symbol,
            'momentum': momentum,
            'currentPrice': current_price
        }
    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return None

def main():
    tickers = get_sp500_tickers()
    # Process all S&P 500 stocks
    limited_tickers = list(tickers.items())
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(calculate_momentum, symbol): (symbol, name) for symbol, name in limited_tickers}
        for future in concurrent.futures.as_completed(futures):
            symbol, name = futures[future]
            data = future.result()
            if data:
                data['name'] = name
                results.append(data)
    results.sort(key=lambda x: x['momentum'], reverse=True)
    with open('data.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Data saved to data.json")

if __name__ == '__main__':
    main()
