from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

def table_book():
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    upc = rows[0].find_element(By.TAG_NAME, 'td').text
    priceExcludingTax = rows[2].find_element(By.TAG_NAME, 'td').text
    priceIncludingTax = rows[3].find_element(By.TAG_NAME, 'td').text
    tax = rows[4].find_element(By.TAG_NAME, 'td').text
    availability = rows[5].find_element(By.TAG_NAME, 'td').text
    numOfReviews = rows[6].find_element(By.TAG_NAME, 'td').text

    return upc, priceExcludingTax, priceIncludingTax, tax, availability, numOfReviews


def rate_treatment():
    star_element = driver.find_element(By.CSS_SELECTOR, "[class*='star-rating']")
    classes = star_element.get_attribute("class")
    class_list = classes.split()
    rate = class_list[1]
    return rate


def info_books():
    name = driver.find_element(By.CSS_SELECTOR, 'article.product_page h1').text
    price = driver.find_element(By.CLASS_NAME, 'price_color').text
    return name, price


start = time.time()


driver = webdriver.Chrome()
driver.get('http://books.toscrape.com')


all_books = []
for page in range(1,50):
    driver.get(f'http://books.toscrape.com/catalogue/page-{page}.html')

    books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')

    for book in books:
        url = book.get_attribute('href')
        driver.get(url)
        upc, priceExcludingTax, priceIncludingTax, tax, availability, numOfReviews = table_book()
        rate = rate_treatment()
        name, price = info_books()

        book_data = {
            'Name': name,
            'Price': price,
            'Rate': rate,
            'UPC': upc,
            'Price Excluding Tax': priceExcludingTax,
            'Price Including Tax': priceIncludingTax,
            'Tax value': tax,
            'Availability': availability,
            'Number of Reviews': numOfReviews
        }
        all_books.append(book_data)

        driver.back()
driver.quit()

df = pd.DataFrame(all_books)
print(df)
df.to_csv("books.csv", index=False)

end = time.time()

print(f"Tempo de execução: {end - start:.2f} segundos")