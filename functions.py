from selenium import webdriver
from selenium.webdriver.common.by import By


def table_book(driver: webdriver) -> tuple:
    """
    Reads the table of details on the book's page using the HTML TAG_NAME to locate each value,
    and returns all values individually.

    :param driver: Selenium WebDriver instance used to access the browser.
    :return: Tuple containing the following strings:
             upc, price_excluding_tax, price_including_tax, tax, availability, number_of_reviews.
    """

    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    upc = rows[0].find_element(By.TAG_NAME, 'td').text
    price_excluding_tax = rows[2].find_element(By.TAG_NAME, 'td').text
    price_including_tax = rows[3].find_element(By.TAG_NAME, 'td').text
    tax = rows[4].find_element(By.TAG_NAME, 'td').text
    availability = rows[5].find_element(By.TAG_NAME, 'td').text
    number_of_reviews = rows[6].find_element(By.TAG_NAME, 'td').text

    return upc, price_excluding_tax, price_including_tax, tax, availability, number_of_reviews


def rate_treatment(driver: webdriver) -> str:
    """
    Retrieves the book's star rating by finding the CSS class that contains 'star-rating'
    and extracting the rating from the class list.

    :param driver: Selenium WebDriver instance used to access the browser.
    :return: String representing the star rating (e.g., 'One', 'Two', 'Three', etc.).
    """
    star_element = driver.find_element(By.CSS_SELECTOR, "[class*='star-rating']")
    classes = star_element.get_attribute("class")
    class_list = classes.split()
    rate = class_list[1]
    return rate


def info_books(driver: webdriver) -> tuple:
    """
    Retrieves the book name and price using CSS selectors.

    :param driver: Selenium WebDriver instance used to access the browser.
    :return: Tuple containing:
             - name (str): The book's title.
             - price (str): The book's price.
    """
    name = driver.find_element(By.CSS_SELECTOR, 'article.product_page h1').text
    price = driver.find_element(By.CLASS_NAME, 'price_color').text
    return name, price
