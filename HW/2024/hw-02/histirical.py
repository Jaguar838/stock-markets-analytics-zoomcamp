from typing import List, Union
import pandas as pd
import yfinance as yf

def get_historical_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    '''
    Завантажує історичні дані OHLCV для заданих акцій за заданий часовий проміжок.
    Args:
    tickers (List[str]): Список символів акцій.
    start_date (str): Дата початку в форматі YYYY-MM-DD.
    end_date (str): Дата закінчення в форматі YYYY-MM-DD.
    Returns:
    pandas.DataFrame: DataFrame з історичними даними Close.
    '''

    # Завантажте дані для кожного символу

    data = {}
    for ticker in tickers:
        try:
        # Завантажте дані для символу
            data[ticker] = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)['Close']
        except KeyError:\
            print(f"Попередження: 'Close' не знайдено для {ticker}. Пропущено...")

    return pd.DataFrame(data)


def add_growth_columns(df, daily_prices_df, min_date_col='ipo_date'):
    """
    Додає стовпці з приростом (growth_future_1d ... growth_future_30d) до датафрейму df.

    Args:
        df: Датафрейм з датою IPO та символом акції.
        daily_prices_df: Датафрейм з денними цінами акцій.
        min_date_col: Назва стовпця з датою IPO.

    Returns:
        Датафрейм з доданими стовпцями зростання.
    """
    for ticker in df['ticker']:
        # Отримайте рядковий індекс для даного символу
        row_idx = df.loc[df['ticker'] == ticker].index[0]
        # Отримайте дату IPO для даного символу
        ipo_date = df.loc[row_idx, min_date_col]
        # Отримайте денні ціни для даного символу
        ticker_prices = daily_prices_df[ticker][ipo_date:]
        # print(row_idx, ticker, ticker_prices.isnull().sum(), ipo_date)
        # Додайте стовпці з приростом
        for i in range(1, 31):
            # Ціна акції в майбутньому через і-днів
            growth = ticker_prices.shift(-1) / ticker_prices
            # Додаемо приріст на кожен день торгів акції
            df.loc[row_idx, f"growth_future_{i}d"] = growth[ipo_date]

    return df
