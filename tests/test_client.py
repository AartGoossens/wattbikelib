from unittest import TestCase

from wattbikelib.client import WattbikeHubClient


class WattbikeHubClientTest(TestCase):
    def setUp(self):
        self.client = WattbikeHubClient()

    def test_init(self):
        self.assertIsInstance(self.client, WattbikeHubClient)

    def test_login(self):
        with self.assertRaises(NotImplementedError):
            self.client.login()

    def test_logout(self):
        with self.assertRaises(NotImplementedError):
            self.client.logout()

    def test_get_user(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user()

    def test_get_sessions(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_sessions()

    def test_get_session_data(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_data()

    def test_get_session_revolutions(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_revolutions()

    def test_get_session_tcx_url(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_tcx_url()

    def test_get_session_wbs_url(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_wbs_url()

    def test_get_session_wbsr_url(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_wbsr_url()

    def test_get_user_preferences(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user_preferences()

    def test_get_user_performance_state(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user_performance_state()
