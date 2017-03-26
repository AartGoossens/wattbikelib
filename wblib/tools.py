import collections

import pandas as pd
import requests

from .constants import WATTBIKE_HUB_FILES_BASE_URL


def flatten(d, parent_key='', sep='_'):
    """
    Credits for this method to: http://stackoverflow.com/users/1897/imran
    Posted on http://stackoverflow.com/a/6027615
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def build_hub_files_url(user_id, session_id, extension='wbs'):
    return WATTBIKE_HUB_FILES_BASE_URL.format(
        user_id=user_id,
        session_id=session_id,
        extension=extension)

def polar_force_column_labels():
    return [f'_{i}' for i in range(361)]
