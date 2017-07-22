from unittest import TestCase

import requests

from vcr_setup import custom_vcr
from wblib import data_models, exceptions


class RideSessionResponseModelTest(TestCase):
    def test_init(self):
        response_model = data_models.RideSessionResponseModel({'results': [{}]})
        self.assertEqual(len(response_model.sessions), 1)

    def test_validate(self):
        response_model = data_models.RideSessionResponseModel({'results': [{}]})
        self.assertIsNone(response_model._validate({'results': [{}]}))

    def test_validate_no_results(self):
        response_model = data_models.RideSessionResponseModel({'results': [{}]})
        with self.assertRaisesRegex(
                expected_exception=exceptions.RideSessionException,
                expected_regex='No results returned'):
            response_model._validate({'results': []})


class RideSessionModelTest(TestCase):
    def setUp(self):
        session_data = {
            'objectId': '2yBuOvd92C',
            'user': {
                'objectId': 'u-1756bbba7e2a350'}}
        self.session = data_models.RideSessionModel(session_data)

    def test_init(self):
        session = data_models.RideSessionModel({})
        self.assertIsInstance(session, data_models.RideSessionModel)
        self.assertIsInstance(session, dict)

    def test_get_user_id(self):
        user_id = self.session.get_user_id()
        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_session_id(self):
        session_id = self.session.get_session_id()
        self.assertEqual(session_id, '2yBuOvd92C')

    def test_build_url(self):
        url = self.session._build_url('bla')
        self.assertEqual(url,
            'https://api.wattbike.com/v2/files/u-1756bbba7e2a350_2yBuOvd92C.bla')

    @custom_vcr.use_cassette()
    def test_get_tcx_url(self):
        url = self.session.get_tcx_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.tcx'))

        response = requests.get(url)
        self.assertTrue(response.ok)

    @custom_vcr.use_cassette()
    def test_get_wbs_url(self):
        url = self.session.get_wbs_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbs'))

        response = requests.get(url)
        self.assertTrue(response.ok)

    @custom_vcr.use_cassette()
    def test_get_wbsr_url(self):
        url = self.session.get_wbsr_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbsr'))

        response = requests.get(url)
        self.assertTrue(response.ok)


class LoginResponseModelTest(TestCase):
    def setUp(self):
        session_data = {
            'objectId': 'u-1756bbba7e2a350',
            'sessionToken': 'r:3cde15b3280d1f55d6cf3c4733f773ae'}
        self.login_response = data_models.LoginResponseModel(session_data)

    def test_init(self):
        session = data_models.LoginResponseModel({})
        self.assertIsInstance(session, data_models.LoginResponseModel)
        self.assertIsInstance(session, dict)

    def test_get_user_id(self):
        user_id = self.login_response.get_user_id()
        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_session_token(self):
        session_token = self.login_response.get_session_token()
        self.assertEqual(session_token, 'r:3cde15b3280d1f55d6cf3c4733f773ae')

class PerformanceStateModelTest(TestCase):
    def setUp(self):
        self.ps_resp = dict(
            results=[
                dict(
                    performanceState=dict(
                        mhr=111,
                        mmp=222,
                        ftp=333
                    )
                )
            ]
        )

    def test_init(self):
        ps_model = data_models.PerformanceStateModel(self.ps_resp)
        self.assertIsInstance(ps_model, data_models.PerformanceStateModel)

    def test_get_methods(self):
        ps_model = data_models.PerformanceStateModel(self.ps_resp)
        self.assertEqual(ps_model.get_max_hr(), 111)
        self.assertEqual(ps_model.get_max_minute_power(), 222)
        self.assertEqual(ps_model.get_ftp(), 333)
