import web
import psycopg2
import arrow
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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

def init():
    point.set_data([], [])
    return point,

def animate(i):
    pass

anim = animation.FuncAnimation(
    plt.gcf(),
    animate,
    init_func=init,
    frames=20,
    interval=500,
    blit=True
)


plt.show()
