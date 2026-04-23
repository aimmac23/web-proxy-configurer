import json
import unittest

import app

class MyTestCase(unittest.TestCase):
    def test_status(self):
        client = app.app.test_client()
        response = client.get("/status")
        self.assertEqual(response.status_code, 200)

    def test_fetch(self):
        # Technically not a unit test if doing an internet HTTP call... but it works.
        proxies = app.get_proxies()
        self.assertTrue(proxies)


if __name__ == '__main__':
    unittest.main()
