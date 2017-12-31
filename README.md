# Kirkpatrick Point Location in Python, with git
We have created a library in Python for running the Kirkpatrick point location algorithm. We provide two versions: one is an optimized, usable version of the library. The other is more of a novelty; the algorithm requires a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph), and we provide an alternate interface which creates and stores this DAG in the filesystem using git. This allows the use of some interesting visualization tools to see how the algorithm is working, is a good benchmark for git and a good learning exercise for its more complex features, but most of all is an extremely fun idea. If you aren't familiar with git, read our appendix [What Is git?](#what-is-git)

# Introduction
This project was created by Matt Asnes and Harrison Kaiser, for COMP-163: Computational Geometry, in Spring 2017 at Tufts University.

# About The Project

![Polygons](https://github.com/uwaces/DAGit/raw/master/img/ex.png)
![Initial Triangulation](https://github.com/uwaces/DAGit/raw/master/img/extri.png)
![After 1 Iteration](https://github.com/uwaces/DAGit/raw/master/img/test2.png)
![After 3 Iterations](https://github.com/uwaces/DAGit/raw/master/img/test3.png)

## What Does This Do?
The goal of point location is that from a set of polygons, like a map, we want to be able to tell which of our polygons a given point is in as fast as we possibly can. We could test each polygon, but if our polygons don't change and we're asking a lot of times, that's going to get inefficient pretty fast. Instead, we want to do a little bit of work up front in exchange for much faster querying.

This repository contains an implementation of the [Kirkpatrick point location](https://en.wikipedia.org/wiki/Point_location#Triangulation_refinement) algorithm, in 2D. This algorithm is passed as input a set of polygons in the plane, and, for n input points, creates a structure in `O(n)` or `O(n log(n))` time which can be queried to determine which polygon of the input set, if any, contains the query point in `O(log(n))` time.


## How Does The Algorithm Work, at a High Level?
At a high level, this algorithm is all about iterating on a triangulation to make it less and less refined. Telling whether a point is inside a polygon isn't too hard, but telling whether a point is inside a triangle can be done very easily by just comparing the point to the three line segments that form the triangle. So we triangulate. But we have a problem: we don't want to have to look at every triangle we make. 

We solve this conundrum by making a series of triangulations. We can visualize this as copying the triangulation, removing some of the points, and making new, bigger triangles. We can do this repeatedly, and keep track of which of our 'bigger' triangles contained our 'smaller' triangles on the level below. Then to query, we just have to tunnel down through our levels of triangulations. We start at a level which only has one triangle, and we ask: which of the triangles this overlaps is our point in? It can be in only one of them, and there can be only a constant number of triangles in the next level by some math that we won't show here. Then all we have to do is repeat this procedure at each level: we're in a triangle, and we know it overlaps only a few triangles in the next level down. Which of those few is it in? Eventually we'll get to one of the triangles in our original triangulation, and we'll know which polygon we were in.

The main differences between the description above and the implementation is that we keep track of the overlaps of our triangles between levels in a DAG which we simply traverse to tunnel down through our triangulations, and since all of our information about overlaps is stored in that structure, we don't actually need to keep each triangulation in its full form.

## How Does The Algorithm Work, in Detail?
The Kirkpatrick point location works as follows. To build the structure:
* Get as input a list of non-overlapping, adjacent simple polygons. Picture the countries on a map, for example.
* Triangulate each polygon by any means (`O(n)` in theory, `O(n log(n))` practically).
* Merge the triangulated polygons into one triangulation, such that the convex hull of the result is a triangle; if it is not, add three dummy points.
* Initialize a DAG as a forest, where each triangle is a node.
* While we are able to do so:
    - Treating the triangulation as a planar graph, find an independent set of low degree vertices. This is guaranteed to (1) exist, (2) be at least 1/18 of the total points in the graph
    - Remove these points from the triangulation and retriangulate the result, but keep track of the triangles the removed points were a part of.
    - In our DAG, add a new 'level', with one node for each new triangle, and create edges from our new triangles to any old triangles which they overlapped, with the edges directed from new to old.
    - When we have only a single triangle left, i.e. only the triangular convex hull remains, mark that node as the root and terminate the procedure.

We can then query for which polygon a point is contained in as follows:
* Beginning at the root, check whether the polygon is contained in the triangle.
* If it is, find which of the children of this node in the DAG the point is contained in.
* For that child, recurse.
* When we find that we are in a leaf of the DAG, a node which has no children, see which polygon of the input polygons that triangle was contained in, and report that as the answer.

# Library Interface

Our interface is as follows:

We have written a library, `kirkpatrick`, This library contains several modules, of which only two or three are used by an end-user in most cases. The most important of these is `pl`, which contains the class `pl.PointLocator`. This class has only one method, `query`, which allows the querying of points. When creating a new point locator, a user passes in one parameter: a list of polygons to operate on. These polygons are of the class `poly.Polygon`, which is created using a list of `simplices.Vertex` objects. Then a typical workflow goes something like:
```
from kirkpatrick import pl
from kirkpatrick import poly
from kirkpatrick import simplices


# ...load data from disk, in any desired format

polygons = []

# Loop over all polygons
for polygon in input_data:
    
    # Make Vertex objects
    vertices = []
    for x_coord, y_coord in input:
        new_vertex = simplices.Vertex(x_coord, y_coord)
        vertices.append(new_vertex)

    # Make polygon object
    polygon = poly.Polygon("Polygon Name Here", vertices)
    polygons.append(polygon)

# Create PointLocator object from our list of polygons
locator = pl.PointLocator(polygons)

# Query it with points
print(locator.query(0, 0))
print(locator.query(0, 10))
print(locator.query(12.4, -2.1))
```

We have an existing example implementation in `main.py`, which loads data from example files in our `test` directory; the input data looks like:

```
15.42 5.32
12.42 -3.08
16.64 -3.74
18.32 4.48
23.94 4.36
14.0 6.0
```

with one such file per polygon.

# Library Architecture

![Architecture Diagram](https://github.com/uwaces/DAGit/raw/master/img/arch.png)

We structured the library around one main interface, `PointLocator`, which is fed by `Polygons`. PointLocator maintains and interoperates between two structures: a `PlanarGraph` and a `DAG`. The planar graph is actually the triangulation of the input polygons, where at first each triangle knows what polygon it was from. Our `Vertex` class ensures that references to vertices with the same coordinates are unique (i.e. vertices are atomic) so polygons which share points use the same `Vertex` object. This triangulation is refined by finding independent sets of low degree vertices, and then removing them (making sure to retriangulate the hole we made). When a set of points is removed, we gather the trangles which contained that vertex (each vertex has a list of triangles it is in) and bring our DAG into the picture. The DAG's nodes represent triangles, and an edge represents a triangle which was removed overlapping a triangle which was created when we retriangulated. In this way we build up our less and less refined picture of the polygons, and can dig through the DAG in logarithmic time for querying.

Our triangulation is done when the `planar` module requests that the `triangulate` module triangulate the graph, which is done using the `earcut` library. Triangulate and our DAG both use `Triangle` objects which can perform simple operations such as detecting overlaps of triangles and telling whether a triangle contains a point.

Our `PlanarGraph` also uses `matplotlib` to generate images of each level of the triangulation.

# Appendix

## What Is git?
Git is a version control system. Version control is a helpful tool in software development: by using it, we can ensure that we'll always be able to go back to a working version of our code once we make a change. Each change is recorded, and the differences between the changed files and the old files is kept track of. It makes for fantastic bookkeeping of code and text documents in general. GitHub is an internet-based place to store your 'git repositories', i.e. your bundles of all of the versions of your code and documents that git has created. You can upload them here, and they'll be nominally safe in the cloud.

### git Example:
As an example of how git works, take this project. We have a bunch of code, and want to store it in a repository. We open up a command line terminal on our preferred operating system, and navigate to wherever our files are. In my case, they're at the path: `/home/matt/dev/DAGit`. If I haven't yet created a git repository here, I can type `git init` to begin. I see a bunch of files here, and I want to add them all to our git repository, so I say `git add .`. The period says "all the files in this place". If instead I just wanted to add this README, I could say `git add README.md`.

In any case, I've now added that file, but what does that mean? It means that I've told git that I'm going to be tracking changes in that file, but git will not yet write those changes and store them permanently. In order for that to happen, I need to say `git commit`. This tells git, "I'm done making changes to those files I told you to track, and you can save those changes now". Git will pop up a window asking you to fill in some details about what changes you made, and then later you can review all changes that have been made with `git log`. Each commit makes one little node in git's storage system that keeps track of the changes that were made and the message that was saved along with them.

If you're using something like GitHub, there's more to do, as well. With `git commit`, git has saved the changes, but it has not uploaded them to GitHub yet. In order to do that, you need to say `git push origin master`. The word `origin` is a special keyword that git knows means GitHub (so long as you're using GitHub). If you created a repository with `git init`, you can then say `git remote add origin https://github.com/uwaces/DAGit.git` to link up GitHub with your local version of the repository; you're linking the word 'origin' to the URL you made on GitHub. 

The word `master` is also special. This is what's called a branch in git. You can say `git branch` to look at all of them; by default there's just one, called `master`. Branches are useful for the real power of git: not just tracking changes, but having a whole team of people working on code, and editing lots of files, but without stepping on one another's toes in the process. git has some powerful difference detection in text files, and can usually 'merge' two changes together.

Branches help with this: if I'm working on implementing the triangulation algorithm, and Harrison is working on implementing the planar graph, I can say `git checkout -b triangulation` and Harrison can say `git checkout -b planar_graph`. Then we can both test our features independently; I can always run my triangulation and know that any time it doesn't work, it's my fault, and I won't be tripped up by bugs from Harrison's code. When we're both done we say say `git checkout master` to go to the master branch, and say `git merge triangulation planar_graph` to merge both branches into master. Sometimes, if the same file has been editied multiple times, git can't figure out how to merge the changes and will request human assistance in a "merge conflict", but most of the time it works out.

This talk of nodes branches merging may be rining bells as this point, but git effectively is a glorified DAG with some text processing utilities. Each branch is a directed edge, where all edges go forwards (representing going forwards in time), a split in the DAG represents a branch separating off from another branch, and two branches merging in git creates the same in the DAG. We use this fact in our project and use git in a way it really, really isn't supposed to be used: we make each 'commit' a triangle, and then branch off from that into different commits which represent more triangles. At the root, the first commit, we have one large triangle that is the largest triangle in the Kirkpatrick point location algorithm.


## References and Credits
We are using a Python port of the earcut triangulation algorithm found at https://github.com/joshuaskelly/earcut-python for our polygon triangulation. This is algorithmically slower, but has an easy interface.

We found https://github.com/rkaneriya/point-location to be a helpful reference implementation, albeit in JavaScript.
