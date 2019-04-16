import datetime as dt
import math
import time

import requests

from .utils import to_dataframe


class AtlasTrendsQuery:

    def __init__(self, resource, msm_id, prb_id, start_dt=None, stop_dt=None, subresource=None):
        self.resource = resource
        self.subresource = subresource
        self.msm_id = msm_id
        self.prb_id = prb_id

        if stop_dt is None:
            stop_dt = dt.datetime.now()

        if start_dt is None:
            start_dt = stop_dt - dt.timedelta(days=7)

        self.start_dt = start_dt
        self.stop_dt = stop_dt

    def path(self):
        p = '/{}/{}/{}'.format(self.resource, self.msm_id, self.prb_id)
        if self.subresource != None:
            p = p + '/{}'.format(self.subresource)
        return p

    def params(self):
        return {
            'start': int(self.start_dt.timestamp()),
            'stop': int(self.stop_dt.timestamp())
        }

    def estimated_time(self):
        """
        Heuristic for estimating the response time of a query, in seconds.
        """
        if self.resource == 'ticks':
            k = 3150
        else:
            k = 450
        interval = dt.timedelta(minutes=4)
        t = 1 + (((self.stop_dt - self.start_dt) / interval) / k)
        return round(t, 1)


class AtlasTrendsClient:
    """
    Client for the RIPE Atlas Trends API.
    """

    DEFAULT_URL = 'https://trends.atlas.ripe.net/api/v1'

    def __init__(self, base_url=None, verbose=False):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = self.DEFAULT_URL
        self.verbose = verbose

    def get(self, query):
        """
        API Errors are raised as Python exceptions.
        """
        if self.verbose:
            print('Estimated query time: {}s'.format(query.estimated_time()))
        wall_time = time.time()
        res = requests.get(self.base_url + query.path(), params=query.params())
        query_time = time.time() - wall_time
        if self.verbose:
            print('Actual query time: {}s'.format(round(query_time, 1)))
        obj = res.json()
        if res.status_code != 200:
            raise ValueError(obj['message'])
        return obj

    def fetch_ticks(self, msm_id, prb_id, start_dt=None, stop_dt=None, as_df=False):
        query = AtlasTrendsQuery('ticks', msm_id, prb_id, start_dt, stop_dt)
        res = self.get(query)
        if as_df:
            return to_dataframe(res)
        else:
            return res

    def fetch_trends(self, msm_id, prb_id, start_dt=None, stop_dt=None, as_df=False):
        query = AtlasTrendsQuery('trends', msm_id, prb_id, start_dt, stop_dt)
        res = self.get(query)
        if as_df:
            return to_dataframe(res)
        else:
            return res

    def fetch_summary(self, msm_id, prb_id, start_dt=None, stop_dt=None):
        query = AtlasTrendsQuery(
            'trends', msm_id, prb_id, start_dt, stop_dt, 'summary')
        return self.get(query)
