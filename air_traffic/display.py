import web
import psycopg2
import arrow
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import helpers as Help
import sys

class Display:

    def __init__(self, set_id):

        self.db = Help.DB.connect()
        self.set_id = set_id
        self.queue = []
        self.counter = 0

        self.frames = self.db.select('air_traffic',
            vars = {'set_id': self.set_id},
            what = 'COUNT(DISTINCT processed) AS c',
            where = 'set_id = $set_id',
        ).first().c

        self.max = self.db.select('air_traffic',
            vars = {'set_id': self.set_id},
            what = 'processed, COUNT(processed) AS c',
            where = 'set_id = $set_id',
            group = 'processed',
            order = 'c DESC',
            limit = 1
        ).first().c + 1

        self.m = Basemap(
            projection='merc',
            llcrnrlat=0,
            llcrnrlon=40,
            urcrnrlat=50,
            urcrnrlon=90,
            lat_ts=20,
            resolution='c'
        )

        self.offset = 0

        self.points = []

        for i in range(self.max):

            x, y = self.m(0, 0)
            pt = self.m.plot(x, y, 'ro', markersize = 1)[0]
            self.points.append(pt)

        self.m.fillcontinents(color = 'gray')
        self.m.drawmapboundary()
        self.m.drawmeridians(np.arange(0, 360, 30))
        self.m.drawparallels(np.arange(-90, 90, 30))

        # x, y = self.m(0, 0)
        # self.point = self.m.plot(x, y, 'ro', markersize=5)[0]

        anim = animation.FuncAnimation(
            fig = plt.gcf(),
            # init_func = self.clear_map,
            func = self.animate,
            frames = 10,
            interval = 10,
            blit = True
            # save_count = 100,
        )

        anim.save('plot_animation.html')

        # plt.show()

    def clear_map(self):

        for pt in self.points:
            pt.set_data([], [])

    def animate(self, i):

        if self.counter > 30:
            sys.exit()

        to_add = self.max - len(self.queue)

        self.queue += self.db.select('air_traffic',
            vars = {'set_id': self.set_id},
            where = 'set_id = $set_id',
            limit = to_add,
            offset = self.offset,
            order = 'id ASC'
        ).list()

        self.offset += to_add

        current_process = self.queue[0].processed

        # while (current_procees - 2) <= self.queue[0].processed <= (current_procees + 2):

        in_batch = 0

        while self.queue[0].processed == current_process:

            record = self.queue.pop(0)
            x, y = self.m(record.lng, record.lat)
            point = self.m.plot(x, y, 'ro', markersize = 1)[0]
            points.append(point)
            in_batch += 1

        # print len(points)

        for pt in self.points[in_batch:]

        # x, y = self.m(0, 0)
        # point = self.m.plot(x, y, 'ro', markersize = 2)[0]
        # point.set_data([], [])
        # return point,

        return points

    def show(self):

        # plt.show()
        pass
