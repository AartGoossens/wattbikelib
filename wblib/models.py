import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.core.accessor import AccessorProperty
import pandas.plotting._core as gfx

from .client import WattbikeHubClient
from .tools import polar_force_column_labels, flatten


class WattbikeFramePlotMethods(gfx.FramePlotMethods):
    polar_angles = np.arange(90, 451) / (180 / np.pi)
    polar_force_columns = polar_force_column_labels()

    def _plot_single_polar(self, ax, polar_forces, mean):
        if mean:
            linewidth = 3
            color = '#5480C7'
        else:
            linewidth = 0.5
            color = '#BDBDBD'

        ax.plot(self.polar_angles, polar_forces, color, linewidth=linewidth)

    def polar(self, full=False, mean=True):
        ax = plt.subplot(111, projection='polar')

        if full:
            for i in range(0, len(self._data) - 50, 50):
                forces = self._data.iloc[i:i + 50, self._data.columns.get_indexer(self.polar_force_columns)].mean()
                self._plot_single_polar(ax, forces, mean=False)

        if mean:
            forces = self._data[self.polar_force_columns].mean()
            self._plot_single_polar(ax, forces, mean=True)

        xticks_num = 8
        xticks = np.arange(0, xticks_num, 2 * np.pi / xticks_num)
        ax.set_xticks(xticks)
        rad_to_label = lambda i: '{}°'.format(int(i / (2 * np.pi) * 360 - 90) % 180)
        ax.set_xticklabels([rad_to_label(i) for i in xticks])
        ax.set_yticklabels([])

        return ax


class WattbikeDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return WattbikeDataFrame

    def load(self, session_id):
        client = WattbikeHubClient()
        if not isinstance(session_id, list):
            session_id = [session_id]

        for session in session_id:
            session_data, ride_session = client.get_session(session)
            wdf = self._raw_session_to_wdf(session_data, ride_session)
            self = self.append(wdf)

        return self

    def load_for_user(self, user_id, before=None, after=None):
        client = WattbikeHubClient()
        if not isinstance(user_id, list):
            user_id = [user_id]
        
        for ID in user_id:
            sessions = client.get_sessions_for_user(
                user_id=ID, before=before, after=after
            )
            for session_data, ride_session in sessions:
                wdf = self._raw_session_to_wdf(session_data, ride_session)
                self = self.append(wdf)
        return self

    def _raw_session_to_wdf(self, session_data, ride_session):
        wdf = WattbikeDataFrame(
            [flatten(rev) for lap in session_data['laps'] for rev in lap['data']])

        wdf['time'] = wdf.time.cumsum()
        wdf['user_id'] = ride_session.get_user_id()
        wdf['session_id'] = ride_session.get_session_id()
        self._process(wdf)

        return wdf

    def _process(self, wdf):
        wdf = wdf._columns_to_numeric()
        wdf = wdf._add_polar_forces()
        wdf = wdf._add_min_max_angles()
        wdf = self._enrich_with_athlete_performance_state(wdf)

        return wdf

    def _columns_to_numeric(self):
        for col in self.columns:
            try:
                self.iloc[:, self.columns.get_loc(col)] = pd.to_numeric(self.iloc[:, self.columns.get_loc(col)])
            except ValueError:
                continue

        return self

    def _add_polar_forces(self):
        _df = pd.DataFrame()
        new_angles = np.arange(0.0, 361.0)
        column_labels = polar_force_column_labels()

        if not '_0' in self.columns:
            for label in column_labels:
                self[label] = np.nan

        for index, pf in self.polar_force.iteritems():
            if not isinstance(pf, str):
                continue

            forces = [int(i) for i in pf.split(',')]
            forces = np.array(forces + [forces[0]])
            forces = forces/np.mean(forces)

            angle_dx = 360.0 / (len(forces)-1)

            forces_interp = np.interp(
                x=new_angles,
                xp=np.arange(0, 360.01, angle_dx),
                fp=forces)

            _df[index] = forces_interp

        _df['angle'] = column_labels
        _df.set_index('angle', inplace=True)
        _df = _df.transpose()

        for angle in column_labels:
            self[angle] = _df[angle]

        return self
    
    def _add_min_max_angles(self):
        # @TODO this method is quite memory inefficient. Row by row calculation is better
        pf_columns = polar_force_column_labels()
        pf_T = self.loc[:, pf_columns].transpose().reset_index(drop=True)

        left_max_angle = pf_T.iloc[:180].idxmax()
        right_max_angle = pf_T.iloc[180:].idxmax() - 180
        
        left_min_angle = pd.concat([pf_T.iloc[:135], pf_T.iloc[315:]]).idxmin()
        right_min_angle = pf_T.iloc[135:315].idxmin() - 180

        self['left_max_angle'] = pd.DataFrame(left_max_angle)
        self['right_max_angle'] = pd.DataFrame(right_max_angle)
        self['left_min_angle'] = pd.DataFrame(left_min_angle)
        self['right_min_angle'] = pd.DataFrame(right_min_angle)

        return self

    def _enrich_with_athlete_performance_state(self, wdf):
        if not hasattr(self, 'peformance_states'):
            self.performance_states = {}

        percentage_of_mhr = []
        percentage_of_mmp = []
        percentage_of_ftp = []

        for index, row in wdf.iterrows():
            if row.user_id not in self.performance_states:
                self.performance_states[row.user_id] = \
                    WattbikeHubClient().get_user_performance_state(row.user_id)

            ps = self.performance_states[row.user_id]

            percentage_of_mmp.append(row.power/ps.get_max_minute_power())
            percentage_of_ftp.append(row.power/ps.get_ftp())
            try:
                percentage_of_mhr.append(row.heartrate/ps.get_max_hr())
            except AttributeError:
                percentage_of_mhr.append(np.nan)

        wdf['percentage_of_mhr'] = percentage_of_mhr
        wdf['percentage_of_mmp'] = percentage_of_mmp
        wdf['percentage_of_ftp'] = percentage_of_ftp

        return wdf

    def average_by_session(self):
        averaged = self._average_by_column('session_id')
        averaged['user_id'] = averaged.session_id.apply(
            lambda x: self.loc[self.session_id == x].iloc[0].user_id)
        return averaged

    def average_by_user(self):
        return self._average_by_column('user_id')

    def _average_by_column(self, column_name):
        averaged_self = self.groupby(column_name).mean().reset_index()
        return WattbikeDataFrame(averaged_self)


WattbikeDataFrame.plot = AccessorProperty(WattbikeFramePlotMethods,
        WattbikeFramePlotMethods)
