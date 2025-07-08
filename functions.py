from selenium import webdriver
from selenium.webdriver.common.by import By

def table_book(driver):
    table = driver.find_element(By.TAG_NAME, 'table')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    upc = rows[0].find_element(By.TAG_NAME, 'td').text
    priceExcludingTax = rows[2].find_element(By.TAG_NAME, 'td').text
    priceIncludingTax = rows[3].find_element(By.TAG_NAME, 'td').text
    tax = rows[4].find_element(By.TAG_NAME, 'td').text
    availability = rows[5].find_element(By.TAG_NAME, 'td').text
    numOfReviews = rows[6].find_element(By.TAG_NAME, 'td').text

    return upc, priceExcludingTax, priceIncludingTax, tax, availability, numOfReviews


def rate_treatment(driver):
    star_element = driver.find_element(By.CSS_SELECTOR, "[class*='star-rating']")
    classes = star_element.get_attribute("class")
    class_list = classes.split()
    rate = class_list[1]
    return rate


def info_books(driver):
    name = driver.find_element(By.CSS_SELECTOR, 'article.product_page h1').text
    price = driver.find_element(By.CLASS_NAME, 'price_color').text
    return name, price
