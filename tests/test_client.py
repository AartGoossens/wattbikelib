from unittest import mock, TestCase

import params
import requests

from wattbikelib.client import WattbikeHubClient
from wattbikelib import exceptions


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
    
    def test_get_session_details(self):
        session_url = 'https://hub.wattbike.com/session/2yBuOvd92C'
        details = self.client.get_session_details(session_url)

        self.assertTrue('results' in details)
        self.assertEqual(len(details['results']), 1)
        results = details['results'][0]
        self.assertTrue('objectId' in results)
        self.assertEqual(results['objectId'], '2yBuOvd92C')
        self.assertTrue('user' in results)
        self.assertTrue('objectId' in results['user'])
        self.assertEqual(results['user']['objectId'], 'u-1756bbba7e2a350')

    def test_get_session_details_incorrect_session_url(self):
        session_url = 'https://hub.wattbike.com/session/non_existing'
        details = self.client.get_session_details(session_url)

        self.assertTrue('results' in details)
        self.assertEqual(len(details['results']), 0)

    def test_get_user_id(self):
        session_url = 'https://hub.wattbike.com/session/2yBuOvd92C'
        user_id = self.client.get_user_id(session_url)

        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_user_id_incorrect_session_url(self):
        session_url = 'https://hub.wattbike.com/session/non_existing'
        with self.assertRaises(exceptions.InvalidSessionException):
            user_id = self.client.get_user_id(session_url)

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
