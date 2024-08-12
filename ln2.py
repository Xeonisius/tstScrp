import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

url = 'https://techcrunch.com/'

driver.get(url)

try:
    accept_cookies_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "I agree")]')
    accept_cookies_button.click()
    print("Cookies accepted.")
except Exception as e:
    print("No cookie consent button found or error:", e)

data = []

for _ in range(3):  
    time.sleep(2)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    articles = soup.find_all('div', class_='post-block')
    
    for article in articles:
        title = article.find('h2', class_='has-link-color wp-block-post-title has-h-5-font-size wp-elements-565fa7bab0152bfdca0217543865c205').text.strip()
        summary = article.find('p', class_='post-wp-block-post-excerpt__excerpt').text.strip()
        link = article.find('a', class_='data-destinationlink')['href']
        data.append([title, summary, link])
    
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.post-picker-group-pagination__next')
        driver.execute_script("arguments[0].click();", next_button)
    except Exception as e:
        print("No more pages or error:", e)
        break

driver.quit()

df = pd.DataFrame(data, columns=['Title', 'Summary', 'URL'])

print(df)

df.to_csv('techcrunch_articles.csv', index=False)
