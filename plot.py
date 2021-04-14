import json
import csv

import pandas
import matplotlib.pyplot as plt


def plot():
    df = pandas.read_csv('gps.csv')
    print(df.head())
    BBox = (df.longitude.min(), df.longitude.max(),
             df.latitude.min(), df.latitude.max())
    print(BBox)
    map_image = plt.imread('map3.png')

    fig, ax = plt.subplots(figsize = (8,7))
    ax.scatter(df.longitude, df.latitude, zorder=1, alpha= 0.2, c='b', s=10)
    ax.set_title('Wardriving Plot')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(map_image, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()

def conv_to_csv(fname, outname):
    with open(outname, 'w') as out:
        writer = csv.DictWriter(out, fieldnames=['latitude', 'longitude'])
        writer.writeheader()
        with open(fname, 'r') as f:
            for line in f.readlines():
                loaded = json.loads(line)
                coords = loaded['coords']
                row = {
                    'latitude': coords['latitude'],
                    'longitude': coords['longitude'],
                }
                writer.writerow(row)

if __name__ == '__main__':
    conv_to_csv('gps.txt', 'gps.csv')
    plot()
