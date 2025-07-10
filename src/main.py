from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from src.functions import table_book, rate_treatment, info_books
from src.model import model_training
import pandas as pd
import time
import logging

# Constants
MAX_RETRIES = 3
WAIT_SECONDS = 2

# Data containers
books_url = []
all_books = []


def start_webdriver() -> webdriver.Chrome:
    """
    Attempts to start the WebDriver up to MAX_RETRIES times.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info('Starting WebDriver...')
            driver = webdriver.Chrome()
            return driver
        except WebDriverException as e:
            logging.warning(f'WebDriver failed to start (attempt {attempt}): {e}')
            if attempt == MAX_RETRIES:
                logging.error('Max retries reached. Raising exception.')
                raise
            time.sleep(WAIT_SECONDS)


def open_url_with_retries(driver):
    """
    Iterates through 50 pages and collects book URLs, retrying if needed.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            for page in range(1, 50):

                logging.info(f'Accessing page {page} on Google Chrome, URL: http://books.toscrape.com/catalogue/page-{page}.html')
                driver.get(f'http://books.toscrape.com/catalogue/page-{page}.html')

                books = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod h3 a')

                for book in books:
                    logging.info(f'Getting URL of book: {book.text}.')
                    url = book.get_attribute('href')

                    logging.info('Inserting info into list of books URLs.')
                    books_url.append(url)

            logging.info(f"Collected {len(books_url)} book URLs.")
            return
        except WebDriverException as e:
            logging.warning(f'Failed to open book list pages (attempt {attempt}): {e}')
            if attempt == MAX_RETRIES:
                logging.error('Could not open URLs after max retries. Raising exception.')
                raise
            time.sleep(WAIT_SECONDS)


def get_book_info(driver):
    """
    Visits each book URL and collects the book information.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            for url in books_url:
                driver.get(url)

                logging.info(f'Collecting info about name and price in URL:{url}.')
                name, price = info_books(driver)

                logging.info('Collecting info about rating.')
                rate = rate_treatment(driver)

                logging.info('Collecting info about books: UPC, Price Excluding Tax, Price Including Tax, Tax, Availability, Number of Reviews.')
                upc, price_excl_tax, price_incl_tax, tax, availability, num_reviews = table_book(driver)

                logging.info('Creating dictionary "book_data".')
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

                logging.info('Inserting infos into "all_books" list')
                all_books.append(book_data)
            return
        except WebDriverException as e:
            logging.warning(f'Failed to get book info (attempt {attempt}): {e}')
            if attempt == MAX_RETRIES:
                logging.error('Could not get book info after max retries. Raising exception.')
                raise
            time.sleep(WAIT_SECONDS)


if __name__ == '__main__':
    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        filename='../outputs/log.txt',
        filemode='w'
    )

    start = time.time()

    try:
        driver = start_webdriver()
        open_url_with_retries(driver)
        get_book_info(driver)

        # Export to CSV
        df = pd.DataFrame(all_books)
        df.to_csv("../outputs/books.csv", index=False)
        model_training()


    finally:
        driver.quit()

    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
