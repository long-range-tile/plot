import sys

import json
import staticmaps

def plot(gps_txt):
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_OSM)

    with open(gps_txt, 'r') as f:
        for line in f.readlines():
            loaded = json.loads(line)
            coords = loaded['coords']
            latitude = coords['latitude']
            longitude = coords['longitude']
            latlng = staticmaps.create_latlng(latitude, longitude)
            marker = staticmaps.Marker(latlng, size=5)
            context.add_object(marker)

    image = context.render_cairo(1000, 1000)
    image.write_to_png("out.png")

if __name__ == '__main__':
    plot('gps.txt')
