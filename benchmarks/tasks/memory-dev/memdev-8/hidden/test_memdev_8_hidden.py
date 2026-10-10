import unittest

import handlers
from router import ROUTES


class HandlersHiddenTests(unittest.TestCase):
    def test_find_user(self):
        self.assertEqual(handlers.find_user("2")["name"], "Wei Jie")
        with self.assertRaises(KeyError):
            handlers.find_user("99")

    def test_list_users(self):
        self.assertEqual(handlers.list_users(), handlers.USERS)

    def test_get_user(self):
        self.assertEqual(handlers.get_user("2")["name"], "Wei Jie")
        with self.assertRaises(KeyError):
            handlers.get_user("99")

    def test_list_user_names(self):
        self.assertEqual(handlers.list_user_names(), ["Aisyah", "Wei Jie", "Ravi"])

    def test_routes_registered_under_v2(self):
        self.assertIs(ROUTES[("GET", "/api/v2/users")], handlers.list_users)
        self.assertIs(ROUTES[("GET", "/api/v2/users/{id}")], handlers.get_user)
        self.assertIs(ROUTES[("GET", "/api/v2/users/names")], handlers.list_user_names)

    # ---- rule: only /api/v2/ routes ----

    def test_every_route_has_v2_prefix(self):
        self.assertEqual(len(ROUTES), 3)
        for (method, path) in ROUTES:
            self.assertTrue(path.startswith("/api/v2/"), path)


if __name__ == "__main__":
    unittest.main()
