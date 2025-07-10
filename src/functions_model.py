import pandas as pd
import re


def rate_to_num(rating: pd.DataFrame):
    """
    Transform rating words (One, Two, Three, Four, Five) in dictionary of numbers (One: 1, Two: 2 etc...)

    :param rating: Dataframe['Rating']
    :return: dictionary: rating_map
    """
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    return rating_map.get(rating, 0)


def price_treatment(price: pd.DataFrame):
    """
    Remove special characters of price, and transforms in float.

    :param price: pd.Dataframe['Price']
    :return: price_clean: float
    """
    if pd.isna(price):
        return
    price_clean = re.sub(r'[^\d.]', '', str(price))
    if price_clean in ('', '.'):
        return 0.0
    return float(price_clean)
