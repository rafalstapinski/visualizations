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
            urcrnrlon=60,
            lat_ts=20,
            resolution='c'
        )

        self.offset = 0

        self.m.fillcontinents(color = 'gray')
        self.m.drawmapboundary()
        self.m.drawmeridians(np.arange(0, 360, 30))
        self.m.drawparallels(np.arange(-90, 90, 30))

        # x, y = self.m(0, 0)
        # self.point = self.m.plot(x, y, 'ro', markersize=5)[0]

        anim = animation.FuncAnimation(
            fig = plt.gcf(),
            init_func = self.clear_map,
            func = self.animate,
            frames = 10,
            interval = 10,
            save_count = 100,
        )

        anim.save('plot_animation.html')

        # plt.show()

    def clear_map(self):

        x, y = self.m(0, 0)
        point = self.m.plot(x, y, 'ro', markersize=5)[0]
        point.set_data([], [])
        return point,

    def animate(self, i):

        if self.counter > 30:
            sys.exit()

        self.queue += self.db.select('air_traffic',
            vars = {'set_id': self.set_id},
            where = 'set_id = $set_id',
            limit = self.max,
            offset = self.offset
        ).list()

        self.offset += self.max

        current_process = self.queue[0].processed

        points = []

        # for record in self.queue:
        #
        #     if record.processed != current_process:
        #         break
        #
        #     x, y = self.m(record.lng, record.lat)
        #     point = self.m.plot(x, y, 'ro', markersize = 2)[0]
        #     points.append(point)

        while self.queue[0].processed == current_process:

            record = self.queue.pop(0)

            x, y = self.m(record.lng, record.lat)

            # print x, y

            point = self.m.plot(x, y, 'ro', markersize = 2)[0]
            points.append(point)

        self.counter += 1

        return points


    def show(self):

        plt.show()

# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.animation as animation
# my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
#           lat_0=0, lon_0=-130)
# my_map.drawcoastlines()
# my_map.drawcountries()
# my_map.fillcontinents(color = 'gray')
# my_map.drawmapboundary()
# my_map.drawmeridians(np.arange(0, 360, 30))
# my_map.drawparallels(np.arange(-90, 90, 30))
#
#
# points = []
#
#
# for i in range(10):
#     lng, lat = np.random.random_integers(-130, 130, 2)
#     x, y = my_map(lng, lat)
#     point = my_map.plot(x, y, 'ro', markersize=5)[0]
#     points.append(point)
#
# def init():
#
#     # points = []
#
#     for i in range(10):
#         lng, lat = np.random.random_integers(-130, 130, 2)
#         x, y = my_map(lng, lat)
#         points[i].set_data(x, y)
#
#     point.set_data([], [])
#     return points
#
# # animation function.  This is called sequentially
# def animate(f):
#
#     for i in range(10):
#         lng, lat = np.random.random_integers(-130, 130, 2)
#         x, y = my_map(lng, lat)
#         points[i].set_data(x, y)
#
#     return points
#
# # call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(plt.gcf(), func = animate, init_func = init,
#                                frames=20, interval=500, blit=True)
#
# plt.show()
