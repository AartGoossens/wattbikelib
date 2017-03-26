from unittest import TestCase

import numpy as np
import pandas as pd
import requests

from vcr_setup import custom_vcr
from wblib import exceptions, models


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

class WattbikeFramePlotMethodsTest(TestCase):
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
        wdf = models.WattbikeDataFrame(self.data * 60)
        wdf.process()
        self.wfpm = models.WattbikeFramePlotMethods(wdf)

    def test_polar(self):
        ax = self.wfpm.polar()
        self.assertTrue(ax.has_data)

    def test_polar_full(self):
        ax = self.wfpm.polar(full=True)
        self.assertTrue(ax.has_data)

    def test_polar_full_without_mean(self):
        ax = self.wfpm.polar(full=True, mean=False)
        self.assertTrue(ax.has_data)

    def test_scatter(self):
        ax = self.wfpm.scatter(x='power', y='cadence')
        self.assertTrue(ax.has_data)

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
            'cadence': '52.1739'},
            {'speed': '30.7822',
            'distance': '9.8332',
            'power': '121.4584',
            'time': '1.1500',
            'force': '130.7665',
            'balance': '58.5158',
            'heartrate': '100.0000',
            'cadence': '52.1739'}
            ]
        self.wdf = models.WattbikeDataFrame(self.data)
        self.wdf.columns_to_numeric()

    def test_init(self):
        wdf = models.WattbikeDataFrame(self.data)
        self.assertIsInstance(wdf, models.WattbikeDataFrame)
        self.assertIsInstance(wdf, pd.DataFrame)
    
    def test_constructor(self):
        # Random command to force calling WattbikeDataFrame._constructor
        wdf = self.wdf[['power', 'cadence']]
        self.assertIsInstance(wdf, models.WattbikeDataFrame)

    def test_columns_to_numeric(self):
        wdf = models.WattbikeDataFrame(self.data)
        self.assertEqual(wdf.balance.dtype.name, 'object')
        self.assertEqual(wdf.polar_cnt.dtype.name, 'float64')
        self.assertEqual(wdf.polar_force.dtype.name, 'object')

        wdf_2 = wdf.columns_to_numeric()
        self.assertEqual(wdf.balance.dtype.name, 'float64')
        self.assertEqual(wdf.polar_cnt.dtype.name, 'float64')
        self.assertEqual(wdf.polar_force.dtype.name, 'object')
        self.assertIsNotNone(wdf_2)

    def test_plot_polar_view(self):
        with self.assertRaises(NotImplementedError):
            self.wdf.plot_polar_view()

    def test_add_polar_forces(self):
        wdf_2 = self.wdf.add_polar_forces()
        self.assertIsNotNone(wdf_2)
        self.assertTrue('_0' in self.wdf.columns)
        self.assertTrue('_359' in self.wdf.columns)
        self.assertIsInstance(self.wdf.loc[0, '_0'], float)
        self.assertEqual(self.wdf.loc[0, '_0'], 0.659439450026441)

    def test_add_polar_forces_columns_already_exist(self):
        self.wdf.add_polar_forces()
        wdf_2 = self.wdf.add_polar_forces()
        self.assertTrue('_0' in self.wdf.columns)
        self.assertTrue('_359' in self.wdf.columns)
        self.assertIsInstance(self.wdf.loc[0, '_0'], float)
        self.assertEqual(self.wdf.loc[0, '_0'], 0.659439450026441)

    def test_min_max_angles(self):
        self.wdf.add_polar_forces()
        self.assertTrue('left_max_angle' not in self.wdf.columns)
        self.wdf.add_min_max_angles()

        self.assertTrue('left_max_angle' in self.wdf.columns)
        self.assertTrue('left_min_angle' in self.wdf.columns)
        self.assertTrue('right_max_angle' in self.wdf.columns)
        self.assertTrue('right_min_angle' in self.wdf.columns)

        self.assertEqual(self.wdf.iloc[0].left_max_angle, 129.0)
        self.assertEqual(self.wdf.iloc[0].left_min_angle, 22.0)
        self.assertEqual(self.wdf.iloc[0].right_max_angle, 121.0)
        self.assertEqual(self.wdf.iloc[0].right_min_angle, 30.0)

        self.assertTrue(np.isnan(self.wdf.iloc[1].left_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].left_min_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_min_angle))

    def test_min_max_angles_columns_already_exist(self):
        self.wdf.add_polar_forces()
        self.wdf.add_min_max_angles()
        self.wdf.add_min_max_angles()

        self.assertEqual(self.wdf.iloc[0].left_max_angle, 129.0)
        self.assertTrue(np.isnan(self.wdf.iloc[1].left_max_angle))

    def test_min_max_angles_without_polar_forces(self):
        self.wdf.add_min_max_angles()

        self.assertTrue(np.isnan(self.wdf.iloc[0].left_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[0].left_min_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[0].right_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[0].right_min_angle))

        self.assertTrue(np.isnan(self.wdf.iloc[1].left_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].left_min_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_min_angle))

    def test_polar_plot(self):
        self.wdf.add_polar_forces()
        ax = self.wdf.plot.polar()
        self.assertTrue(ax.has_data)

    def test_process(self):
        wdf = models.WattbikeDataFrame(self.data)

        self.assertTrue(isinstance(wdf.iloc[0].power, str))
        self.assertTrue('_0' not in wdf.columns)
        self.assertTrue('left_max_angle' not in wdf.columns)

        wdf.process()

        self.assertTrue(isinstance(wdf.iloc[0].power, float))
        self.assertTrue('_0' in wdf.columns)
        self.assertTrue('left_max_angle' in wdf.columns)
        self.assertEqual(wdf.iloc[0]._0, 0.659439450026441)
        self.assertEqual(wdf.iloc[0].left_max_angle, 129.0)

    def _create_multi_user_session_wdf(self):
        wdf = self.wdf
        for i in range(5):
            wdf = wdf.append(self.wdf)
        wdf.reset_index

        wdf['session_id'] = [f'session_{i}' for i in range(4)] * 3
        wdf['user_id'] = [f'user_{i}' for i in range(2)] * 6
        return wdf

    def test_reduce_by_session(self):
        wdf = self._create_multi_user_session_wdf()
        reduced_wdf = wdf.reduce_by_session()

        self.assertEqual(len(reduced_wdf), 4)
        self.assertEqual(len(set(reduced_wdf.session_id)), 4)
        self.assertEqual(len(set(reduced_wdf.user_id)), 2)

    def test_reduce_by_user(self):
        wdf = self._create_multi_user_session_wdf()
        reduced_wdf = wdf.reduce_by_user()

        self.assertEqual(len(reduced_wdf), 2)
        self.assertEqual(len(set(reduced_wdf.user_id)), 2)
        self.assertTrue('session_id' not in reduced_wdf.columns)
