from unittest import TestCase

from load_data import load_company_data, load_isin_data, load_day_end_data

class Test(TestCase):
    def test_load_company_data(self):
        df = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        self.assertEqual(len(df), 2115)

    def test_load_isin_data(self):
        df = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        self.assertEqual(len(df), 15688)

    def test_load_day_end_data(self):
        df, min_date, max_date = load_day_end_data('./fixtures/dayend')
        self.assertEqual(len(df), 56072)
