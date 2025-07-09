from selenium import webdriver                                 # Selenium WebDriver
from selenium.webdriver.common.by import By                    # 'By' used to locate elements (tags, CSS selectors, classes, etc.)
from functions import table_book, rate_treatment, info_books   # Functions defined in functions.py
import pandas as pd                                            # Used to create DataFrame and export to CSV
import time                                                    # Used to measure execution time
import logging                                                 # Used for logging and tracking execution flow

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log.txt',
    filemode='w'
)

# Lists to store book URLs and book data
books_url = []
all_books = []

# Start WebDriver
driver = webdriver.Chrome()

# Start timing
start = time.time()

# Iterate through pages 1 to 50
for page in range(1, 50):
    driver.get(f'http://books.toscrape.com/catalogue/page-{page}.html')

    # Get all book links on the current page
    books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')

    for book in books:
        url = book.get_attribute('href')
        books_url.append(url)

# Visit each book URL to collect data
for url in books_url:
    driver.get(url)

    # Extract data using functions from functions.py
    upc, price_excl_tax, price_incl_tax, tax, availability, num_reviews = table_book(driver)
    rate = rate_treatment(driver)
    name, price = info_books(driver)

    # Store book data in a dictionary
    book_data = {
        'Name': name,
        'Price': price,
        'Rate': rate,
        'UPC': upc,
        'Price Excluding Tax': price_excl_tax,
        'Price Including Tax': price_incl_tax,
        'Tax Value': tax,
        'Availability': availability,
        'Number of Reviews': num_reviews
    }

    all_books.append(book_data)

# Convert list of books to a DataFrame and export to CSV
df = pd.DataFrame(all_books)
df.to_csv("books.csv", index=False)

# End timing and display duration
end = time.time()
print(f"Execution time: {end - start:.2f} seconds")
