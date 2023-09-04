from unittest import TestCase

import filters
from load_data import load_day_end_data,load_isin_data,load_company_data
from entry_strategies import daily_range_breakout
import portfolio
import isin_types
import field_names

class Test_run(TestCase):
    def test_simple_run(self):
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')

        portfolio_data = filters.isin_type_filter(
            filters.avg_filter(
                filters.equal_data_by_tkr_filter(day_end_data, companies_data, isin_data),
                companies_data, isin_data, field_names.CLOSE, 10, None
            ),
            companies_data, isin_data, isin_types.ORDINARY_FULLY_PAID
        )

        stop_loss_perc = .1
        max_trade_amount = 1000
        starting_capital = 100000
        def cost_fn(amound):
            return 10

        portfolio_positions = portfolio.run(
            portfolio_data,
            companies_data,
            isin_data,
            daily_range_breakout,
            cost_fn,
            max_trade_amount,
            stop_loss_perc,
            starting_capital
        )

        self.assertEqual(864,  len(portfolio_positions))


