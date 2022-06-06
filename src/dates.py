import field_names
import pandas as pd
import datetime


def create_date_series_from_dayend_data(day_end_data):
    min_date = day_end_data[field_names.DATE].min()
    max_date = day_end_data[field_names.DATE].max()

    dates_with_data_df = pd.DataFrame({
        field_names.DATE: day_end_data.sort_values(by=field_names.DATE)[field_names.DATE].unique()
    }, index=day_end_data.sort_values(by=field_names.DATE)[field_names.DATE].unique())

    all_dates_df = pd.DataFrame({
        field_names.DATE: pd.date_range(start=min_date, end=max_date).to_list()
    }, index=pd.date_range(start=min_date, end=max_date).to_list())

    dates_df = all_dates_df.join(dates_with_data_df, rsuffix="_with_data", lsuffix="")

    dates_df["next_date"] = dates_df["date"] + datetime.timedelta(days=1)
    dates_df["prev_date"] = dates_df["date"] + datetime.timedelta(days=-1)
    dates_df["has_data"] = ~dates_df["date_with_data"].isna()


    # Build the next date with data column
    #
    last_date = dates_df.iloc[len(dates_df)-1]["date"]
    next_date_with_data = [last_date]
    for i in range(len(dates_df)-2, -1, -1):
        cur = dates_df.iloc[i]
        nxt = dates_df.iloc[i+1]

        if cur["has_data"] and not nxt["has_data"]:
            next_date_with_data.append(last_date)
        elif not cur["has_data"]:
            next_date_with_data.append(last_date)
        else:
            next_date_with_data.append(nxt["date"])
            last_date = cur["date"]

    next_date_with_data.reverse()
    dates_df["next_date_with_data"] = next_date_with_data

    # Build the prev date with data column
    #
    last_date = dates_df.iloc[0]["date"]
    prev_date_with_data = [last_date]
    for i in range(1, len(dates_df)):
        cur = dates_df.iloc[i]
        prv = dates_df.iloc[i-1]

        if cur["has_data"] and not prv["has_data"]:
            prev_date_with_data.append(last_date)
        elif not cur["has_data"]:
            prev_date_with_data.append(last_date)
        else:
            prev_date_with_data.append(prv["date"])
            last_date = cur["date"]

    dates_df["prev_date_with_data"] = prev_date_with_data

    return dates_df


