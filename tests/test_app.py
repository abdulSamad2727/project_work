import unittest
from app import get_sql, cur

class TestTransportBot(unittest.TestCase):
    def test_sql(self):
        s = get_sql("show trips", "abc")
        self.assertEqual(s, "SELECT * FROM trips WHERE company = 'abc'")

    def test_company_isolation(self):
        r = cur.execute(get_sql("show all users", "abc")).fetchall()
        # should only return abc users
        self.assertEqual(len(r), 2)

    def test_dummy(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
