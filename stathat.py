# -*- coding: utf-8 -*-

"""
stathat.py
~~~~~~~~~~

A minimalistic API wrapper for StatHat.com, powered by Requests.

Usage::

    >>> from stathat import StatHat
    >>> stats = StatHat('me@kennethreitz.com')
    >>> stats.count('wtfs/minute', 10)
    True
    >>> stats.count('connections.active', 85092)
    True

Enjoy.

"""

import requests

DEFAULT_STATHAT_URL = 'https://api.stathat.com'


class StatHat(object):
    """The StatHat API wrapper."""

    STATHAT_URL = DEFAULT_STATHAT_URL

    def __init__(self, email=None):
        self.email = email

        # Enable keep-alive and connection-pooling.
        self.session = requests.session()

    def _http_post(self, path, data):
        """
        Make HTTP Post to EZ API

        Payload structure example:
        {
            "ezkey": "XXXYYYZZZ",
            "data": [
                {"stat": "page view", "count": 2},
            ]
        }
        """
        url = self.STATHAT_URL + path
        headers = {'content_type': 'application/json'}
        payload = {
            'ezkey': self.email,
            'data': [data]
        }
        r = self.session.post(url, json=payload, headers=headers)
        return r

    def value(self, key, value, timestamp=None):
        data = {'stat': key, 'value': value}
        if timestamp:
            data['t'] = timestamp
        r = self._http_post('/ez', data)
        return r.ok

    def count(self, key, count, timestamp=None):
        data = {'stat': key, 'count': count}
        if timestamp:
            data['t'] = timestamp
        r = self._http_post('/ez', data)
        return r.ok
