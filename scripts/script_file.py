import requests
from bs4 import BeautifulSoup

url="https://www.dailyscript.com/scripts/pulp_fiction.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text()

with open("pulp_fiction.txt", "w", encoding="utf-8") as f:
    f.write(text)