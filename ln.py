import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.bbc.com/news' 
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')   
    titles = soup.find_all('h2', class_='sc-4fedabc7-3 zTZri')
    for title in titles:
        print(title.text.strip())
    title_list = [title.text.strip() for title in titles]

df = pd.DataFrame(title_list, columns=['Article Title'])
print(df)
