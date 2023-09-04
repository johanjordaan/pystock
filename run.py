import pandas as pd

import filters
from load_data import load_day_end_data, load_isin_data, load_company_data
from entry_strategies import daily_range_breakout, random
import portfolio
import isin_types
import field_names
from functools import partial
import itertools

day_end_data, min_date, max_date = load_day_end_data('../data/dayend')
companies_data = load_company_data('../data/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
isin_data = load_isin_data('../data/companies/ISIN-20220509.csv')

portfolio_data = filters.equal_data_by_tkr_filter(
    filters.avg_filter(
        filters.isin_type_filter(day_end_data, companies_data, isin_data, isin_types.ORDINARY_FULLY_PAID),
        companies_data, isin_data, field_names.CLOSE, 10, None
    ),
    companies_data, isin_data
)

#portfolio_data = filters.tkr_filter(portfolio_data, companies_data,isin_data, ['ASX'])

def cost_fn(amount):
    return 10

max_trade_amount = 1000
starting_capital = 100000

world = {
    "window": [3, 5, 7],
    "stop_loss_perc": [.05, .1, .25],
}

for i in itertools.product(world["window"], world["stop_loss_perc"]):
    window = i[0]
    stop_loss_perc = i[1]
    print(f"window={window}, stop_loss_perc={stop_loss_perc}")
    portfolio_positions = portfolio.run(
        portfolio_data,
        companies_data,
        isin_data,
        partial(daily_range_breakout, {"window": window}),
        cost_fn,
        max_trade_amount,
        stop_loss_perc,
        starting_capital
    )
    portfolio_positions.to_csv(f'results/strategy[{"daily_range_breakout"}]-window[{window}]-stop_loss_perc[{stop_loss_perc}].csv', index=False)

world = {
    "probability": [.1, .2, .5],
    "stop_loss_perc": [.05, .1, .25],
}

for i in itertools.product(world["probability"], world["stop_loss_perc"]):
    probability = i[0]
    stop_loss_perc = i[1]
    print(f"window={window}, stop_loss_perc={stop_loss_perc}")
    portfolio_positions = portfolio.run(
        portfolio_data,
        companies_data,
        isin_data,
        partial(random, {"probability": probability}),
        cost_fn,
        max_trade_amount,
        stop_loss_perc,
        starting_capital
    )
    portfolio_positions.to_csv(f'results/strategy[{"random"}]-probability[{probability}]-stop_loss_perc[{stop_loss_perc}].csv', index=False)
