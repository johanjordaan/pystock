from unittest import TestCase

import field_names
from load_data import load_day_end_data
from entry_strategies import daily_range_breakout
from filters import tkr_filter


class Test(TestCase):
    def test_daily_range_breakout(self):
        day_end_data, min_date, max_date = load_day_end_data('./fixtures/dayend')
        entries = daily_range_breakout(tkr_filter(day_end_data, None, None, ["GOLD", 'AGL']))

        gold = entries[entries[field_names.TKR] == "GOLD"]
        self.assertEqual(2, len(gold))

        agl = entries[entries[field_names.TKR] == "AGL"]
        self.assertEqual(1, len(agl))
