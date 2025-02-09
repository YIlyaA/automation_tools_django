from bs4 import BeautifulSoup
import requests

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
table = soup.find(class_="wikitable")
tbody = table.find("tbody")
rows = tbody.find_all("tr")[1:]
print(rows)

mutable = []
immutable = []

for row in rows:
    type = row.find_all('td')
    if type[1].get_text() == 'mutable\n':
        mutable.append(type[0].get_text().strip())
    else:
        immutable.append(type[0].get_text().strip())

print(mutable)
print(immutable)