import requests
import datetime
import json

RAINLOG_API_BASE                  = 'https://rainlog.org/api/';
RAINLOG_VERSIONED_API_BASE        = RAINLOG_API_BASE + '1.0/';
RAINLOG_READING_GETFILTERED       = RAINLOG_VERSIONED_API_BASE + 'Reading/getFiltered';
RAINLOG_GAUGE_GETFILTERED         = RAINLOG_VERSIONED_API_BASE + 'Gauge/getFiltered';
RAINLOG_GAUGEREVISION_GETFILTERED = RAINLOG_VERSIONED_API_BASE + 'GaugeRevision/getFiltered';
RAINLOG_DEFAULT_HEADERS_NO_AUTH   = {'content-type': 'application/json'};

def simpleDate(date):
    return date.isoformat()[:10];

yesterday = simpleDate(datetime.datetime.now() - datetime.timedelta(1));

# call the api, return the json, raises exception on error
def apiPostNoAuth(url, json):
    print('Posting to ' + url, 'with', json);
    response = requests.post(
        url,
        headers = RAINLOG_DEFAULT_HEADERS_NO_AUTH,
        json = json
    );

    if response.status_code != requests.codes.ok:
        raise Exception('Request failed.' + request.data());
    return response.json();

def getReadingsNearUA():
    # radius is in miles
    region = {
        "type": "Circle",
        "center": {'lat': 32.2332841, 'lng':-110.9488008},
        "radius": 3.0
    };

    # instead, we could use a rectangle
    # region = {
    #     "type": "Rectangle",
    #     "westLng": -111.0488008,
    #     "eastLng": -110.8488008,
    #     "northLat": 32.3332841,
    #     "southLat": 32.1332841,
    # };

    params = {
        'dateRangeStart': yesterday,
        'dateRangeEnd': yesterday,
        'region': region,
        'pagination': {'limit': 3}
    };
    readings = apiPostNoAuth(RAINLOG_READING_GETFILTERED, params);
    print(json.dumps(readings, indent=3));

def getReadingsFromFunnelGauges():
    params = {
        'dateRangeStart': yesterday,
        'dateRangeEnd': yesterday,
        'gaugeType': ['FunnelCatch', 'FunnelCatchWithOverflow'],
        'pagination': {'limit': 3}
    }

    readings = apiPostNoAuth(RAINLOG_READING_GETFILTERED, params);
    print(json.dumps(readings, indent=3));

# gets readings recorded yesterday, then gets the associated gaugeRevision information
def getReadingsWithGaugeInfo():
    #convenience function to pull out gaugeRevisionId
    byRevisionId = lambda elem: elem['gaugeRevisionId'];

    getReadingsParams = {
        'dateRangeStart': yesterday,
        'dateRangeEnd': yesterday,
        'gaugeType': ['FunnelCatch', 'FunnelCatchWithOverflow'],
        'pagination': {'limit': 3}
    };
    readings = apiPostNoAuth(RAINLOG_READING_GETFILTERED, getReadingsParams);

    getGaugeRevisionsParams = {
        'gaugeRevisionIds': list(map(byRevisionId, readings))
    };
    gaugeRevisions = apiPostNoAuth(RAINLOG_GAUGEREVISION_GETFILTERED, getGaugeRevisionsParams);

    # note that the API does no ordering - you will need to sort locally if you need that
    grouped = dict();
    for reading in readings:
        grouped[byRevisionId(reading)] = {'reading': reading};
    for gaugeRevision in gaugeRevisions:
        grouped[byRevisionId(gaugeRevision)]['gaugeRevision'] = gaugeRevision;

    for key, value in grouped.items():
        print(json.dumps(value, indent=3));

print('=======================================');
print('= Rainlog read-only API example usage =');
print('=======================================');

calls = [getReadingsNearUA, getReadingsFromFunnelGauges, getReadingsWithGaugeInfo];
for call in calls:
    print();
    print('==================================================');
    print(call);
    print('==================================================');
    call();
    input("Press Enter to continue...");
