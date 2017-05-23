import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.core.base import AccessorProperty
from pandas.tools.plotting import FramePlotMethods

from .constants import WATTBIKE_HUB_FILES_BASE_URL
from .exceptions import RideSessionException
from .tools import build_hub_files_url, polar_force_column_labels


class RideSessionResponseModel:
    def __init__(self, data):
        self._validate(data)
        self.sessions = [RideSessionModel(s) for s in data['results']]

    def _validate(self, response):
        sessions = response['results']
        if not len(sessions):
            raise RideSessionException('No results returned')


class RideSessionModel(dict):
    def get_user_id(self):
        return self['user']['objectId']
    
    def get_session_id(self):
        return self['objectId']
    
    def _build_url(self, extension):
        return build_hub_files_url(
            user_id=self.get_user_id(),
            session_id=self.get_session_id(),
            extension=extension)

    def get_tcx_url(self):
        return self._build_url('tcx')

    def get_wbs_url(self):
        return self._build_url('wbs')

    def get_wbsr_url(self):
        return self._build_url('wbsr')


class LoginResponseModel(dict):
    def get_user_id(self):
        return self['objectId']

    def get_session_token(self):
        return self['sessionToken']


class WattbikeFramePlotMethods(FramePlotMethods):
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
                forces = self._data.ix[i:i + 50, self.polar_force_columns].mean()
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

    def plot_polar_view(self):
        raise NotImplementedError

    def columns_to_numeric(self):
        for col in self.columns:
            try:
                self.ix[:, col] = pd.to_numeric(self.ix[:, col])
            except ValueError:
                continue

        return self

    def add_polar_forces(self):
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
    
    def add_min_max_angles(self):
        # @TODO this method is quite memory inefficient. Row by row calculation is better
        pf_columns = polar_force_column_labels()
        pf_T = self.ix[:, pf_columns].transpose().reset_index(drop=True)

        left_max_angle = pf_T.ix[:180].idxmax()
        right_max_angle = pf_T.ix[180:].idxmax() - 180
        
        left_min_angle = pd.concat([pf_T.ix[:135], pf_T.ix[315:]]).idxmin()
        right_min_angle = pf_T.ix[135:315].idxmin() - 180

        self['left_max_angle'] = pd.DataFrame(left_max_angle)
        self['right_max_angle'] = pd.DataFrame(right_max_angle)
        self['left_min_angle'] = pd.DataFrame(left_min_angle)
        self['right_min_angle'] = pd.DataFrame(right_min_angle)

        return self

    def process(self):
        self.columns_to_numeric()
        self.add_polar_forces()
        self.add_min_max_angles()

        return self

    def _average_by_column(self, column_name):
        averaged_self = self.groupby(column_name).mean().reset_index()
        return WattbikeDataFrame(averaged_self)

    def average_by_session(self):
        averaged = self._average_by_column('session_id')
        averaged['user_id'] = averaged.session_id.apply(
            lambda x: self.loc[self.session_id == x].iloc[0].user_id)
        return averaged

    def average_by_user(self):
        return self._average_by_column('user_id')

WattbikeDataFrame.plot = AccessorProperty(WattbikeFramePlotMethods,
        WattbikeFramePlotMethods)
