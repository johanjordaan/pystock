from unittest import TestCase

from load_data import load_company_data, load_isin_data, load_day_end_data
from filters import isin_type_filter, avg_filter, tkr_filter, equal_data_by_tkr_filter
import isin_types
import field_names


class Test_isin_type_filter(TestCase):
    def test_single_isin(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = isin_type_filter(day_end_data, companies_data, isin_data, isin_types.ORDINARY_FULLY_PAID)

        self.assertNotEqual(len(filtered_data), len(day_end_data))

    def test_isin_list(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = isin_type_filter(day_end_data, companies_data, isin_data, [isin_types.ORDINARY_FULLY_PAID])

        self.assertNotEqual(len(filtered_data), len(day_end_data))


class Test_avg_filter(TestCase):
    def test_min_only(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = avg_filter(day_end_data, companies_data, isin_data, field_names.CLOSE, 10, None)

        self.assertNotEqual(len(filtered_data), len(day_end_data))

    def test_max_only(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = avg_filter(day_end_data, companies_data, isin_data, field_names.CLOSE, None, 10)

        self.assertNotEqual(len(filtered_data), len(day_end_data))

    def test_min_and_max(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = avg_filter(day_end_data, companies_data, isin_data, field_names.CLOSE, 10, 20)

        self.assertNotEqual(len(filtered_data), len(day_end_data))


class Test_tkr_filter(TestCase):
    def test_single_tkr(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = tkr_filter(day_end_data, companies_data, isin_data, "GOLD")

        self.assertNotEqual(len(filtered_data), len(day_end_data))

    def test_tkr_list(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = tkr_filter(day_end_data, companies_data, isin_data, ["GOLD"])

        self.assertNotEqual(len(filtered_data), len(day_end_data))


class Test_equal_data_by_tkr_filter(TestCase):
    def test_filter(self):
        companies_data = load_company_data('./fixtures/companies/ASX_Listed_Companies_11-05-2022_07-38-19_AEST.csv')
        isin_data = load_isin_data('./fixtures/companies/ISIN-20220509.csv')
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')

        filtered_data = equal_data_by_tkr_filter(day_end_data, companies_data, isin_data)

        self.assertNotEqual(len(filtered_data), len(day_end_data))
