#!/usr/bin/env python3

from excel_time_series_provider import ExcelTimeSeriesProvider
from utils import *
from matplotlib import pyplot
import pandas as pd
import numpy as np

##Parameters
stock_name = "NESTE FH Equity"
index_name = "SXXP Index"
filename = "Neste and SXXP price.xlsx"
price_type = "PX_LAST"

##parse time series and create resulting dataframe

ts_provider = ExcelTimeSeriesProvider(filename)
NESTE_ts = ts_provider.get_time_series(stock_name, price_type)
SXXP_ts = ts_provider.get_time_series(index_name, price_type)
dates = ts_provider.get_time_series("Dates")
ts_df = pd.DataFrame(list(zip(dates, NESTE_ts, SXXP_ts)), columns =['Dates', stock_name, index_name], index=dates)

## Add resulting relative performance to dataframe
ts_df['daily_relative_performance'] = ts_df[stock_name] / ts_df[index_name]

## Compute 3M rolling max and add it to dataframe
## If the start day of the rolling period falls on a weekend, we take the following week day
ts_df['3M rolling max'] = [
    ts_df.loc[
        edt - pd.tseries.offsets.DateOffset(months=3):edt, 'daily_relative_performance'
    ].max() if (edt - pd.tseries.offsets.DateOffset(months=3) >= ts_df['Dates'].iloc[0]) else np.NaN for edt in ts_df.index
]

##Get 1 month, 3month and 6month relative performance following 3 month rolling max
##A signal is generated whenever 3month hight is reached, even if right after another 3 month high
##We store the 3 month high generating the signal, the 1/3/6 month relative performance following the signal, and the date of the signal generation 
##In addition we are going to compute the market neutral sharpe ratio (long 1$ stock short 1$ index) to compare performance of the stock comapred to index
forward_looking_relative_performance ={'1M':[], '3M':[], '6M':[]}
last_date = ts_df['Dates'].iloc[-1]
##We add the daily returns columns to the dataframe in order to compute sharpe ratio of the market neutral strategy
ts_df['NESTE FH Equity pct_change'] = ts_df[stock_name].pct_change()
ts_df['SXXP Index pct_change'] = ts_df[index_name].pct_change()

for index,row in ts_df.iterrows():
    if row['3M rolling max'] == row['daily_relative_performance']:
        offset_1m = add_months(index, 1)
        if offset_1m <= last_date:
            #strategy daily return = stock return - benchmark return / 2
            sr = sharpe_ratio_annualized((ts_df.loc[index:offset_1m]['NESTE FH Equity pct_change'] - ts_df.loc[index:offset_1m]['SXXP Index pct_change'])/2)
            forward_looking_relative_performance['1M'].append((row['3M rolling max'], ts_df.loc[offset_1m]['daily_relative_performance'], index, sr))
        else:
            ## if current date > last_date - 1 month, stop looping
            break
        offset_3m = add_months(index, 3)
        if offset_3m <= last_date:
            sr = sharpe_ratio_annualized((ts_df.loc[index:offset_3m]['NESTE FH Equity pct_change'] - ts_df.loc[index:offset_3m]['SXXP Index pct_change'])/2)
            forward_looking_relative_performance['3M'].append((row['3M rolling max'], ts_df.loc[offset_3m]['daily_relative_performance'], index, sr))
        else:
            ## if current date > last_date - 3 month, no need to check the 6 month relative performance
            continue
        offset_6m = add_months(index, 6)
        if offset_6m <= last_date:
            sr = sharpe_ratio_annualized((ts_df.loc[index:offset_6m]['NESTE FH Equity pct_change'] - ts_df.loc[index:offset_6m]['SXXP Index pct_change'])/2)
            forward_looking_relative_performance['6M'].append((row['3M rolling max'], ts_df.loc[offset_6m]['daily_relative_performance'], index, sr))

##Compute performance metrics and store in a dataframe
perf_metrics = {key: {} for key in forward_looking_relative_performance.keys()}
for key in perf_metrics.keys():
    geometric_rr = [(a[1]-a[0])/a[0] for a in forward_looking_relative_performance[key]]
    perf_metrics[key]['nb obs'] = len(geometric_rr)
    perf_metrics[key]['average geometric relative return'] = np.average(geometric_rr)
    perf_metrics[key]['stdev geometric relative return'] = np.std(geometric_rr)
    perf_metrics[key]['median geometric relative return'] = np.median(geometric_rr)
    perf_metrics[key]['max geometric relative return'] = np.max(geometric_rr)
    perf_metrics[key]['min geometric relative return'] = np.min(geometric_rr)
    perf_metrics[key]['annualized average geometric relative return'] = pow((1+perf_metrics[key]['average geometric relative return']),12/int(key[0]))-1
    perf_metrics[key]['hit ratio'] = sum([1 if i>0 else 0 for i in geometric_rr])/len(geometric_rr)
    perf_metrics[key]['average annualized sharpe ratio (market neutral)'] = np.mean([a[3] for a in forward_looking_relative_performance[key]])

metrics_df = pd.DataFrame.from_dict(perf_metrics, orient = 'index')

occurences= pd.Series([a[0] for a in forward_looking_relative_performance['1M']], index=[a[2] for a in forward_looking_relative_performance['1M']])
pyplot.figure(figsize=(20,10))
ax = pyplot.subplot(131)
ax.set_title('Relative performance max values (3 month rolling window)')
ax.set_xlabel('Date')
ax.set_ylabel('Relative performance')
occurences.plot(style = 'k.')
geometric_rr = []
label_keys = forward_looking_relative_performance.keys()
for key in label_keys:
    geometric_rr.append([(a[1]-a[0])/a[0] for a in forward_looking_relative_performance[key]])
ax = pyplot.subplot(132)
ax.set_title('Box plot of the geometric relative return for each holding period')
ax.set_xlabel('Holding period')
ax.set_ylabel('Geometric relative return')
pyplot.boxplot(geometric_rr, labels=label_keys, showfliers=True)
ax = pyplot.subplot(133)
ax.set_title('Stock/Index Scatter plot and regression line')
ax.set_xlabel(index_name)
ax.set_ylabel(stock_name)
pyplot.scatter(ts_df[index_name], ts_df[stock_name], s = 10)
a, b = np.polyfit(ts_df[index_name], ts_df[stock_name], 1)
ax.text(310, 15, f'r = {round(a, 3)}', color = "red")
pyplot.plot(ts_df[index_name], a*ts_df[index_name] + b, 'r-')
pyplot.show(block=True)
print("Done")
