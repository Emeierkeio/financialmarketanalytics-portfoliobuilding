import pandas as pd
import numpy as np
import math

def get_log_returns(filename):
    closing_prices = pd.read_csv(filename)
    closing_prices.fillna(np.nan, inplace=True)
    dates = closing_prices.iloc[:,0]
    closing_prices = closing_prices.iloc[: , 1:]
    columns_names = closing_prices.columns.tolist()
    df_log_returns = np.log(closing_prices) - np.log(closing_prices.shift(1))
    df_log_returns['Dates'] = dates
    df_log_returns = df_log_returns[['Dates'] + columns_names]
    df_log_returns = df_log_returns.iloc[1:,:]
    return df_log_returns

def color_negative_red(val):
    if isinstance(val, float):
        color = 'red' if val < 0 else 'black'
        return 'color: %s' % color
    else:
        return 'color: %s' % 'back'

def get_absolute_return_old(daily_returns):
    returns = []
    returns.append(100 * math.exp(daily_returns[0]))
    for i in range(1, len(daily_returns)):
        returns.append(returns[i-1] * math.exp(daily_returns[i]))

def get_absolute_return(daily_returns):
    current_value = 100 * math.exp(daily_returns[0])
    for i in range(1, len(daily_returns)):
        current_value = current_value * math.exp(daily_returns[i])
    return current_value / 100 - 1


    