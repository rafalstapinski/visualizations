import web
import requests
import helpers as Help
import json
import pickle
import arrow
import datetime
import psycopg2

class Collect:

    @staticmethod
    def tile(x, y, zoom = 3):

        db = Help.DB.connect()

        processed = arrow.get(datetime.datetime.utcnow()).timestamp

        base_url = Help.Config.get('air-traffic/base_url')
        user_key = Help.Config.get('air-traffic/user_key')

        url = base_url % (zoom, x, y)

        params = {
            'user_key': user_key,
            'format': 'json'
        }

        r = requests.get(url, params = params)

        # data = json.loads(r.text)

        print r
        data = json.loads(r.text)

        for feature in data['features']:

            _id = feature['id']

            lat = feature['geometry']['coordinates'][0]
            lng = feature['geometry']['coordinates'][1]

            if 'altitude' in feature['properties']['positionReport']:
                altitude = feature['properties']['positionReport']['altitude']
            else:
                altitude = None

            if 'track' in feature['properties']['positionReport']:
                track = feature['properties']['positionReport']['track']
            else:
                track = None

            capture = arrow.get(
                feature['properties']['positionReport']['captureTimestamp']
            ).timestamp

            status = feature['properties']['flightStatus']

            if 'callsign' in feature['properties']:
                callsign = feature['properties']['callsign']
            else:
                callsign = None

            if 'airline' in feature['properties']:
                airline = feature['properties']['airline']
            else:
                airline = None

            if 'departure' in feature['properties']:

                try:
                    departure = arrow.get(
                        feature['properties']['departure']['runwayTime']['actual']
                    ).timestamp

                    in_air = capture - departure

                except KeyError:

                    try:
                        departure = arrow.get(
                            feature['properties']['departure']['runwayTime']['extimate']
                        ).timestamp

                        in_air = capture - departure

                    except KeyError:
                        in_air = None

            else:
                in_air = None

            if 'source' in feature['properties']['positionReport']:
                source = feature['properties']['positionReport']['source']
            else:
                source = None

            try:
                db.insert('air_traffic',
                    flight_id = _id,
                    lat = lat,
                    lng = lng,
                    alt = altitude,
                    track = track,
                    capture = capture,
                    processed = processed,
                    status = status,
                    callsign = callsign,
                    in_air = in_air,
                    airline = airline,
                    source = source
                )
            except psycopg2.IntegrityError, e:
                print e

        # # print url
        #
        # r = requests.get(url, params = params)
        #
        # data = json.loads(r.text)
        #
        # pickle.dump(data, open('test.p', 'wb'))
        #
        # db = Help.DB.connect()
