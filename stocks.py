from bs4 import BeautifulSoup
import requests

def scrape_stock_data(symbol, exchange):
    if exchange == "NSE":
        symbol += '.NS'
    url = f"https://finance.yahoo.com/quote/{symbol}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    current_price = soup.find('span', {'data-testid': 'qsp-price'}).get_text()

    price_changed = soup.find('span', {'data-testid': 'qsp-price-change'}).get_text()

    percentage_change = soup.find('span', {'data-testid': 'qsp-price-change-percent'}).get_text()

    label_span = soup.find('span', string='Previous Close')
    price_span = label_span.find_next_sibling('span', class_='value yf-gn3zu3')
    previous_close = price_span.find('fin-streamer').get_text(strip=True)

    label_span = soup.find('span', string='52 Week Range')
    price_span = label_span.find_next_sibling('span', class_='value yf-gn3zu3')
    week_52_high = price_span.find('fin-streamer').get_text(strip=True).split(" - ")[1]
    week_52_low = price_span.find('fin-streamer').get_text(strip=True).split(" - ")[0]

    label_span = soup.find('span', string='Market Cap (intraday)')
    price_span = label_span.find_next_sibling('span', class_='value yf-gn3zu3')
    market_cap = price_span.find('fin-streamer').get_text(strip=True)

    label_span = soup.find('span', string='PE Ratio (TTM)')
    price_span = label_span.find_next_sibling('span', class_='value yf-gn3zu3')
    pe_ratio = price_span.find('fin-streamer').get_text(strip=True)

    label_span = soup.find('span', string='Forward Dividend & Yield')
    dividend_yield = label_span.find_next_sibling('span', class_='value yf-gn3zu3').get_text(strip=True)
    # dividend_yield = price_span.find('fin-streamer').get_text(strip=True)

    stock_response = {
        'current_price': current_price,
        'price_changed': price_changed,
        'percentage_change': percentage_change,
        'previous_close': previous_close,
        'week_52_high': week_52_high,
        'week_52_low': week_52_low,
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
        'dividend_yield': dividend_yield,
    }

    print(stock_response)

scrape_stock_data("AAPL", "NasdaqGS")