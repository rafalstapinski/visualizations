import web
import psycopg2
import arrow
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import helpers as Help

class Display:

    def __init__(self, set_id):

        self.db = Help.DB.connect()

        self.frames = self.db.select('air_traffic',
            vars = {'set_id': set_id},
            what = 'COUNT(DISTINCT processed) AS c',
            where = 'set_id = $set_id',
        ).first().c

        self.max = self.db.select('air_traffic',
            vars = {'set_id': set_id},
            what = 'processed, COUNT(processed) AS c',
            where = 'set_id = $set_id',
            group = 'processed',
            order = 'c DESC',
            limit = 1
        ).first().c

        self.points = []
        

    def map_init():

        for pt in points:
            pt.set_data([], [])

        return points

    def animate(i):
        pass


    def run(self):

        my_map = Basemap(
            projection='merc',
            llcrnrlat=40,
            urcrnrlat=70,
            llcrnrlon=-5,
            urcrnrlon=50,
            lat_ts=20,
            resolution='c'
        )

        my_map.fillcontinents(color = 'gray')
        my_map.drawmapboundary()
        my_map.drawmeridians(np.arange(0, 360, 30))
        my_map.drawparallels(np.arange(-90, 90, 30))

        x,y = my_map(0, 0)
        point = my_map.plot(x, y, 'ro', markersize=5)[0]

        anim = animation.FuncAnimation(
            plt.gcf(),
            self.animate,
            init_func=self.map_init,
            frames=100,
            interval=500,
            blit=True
        )


        plt.show()
