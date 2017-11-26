import datetime
from unittest import TestCase, mock

import numpy as np
import pandas as pd
from vcr_setup import custom_vcr

from wblib import models


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
            'cadence': '52.1739',
            'user_id': 'u-1756bbba7e2a350'
        }]
        wdf = models.WattbikeDataFrame(self.data * 60)
        wdf._process(wdf)
        self.wfpm = models.WattbikeFramePlotMethods(wdf)

    def test_polar(self):
        ax = self.wfpm.polar()
        self.assertTrue(ax.has_data)

    def test_polar_full(self):
        ax = self.wfpm.polar(full=True)
        self.assertTrue(ax.has_data)

    def test_polar_propagate_plot_arguments(self):
        ax = self.wfpm.polar(color='r')
        self.assertTrue(ax.has_data)

    def test_polar_linewidth(self):
        ax = self.wfpm.polar(linewidth=1)
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
            'cadence': '52.1739',
            'user_id': 'u-1756bbba7e2a350'
            },
            {'speed': '30.7822',
            'distance': '9.8332',
            'power': '121.4584',
            'time': '1.1500',
            'force': '130.7665',
            'balance': '58.5158',
            'heartrate': '100.0000',
            'cadence': '52.1739',
            'user_id': 'u-1756bbba7e2a350'
            }
            ]
        self.wdf = models.WattbikeDataFrame(self.data)
        self.wdf = self.wdf._process(self.wdf)
        # self.wdf._columns_to_numeric()

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

        wdf_2 = wdf._columns_to_numeric()
        self.assertEqual(wdf.balance.dtype.name, 'float64')
        self.assertEqual(wdf.polar_cnt.dtype.name, 'float64')
        self.assertEqual(wdf.polar_force.dtype.name, 'object')
        self.assertIsNotNone(wdf_2)

    def test_add_polar_forces(self):
        wdf_2 = self.wdf._add_polar_forces()
        self.assertIsNotNone(wdf_2)
        self.assertTrue('_0' in self.wdf.columns)
        self.assertTrue('_359' in self.wdf.columns)
        self.assertIsInstance(self.wdf.loc[0, '_0'], float)
        self.assertEqual(self.wdf.loc[0, '_0'], 0.659439450026441)

    def test_add_polar_forces_columns_already_exist(self):
        self.wdf._add_polar_forces()
        wdf_2 = self.wdf._add_polar_forces()
        self.assertTrue('_0' in self.wdf.columns)
        self.assertTrue('_359' in self.wdf.columns)
        self.assertIsInstance(self.wdf.loc[0, '_0'], float)
        self.assertEqual(self.wdf.loc[0, '_0'], 0.659439450026441)

    def test_min_max_angles(self):
        wdf = models.WattbikeDataFrame(self.data * 60)
        wdf._add_polar_forces()
        self.assertFalse('left_max_angle' in wdf.columns)
        wdf._add_min_max_angles()

        self.assertTrue('left_max_angle' in wdf.columns)
        self.assertTrue('left_min_angle' in wdf.columns)
        self.assertTrue('right_max_angle' in wdf.columns)
        self.assertTrue('right_min_angle' in wdf.columns)

        self.assertEqual(wdf.iloc[0].left_max_angle, 129.0)
        self.assertEqual(wdf.iloc[0].left_min_angle, 22.0)
        self.assertEqual(wdf.iloc[0].right_max_angle, 121.0)
        self.assertEqual(wdf.iloc[0].right_min_angle, 30.0)

        self.assertTrue(np.isnan(wdf.iloc[1].left_max_angle))
        self.assertTrue(np.isnan(wdf.iloc[1].left_min_angle))
        self.assertTrue(np.isnan(wdf.iloc[1].right_max_angle))
        self.assertTrue(np.isnan(wdf.iloc[1].right_min_angle))

    def test_min_max_angles_columns_already_exist(self):
        self.wdf._add_polar_forces()
        self.wdf._add_min_max_angles()
        self.wdf._add_min_max_angles()

        self.assertEqual(self.wdf.iloc[0].left_max_angle, 129.0)
        self.assertTrue(np.isnan(self.wdf.iloc[1].left_max_angle))

    def test_min_max_angles_without_polar_forces(self):
        self.wdf._add_min_max_angles()

        self.assertFalse(np.isnan(self.wdf.iloc[0].left_max_angle))
        self.assertFalse(np.isnan(self.wdf.iloc[0].left_min_angle))
        self.assertFalse(np.isnan(self.wdf.iloc[0].right_max_angle))
        self.assertFalse(np.isnan(self.wdf.iloc[0].right_min_angle))

        self.assertTrue(np.isnan(self.wdf.iloc[1].left_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].left_min_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_max_angle))
        self.assertTrue(np.isnan(self.wdf.iloc[1].right_min_angle))

    def test_polar_plot(self):
        self.wdf._add_polar_forces()
        ax = self.wdf.plot.polar()
        self.assertTrue(ax.has_data)

    def test_process(self):
        wdf = models.WattbikeDataFrame(self.data)

        self.assertTrue(isinstance(wdf.iloc[0].power, str))
        self.assertTrue('_0' not in wdf.columns)
        self.assertTrue('left_max_angle' not in wdf.columns)

        wdf = wdf._process(wdf)

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
        wdf['user_id'] = ['u-1756bbba7e2a350', 'u-1656bbbb46272a5'] * 6
        return wdf

    def test_average_by_session(self):
        wdf = self._create_multi_user_session_wdf()
        averaged_wdf = wdf.average_by_session()

        self.assertEqual(len(averaged_wdf), 4)
        self.assertEqual(len(set(averaged_wdf.session_id)), 4)
        self.assertEqual(len(set(averaged_wdf.user_id)), 2)

    def test_average_by_user(self):
        wdf = self._create_multi_user_session_wdf()
        averaged_wdf = wdf.average_by_user()

        self.assertEqual(len(averaged_wdf), 2)
        self.assertEqual(len(set(averaged_wdf.user_id)), 2)
        self.assertTrue('session_id' not in averaged_wdf.columns)

    def test_enrich_with_athlete_performance_state(self):
        wdf = self._create_multi_user_session_wdf()
        wdf = wdf._enrich_with_athlete_performance_state(wdf)
        self.assertEqual(wdf.iloc[0].percentage_of_ftp, 121.4584/323)
        self.assertEqual(wdf.iloc[1].percentage_of_ftp, 121.4584/321)
        self.assertEqual(wdf.iloc[0].percentage_of_mmp, 121.4584/453)
        self.assertEqual(wdf.iloc[1].percentage_of_mmp, 121.4584/450)
        self.assertEqual(wdf.iloc[0].percentage_of_mhr, 100.0/200)
        self.assertEqual(wdf.iloc[1].percentage_of_mhr, 100.0/195)

    def test_enrich_with_athlete_performance_state_without_heartrate(self):
        wdf = self._create_multi_user_session_wdf()
        del wdf['heartrate']
        wdf = wdf._enrich_with_athlete_performance_state(wdf)
        self.assertTrue(np.isnan(wdf.iloc[0].percentage_of_mhr))
        self.assertTrue(np.isnan(wdf.iloc[1].percentage_of_mhr))

    @mock.patch('wblib.client.WattbikeHubClient.get_session')
    @mock.patch('wblib.models.WattbikeDataFrame._raw_session_to_wdf')
    def test_load(self, mock_raw, mock_get_session):
        mock_get_session.return_value = ('session_data', 'ride_session')
        mock_raw.return_value = models.WattbikeDataFrame([1])
        wdf = models.WattbikeDataFrame()
        wdf = wdf.load('i6LY60PUyH')
        mock_get_session.assert_called_once_with('i6LY60PUyH')
        mock_raw.assert_called_once_with('session_data', 'ride_session')
    
    @mock.patch('wblib.client.WattbikeHubClient.get_session')
    @mock.patch('wblib.models.WattbikeDataFrame._raw_session_to_wdf')
    def test_load_multiple(self, mock_raw, mock_get_session):
        mock_get_session.return_value = ('session_data', 'ride_session')
        mock_raw.return_value = models.WattbikeDataFrame([1])
        wdf = models.WattbikeDataFrame()
        wdf = wdf.load(['i6LY60PUyH', '8lQVvY2bEG'])
        self.assertEqual(mock_get_session.call_count, 2)
        self.assertEqual(mock_raw.call_count, 2)

    @mock.patch('wblib.client.WattbikeHubClient.get_sessions_for_user')
    @mock.patch('wblib.models.WattbikeDataFrame._raw_session_to_wdf')
    def test_load_for_user(self, mock_raw, mock_get_sessions):
        mock_get_sessions.return_value = [('session_data', 'ride_session')]
        mock_raw.return_value = models.WattbikeDataFrame([1])
        wdf = models.WattbikeDataFrame()
        self.assertEqual(len(wdf), 0)
        wdf = wdf.load_for_user('u-1756bbba7e2a350')
        mock_get_sessions.assert_called_once_with(
            user_id='u-1756bbba7e2a350',
            after=None,
            before=None
        )
        mock_raw.assert_called_once_with('session_data', 'ride_session')
        self.assertEqual(len(wdf), 1)

    @mock.patch('wblib.client.WattbikeHubClient.get_sessions_for_user')
    @mock.patch('wblib.models.WattbikeDataFrame._raw_session_to_wdf')
    def test_load_for_user_multiple(self, mock_raw, mock_get_sessions):
        mock_get_sessions.return_value = [('session_data', 'ride_session')]
        mock_raw.return_value = models.WattbikeDataFrame([1])
        wdf = models.WattbikeDataFrame()
        wdf = wdf.load_for_user(['u-1756bbba7e2a350'])
        mock_get_sessions.assert_called_once_with(
            user_id='u-1756bbba7e2a350',
            after=None,
            before=None
        )
        mock_raw.assert_called_once_with('session_data', 'ride_session')

    @mock.patch('wblib.models.WattbikeDataFrame._process')
    def test_raw_session_to_wdf(self, mock_process):
        session_data = dict(
            laps=[dict(
                data=[dict(
                    heartrate=123,
                    power=234,
                    cadence=345,
                    time=456
                )]
            )]
        )
        ride_session = mock.Mock()
        ride_session.get_user_id = lambda: 'user_id'
        ride_session.get_session_id = lambda: 'session_id'

        wdf = models.WattbikeDataFrame()
        wdf = wdf._raw_session_to_wdf(session_data, ride_session)

        self.assertEqual(wdf.heartrate.iloc[0], 123)
        self.assertEqual(wdf.power.iloc[0], 234)
        self.assertEqual(wdf.cadence.iloc[0], 345)
        self.assertEqual(wdf.time.iloc[0], 456)
        self.assertEqual(wdf.session_id.iloc[0], 'session_id')
        self.assertEqual(wdf.user_id.iloc[0], 'user_id')
