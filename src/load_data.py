import os
import pandas as pd

import field_names


def load_company_data(file):
    names = [field_names.TKR, "name", "listing_date", "industry", "market_cap"]
    df = pd.read_csv(file, names=names, header=0, index_col=None)
    df['listing_date'] = pd.to_datetime(df['listing_date'], format='%Y-%m-%d')
    return df


def load_isin_data(file):
    names = [field_names.TKR, "name", field_names.ISIN_TYPE, "isin"]
    df = pd.read_csv(file, names=names, header=0, index_col=None)
    return df


def load_day_end_data(path):
    df = None
    names = [
        field_names.TKR,
        field_names.DATE,
        field_names.OPEN,
        field_names.HIGH,
        field_names.LOW,
        field_names.CLOSE,
        field_names.VOLUME
    ]
    for file in os.listdir(path):
        file_name = os.path.join(path, file)

        day_df = pd.read_csv(file_name, names=names, header=0, index_col=None)
        if df is None:
            df = day_df
        else:
            df = df.append(day_df)

    df = df.dropna()
    df[field_names.DATE] = pd.to_datetime(df[field_names.DATE], format='%Y%m%d')
    df['dr_hl'] = df[field_names.HIGH] - df[field_names.LOW]  # Daily range
    df['mid_hl'] = df[field_names.LOW] + (df['dr_hl']) / 2

    min_date = df[field_names.DATE].min()
    max_date = df[field_names.DATE].max()

    return df, min_date, max_date
