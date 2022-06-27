import typing as tp

import pycountry
import pandas as pd


def return_none_decorator(func: tp.Callable) -> tp.Callable:
    def wrap(arg):
        try:
            return func(arg)
        except (ValueError, AttributeError, IndexError):
            return None
    return wrap


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.isnull().values.any():
        raise ValueError("file contains empty values")

    result_df = df.copy()
    columns = ['ID', 'Release Date', 'Name', 'Country', 'Copies Sold', 'Copy Price']
    if result_df.shape[1] != len(columns):
        raise ValueError(f"file should contain following columns: {', '.join(columns)}")

    result_df.columns = columns
    result_df['Release Date'] = pd.to_datetime(result_df['Release Date'])
    result_df['Name'] = result_df['Name'].apply(lambda name: ' '.join(name.split('-')).title())
    result_df['Country'] = result_df['Country'].apply(
        return_none_decorator(lambda alpha_3: pycountry.countries.get(alpha_3=alpha_3).name)
    )
    result_df['price'] = result_df['Copy Price'].apply(
        return_none_decorator(lambda price_str: float(price_str.split()[0]))
    )
    result_df['currency'] = result_df['Copy Price'].apply(
        return_none_decorator(lambda price_str: price_str.split()[1])
    )

    if result_df['price'].isnull().values.any():
        raise ValueError(f"file contains incorrect prices")
    if result_df['currency'].isnull().values.any():
        raise ValueError(f"file contains incorrect or missing currencies")
    if result_df['Country'].isnull().values.any():
        raise ValueError(f"file contains alpha-3 codes that do not exist")
    if result_df['Copies Sold'].dtype != 'int64':
        raise ValueError(f"'Copies Sold' column should be integer")

    result_df['Total Revenue'] = result_df.apply(
        lambda row: round(row['Copies Sold'] * row['price']),
        axis=1
    )
    result_df['Total Revenue'] = result_df.apply(
        lambda row: ' '.join([str(row['Total Revenue']), row['currency']]),
        axis=1
    )

    return result_df.drop(['price', 'currency'], axis=1).sort_values(by=['Release Date'])
