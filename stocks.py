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

    label_span = soup.find('span', string='Previous Close')
    price_span = label_span.find_next_sibling('span', class_='value yf-gn3zu3')
    previous_price = price_span.find('fin-streamer').get_text(strip=True)
    print(current_price)
    print(previous_price)


scrape_stock_data("AAPL", "NasdaqGS")