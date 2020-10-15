#/bin/bash
wait_for_keypress() {
    echo
    echo "Next operation: $1. Press any key to continue."
    read -n 1 -s
    clear
    echo "Operation: $1"
    echo "==============================================="
}

wait_for_keypress "Reading/getFiltered"
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "dateRangeStart":"2000-01-01",
           "dateRangeEnd":"2015-01-05",
	         "region": {
             "type": "Circle",
             "center": {"lat": 32, "lng": -111},
             "radius": 3.0
           },
           "quality": ["Good", "Trace", "Snow"],
           "pagination": {"offset":0, "limit": 3}
        }' \
     -v https://rainlog.org/api/1.0/Reading/getFiltered

wait_for_keypress "GaugeRevision/getFiltered"
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "dateRangeStart":"2000-01-01",
           "dateRangeEnd":"2015-01-05",
           "pagination": {"offset":0, "limit": 3}
        }' \
     -v https://rainlog.org/api/1.0/GaugeRevision/getFiltered

wait_for_keypress "Gauge/getFiltered"
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "dateRangeStart":"2000-01-01",
           "dateRangeEnd":"2015-01-05",
           "pagination": {"offset":0, "limit": 3}
        }' \
     -v https://rainlog.org/api/1.0/Gauge/getFiltered
