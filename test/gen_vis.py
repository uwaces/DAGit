import numpy as np
import pylab as pl
from matplotlib import collections  as mc
import csv

class Point:
        def __init__(self, x, y):
                self.x = x
                self.y = y
                

adj_list = dict()

lines = []

points_x = []
points_y = []

p = []
p_p = []
with open('simple_polygon.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        p.append((float(row[0]), float(row[1])))
        point = Point(float(row[0]), float(row[1]))
        p_p.append(point)
        adj_list[point] = set()

for i in range(0, len(p)-1):
        lines.append([p[i], p[i+1]])
        adj_list[p_p[i]].add(p_p[i+1])
lines.append([p[-1], p[0]])
adj_list[p_p[-1]].add(p_p[0])

for x, y in p:
        points_y.append(y)
        points_x.append(x)

h = []
h_p = []
with open('outer_triangle.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        h.append((float(row[0]), float(row[1])))
        point = Point(float(row[0]), float(row[1]))
        h_p.append(point)
        adj_list[point] = set()

for i in range(0, len(h)-1):
        lines.append([h[i], h[i+1]])
        adj_list[h_p[i]].add(h_p[i+1])
lines.append([h[-1], h[0]])
adj_list[h_p[-1]].add(h_p[0])

for x, y in h:
        points_y.append(y)
        points_x.append(x)


# ------------------------- USE CODE FROM HERE DOWN ---------------------------

# With ADJ_LIST
points_x = [p.x for p in adj_list.keys()]
points_y = [p.y for p in adj_list.keys()]
lines = []
for p1, adj_list in adj_list.items():
        for p2 in adj_list:
                # OR however we represent points now:
                lines.append([(p1.x, p1.y), (p2.x, p2.y)])


lc = mc.LineCollection(lines, linewidths=2)

fig, ax = pl.subplots()
ax.axis("off")
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
ax.plot(points_x, points_y, 'ro')


fig.savefig("fig.png")