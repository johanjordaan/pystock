import pandas as pd
import field_names


def daily_range_breakout(day_end_data):

    ret_val = {
        field_names.TKR:[],
        field_names.DATE: [],
    }

    for tkr in day_end_data['tkr'].unique():
        tkr_day_end_data = day_end_data[day_end_data['tkr'] == tkr]
        tkr_day_end_data_ma = tkr_day_end_data.rolling(window=5, min_periods=1).mean()
        current_range = tkr_day_end_data['mid_hl'] - tkr_day_end_data_ma['mid_hl']
        avg_daily_range = tkr_day_end_data_ma['dr_hl']

        entries = tkr_day_end_data[(current_range.shift(1) < avg_daily_range.shift(1)) & (current_range > avg_daily_range)]
        ret_val[field_names.TKR].extend(entries[field_names.TKR])
        ret_val[field_names.DATE].extend(entries[field_names.DATE])

    return pd.DataFrame(ret_val)
