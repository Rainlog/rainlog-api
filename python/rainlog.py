"""
Functions for reading data from rainlog in Python.
Run `python python/rainlog.py` to get an example print out.
"""

import datetime
import json
import logging

import pandas as pd
import requests

RAINLOG_API_BASE = 'https://rainlog.org/api/'
RAINLOG_VERSIONED_API_BASE = RAINLOG_API_BASE + '1.0/'
RAINLOG_READING_GETFILTERED = RAINLOG_VERSIONED_API_BASE + 'Reading/getFiltered'
RAINLOG_GAUGE_GETFILTERED = RAINLOG_VERSIONED_API_BASE + 'Gauge/getFiltered'
RAINLOG_GAUGEREVISION_GETFILTERED = RAINLOG_VERSIONED_API_BASE + 'GaugeRevision/getFiltered'
RAINLOG_DEFAULT_HEADERS_NO_AUTH = {'content-type': 'application/json'}


CIRCLE_NEAR_UA = {
    "type": "Circle",
    "center": {'lat': 32.2133, 'lng': -110.9542},
    "radius": .1  # in miles
}

BOX_NEAR_UA = {
    "type": "Rectangle",
    "westLng": -111.0488008,
    "eastLng": -110.8488008,
    "northLat": 32.3332841,
    "southLat": 32.1332841,
}


# call the api, return the json, raises exception on error
def api_post(url, params):
    logging.info('Posting to %s with %s', url, json)
    r = requests.post(
        url,
        headers=RAINLOG_DEFAULT_HEADERS_NO_AUTH,
        json=params
    )
    r.raise_for_status()
    return r.content


def parse_date(datetimelike):
    # fairly robust to many formats: string, python date, datetime, and
    # pandas timestamps
    dt = pd.Timestamp(datetimelike)
    return dt.strftime('%Y-%m-%d')


def get_readings(date_range_start, date_range_end, region, limit=None):
    params = {
        'dateRangeStart': parse_date(date_range_start),
        'dateRangeEnd': parse_date(date_range_end),
        'region': region,
    }
    if limit:
        params['pagination'] = {'limit': 3}
    readings = api_post(RAINLOG_READING_GETFILTERED, params)
    return readings


def getReadingsFromFunnelGauges():
    params = {
        'dateRangeStart': yesterday,
        'dateRangeEnd': yesterday,
        'gaugeType': ['FunnelCatch', 'FunnelCatchWithOverflow'],
        'pagination': {'limit': 3}
    }

    readings = api_post(RAINLOG_READING_GETFILTERED, params)
    return json.dumps(readings, indent=3)


# gets readings recorded yesterday,
# then gets the associated gaugeRevision information
def getReadingsWithGaugeInfo():
    #convenience function to pull out gaugeRevisionId
    byRevisionId = lambda elem: elem['gaugeRevisionId']

    getReadingsParams = {
        'dateRangeStart': yesterday,
        'dateRangeEnd': yesterday,
        'gaugeType': ['FunnelCatch', 'FunnelCatchWithOverflow'],
        'pagination': {'limit': 3}
    }
    readings = apiPostNoAuth(RAINLOG_READING_GETFILTERED, getReadingsParams)

    getGaugeRevisionsParams = {
        'gaugeRevisionIds': list(map(byRevisionId, readings))
    }
    gaugeRevisions = api_post(RAINLOG_GAUGEREVISION_GETFILTERED, getGaugeRevisionsParams)

    # note that the API does no ordering - you will need to sort locally if you need that
    grouped = dict()
    for reading in readings:
        grouped[byRevisionId(reading)] = {'reading': reading}
    for gaugeRevision in gaugeRevisions:
        grouped[byRevisionId(gaugeRevision)]['gaugeRevision'] = gaugeRevision

    out = {key: json.dumps(value, indent=3) for key, value in grouped.items()}
    return out


def to_dataframe(json_bytes):
    """
    Convert API response to pandas DataFrame. Input must be in bytes.
    Do not call response.json() before passing in the data.
    """
    df = pd.read_json(json_bytes)
    return df


if __name__ == '__main__':
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    out = get_readings(yesterday, yesterday, BOX_NEAR_UA)
    out = to_dataframe(out)
    print(out)
