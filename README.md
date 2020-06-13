# svgelements

Parsing for SVG Files, Path, Matrix, Angle, Length, Color, Point and other SVG and CSS Elements. The SVG spec defines a variety of elements which generally interoperate. In order to have a robust experience with SVGs we must be able to correctly deal with the parsing and interactions of these elements.

This project began as part of `meerK40t` which does SVG loading of files for laser cutting. It attempts to more fully map out the SVG specification, objects, and paths, while remaining easy to use and largely backwards compatible.

# License

This module is under a MIT License.


# Installing
`pip install svgelements`

Then in a script:

`from svgelements import *`

# Requirements

None.

However, some common additions do modify the functionality slightly. If `scipy` is installed then the arc length code quickly provide the exact correct answer. Some of the SVGImage code is able to load the images if given access to PIL/Pillow. 

# Compatibility

`svgelements` is compatible with Python 3+.  Support for 2.7 was dropped at Python 2 End-Of-Life January 1, 2020.

We remain nominally backwards compatible with `svg.path`, passing the same robust tests from that project. There may be number of breaking changes. However, since `svgelements` permit a lot of leeway in what is accepted and how it's accepted it will have a huge degree of compatibility with projects seen and unseen. 


# Philosophy

The goal of this project is to provide SVG spec-like elements and structures. The SVG standard 1.1 and elements of 2.0 will be used to provide much of the decisions making for implementation objects. If there is a question on implementation and the SVG documentation has a methodology, that is the preferred methodology.

The primary goal of this project is to make a more robust version of `svg.path` including other elements like `Point` and `Matrix` with clear emphasis on conforming to the SVG spec in all ways that realworld uses for SVG demands.

`svgelements` should conform to the SVG Conforming Interpreter class (2.5.4. Conforming SVG Interpreters):

>An SVG interpreter is a program which can parse and process SVG document fragments. Examples of SVG interpreters are server-side transcoding tools or optimizer (e.g., a tool which converts SVG content into modified SVG content) or analysis tools (e.g., a tool which extracts the text content from SVG content, or a validity checker).

Real world functionality demands we must correctly and reasonably provide reading, transcoding, and manipulation of SVG content.


# Overview

The versatility of the project is provided through through expansive and highly intuitive dunder methods, and robust parsing of object parameters. Points, PathSegments, Paths, Shapes, Subpaths can be multiplied by a matrix. We can add Shapes, Paths, PathSegments, and Subpaths together. And many non-declared but functionally understandable elements are automatically parsed. Such as adding strings of path_d characters to a Path or multiplying an element by the SVG Transform string elements.

While many objects perform a lot of interoperations, a lot many svg elements are designed to also work independently.

## Point

Points define a single location in 2D space. The Point class is intended to take a wide variety of different initial definitions to wrap them into being a point.

* Point(x,y)
* (x,y)
* [x,y]
* "x, y"
* x + yj (complex number)
* a class with .x and .y as methods.

Most objects requiring a point will wrap that object with the included Point class meaning any of these initial arguments is acceptable. Including independent x and y parameters, a tuple of x and y, a list of x and y, a string that parses akin to points within `polyline` objects, complex numbers with a real x and imag y values. And any class with `.x` or `.y` attributes.

---

    >>> Point(10,10) * "rotate(90)"
    Point(-10,10)

## Matrix

Matrices define affine transformations of 2d space and objects.

* Matrix.scale(s)
* Matrix.scale(sx,sy)
* Matrix.scale(sx,sy,px,py)
* Matrix.rotate(angle)
* Matrix.rotate(angle, px, py
* Matrix.skew_x(angle)
* Matrix.skew_x(angle, px, py)
* Matrix.skew_y(angle)
* Matrix.skew_y(angle, px, py)
* Matrix.translate(tx)
* Matrix.translate(tx, ty)
* Transform string values.
    * "scale(s)"
    * "scale(sx,sy)"
    * "translate(20,20) scale(2)"
    * "rotate(0.25 turns)"
    * Any valid SVG or CSS transform string will be accepted as a matrix.
    
---

    >>> Matrix("rotate(100grad)")
    Matrix(0, 1, -1, 0, 0, 0)
    
The matrix class also supports Length translates for x, and y. In some instances CSS transforms permit length transforms so "translate(20cm, 200mm)" are valid tranformations. However, these will cause issues for objects which require non-native units so it is expected that .render() will be called on these before they are used in some manner.

## Path

Paths define sequences of PathSegments that can map out any path element in SVG.

* Path() object
* String path_d value.

---

    >>> Path() + "M0,0z"
    Path(Move(end=Point(0,0)), Close(start=Point(0,0), end=Point(0,0)))


## Angle

Angles define various changes in direction.

* Angle.degrees(degree_angle)
* Angle.radians(radians_angle)
* Angle.turns(turns)
* Angle.gradians(gradian_angles)
* CSS angle string.
    * "20deg"
    * "0.3turns"
    * "1rad"
    * "100grad"
    
---

    >>> Point(0,100) * "rotate(1turn)"
    Point(0,100)
    >>> Point(0,100) * "rotate(0.5turn)"
    Point(-0,-100)
    

## Color

Colors define object color.

* XHTML color names: "red", "blue", "dark grey", etc.
* 3 digit hex: "#F00"
* 4 digit hex: "#FF00"
* 6 digit hex: "#FF0000"
* 8 digit hex: "#FFFF0000"
* "RGB(r,g,b)"
* "RGB(r%, g%, b%)"

---

    >>> Circle(stroke="yellow")
    Circle(center=Point(0,0), r=1, stroke="#ffff00")


## Length

Lengths define the amount of linear space between two things.

* "20cm"
* "200mm"
* "3in"
* Length('200mm')

    
# Examples

Parse an SVG file:

    >>> svg = SVG(file)
    >>> list(svgelements())

Make a PathSegment

    >>> Line((20,20), (40,40))
    Line(start=Point(20,20), end=Point(40,40))

Rotate a PathSegment:

    >>> Line((20,20), (40,40)) * Matrix.rotate(Angle.degrees(45))
    Line(start=Point(0,28.284271247462), end=Point(0,56.568542494924))
    
Rotate a PathSegment with a parsed matrix:

    >>> Line((20,20), (40,40)) * Matrix("Rotate(45)")
    Line(start=Point(0,28.284271247462), end=Point(0,56.568542494924))

Rotate a PathSegment with an implied parsed matrix:

    >>> Line((20,20), (40,40)) * "Rotate(45)"
    Line(start=Point(0,28.284271247462), end=Point(0,56.568542494924))

Rotate a Partial Path with an implied matrix:
(Note: The SVG does not allow us to specify a start point for this invalid path)

    >>> Path("L 40,40") * "Rotate(45)"
    Path(Line(end=Point(40,40)), transform=Matrix(0.707106781187, 0.707106781187, -0.707106781187, 0.707106781187, 0, 0), stroke='None', fill='None')
    >>> abs(Path("L 40,40") * "Rotate(45)")
    Path(Line(end=Point(0,56.568542494924)), stroke='None', fill='None')

Since Move() is a qualified element we can postpend the SVG text:

    >>> (Move((20,20)) + "L 40,40")
    Path(Move(end=Point(20,20)), Line(start=Point(20,20), end=Point(40,40)), stroke='None', fill='None')

Define the entire qualified path:

    >>> Path("M 20,20 L 40,40")"
    Path(Move(end=Point(20,20)), Line(start=Point(20,20), end=Point(40,40)))

Combine individual PathSegments together:

    >>> Move((2,2)) + Close()
    Path(Move(end=Point(2,2)), Close())

Print that as SVG path_d object:

    >>> print(Move((2,2)) + Close())
    M 2,2 Z

Scale a path:

    >>> Path("M1,1 1,2 2,2 2,1z") * "scale(2)"
    Path(Move(end=Point(1,1)), Line(start=Point(1,1), end=Point(1,2)), Line(start=Point(1,2), end=Point(2,2)), Line(start=Point(2,2), end=Point(2,1)), Close(start=Point(2,1), end=Point(1,1)), transform=Matrix(2, 0, 0, 2, 0, 0), stroke='None', fill='None')
 
Print that:

    >>> print(Path("M1,1 1,2 2,2 2,1z") * "scale(2)")
    M 2,2 L 2,4 L 4,4 L 4,2 Z
 
Reverse a scaled path:

    >>> p = (Path("M1,1 1,2 2,2 2,1z") * "scale(2)")
    >>> p.reverse()
    Path(Move(end=Point(2,1)), Line(start=Point(2,1), end=Point(2,2)), Line(start=Point(2,2), end=Point(1,2)), Line(start=Point(1,2), end=Point(1,1)), Close(start=Point(1,1), end=Point(2,1)), transform=Matrix(2, 0, 0, 2, 0, 0), stroke='None', fill='None')
    >>> print(p)
    M 4,2 L 4,4 L 2,4 L 2,2 Z

Query length of paths:

    >>> QuadraticBezier("0,0", "50,50", "100,0").length()
    114.7793574696319

Apply a translations:

    >>> Path('M 0,0 Q 50,50 100,0') * "translate(40,40)"
    Path(Move(end=Point(0,0)), QuadraticBezier(start=Point(0,0), control=Point(50,50), end=Point(100,0)), transform=Matrix(1, 0, 0, 1, 40, 40), stroke='None', fill='None')
    >>> abs(Path('M 0,0 Q 50,50 100,0') * "translate(40,40)")
    Path(Move(end=Point(40,40)), QuadraticBezier(start=Point(40,40), control=Point(90,90), end=Point(140,40)), stroke='None', fill='None')

    
Query lengths of translated paths:

    >>> (Path('M 0,0 Q 50,50 100,0') * "translate(40,40)").length()
    114.7793574696319
    >>> Path('M 0,0 Q 50,50 100,0').length()
    114.7793574696319

Query a subpath:

    >>> Path('M 0,0 Q 50,50 100,0 M 20,20 v 20 h 20 v-20 h-20 z').subpath(1).d()
    'M 20,20 L 20,40 L 40,40 L 40,20 L 20,20 Z'

Reverse a subpath:

    >>> p = Path('M 0,0 Q 50,50 100,0 M 20,20 v 20 h 20 v-20 h-20 z')
    >>> print(p)
    M 0,0 Q 50,50 100,0 M 20,20 L 20,40 L 40,40 L 40,20 L 20,20 Z
    >>> p.subpath(1).reverse()
    Path(Move(start=Point(100,0), end=Point(20,20)), Line(start=Point(20,20), end=Point(40,20)), Line(start=Point(40,20), end=Point(40,40)), Line(start=Point(40,40), end=Point(20,40)), Line(start=Point(20,40), end=Point(20,20)), Close(start=Point(20,20), end=Point(20,20)))
    >>> print(p)
    M 0,0 Q 50,50 100,0 M 20,20 L 40,20 L 40,40 L 20,40 L 20,20 Z

Query a bounding box:

    >>> QuadraticBezier("0,0", "50,50", "100,0").bbox()
    (0.0, 0.0, 100.0, 50.0)

Query a translated bounding box:

    >>> (Path('M 0,0 Q 50,50 100,0') * "translate(40,40)").bbox()
    (40.0, 40.0, 140.0, 90.0)
    
Query a translated path's untranslated bounding box.

    >>> (Path('M 0,0 Q 50,50 100,0') * "translate(40,40)").bbox(transformed=False)
    (0.0, 0.0, 100.0, 50.0)

Add a path and shape:

    >>> print(Path("M10,10z") + Circle("12,12", 2))
    M 10,10 Z M 14,12 A 2,2 0 0,1 12,14 A 2,2 0 0,1 10,12 A 2,2 0 0,1 12,10 A 2,2 0 0,1 14,12 Z

Add two shapes, and query their bounding boxes:

    >>> (Circle() + Rect()).bbox()
    (-1.0, -1.0, 1.0, 1.0)

Add two shapes and query their length:

    >>> (Circle() + Rect()).length()
    10.283185307179586
    >>> tau + 4
    10.283185307179586

Etc.


# Elements

The elements are the core functionality of this class. These are svg-based objects which interact in coherent ways.

## Path

The Path element is based on regebro's code and methods from the `svg.path` project. The primary methodology is to use different PathSegment classes for each segment within a pathd code. These should always have a high degree of backwards compatibility. And for most purposes importing the relevant classes from `svgelements` should be highly compatible with any existing code.


For this reason `svgelements` tests include `svg.path` tests in this project. And while the Point class accepts and works like a `complex` it is not actually a complex. This permits code from other projects to quickly port without requiring an extensive rewrite. But, the custom class allows for improvements like making the `Matrix` object easy.

* ``Path(*segments)``

Just as with `svg.path` the ``Path`` class is a mutable sequence, and it behaves like a list.
You can add to it and replace path segments etc:

    >>> path = Path(Line(100+100j,300+100j), Line(100+100j,300+100j))
    >>> path.append(QuadraticBezier(300+100j, 200+200j, 200+300j))
    >>> print(path)
    L 300,100 L 300,100 Q 200,200 200,300
    
    >>> path[1] = Line(200+100j,300+100j)
    >>> print(path)
    L 300,100 L 300,100 Q 200,200 200,300
    
    >>> del path[1]
    >>> print(path)
    L 300,100 Q 200,200 200,300
    
    >>> path = Move() + path
    >>> print(path)
    M 100,100 L 300,100 Q 200,200 200,300

The path object also has a ``d()`` method that will return the
SVG representation of the Path segments:

    >>> path.d()
    'M 100,100 L 300,100 Q
 200,200 200,300'

The d() parameter also takes a value for relative:

    >>> path.d(relative=True)
    'm 100,100 l 200,0 q -100,100 -100,200'

More modern and preferred methods are to simply use path_d strings where needed.

     >>> print(Path("M0,0v1h1v-1z"))
    M 0,0 L 0,1 L 1,1 L 1,0 Z

And to use scaling factors as needed.

    >>> (Path("M0,0v1h1v-1z") * "scale(20)").bbox()
    (0.0, 0.0, 20.0, 20.0)

---

A ``Path`` object that is a collection of the PathSegment objects. These can be defined by combining a PathSegment with another PathSegment initializing it with `Path()` or `Path(*segments)` or `Path(<svg_text>)`.

### Subpaths

Subpaths provide a window into a Path object. These are backed by the Path they are created from and consequently operations performed on them apply to that part of the path.

    >>> p = Path('M 0,0 Q 50,50 100,0 M 20,20 v 20 h 20 v-20 h-20 z')
    >>> print(p)
    M 0,0 Q 50,50 100,0 M 20,20 L 20,40 L 40,40 L 40,20 L 20,20 Z
    >>> q = p.subpath(1) 
    >>> q *= "scale(2)"
    >>> print(p)
    M 0,0 Q 50,50 100,0 M 40,40 L 40,80 L 80,80 L 80,40 L 40,40 Z

or likewise `.reverse()` 
(notice the path will go 80,40 first rather than 40,80.)

    >>> q.reverse()
    >>> print(p)
    M 0,0 Q 50,50 100,0 M 40,40 L 80,40 L 80,80 L 40,80 L 40,40 Z

### Segments

There are 6 PathSegment objects:
``Line``, ``Arc``, ``CubicBezier``, ``QuadraticBezier``, ``Move`` and ``Close``. These have a 1:1 correspondence to the commands in a `pathd`.

    >>> from svgelements import Path, Line, Arc, CubicBezier, QuadraticBezier, Close

All of these objects have a ``.point()`` function which will return the
coordinates of a point on the path, where the point is given as a floating
point value where ``0.0`` is the start of the path and ``1.0`` is end.

You can calculate the length of a Path or its segments with the ``.length()`` function. For CubicBezier and Arc segments this is done by geometric approximation and for this reason **may be very slow**. You can make it faster by passing in an ``error`` option to the method. If you don't pass in error, it defaults to ``1e-12``. While the project has no dependencies, if you have `scipy` installed the Arc.length() function will use to the hypergeometric exact formula contained and will quickly return with the exact answer.

    >>> CubicBezier(300+100j, 100+100j, 200+200j, 200+300j).length(error=1e-5)
    297.2208145656899

CubicBezier and Arc also has a ``min_depth`` option that specifies the
minimum recursion depth. This is set to 5 by default, resulting in using a
minimum of 32 segments for the calculation. Setting it to 0 is a bad idea for
CubicBeziers, as they may become approximated to a straight line.

``Line.length()`` and ``QuadraticBezier.length()`` also takes these
parameters, but they unneeded as direct values rather than approximations are returned.

CubicBezier and QuadraticBezier also have ``is_smooth_from(previous)``
methods, that checks if the segment is a "smooth" segment compared to the
given segment.

Unlike `svg.path` the preferred method of getting a Path from a `pathd` string is
as an argument:

    >>> from svgelements import Path
    >>> Path('M 100 100 L 300 100')
    Path(Move(end=Point(100,100)), Line(start=Point(100,100), end=Point(300,100)))

#### PathSegment Classes

These are the SVG PathSegment classes. See the `SVG specifications
<http://www.w3.org/TR/SVG/paths.html>`_ for more information on what each
parameter means.

* ``Move(start, end)`` The move object describes a move to the start of the next subpath. It may lack a start position but not en end position.

* ``Close(start, end)`` The close object describes a close path element. It will have a length if and only if the end point is not equal to the subpath start point. Neither the start point or end point is required.

* ``Line(start, end)`` The line object describes a line moving straight from one point to the next point. 

* ``Arc(start, radius, rotation, arc, sweep, end)`` The arc object describes an arc across a circular path. This supports multiple types of parameterizations. The given default there is compatible with `svg.path` and has a complex radius. It is also valid to divide radius into `rx` and `ry` or Arc(start, end, center, prx, pry, sweep) where start, end, center, prx, pry are points and sweep is the radians value of the arc distance traveled.

* ``QuadraticBezier(start, control, end)`` the quadratic bezier object describes a single control point bezier curve.

* ``CubicBezier(start, control1, control2, end)`` the cubic bezier curve object describes a two control point bezier curve.


### Examples

This SVG path example draws a triangle:

    >>> path1 = Path('M 100 100 L 300 100 L 200 300 z')

You can format SVG paths in many different ways, all valid paths should be
accepted::

    >>> path2 = Path('M100,100L300,100L200,300z')

And these paths should be equal:

    >>> path1 == path2
    True

You can also build a path from objects:

    >>> path3 = Path(Move(100 + 100j), Line(100 + 100j, 300 + 100j), Line(300 + 100j, 200 + 300j), Close(200 + 300j, 100 + 100j))

And it should again be equal to the first path::

    >>> path1 == path3
    True

Paths are mutable sequences, you can slice and append::

    >>> path1.append(QuadraticBezier(300+100j, 200+200j, 200+300j))
    >>> len(path1[2:]) == 3
    True

Note that there is no protection against you creating paths that are invalid.
You can for example have a Close command that doesn't end at the path start:

    >>> wrong = Path(Line(100+100j,200+100j), Close(200+300j, 0))
    >>> wrong.d()
    'L 200,100 Z'

## Matrix (Transformations)

SVG 1.1, 7.15.3 defines the matrix form as:

    [a c  e]
    [b d  f]

Since we are delegating to SVG spec for such things, this is how it is implemented in elements.

To be compatible with SVG 1.1 and SVG 2.0 the matrix class provided has all the SVG functions as well as the CSS functions:

* translate(x,[y])
* translateX(x)
* translateY(y)
* scale(x,[y])
* scaleX(x)
* scaleY(y)
* skew(x,[y])
* skewX(x)
* skewY(y)

Since we have compatibility with CSS for the SVG 2.0 spec compatibility we can perform length translations:

    >>> Point(0,0) * Matrix("Translate(1cm,1cm)")
    Point('1cm','1cm')

Do note, however that this isn't an intended purpose. Points are expected in native units. You should render the Matrix prior to using it. This means you must give it the correct units to translate the information from one form to another. 

    >>> Point(0,0) * (Matrix("Translate(1cm,1cm)").render(ppi=96.0))
    Point(37.795296,37.795296)

We can also rotate by `turns`, `grad`, `deg`, `rad` which are permitted CSS angles:
    
    >>> Point(10,0) * Matrix("Rotate(1turn)")
    Point(10,-0)
    >>> Point(10,0) * Matrix("Rotate(400grad)")
    Point(10,-0)
    >>> Point(10,0) * Matrix("Rotate(360deg)")
    Point(10,-0)
    
A large goal of this project is to provide a more robust modifications of Path objects including matrix transformations. This is done by three major shifts from `svg.path`s methods. 

* Points are not stored as complex numbers. These are stored as Point objects, which have backwards compatibility with complex numbers, without the data actually being backed by a `complex`.
* A matrix is added which conforms to the SVGMatrix Element. The matrix contains valid versions of all the affine transformations elements required by the SVG Spec.
* The `Arc` object is fundamentally backed by a different point-based parameterization.

The objects themselves have robust dunder methods. So if you have a path object you may simply multiply it by a matrix.

    >>> Path(Line(0+0j, 100+100j)) * Matrix.scale(2)
    Path(Line(start=Point(0,0), end=Point(100,100)), transform=Matrix(2, 0, 0, 2, 0, 0), stroke='None', fill='None')

Or rotate a parsed path.

    >>> Path("M0,0L100,100") * Matrix.rotate(30)
    Path(Move(end=Point(0,0)), Line(start=Point(0,0), end=Point(100,100)), transform=Matrix(0.154251449888, -0.988031624093, 0.988031624093, 0.154251449888, 0, 0))

Or modify an SVG path.

    >>> str(Path("M0,0L100,100") * Matrix.rotate(30))
    'M 0,0 L 114.228,-83.378'
    
The Matrix objects can be used to modify points:

    >>> Point(100,100) * Matrix("scale(2)")
    Point(200,200)
    
    >>> Point(100,100) * (Matrix("scale(2)") * Matrix("Translate(40,40)"))
    Point(240,240)
    
Do note that the order of operations for matrices matters:

    >>> Point(100,100) * (Matrix("Translate(40,40)") * Matrix("scale(2)"))
    Point(280,280)
    
The first version is:
 
    >>> (Matrix("scale(2)") * Matrix("Translate(40,40)"))
    Matrix(2, 0, 0, 2, 40, 40)

The second is:

    >>>> (Matrix("Translate(40,40)") * Matrix("scale(2)"))
    Matrix(2, 0, 0, 2, 80, 80)
    
This is:

    >>>> Point(100,100) * Matrix("Matrix(2,0,0,2,80,80)")
    Point(280,280)


### SVG Transform Parsing

Within the SVG.elements() schema objects SVG elements. The `transform` tags within objects are combined together. These are automatically applied if `reify=True` is set.


### SVG Dictionary Parsing

    >>> node = { 'd': "M0,0 100,0, 0,100 z", 'transform': "scale(0.5)"}
    >>> print(Path(node['d']) * Matrix(node['transform']))
    M 0,0 L 50,0 L 0,50 Z

### SVG Viewport Scaling, Unit Scaling

There is need in many applications to append a transformation for the viewbox, height, width. So as to prevent a variety of errors where the expected size is far vastly different from the actual size. If we have a viewbox of "0 0 100 100" but the height and width show that to be 50cm wide, then a path "M25,50L75,50" within that viewbox has a real size of length of 25cm which can be quite different from 50 (unit-less value).

This conversion is done through the `Viewbox` object. This operation is automatically done for SVG.elements() objects.

Viewbox objects have a call to `.transform()` which will provide the string for an equivolent transformation for the given viewbox.

The `Viewbox.transform()` code conforms to the algorithm given in SVG 1.1 7.2, SVG 2.0 8.2 'equivalent transform of an SVG viewport.' This will also fully implement the `preserveAspectRatio`, `xMidYMid`, and `meetOrSlice` values.

## SVG Shapes

Another important SVG elements are the shapes. While all of these can be converted to paths. They can serve some usages in their original form. There are methods to deform a rectangle that simple don't exist in the path form of that object.
* Rect
* Ellipse
* Circle
* Line (SimpleLine)
* Polyline
* Polygon

The Line shape is converted into a shape called SimpleLine to not interfere with the Line(PathSegment).

A Shape is said to be equal to another Shape or a Path if they decompose to same Path.

    >>> Circle() == Ellipse()
    True
     >>> Rect() == Path('m0,0h1v1h-1z')
    True

### Rect

Rectangles are defined by x, y and height, width. Within SVG there are also rounded corners defined with `rx` and `ry`. 

    >>> Rect(10,10,8,4).d()
    'M 10,10 L 18,10 L 18,14 L 10,14 Z'

Much like all the paths these shapes also contain a `.d()` function that produces the path data for them. This could then be wrapped into a Path().

    >>> print(Path(Rect(10,10,8,4).d()) * "rotate(0.5turns)")
    M -10,-10 L -18,-10 L -18,-14 L -10,-14 Z
    
Or simply passed to the Path:

    >>> print(Path(Rect(10,10,8,4)) * "rotate(0.5turns)")
    M -10,-10 L -18,-10 L -18,-14 L -10,-14 L -10,-10 Z

Or simply multiplied by the matrix itself:

    >>> print(Rect(10,10,8,4) * "rotate(0.5turns)")
    Rect(x=10, y=10, width=8, height=4, transform=Matrix(-1, 0, -0, -1, 0, 0), stroke='None', fill='None')

And you can equally decompose that Shape:

    >>> (Rect(10,10,8,4) * "rotate(0.5turns)").d()
    'M -10,-10 L -18,-10 L -18,-14 L -10,-14 L -10,-10 Z'


Matrices can be applied to Rect objects directly.

    >>> from svgelements import *
    >>> Rect(10,10,8,4) * "rotate(0.5turns)"
    Rect(x=10, y=10, width=8, height=4, transform=Matrix(-1, 0, -0, -1, 0, 0), stroke='None', fill='None')
    
    >>> Rect(10,10,8,4) * "rotate(0.25turns)"
    Rect(x=10, y=10, width=8, height=4, transform=Matrix(0, 1, -1, 0, 0, 0))

Rotated Rects produce path_d srings.:

    >>> Rect(10,10,8,4) * "rotate(14deg)"
    Rect(x=10, y=10, width=8, height=4, transform=Matrix(0.970295726276, 0.2419218956, -0.2419218956, 0.970295726276, 0, 0))
    >>> (Rect(10,10,8,4) * "rotate(14deg)").d()
    'M 7.28373830676,12.1221762188 L 15.046104117,14.0575513836 L 14.0784165346,17.9387342887 L 6.31605072436,16.0033591239 Z'
    
 This also works with `rx` and `ry`:
 (Note: the path will now contain Arcs)
 
    >>> (Rect(10,10,8,4, 2, 1) * "rotate(0.25turns)").d()
    'M -10,12 L -10,16 A 2,1 90 0,1 -11,18 L -13,18 A 2,1 90 0,1 -14,16 L -14,12 A 2,1 90 0,1 -13,10 L -11,10 A 2,1 90 0,1 -10,12 Z'

You can also decompose the shapes in relative modes:

    >>> (Rect(10,10,8,4, 2, 1) * "rotate(0.25turns)").d(relative=True)
    'm -10,12 l 1.77636E-15,4 a 2,1 90 0,1 -1,2 l -2,0 a 2,1 90 0,1 -1,-2 l -1.77636E-15,-4 a 2,1 90 0,1 1,-2 l 2,0 a 2,1 90 0,1 1,2 z'


### Ellipse & Circle

Ellipses and Circles are different shapes but since a circle is a particular kind of Ellipse much of the functionality here is duplicated.

While the objects are different they can be checked for equivalency:

    >>> Ellipse(center=(0,0), rx=10, ry=10) == Circle(center="0,0", r=10.0)
    True


### SimpleLine

SimpleLine is renamed from the SVG form of `Line` since we already have `Line` objects as `PathSegment`. 

    >>> s = SimpleLine(0,0,200,200)
    >>> s
    SimpleLine(x1=0.0, y1=0.0, x2=200.0, y2=200.0)
    >>> s *= "rotate(45)"
    >>> s
    SimpleLine(x1=0.0, y1=0.0, x2=200.0, y2=200.0, transform=Matrix(0.707106781187, 0.707106781187, -0.707106781187, 0.707106781187, 0, 0))
    >>> abs(s)
    SimpleLine(x1=0.0, y1=0.0, x2=2.842170943040401e-14, y2=282.842712474619, stroke='None', fill='None')
    >>> s.d()
    'M 0,0 L 2.84217094304E-14,282.842712475


### Polyline and Polygon

The difference here is polylines are not closed while Polygons are closed.

    >>> p = Polygon(0,0, 100,0, 100,100, 0,100)
    >>> p *= "scale(2)"
    >>> p.d()
    'M 0,0, L 200,0, L 200,200, L 0,200 Z'

and the same for Polyline:

    >>> p = Polyline(0,0, 100,0, 100,100, 0,100)
    >>> p *= "scale(2)"
    >>> p.d()
    'M 0,0, L 200,0, L 200,200, L 0,200'
    
You can just append a "z" to the polyline path though. 

    >>> Path(Polyline((20,0), (10,10), 0)) + "z" == Polygon("20,0 10,10 0,0")
    True

## CSS Length

The conversion of lengths to utilizes another element `Length` It provides conversions for `mm`, `cm`, `in`, `px`, `pt`, `pc`, `%`. You can also parse an element like the string '25mm' calling Length('25mm').value(ppi=96) and get the expected results. You can also call `Length('25mm').in_inches()` which will return  25mm in inches.

    >>> Length('25mm').in_inches()
    0.9842525

## Color

Color is another important element it contains an 'int' as 'value' in the form of an ARGB 32-bit integer. It will parse all the SVG color functions.

If we get the fill or stroke of an object from a node be a text element. This needs to be converted to a consistent form. We could have a 3, 4, 6, or 8 digit hex. rgb(r,g,b) value, a static dictionary name or percent rgb(r,g,b). And must be properly parsed according to the spec.

    >>> Color("red").hex
    '#ff0000'
    
    >>> Color('red').red
    255
    
    >>>Color('hsl(120, 100%, 50%)')
    Color('#00ff00')
    
    >>> c = Color('hsl(120, 100%, 50%)')
    >>> c.blue = 50
    >>> c
    Color('#00ff32')
    
In addition you can set various properties of a particular color. Check distances to other colors.

    >>> Color.distance('red', 'lightred')
    25.179356624028344
    >>> Color.distance('red', 'blue')
    403.97524676643246
    >>> Color('red').distance_to('blue')
    403.97524676643246

## Angle

Angle is backed by a 'float' and contains all the CSS angle values. 'deg', 'rad', 'grad', 'turn'.

    >>> Angle.degrees(360).as_radians
    Angle(6.283185307180)

The Angle element is used automatically with the Skew and Rotate for matrix. 

    >>> Point(100,100) * Matrix("SkewX(0.05turn)")
    Point(132.491969623291,100)

## Point

Point is used in all the SVG path segment objects. With regard to `svg.path` it is not back by, but implements all the same functionality as a `complex` and will take a complex as an input. So older `svg.path` code will remain valid. While also allowing for additional functionality like finding a distance.

    >>> Point(0+100j).distance_to([0,0])
    100.0

The class supports `complex` subscribable elements, `.x` and `.y` methods, and `.imag` and `.real`. As well as providing several of these indexing methods.

It includes a number of point functions like:
* `move_towards(point,float)`: Move this point towards the other point. with an amount [0,1]
* `distance_to(point)`: Calculate the Euclidean distance to the other point.
* `angle_to(point)`: Calculate the angle to the given point.
* `polar_to(angle,distance)`:  Return a point via polar coords at the angle and distance.
* `reflected_across(point)`: Returns a point reflected across another point. (Smooth bezier curves use this).

This for example takes the 0,0 point turns 1/8th of a turn, and moves forward by 5cm.

    >>> Point(0).polar_to(Angle.turns(0.125), Length("5cm").value(ppi=96))
    Point(133.626550492764,133.626550492764)


# Acknowledgments

The Path element of this project is based in part on the `regebro/svg.path` ( https://github.com/regebro/svg.path ) project. It is also may be based, in part, on some elements of `mathandy/svgpathtools` ( https://github.com/mathandy/svgpathtools ).

