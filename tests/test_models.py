from unittest import TestCase

import pandas as pd
import requests

from wattbikelib import exceptions, models


class RideSessionResponseModelTest(TestCase):
    def test_init(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
        self.assertEqual(len(response_model.sessions), 1)

    def test_validate(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
        self.assertIsNone(response_model._validate({'results': [{}]}))

    def test_validate_no_results(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
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
        self.session = models.RideSessionModel(session_data)

    def test_init(self):
        session = models.RideSessionModel({})
        self.assertIsInstance(session, models.RideSessionModel)
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

    def test_get_tcx_url(self):
        url = self.session.get_tcx_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.tcx'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)

    def test_get_wbs_url(self):
        url = self.session.get_wbs_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbs'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)

    def test_get_wbsr_url(self):
        url = self.session.get_wbsr_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbsr'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)


class LoginResponseModelTest(TestCase):
    def setUp(self):
        session_data = {
            'objectId': 'u-1756bbba7e2a350',
            'sessionToken': 'r:3cde15b3280d1f55d6cf3c4733f773ae'}
        self.login_response = models.LoginResponseModel(session_data)

    def test_init(self):
        session = models.LoginResponseModel({})
        self.assertIsInstance(session, models.LoginResponseModel)
        self.assertIsInstance(session, dict)

    def test_get_user_id(self):
        user_id = self.login_response.get_user_id()
        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_session_token(self):
        session_token = self.login_response.get_session_token()
        self.assertEqual(session_token, 'r:3cde15b3280d1f55d6cf3c4733f773ae')


class WattbikeDataFrameTest(TestCase):
    def setUp(self):
        self.data = [{
            'speed': '30.7822',
            'polar_force': '86,72,57,48,40,33,31,30,30,31,31,32,33,35,41,48,57,69,81,92,103,110,121,131,144,158,168,178,189,198,209,220,229,237,240,244,248,252,255,256,257,259,259,259,256,255,248,242,230,220,208,194,180,163,148,129,113,98,83,73,61,53,46,42,38,36,35,33,33,37,42,52,63,76,86,94,105,113,124,131,139,143,148,153,157,162,164,168,171,175,177,177,177,177,178,178,180,178,177,173,171,166,160,153,143,131,120,107,93,83,72,67,62,62,59',
            'polar_lcnt': 61,
            'polar_cnt': 115,
            'distance': '9.8332',
            'power': '121.4584',
            'time': '1.1500',
            'force': '130.7665',
            'balance': '58.5158',
            'heartrate': '100.0000',
            'cadence': '52.1739'}]
        self.wdf = models.WattbikeDataFrame(self.data)

    def test_init(self):
        wdf = models.WattbikeDataFrame(self.data)
        self.assertIsInstance(wdf, models.WattbikeDataFrame)
        self.assertIsInstance(wdf, pd.DataFrame)
    
    def test_constructor(self):
        # Random command to force calling WattbikeDataFrame._constructor
        wdf = self.wdf[['power', 'cadence']]
        self.assertIsInstance(wdf, models.WattbikeDataFrame)

    def test_columns_to_numeric(self):
        self.assertEqual(self.wdf.balance.dtype.name, 'float64')
        self.assertEqual(self.wdf.cadence.dtype.name, 'float64')
        self.assertEqual(self.wdf.distance.dtype.name, 'float64')
        self.assertEqual(self.wdf.force.dtype.name, 'float64')
        self.assertEqual(self.wdf.heartrate.dtype.name, 'float64')
        self.assertEqual(self.wdf.polar_cnt.dtype.name, 'int64')
        self.assertEqual(self.wdf.polar_lcnt.dtype.name, 'int64')
        self.assertEqual(self.wdf.power.dtype.name, 'float64')
        self.assertEqual(self.wdf.speed.dtype.name, 'float64')
        self.assertEqual(self.wdf.time.dtype.name, 'float64')
        self.assertEqual(self.wdf.polar_force.dtype.name, 'object')

    def test_plot_polar_view(self):
        with self.assertRaises(NotImplementedError):
            self.wdf.plot_polar_view()
