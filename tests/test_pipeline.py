import unittest
import datetime

def calculate_delivery_diff(actual_date, estimated_date):
    """Reflected logic: Calculates delivery delay/advance in days."""
    if not actual_date or not estimated_date:
        return 0
    try:
        act = datetime.datetime.strptime(actual_date, "%Y-%m-%d")
        est = datetime.datetime.strptime(estimated_date, "%Y-%m-%d")
        return (act - est).days
    except ValueError:
        return 0

def get_freight_ratio(price, freight_value):
    """Reflected logic: Calculates ratio of freight cost over price."""
    if not price or price <= 0:
        return 0.0
    return round((freight_value / price) * 100, 2)

class TestTargetPipeline(unittest.TestCase):
    def test_delivery_diff(self):
        self.assertEqual(calculate_delivery_diff("2026-07-10", "2026-07-15"), -5) # 5 days early
        self.assertEqual(calculate_delivery_diff("2026-07-20", "2026-07-15"), 5) # 5 days late
        self.assertEqual(calculate_delivery_diff("", "2026-07-15"), 0)
        
    def test_freight_ratio(self):
        self.assertEqual(get_freight_ratio(100.0, 15.0), 15.0)
        self.assertEqual(get_freight_ratio(0.0, 15.0), 0.0)
        self.assertEqual(get_freight_ratio(50.0, 0.0), 0.0)

if __name__ == '__main__':
    unittest.main()
