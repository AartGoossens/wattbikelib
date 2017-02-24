from unittest import mock, TestCase

import params
import requests

from wattbikelib.client import WattbikeHubClient


class WattbikeHubClientTest(TestCase):
    def setUp(self):
        self.client = WattbikeHubClient()

    def test_init(self):
        self.assertIsInstance(self.client, WattbikeHubClient)
        self.assertIsNone(self.client.session_token)

    def test_login(self):
        self.assertIsNone(self.client.session_token)
        self.client.login()
        self.assertRegex(self.client.session_token, 'r:[a-z0-9]{32}')

    def test_login_incorrect_credentials(self):
        correct_password = params.WATTBIKE_HUB_PASSWORD
        params.WATTBIKE_HUB_PASSWORD = 'incorrect_password'

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.login()
            self.assertIsNone(self.client.session_token)

        params.WATTBIKE_HUB_PASSWORD = correct_password

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
