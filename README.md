# svg.elements
SVG Parsing for Elements, Paths, and other SVG Objects.

This project is based on the `regebro/svg.path` project.  It is also may be based, in part, on some elements of `mathandy/svgpathtools`.

This project began as part of `meerK40t` which does svg loading of files for laser cutting. It attempts to more fully map out the svg spec, objects, and paths, while remaining easy to use and highly backwards compatable.

`svg.elements` is derived from regebro's svg.path project ( https://github.com/regebro/svg.path )
some of the math is from mathandy's svgpathtools project ( https://github.com/mathandy/svgpathtools ).

The Zingl-Bresenham plotting algorithms are from Alois Zingl's "The Beauty of Bresenham's Algorithm"
( http://members.chello.at/easyfilter/bresenham.html ). They are all MIT Licensed and this library is
also MIT licensed. In the case of Zingl's work this isn't explicit from his website, however from personal
correspondence "'Free and open source' means you can do anything with it like the MIT licence."

# Goals/Philsophy

The goal is to provide svg like objects and structures. The svg standard 1.1 and elements of 2.0 will
be used to provide much of the decisions making for implementation objects. If there is a question on
implementation, if the SVG documentation has a methodology it should be used.

The primary goal is to make a more robust version of `svg.path` including other elements like `SVGPoint` and `SVGMatrix` with clear emphasis on conforming to the SVG spec in all ways that real world uses for SVG demands.

`svg.elements` should conform to the SVG Conforming Interpretor class (2.5.4. Conforming SVG Interpreters):

>An SVG interpreter is a program which can parse and process SVG document fragments. Examples of SVG interpreters are server-side transcoding tools or optimizers (e.g., a tool which converts SVG content into modified SVG content) or analysis tools (e.g., a tool which extracts the text content from SVG content, or a validity checker).

For real world functionality we must correctly and reasonably provide the ability to do transcoding of svg as well as accessing and modifying content.

# Elements

The core functionality of this class are the elements. These are svg based objects which interact work in various reasonable methods.

## Path

The base code for this is regebro's code and methods from the svg.path class. The primary methods is to use different path classes for the various elements within a pathd code. These should always have a high degree of backwards compatability.

### Segments

There are 6 path segment objects:
``Line``, ``Arc``, ``CubicBezier``, ``QuadraticBezier``, ``Move`` and ``Close``. These correspond to all the objects a path can use. 

There is also a ``Path`` object that acts as a collection of the path segment objects.

While `svg.path` objects used complex values for coordinate data. We use `Point` objects which are backwards compatible with other point objects, including complex numbers. Because of this, there should be a high degree of compatibility between this project and ones that used `svg.path`. You can use complex numbers as points, and they should seemlessly convert.

    >>> from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close

All of these objects have a ``.point()`` function which will return the
coordinates of a point on the path, where the point is given as a floating
point value where ``0.0`` is the start of the path and ``1.0`` is end end.

You can calculate the length of a Path or it's segments with the
``.length()`` function. For CubicBezier and Arc segments this is done by
geometric approximation and for this reason **may be very slow**. You can
make it faster by passing in an ``error`` option to the method. If you
don't pass in error, it defaults to ``1e-12``::

    >>> CubicBezier(300+100j, 100+100j, 200+200j, 200+300j).length(error=1e-5)
    297.2208145656899

CubicBezier and Arc also has a ``min_depth`` option that specifies the
minimum recursion depth. This is set to 5 by default, resulting in using a
minimum of 32 segments for the calculation. Setting it to 0 is a bad idea for
CubicBeziers, as they may become approximated to a straight line.

``Line.length()`` and ``QuadraticBezier.length()`` also takes these
parameters, but they unneeded as direct values rather than approximations are returned.

CubicBezier and QuadraticBezier also has ``is_smooth_from(previous)``
methods, that check if the segment is a "smooth" segment compared to the
given segment.

There is also a ``parse_path()`` function that will take an SVG path definition
and return a ``Path`` object::

    >>> from svg.path import parse_path
    >>> parse_path('M 100 100 L 300 100')
    Path(Move(to=(100+100j)), Line(start=(100+100j), end=(300+100j)))


### Segment Classes

These are the SVG path segment classes. See the `SVG specifications
<http://www.w3.org/TR/SVG/paths.html>`_ for more information on what each
parameter means.

* ``Move(start, end)`` The move object describes a move to the start of the next subpath. It may lack a start position but not en end position.

* ``Close(start, end)`` The close object describes a close path element. It will have a length if and only if the end point is not equal to the subpath start point. Neither the start point or end point is required.

* ``Line(start, end)`` The line object describes a line moving straight from one point to the next point. 

* ``Arc(start, radius, rotation, arc, sweep, end)`` The arc object describes an arc across a circular path. This supports multiple types of parameterizations. The given default there is compatable with `svg.path` and has a complex radius. It is also valid to divide radius into `rx` and `ry` or Arc(start, end, center, prx, pry, sweep) where start, end, center, prx, pry are points and sweep is the radians value of the arc distance travelled.

* ``QuadraticBezier(start, control, end)`` the quadraticbezier object describes a single control point bezier curve.

* ``CubicBezier(start, control1, control2, end)`` the cubic bezier curve object describes a two control point bezier curve.

In addition to that, there is the ``Path`` class, which is instantiated with a sequence of path segments:

* ``Path(*segments)``

The ``Path`` class is a mutable sequence, so it behaves like a list.
You can add to it and replace path segments etc:

    >>> path = Path(Line(100+100j,300+100j), Line(100+100j,300+100j))
    >>> path.append(QuadraticBezier(300+100j, 200+200j, 200+300j))
    >>> path[0] = Line(200+100j,300+100j)
    >>> del path[1]

The path object also has a ``d()`` method that will return the
SVG representation of the Path segments:

    >>> path.d()
    'M 200,100 L 300,100 Q 200,200 200,300'


### Examples

This SVG path example draws a triangle:

    >>> path1 = parse_path('M 100 100 L 300 100 L 200 300 z')

You can format SVG paths in many different ways, all valid paths should be
accepted::

    >>> path2 = parse_path('M100,100L300,100L200,300z')

And these paths should be equal:

    >>> path1 == path2
    True

You can also build a path from objects:

    >>> path3 = Path(Line(100+100j,300+100j), Line(300+100j, 200+300j), Line(200+300j, 100+100j))

And it should again be equal to the first path::

    >>> path1 == path2
    True

Paths are mutable sequences, you can slice and append::

    >>> path1.append(QuadraticBezier(300+100j, 200+200j, 200+300j))
    >>> len(path1[2:]) == 3
    True

Note that there is no protection against you creating paths that are invalid.
You can for example have a Close command that doesn't end at the path start::

    >>> wrong = Path(Line(100+100j,200+100j), Close(200+300j, 0))

# Transformations

A large goal of this project is to provide a more robust modifications of Path objects including matrix transformations. This is done by three major shifts from `svg.path`s methods. 

* Points are not stored as complex numbers. These are stored as Point objects, which have backwards compatability with complex numbers, without the data actually being backed by a `complex`.
* A matrix is added which conforms to the SVGMatrix Element. The matrix contains valid versions of all the affline transformations elements required by the SVG Spec.
* The `Arc` object is fundamentally backed by a different point-based parameterization.

The objects themselves have robust dunder methods. So if you have a path object you may simply multiply it by a matrix.

    >>> Path(Line(0+0j, 100+100j)) * Matrix.scale(2)
    >>> Path(Line(start=Point(0.000000000000,0.000000000000), end=Point(200.000000000000,200.000000000000)))

Or rotate a parsed path.

    >>> parse_svg_path(Path(), "M0,0L100,100") * Matrix.rotate(30)
    >>> Path(Move(end=Point(0.000000000000,0.000000000000)), Line(start=Point(0.000000000000,0.000000000000), end=Point(114.228307398045,-83.378017420528)))

Or modify an svg path.

    >>> (parse_svg_path(Path(), "M0,0L100,100") * Matrix.rotate(30)).d()
    >>> 'M 0,0 L 114.228,-83.378'
    
# Transform Parsing

The extra robustness metric also includes a few additional robust methodologies above those provided by `svg.path` firstly, the `transform` tags within objects are combined together within the `dict` objects. This means that if you get a the 'd' object from an end-node in the SVG you can choose to apply the transformations. This list of transformations complies with the SVG spec. They merely aren't applied until requested.

    >>> parse_svg_transform("scale(2) translate(100,100)", Matrix())
    >>> Matrix(2.000000, 0.000000, 0.000000, 2.000000, 200.000000, 200.000000)

## Real Size scaling

There is also a need in many applications to append a transformation for the viewbox height width, preserve to shapes. So as to prevent a variety of errors where the expected size is far different. If we have a viewbox of "0 0 100 100" but the height and width show that to be 50cm wide, then a path "M25,50L75,50" within that viewbox has a real size of length of 25cm which is different than parsing. 

`parse_viewbox_transform` performs this operation. It uses the conversion of the width and height to real world units. With a variable setting of `ppi` or pixels_per_inch. The standard default value for this is 96. Though other values have been used in other places.

This can be easily invoked calling `parse_svg_file` which parses the svg file as a whole. If called with `viewport_transform=True` it will parse this viewport appending the required transformation to the SVG root object. If you then apply the transform string to the svg object it will be correctly applied. And scaled to the real size.  

The parse_viewbox_transform code conforms to the algorithm given in SVG 1.1 7.2, SVG 2.0 8.2 'equivalent transform of an SVG viewport.' This will also fully implement the `preserveAspectRatio`, `xMidYMid`, and `meetOrSlice` values.

The conversion of to real size elements utilizes another parser element of `parse_svg_distance` which gives the scaling for `mm`, `cm`, `in`, `px`, `pt`, `pc`.

# SVG Colors

There is also a real need to extract colors from SVG elements. If we get the fill or stroke of an object it can be colored in a number of different ways `parse_svg_color` will return the ARGB value given by the svg color text string. This could be 3, 4, 6, or 8 digit hex. rgb(r,g,b), a static dictionary name or percent rgb(r,g,b). And these should be properly parsed according to the spec.


# License

This module is under a MIT License.
