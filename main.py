from datetime import date
import pandas as pd
from load_data import load_company_data, load_isin_data, load_day_end_data


def run(grouped_data, tkr, tstop_perc):
    # Get data from one tkr
    #
    data = grouped_data.get_group(tkr).copy()

    # Derive values for entry decisions
    data_ma5 = data.rolling(window=5, min_periods=1).mean()
    p = data['mid_hl'] - data_ma5['mid_hl']
    m = data_ma5['dr_hl']
    data['entry'] = (p.shift(1) < m.shift(1)) & (p > m)
    data_entry = data[data['entry'] == True]

    # Apply a trailing stop
    #
    level = tstop_perc / 100  # Percentage
    data['exit'] = False
    last_stop = None

    for i in range(0, len(data)):
        entry = data.iloc[i]['entry']
        stop = data.iloc[i]['mid_hl'] * (1 - level)

        if entry == True and last_stop is None:
            last_stop = stop
        else:
            if last_stop is not None:
                if stop > last_stop:
                    last_stop = stop
        if last_stop is not None:
            if data.iloc[i]['mid_hl'] < last_stop:
                data.iloc[i, data.columns.get_loc('exit')] = True
                last_stop = None

    data_exit = data[data['exit'] == True]

    # Calculate trades
    #
    trades = {'tkr': [], 'entry_date': [], 'exit_date': [], 'pl_perc': []}
    buy = None
    sell = None
    for i in range(0, len(data)):
        if data.iloc[i]['entry'] == True and buy is None:
            buy = data.iloc[i]

        if data.iloc[i]['exit'] == True and buy is not None:
            sell = data.iloc[i]

        if buy is not None and sell is not None:
            trades['tkr'].append(tkr)
            trades['entry_date'].append(buy['date'])
            trades['exit_date'].append(sell['date'])
            trades['pl_perc'].append(((sell['mid_hl'] - buy['mid_hl']) / buy['mid_hl']) * 100)
            buy = None
            sell = None
    trades_df = pd.DataFrame(trades)

    return data, data_ma5, data_entry, data_exit, trades_df


def trade(dfg, whitelist, start_date, end_date):
    all_trades = None
    for tkr in whitelist:
            data, data_ma5, data_entry, data_exit, trades = run(dfg, tkr, 2)
            if all_trades is None:
                all_trades = trades.copy()
            else:
                all_trades = all_trades.append(trades.copy())

            today_trades = data_entry[data_entry['date'] == today]
            if len(today_trades)>0:
                print('buy', today_trades)
            today_trades = data_exit[data_exit['date']==today]
            if len(today_trades)>0:
                print('sell', today_trades)

    return all_trades


# Processing
#

today = date.today()
#today = '2022-05-09'

companies = load_company_data('../data/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
isin = load_isin_data('../data/companies/ISIN-20220509.csv')
dfg, min_date, max_date = load_day_end_data('../data/dayend')


all_trades = trade(dfg, filter(dfg), None, None)
all_trades.to_csv('trades.csv', index=False)

def get_trade_stats(all_trades):
    ret_val = {'date': pd.date_range(start=min_date, end=max_date), 'entry_cnt': [], 'exit_cnt': [], 'delta': [], 'position': []}

    entries_by_date = all_trades.groupby('entry_date').count()
    exits_by_date = all_trades.groupby('exit_date').count()

    position = 0
    pl = 0
    for date in ret_val['date']:
        date_str = date.strftime('%Y-%m-%d')
        entry_count = 0
        exit_count = 0

        if date in entries_by_date['tkr'].keys():
            entry_count = entries_by_date['tkr'][date_str]
        if date in exits_by_date['tkr'].keys():
            exit_count = exits_by_date['tkr'][date_str]

        delta = entry_count-exit_count
        position = position + delta


        ret_val['entry_cnt'].append(entry_count)
        ret_val['exit_cnt'].append(exit_count)
        ret_val['delta'].append(delta)
        ret_val['position'].append(position)

    ret_val_df = pd.DataFrame(ret_val)
    return ret_val_df

trade_stats = get_trade_stats(all_trades)
trade_stats.to_csv('trade_stats.csv', index=False)


def trade_cost(size):
    return 10



def run_portfolio(dfg, filter, from_date,to_date,starting_capital,max_trade_size,trade_cost_fn):
    trades = trade(dfg, filter(dfg), from_date, to_date)
    dates = pd.date_range(start=from_date, end=to_date)

    for date in dates:
        # Get Trades for date
        #







portfolio = run_portfolio(dfg, filter, min_date, max_date,100000,1000,trade_cost)


if __name__ == '__main__':
    pass
