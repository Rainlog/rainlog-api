# rainlog-api

The public Rainlog API is defined in OpenAPI 3.0 and is viewable in a user-friendly way at Swaggerhub:
https://app.swaggerhub.com/apis/rainlog/rainlog/1.0.0

The public API is a minimal RESTful JSON API designed to return hundreds of data elements per call. Typical "CRUD" verbs are not used. All http interactions must occur through https POST requests.

The primary workhorse for getting daily reading data is the Reading/getFiltered call. It is capable of filtering by many types of criteria. The GaugeRevision/getFiltered call can provide information about gauges at the time of the reading.

The server limits request results to 1000 results per request. If this is an issue for you, you can work around it by using the pagination field. After each call, increase the offset by your limit and repeat until no results are returned.

## Types
For more detailed information about fields, see the OpenAPI spec.

### Gauge
Essentially an identifier with a name, used to link multiple GaugeRevisions together.

### GaugeRevision
Whenever a user creates or modifies a gauge a new GaugeRevision is created. This allows a user to swap out the physical gauge and provide new information about it, but still retain related history.

### Reading
A daily reading of rain accumulated from 7am to 7am the next day. Note the associated date is the date the *reading was taken*, meaning the reading reaches back about 24 hours from the readingDate field.

### MonthReading
A legacy type of reading for an entire month's worth of rain. There are very few readings of this type and the future of this type is unclear. It is not recommended for use.

## Examples

In addition to these descriptive examples, there are bash (curl) and python examples in their respective folders.

### Get all readings from a day:  
POST /Reading/getFiltered  
```json
{
  "dateRangeStart": "2018-02-27",
  "dateRangeEnd": "2018-02-27",
}
```

### Get all Good or Trace readings from a day, in a circular region
POST /Reading/getFiltered
```json
{
  "dateRangeStart": "2018-02-27",
  "dateRangeEnd": "2018-02-27",
  "quality": ["Good", "Trace"],
  "region": {
    "type": "Circle",
    "center": {
      "lat": 32.1,
      "lng": -111.4
    },
    "radius": 1.2,
  }
}
```

### Get GaugeRevisions, then Readings created by them

Get all funnel or cylinder GaugeRevisions that have ever existed in a rectangular region:  
POST /GaugeRevision/getFiltered  
```json
{
  "gaugeType":["FunnelCatch", "SimpleCylinderRectangularCatch"],
  "region": {
    "type": "Rectangle",
    "westLng": -112,
    "eastLng": -111,
    "northLat": 25,
    "southLat": 35,
  }
}
```

Now you will have a bunch of gauges with their attributes, but lets say you want their readings from January:  
POST /Reading/getFiltered
```json
{
  "gaugeRevisionIds": [304, 355, 549, 2301, ..., 8574, 9204], /*Copy the ID's in*/
  "dateRangeStart": "2018-01-01",
  "dateRangeEnd": "2018-01-31"
}
```


## Data returned

### An array of Readings:
```json
[
  {
    "readingId": 0,
    "gaugeId": 0,
    "gaugeRevisionId": 0,
    "remarks": "",
    "readingDate": "1999-02-25",
    "readingHour": 7,
    "readingMinute": 0,
    "quality": "Good",
    "rainAmount": 0,
    "snowDepth": null,
    "snowAccumulation": null
  },
  {
    "readingId": 1,
    "gaugeId": 1,
    "gaugeRevisionId": 1,
    "remarks": "",
    "readingDate": "1999-02-25",
    "readingHour": 7,
    "readingMinute": 0,
    "quality": "Trace",
    "rainAmount": 0,
    "snowDepth": null,
    "snowAccumulation": null
  },
  ...
]
```

### An array of GaugeRevisions:
```json
[
  {
    "gaugeRevisionId": 0,
    "gaugeId": 0,
    "createdDate": "1999-02-25",
    "brand": "AccuGauge",
    "model": "AccuGauge 2000",
    "description": "On South side of house",
    "position": {
      "lat": 0,
      "lng": 0
    },
    "gaugeType": "TruCheckWedge",
    "gaugeTypeOther": null
  },
  {
    "gaugeRevisionId": 1,
    "gaugeId": 1,
    "createdDate": "1999-02-25",
    "brand": "AccuGauge",
    "model": "AccuGauge 2000",
    "description": "On South side of house",
    "position": {
      "lat": 0,
      "lng": 0
    },
    "gaugeType": "TruCheckWedge",
    "gaugeTypeOther": null
  },
  ...
]
```
