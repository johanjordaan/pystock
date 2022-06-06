from unittest import TestCase
from load_data import load_day_end_data, load_isin_data, load_company_data
import dates
import datetime


class Test(TestCase):
    def test_create_date_series_from_dayend_data(self):
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')

        result = dates.create_date_series_from_dayend_data(day_end_data)

        self.assertTrue(result.iloc[4]["has_data"] == True)
        self.assertTrue(result.iloc[4]["next_date_with_data"] == datetime.datetime.strptime("2021-11-08", '%Y-%m-%d'))
        self.assertTrue(result.iloc[5]["has_data"] == False)
        self.assertTrue(result.iloc[5]["prev_date_with_data"] == datetime.datetime.strptime("2021-11-05", '%Y-%m-%d'))
