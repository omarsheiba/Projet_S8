import numpy as np
import pandas as pd

##if last day falls in a weekend, takes the previous weekday (previous friday)
def add_months(date: np.datetime64, month_offset: int):
    offseted_date = date + pd.tseries.offsets.DateOffset(months=month_offset)
    if offseted_date.dayofweek >= 5:
        return offseted_date + pd.tseries.offsets.DateOffset(days = 4-offseted_date.dayofweek)
    return offseted_date

def sharpe_ratio_annualized(ts: pd.Series):
    N=252 
    return np.sqrt(N) * ts.mean()/ts.std()
