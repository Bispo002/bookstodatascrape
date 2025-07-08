from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from functions import table_book, rate_treatment, info_books


start = time.time()


driver = webdriver.Chrome()

books_url = []
all_books = []
for page in range(1, 50):
    driver.get(f'http://books.toscrape.com/catalogue/page-{page}.html')

    books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')

    for book in books:
        url = book.get_attribute('href')
        books_url.append(url)
        driver.get(url)
        upc, priceExcludingTax, priceIncludingTax, tax, availability, numOfReviews = table_book(driver)
        rate = rate_treatment(driver)
        name, price = info_books(driver)

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
df.to_csv("books.csv", index=False)
end = time.time()
print(f"Tempo de execução: {end - start:.2f} segundos")
