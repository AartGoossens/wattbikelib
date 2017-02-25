import datetime
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

    def test_ride_session_call(self):
        payload = {
            'where': {
                'objectId': '2yBuOvd92C'}}

        sessions = self.client._ride_session_call(payload)
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertTrue('objectId' in session)
        self.assertEqual(session['objectId'], '2yBuOvd92C')

    def test_get_session_by_url(self):
        session_url = 'https://hub.wattbike.com/session/2yBuOvd92C'
        session = self.client.get_session_by_url(session_url)

        self.assertTrue('objectId' in session)
        self.assertEqual(session['objectId'], '2yBuOvd92C')
        self.assertTrue('user' in session)
        self.assertTrue('objectId' in session['user'])
        self.assertEqual(session['user']['objectId'], 'u-1756bbba7e2a350')

    def test_get_user_id(self):
        session_url = 'https://hub.wattbike.com/session/2yBuOvd92C'
        user_id = self.client.get_user_id(session_url)

        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_user(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user()

    def test_get_sessions(self):
        before = datetime.datetime(2017, 1, 1)
        after = datetime.datetime(2015, 12, 31)
        sessions = self.client.get_sessions(
            user_id='u-1756bbba7e2a350',
            before=before,
            after=after)
        self.assertEqual(len(sessions), 11)
        self.assertEqual(sessions[0]['user']['objectId'], 'u-1756bbba7e2a350')

    def test_get_session_data(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_data()

    def test_get_session_revolutions(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_session_revolutions()

    def test_get_user_preferences(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user_preferences()

    def test_get_user_performance_state(self):
        with self.assertRaises(NotImplementedError):
            self.client.get_user_performance_state()
