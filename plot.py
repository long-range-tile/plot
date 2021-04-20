import sys

import json
import staticmaps
import datetime

def timestamp_to_datetime_bt(ts):
    return datetime.datetime.fromtimestamp(ts / 1000000000.0)

def timestamp_to_datetime_gps(ts):
    return datetime.datetime.fromtimestamp(ts / 1000.0)

def plot(gps_txt):
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)

    gps_objs = []

    with open(gps_txt, 'r') as f:
        for line in f.readlines():
            loaded = json.loads(line)
            coords = loaded['coords']
            latitude = coords['latitude']
            longitude = coords['longitude']
            latlng = staticmaps.create_latlng(latitude, longitude)
            marker = staticmaps.Marker(latlng, size=5)
            context.add_object(marker)
            timestamp = loaded['timestamp']
            ts = timestamp_to_datetime_gps(timestamp)
            gps_objs.append({
                'ts': ts,
                'latitude': latitude,
                'longitude': longitude,
            })

    i = 0
    with open('bt-2.txt', 'r') as f:
        for line in f.readlines():
            i += 1
            print('progress:', i)
            loaded = json.loads(line)
            timestamp = loaded['Timestamp']
            ts = timestamp_to_datetime_bt(timestamp)
            last = None
            current = None
            found = None
            for gps_obj in gps_objs:
                if gps_obj['ts'] > ts:
                    if last is None:
                        print('bad gps: no previous')
                    else:
                        found = last
                        current = gps_obj
                    break
                else:
                    last = gps_obj
            if found is None:
                print('bad gps: not found!')
                break
            device_lat = (last['latitude'] + current['latitude']) / 2.0
            device_long = (last['longitude'] + current['longitude']) / 2.0
            lat_dist = abs(current['latitude'] - last['latitude'])
            long_dist = abs(current['longitude'] - last['longitude'])
            radius = lat_dist + long_dist
            multiplier = 100

            latlng = staticmaps.create_latlng(device_lat, device_long)
            circle = staticmaps.Circle(latlng, radius * multiplier, fill_color=staticmaps.TRANSPARENT, color=staticmaps.BLUE, width=2)
            context.add_object(circle)


    image = context.render_cairo(1600, 900)
    image.write_to_png("out.png")

if __name__ == '__main__':
    plot('gps.txt')
