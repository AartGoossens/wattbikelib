import datetime
from unittest import TestCase, mock

import requests

import params
from vcr_setup import custom_vcr
from wblib import exceptions
from wblib.client import WattbikeHubClient


class WattbikeHubClientTest(TestCase):
    def setUp(self):
        self.client = WattbikeHubClient()

    def test_init(self):
        self.assertIsInstance(self.client, WattbikeHubClient)
        self.assertIsNone(self.client.session_token)

    @custom_vcr.use_cassette()
    def test_login(self):
        self.assertIsNone(self.client.session_token)
        self.client.login(params.WATTBIKE_HUB_USERNAME, params.WATTBIKE_HUB_PASSWORD)

        self.assertRegex(self.client.session_token, 'r:[a-z0-9]{32}')
        self.assertRegex(self.client.user_id, 'u-[a-z0-9]{15}')

    @custom_vcr.use_cassette()
    def test_login_incorrect_credentials(self):
        correct_password = params.WATTBIKE_HUB_PASSWORD
        params.WATTBIKE_HUB_PASSWORD = 'incorrect_password'

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.login('wrong_username', 'wrong_password')
            self.assertIsNone(self.client.session_token)

        params.WATTBIKE_HUB_PASSWORD = correct_password

    @custom_vcr.use_cassette()
    def test_logout(self):
        with self.assertRaises(NotImplementedError):
            self.client.logout()

    @custom_vcr.use_cassette()
    def test_ride_session_call(self):
        payload = {
            'where': {
                'objectId': '2yBuOvd92C'}}

        sessions = self.client._ride_session_call(payload)
        self.assertEqual(len(sessions), 1)
        session = sessions[0]

    @custom_vcr.use_cassette()
    def test_ride_session_call_logged_in(self):
        self.client.login(params.WATTBIKE_HUB_USERNAME, params.WATTBIKE_HUB_PASSWORD)
        payload = {
            'where': {
                'objectId': '2yBuOvd92C'}}

        sessions = self.client._ride_session_call(payload)
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session.get_session_id(), '2yBuOvd92C')
        self.assertEqual(session.get_session_id(), '2yBuOvd92C')

    @custom_vcr.use_cassette()
    def test_get_session(self):
        session_url = 'https://hub.wattbike.com/session/2yBuOvd92C'
        session = self.client.get_session(session_url)

        self.assertEqual(session[1].get_session_id(), '2yBuOvd92C')
        self.assertEqual(session[1].get_user_id(), 'u-1756bbba7e2a350')

    @custom_vcr.use_cassette()
    def test_get_sessions_for_user(self):
        before = datetime.datetime(2017, 3, 1)
        after = datetime.datetime(2017, 1, 1)
        sessions = self.client.get_sessions_for_user(
            user_id='u-1756bbba7e2a350',
            before=before,
            after=after)
        self.assertEqual(len(sessions), 4)
        self.assertEqual(sessions[0][1].get_user_id(), 'u-1756bbba7e2a350')

    @custom_vcr.use_cassette()
    def test_get_sessions_for_user_without_before_after(self):
        sessions = self.client.get_sessions_for_user(
            user_id='u-1756bbba7e2a350')
        self.assertEqual(len(sessions), 24)
        self.assertEqual(sessions[0][1].get_user_id(), 'u-1756bbba7e2a350')

    @custom_vcr.use_cassette()
    def test_get_user_performance_state(self):
        ps_data = self.client.get_user_performance_state(
            user_id='u-1756bbba7e2a350'
        )

    @custom_vcr.use_cassette()
    def test_get_user_id_from_session_url(self):
        session_url = 'https://hub.wattbike.com/session/LYPWXEjF9B'
        user_id = self.client.get_user_id_from_session_url(session_url)
        self.assertEqual(user_id, 'u-1756bbba7e2a350')
