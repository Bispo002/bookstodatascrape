import pandas as pd
import re

df = pd.read_csv('../books.csv')


def rate_to_num(rating):
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    return rating_map.get(rating, 0)


def price_treatment(price):
    if pd.isna(price):
        return
    price_clean = re.sub(r'[^d\.]', '', str(price))
    if price_clean in ('', '.'):
        return 0.0
    return float(price_clean)


def availability_number(availability):
    if pd.isna(availability):
        return 0
    numbers = re.findall(r'\d+', str(availability))
    return int(numbers[0]) if numbers else 0