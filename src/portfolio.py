from turtle import position

import pandas as pd
import field_names
import math
from copy import deepcopy
from dates import create_date_series_from_dayend_data


def buy(date, price_data, entry, cost_fn, max_trade_amount):
    price = price_data.squeeze().to_dict()[field_names.CLOSE]
    number_shares = math.trunc(max_trade_amount/price)
    outlay = number_shares*price
    return({
        field_names.ACTION: type,
        field_names.TKR: entry[field_names.TKR],
        field_names.DATE: entry[field_names.DATE],
        "price": price,
        "num_shares": number_shares,
        "outlay": outlay,
        "cost": cost_fn(outlay)
    })


def sell(date, price_data, position, cost_fn):
    price = price_data.squeeze().to_dict()[field_names.CLOSE]
    number_shares = -position["num_shares"]
    outlay = number_shares * price
    return ({
        field_names.ACTION: type,
        field_names.TKR: position[field_names.TKR],
        field_names.DATE: date,
        "price": price,
        "num_shares": number_shares,
        "outlay": outlay,
        "cost": cost_fn(outlay)
    })


def run(day_end_data, companies_data, isin_data, entry_strategy_fn, cost_fn, max_trade_amount, stop_loss_perc, starting_capital):
    # Setup the dates from this run based on the end of day data
    #
    dates = create_date_series_from_dayend_data(day_end_data)
    min_date = dates[field_names.DATE].min()
    max_date = dates[field_names.DATE].max()

    # Setup the portfolio
    #
    positions_history = []
    positions = [{
        field_names.DATE: dates[dates[field_names.DATE]==min_date]["prev_date"].squeeze(),
        field_names.TKR: "CASH",
        "price": 1,
        "best_price":1,
        "num_shares":starting_capital,
        "outlay":0,
        "cost":0
    }]
    current_tkrs = []

    # Get all the potential entry trades
    #
    entries = entry_strategy_fn(day_end_data)

    # Here we keep the stop losses detected
    # We keep them here because they are detected and then needs to be applied the next day
    #
    stops = []

    # Now run through all the dates
    #
    # 1) Save last position to position history
    # 2) Update positions (date and price)
    # 3) Apply previous stops
    # 3) Calculate next stops
    # 4) Add new positions
    #
    for date_index in range(len(dates)):
        date = dates.iloc[date_index]
        data_for_today = day_end_data[day_end_data[field_names.DATE] == date[field_names.DATE]]

        # 1) Save current positions to history
        #
        positions_history.extend(deepcopy(positions))

        # 2) Update positions price and date and select the cash position
        #
        cash = None
        for position in positions:
            position[field_names.DATE] = date[field_names.DATE]
            if position[field_names.TKR] == "CASH":
                cash = position
            else:
                if date["has_data"]:
                    price = data_for_today[data_for_today[field_names.TKR] == position[field_names.TKR]].squeeze()[field_names.OPEN]
                    position["best_price"] = position["best_price"] if price < position["best_price"] else price
                    position["price"] = price

        # If we don't have data for this date just skip the rest
        if not date["has_data"]:
            continue

        # 3) Apply previous stop losses
        #
        hitlist = []
        for position in positions:
            if position[field_names.TKR] in stops:
                hitlist.append(position)
        for position in hitlist:
            positions.remove(position)
            proceeds = position["price"]*position["num_shares"]
            cost = cost_fn(proceeds)
            cash["num_shares"] += proceeds - cost
            current_tkrs.remove(position[field_names.TKR])


        # 4) Detect next stop losses
        #
        stops = []
        for position in positions:
            if (position["price"]-position["best_price"])/position["best_price"] < -stop_loss_perc:
                stops.append(position[field_names.TKR])
        # 5) Add new positions
        #
        entries_detected_yesterday = entries[entries[field_names.DATE] == date["prev_date_with_data"]]
        for entry_index in range(len(entries_detected_yesterday)):
            potential_entry = entries_detected_yesterday.iloc[entry_index]
            if potential_entry[field_names.TKR] not in current_tkrs:
                price = data_for_today[
                    data_for_today[field_names.TKR] == potential_entry[field_names.TKR]
                ].squeeze()[field_names.OPEN]
                num_shares = math.trunc(max_trade_amount / price)
                outlay = num_shares * price
                cost = cost_fn(outlay)

                if cash["num_shares"]>(outlay + cost):
                    positions.append({
                        field_names.DATE: date[field_names.DATE],
                        field_names.TKR: potential_entry[field_names.TKR],
                        "price": price,
                        "best_price": price,
                        "num_shares": num_shares,
                        "outlay": outlay,
                        "cost": cost
                    })
                    current_tkrs.append(potential_entry[field_names.TKR])
                    cash["num_shares"] -= outlay + cost
                else:
                    print("No more cash")

    return pd.DataFrame(positions_history)
