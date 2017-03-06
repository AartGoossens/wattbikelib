import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .constants import WATTBIKE_HUB_FILES_BASE_URL
from .exceptions import RideSessionException
from .tools import build_hub_files_url


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
        column_labels = ['_{}'.format(int(i)) for i in new_angles]

        if not '_0' in self.columns:
            for label in column_labels:
                self[label] = np.nan

        for index, pf in self.polar_force.iteritems():
            if not isinstance(pf, str):
                continue

            forces = [int(i) for i in pf.split(',')]
            forces = np.array(forces + [forces[0]])
            forces = forces/np.median(forces)

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
    
    def polar_plot(self):
        ax = plt.subplot(111, projection='polar')

        polar_force_columns = ['_{}'.format(i) for i in range(361)]
        mean_polar_forces = self[polar_force_columns].mean()
        polar_angles = np.arange(90, 451) / (180 / np.pi)
        ax.plot(polar_angles, mean_polar_forces)

        xticks_num = 8
        xticks = np.arange(0, xticks_num, 2 * np.pi / xticks_num)
        ax.set_xticks(xticks)
        rad_to_label = lambda i: '{}°'.format(int(i / (2 * np.pi) * 360 - 90) % 180)
        ax.set_xticklabels([rad_to_label(i) for i in xticks])
        ax.set_yticklabels([])

        return ax
