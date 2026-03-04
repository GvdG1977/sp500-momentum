# S&P 500 Stock Momentum Ranking

A web page that ranks all S&P 500 stocks based on 12-1 month price momentum using yfinance data.

## Features

- Displays ranked list of S&P 500 stocks by momentum
- Momentum calculated as (price 1 month ago - price 12 months ago) / price 12 months ago * 100
- Real-time data fetched using yfinance
- Responsive web design

## Files

- `index.html`: Main HTML page
- `styles.css`: CSS styles
- `script.js`: JavaScript for loading and displaying data
- `fetch_data.py`: Python script to fetch and calculate momentum data using yfinance
- `data.json`: Generated data file (run fetch_data.py to create/update)

## Usage

1. Ensure Python 3 and yfinance are installed: `pip install yfinance requests pandas`
2. Run `python3 fetch_data.py` to generate/update `data.json` with current stock data
3. Open `index.html` in a web browser
4. For live updates, rerun `fetch_data.py` periodically

## Requirements

- Python 3
- yfinance library
- Web browser

## Notes

- Data fetching for 500 stocks may take several minutes
- Some stocks may fail if delisted or data unavailable
- Parallel processing is used to speed up data fetching
