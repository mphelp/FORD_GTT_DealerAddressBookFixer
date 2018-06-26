==============
timezonefinder
==============

.. image:: https://travis-ci.org/MrMinimal64/timezonefinder.svg?branch=master
    :target: https://travis-ci.org/MrMinimal64/timezonefinder


.. image:: https://img.shields.io/pypi/wheel/timezonefinder.svg
    :target: https://pypi.python.org/pypi/timezonefinder


.. image:: https://img.shields.io/pypi/v/timezonefinder.svg
    :target: https://pypi.python.org/pypi/timezonefinder



This is a fast and lightweight python project for looking up the corresponding
timezone for a given lat/lng on earth entirely offline.

NOTE: the old smaller data set `tz_world <http://efele.net/maps/tz/world/>`__  is not being maintained any more and the new data (s. below) is unfortunately much bigger (40+MB).
I originally wanted to keep this package as lightweight as possible, but actuality is even more important I guess.
In case size and speed matter more you than actuality, consider checking out older versions of timezonefinder(L).

NOTE: The timezone polygons also do NOT follow the shorelines any more (as they did with tz_world).
This makes the results of closest_timezone_at() and certain_timezone_at() somewhat meaningless (as with timezonefinderL).

Current data set in use (since 3.0.0): precompiled `timezone-boundary-builder <https://github.com/evansiroky/timezone-boundary-builder>`__ release. version: 2018d (without oceans, Apr2018, 116MB, JSON)

Also see:
`GitHub <https://github.com/MrMinimal64/timezonefinder>`__,
`PyPI <https://pypi.python.org/pypi/timezonefinder/>`__,
`conda-forge feedstock <https://github.com/conda-forge/timezonefinder-feedstock>`__,
`timezone_finder <https://github.com/gunyarakun/timezone_finder>`__: ruby port,
`timezonefinderL <https://github.com/MrMinimal64/timezonefinderL>`__: faster, lighter (but outdated) version
`timezonefinderL GUI <http://timezonefinder.michelfe.it/gui>`__: demo and online API of timezonefinderL


Dependencies
============

(``python``)
``numpy``
``six``

**Optional:**

If the vanilla Python code is too slow for you, also install

``Numba`` (https://github.com/numba/numba) and all its Requirements (e.g. `llvmlite <http://llvmlite.pydata.org/en/latest/install/index.html>`_)

This causes the time critical algorithms (in ``helpers_numba.py``) to be automatically precompiled to speed things up.


Installation
============


Installation with conda: see instructions at `conda-forge feedstock <https://github.com/conda-forge/timezonefinder-feedstock>`__ (NOTE: The newest version of timezonefinder might not be available via conda yet)


Installation with pip:
(install the dependencies)
then in the command line:

::

    pip install timezonefinder





Usage
=====

Basics:
-------

in Python:

::

    from timezonefinder import TimezoneFinder

    tf = TimezoneFinder()


for testing if numba is being used:
(if the import of the optimized algorithms worked)

::

    TimezoneFinder.using_numba()   # this is a static method returning True or False


**timezone_at():**

This is the default function to check which timezone a point lies within (similar to tzwheres ``tzNameAt()``).
If no timezone has been found, ``None`` is being returned.

**PLEASE NOTE:** This approach is optimized for speed and the common case to only query points within a timezone.
The last possible timezone in proximity is always returned (without checking if the point is really included).
So results might be misleading for points outside of any timezone.


::

    longitude = 13.358
    latitude = 52.5061
    tf.timezone_at(lng=longitude, lat=latitude) # returns 'Europe/Berlin'


**certain_timezone_at():**

This function is for making sure a point is really inside a timezone. It is slower, because all polygons (with shortcuts in that area)
are checked until one polygon is matched. ``None`` is being returned without any match.

NOTE: The timezone polygons do NOT follow the shorelines any more. Just because you do not get ``None``,
the point could still lie off land!


::

    tf.certain_timezone_at(lng=longitude, lat=latitude) # returns 'Europe/Berlin'


**closest_timezone_at():**

Only use this when the point is not inside a polygon (simply computes and compares the distances to the polygon boundaries!).
This returns the closest timezone of all polygons within +-1 degree lng and +-1 degree lat (or None).

NOTE: The timezone polygons do NOT follow the shorelines any more. This makes the results of closest_timezone_at() somewhat meaningless.

::

    longitude = 12.773955
    latitude = 55.578595
    tf.closest_timezone_at(lng=longitude, lat=latitude) # returns 'Europe/Copenhagen'

Other options:
To increase search radius even more, use the ``delta_degree``-option:

::

    tf.closest_timezone_at(lng=longitude, lat=latitude, delta_degree=3)


This checks all the polygons within +-3 degree lng and +-3 degree lat.
I recommend only slowly increasing the search radius, since computation time increases quite quickly
(with the amount of polygons which need to be evaluated). When you want to use this feature a lot,
consider using ``Numba`` to save computing time.


Also keep in mind that x degrees lat are not the same distance apart than x degree lng (earth is a sphere)!
As a consequence getting a result does NOT mean that there is no closer timezone! It might just not be within the area being queried.

With ``exact_computation=True`` the distance to every polygon edge is computed (way more complicated), instead of just evaluating the distances to all the vertices.
This only makes a real difference when polygons are very close.


With ``return_distances=True`` the output looks like this:

( 'tz_name_of_the_closest_polygon',[ distances to every polygon in km], [tz_names of every polygon])

Note that some polygons might not be tested (for example when a zone is found to be the closest already).
To prevent this use ``force_evaluation=True``.

::

    longitude = 42.1052479
    latitude = -16.622686
    tf.closest_timezone_at(lng=longitude, lat=latitude, delta_degree=2,
                                        exact_computation=True, return_distances=True, force_evaluation=True)
    '''
    returns ('uninhabited',
    [80.66907784731714, 217.10924866254518, 293.5467252349301, 304.5274937839159, 238.18462606485667, 267.918674688949, 207.43831938964408, 209.6790144988553, 228.42135641542546],
    ['uninhabited', 'Indian/Antananarivo', 'Indian/Antananarivo', 'Indian/Antananarivo', 'Africa/Maputo', 'Africa/Maputo', 'Africa/Maputo', 'Africa/Maputo', 'Africa/Maputo'])
    '''



**get_geometry:**


for querying timezones for their geometric shape use ``get_geometry()``.
output format: ``[ [polygon1, hole1,...), [polygon2, ...], ...]``
and each polygon and hole is itself formated like: ``([longitudes], [latitudes])``
or ``[(lng1,lat1), (lng2,lat2),...]`` if ``coords_as_pairs=True``.

::

    tf.get_geometry(tz_name='Africa/Addis_Ababa', coords_as_pairs=True)

    tf.get_geometry(tz_id=400, use_id=True)




Further application:
--------------------

**To maximize the chances of getting a result in a** ``Django`` **view it might look like:**

::

    def find_timezone(request, lat, lng):
        lat = float(lat)
        lng = float(lng)

        try:
            timezone_name = tf.timezone_at(lng=lng, lat=lat)
            if timezone_name is None:
                timezone_name = tf.closest_timezone_at(lng=lng, lat=lat)
                # maybe even increase the search radius when it is still None

        except ValueError:
            # the coordinates were out of bounds
            # {handle error}

        # ... do something with timezone_name ...

**To get an aware datetime object from the timezone name:**

::

    # first pip install pytz
    from pytz import timezone, utc
    from pytz.exceptions import UnknownTimeZoneError

    # tzinfo has to be None (means naive)
    naive_datetime = YOUR_NAIVE_DATETIME

    try:
        tz = timezone(timezone_name)
        aware_datetime = naive_datetime.replace(tzinfo=tz)
        aware_datetime_in_utc = aware_datetime.astimezone(utc)

        naive_datetime_as_utc_converted_to_tz = tz.localize(naive_datetime)

    except UnknownTimeZoneError:
        # ... handle the error ...

also see the `pytz Doc <http://pytz.sourceforge.net/>`__.

**parsing the data:**


Download the latest ``timezones.geojson.zip`` file from `GitHub <https://github.com/evansiroky/timezone-boundary-builder/releases>`__, unzip and
place the ``combined.json`` inside the timezonefinder folder. Now run the ``file_converter.py`` until the compilation of the binary files is completed.


**Calling timezonefinder from the command line:**

With -v you get verbose output, without it only the timezone name is being printed.
Choose between functions timezone_at() and certain_timezone_at() with flag -f (default: timezone_at()).
Please note that this is much slower than keeping a Timezonefinder class directly in Python,
because here all binary files are being opend again for each query.

::

    usage: timezonefinder.py [-h] [-v] [-f {0,1}] lng lat






Contact
=======

Most certainly there is stuff I missed, things I could have optimized even further etc. I would be really glad to get some feedback on my code.

If you notice that the tz data is outdated, encounter any bugs, have
suggestions, criticism, etc. feel free to **open an Issue**, **add a Pull Requests** on Git or ...

contact me: *[python] {at} [michelfe] {dot} [it]*


Acknowledgements
================

Thanks to:

`Adam <https://github.com/adamchainz>`__ for adding organisational features to the project and for helping me with publishing and testing routines.

`snowman2 <https://github.com/snowman2>`__ for creating the conda-forge recipe.

`synapticarbors <https://github.com/synapticarbors>`__ for fixing Numba import with py27.

License
=======

``timezonefinder`` is distributed under the terms of the MIT license
(see LICENSE.txt).


Comparison to pytzwhere
=======================

This project has originally been derived from `pytzwhere <https://pypi.python.org/pypi/tzwhere>`__
(`github <https://github.com/pegler/pytzwhere>`__), but aims at providing
improved performance and usability.

``pytzwhere`` is parsing a 76MB .csv file (floats stored as strings!) completely into memory and computing shortcuts from this data on every startup.
This is time, memory and CPU consuming. Additionally calculating with floats is slow,
keeping those 4M+ floats in the RAM all the time is unnecessary and the precision of floats is not even needed in this case (s. detailed comparison and speed tests below).

In comparison most notably initialisation time and memory usage are significantly reduced.
``pytzwhere`` is using up to 450MB of RAM (with ``shapely`` and ``numpy`` active),
because it is parsing and keeping all the timezone polygons in the memory.
This uses unnecessary time/ computation/ memory and this was the reason I created this package in the first place.
This package uses at most 40MB (= encountered memory consumption of the python process) and has some more advantages:

**Differences:**

-  highly decreased memory usage

-  highly reduced start up time

-  usage of 32bit int (instead of 64+bit float) reduces computing time and memory consumption. The accuracy of 32bit int is still high enough. According to my calculations the worst accuracy is 1cm at the equator. This is far more precise than the discrete polygons in the data.

-  the data is stored in memory friendly binary files (approx. 41MB in total, original data 120MB .json)

-  data is only being read on demand (not completely read into memory if not needed)

-  precomputed shortcuts are included to quickly look up which polygons have to be checked

-  available proximity algorithm ``closest_timezone_at()``

-  function ``get_geometry()`` enables querying timezones for their geometric shape (= multipolygon with holes)

-  further speedup possible by the use of ``numba`` (code precompilation)



test results:
===============

::


    Speed Tests:
    _________________________
    shapely: ON (tzwhere)
    Numba: ON (timezonefinder)

    tzwhere: 0:01:53.723689
    timezonefinder: 0:00:00.002525
    45038.08 times faster


    all other cross tests are not meaningful because tz_where is still using the outdated tz_world data set



Changelog
=========


3.0.1 (2018-05-30)
------------------

* fixing minor issue #58 (readme not rendering in pyPI)


3.0.0 (2018-05-17)
------------------

* ATTENTION: the package six is now required! (was necessary because of the new testing routine. improves compatibility standards)
* updated build/testing/publishing routine
* updated the data to `2018d <https://github.com/evansiroky/timezone-boundary-builder/releases/tag/2018d>`__
* fixing minor issue #52 (shortcuts being out of bounds for extreme coordinate values)
* the list of polygon ids in each shortcut is sorted after freq. of appearance of their zone id.
    this is critical for ruling out zones faster (as soon as just polygons of one zone are left this zone can be returned)
* using argparse package now for parsing the command line arguments
* added option of choosing between functions timezone_at() and certain_timezone_at() on the command line with flag -f
* the timezone names are now being stored in a readable JSON file
* adjusted the main test cases
* corrections and clarifications in the readme and code comments


2.1.1 (2017-11-20)
------------------

* updated the data to `2017c <https://github.com/evansiroky/timezone-boundary-builder/releases/tag/2017c>`__
* minor improvements in code style and readme
* include publishing routine script


2.1.0 (2017-05-19)
------------------

* updated the data to `2017a <https://github.com/evansiroky/timezone-boundary-builder/releases/tag/2017a>`__ (tz_world is not being maintained any more)
* the file_converter has been updated to parse the new format of .json files
* the new data is much bigger (based on OSM Data, +40MB). I am sorry for this but its still better than small outdated data!
* in case size and speed matter more you than actuality, you can still check out older versions of timezonefinder(L)
* the new timezone polygons are not limited to the coastlines, but they are including some large parts of the sea. This makes the results of closest_timezone_at() somewhat meaningless (as with timezonefinderL).
* the polygons can not be simplified much more and as a consequence timezonefinderL is not being updated any more.
* simplification functions (used for compiling the data for timezonefinderL) have been deleted from the file_converter
* the readme has been updated to inform about this major change
* some tests have been temporarily disabled (with tzwhere still using a very old version of tz_world, a comparison does not make too much sense atm)

2.0.1 (2017-04-08)
------------------

* added missing package data entries (2.0.0 didn't include all necessary .bin files)


2.0.0 (2017-04-07)
------------------

* ATTENTION: major change!: there is a second version of timezonefinder now: `timezonefinderL <https://github.com/MrMinimal64/timezonefinderL>`__. There the data has been simplified
    for increasing speed reducing data size. Around 56% of the coordinates of the timezone polygons have been deleted there. Around 60% of the polygons (mostly small islands) have been included in the simplified polygons.
    For any coordinate on landmass the results should stay the same, but accuracy at the shorelines is lost.
    This eradicates the usefulness of closest_timezone_at() and certain_timezone_at() but the main use case for this package (= determining the timezone of a point on landmass) is improved.
    In this repo timezonefinder will still be maintained with the detailed (unsimplified) data.
* file_converter.py has been complemented and modified to perform those simplifications
* introduction of new function get_geometry() for querying timezones for their geometric shape
* added shortcuts_unique_id.bin for instantly returning an id if the shortcut corresponding to the coords only contains polygons of one zone
* data is now stored in separate binaries for ease of debugging and readability
* polygons are stored sorted after their timezone id and size
* timezonefinder can now be called directly as a script (experimental with reduced functionality, cf. readme)
* optimisations on point in polygon algorithm
* small simplifications in the helper functions
* clarification of the readme
* clarification of the comments in the code
* referenced the new conda-feedstock in the readme
* referenced the new timezonefinder API/GUI



1.5.7 (2016-07-21)
------------------


* ATTENTION: API BREAK: all functions are now keyword-args only (to prevent lng lat mix-up errors)
* fixed a little bug with too many arguments in a @jit function
* clarified usage of the package in the readme
* prepared the usage of the ahead of time compilation functionality of Numba. It is not enabled yet.
* sorting the order of polygons to check in the order of how often their zones appear, gives a speed bonus (for closest_timezone_at)


1.5.6 (2016-06-16)
------------------

* using little endian encoding now
* introduced test for checking the proper functionality of the helper functions
* wrote tests for proximity algorithms
* improved proximity algorithms: introduced exact_computation, return_distances and force_evaluation functionality (s. Readme or documentation for more info)

1.5.5 (2016-06-03)
------------------

* using the newest version (2016d, May 2016) of the `tz world data`_
* holes in the polygons which are stored in the tz_world data are now correctly stored and handled
* rewrote the file_converter for storing the holes at the end of the timezone_data.bin
* added specific test cases for hole handling
* made some optimizations in the algorithms

1.5.4 (2016-04-26)
------------------

* using the newest version (2016b) of the `tz world data`_
* rewrote the file_converter for parsing a .json created from the tz_worlds .shp
* had to temporarily fix one polygon manually which had the invalid TZID: 'America/Monterey' (should be 'America/Monterrey')
* had to make tests less strict because tzwhere still used the old data at the time and some results were simply different now


1.5.3 (2016-04-23)
------------------

* using 32-bit ints for storing the polygons now (instead of 64-bit): I calculated that the minimum accuracy (at the equator) is 1cm with the encoding being used. Tests passed.
* Benefits: 18MB file instead of 35MB, another 10-30% speed boost (depending on your hardware)


1.5.2 (2016-04-20)
------------------

* added python 2.7.6 support: replaced strings in unpack (unsupported by python 2.7.6 or earlier) with byte strings
* timezone names are now loaded from a separate file for better modularity


1.5.1 (2016-04-18)
------------------

* added python 2.7.8+ support:
    Therefore I had to change the tests a little bit (some operations were not supported). This only affects output.
    I also had to replace one part of the algorithms to prevent overflow in Python 2.7


1.5.0 (2016-04-12)
------------------

* automatically using optimized algorithms now (when numba is installed)
* added TimezoneFinder.using_numba() function to check if the import worked


1.4.0 (2016-04-07)
------------------

* Added the ``file_converter.py`` to the repository: It converts the .csv from pytzwhere to another ``.csv`` and this one into the used ``.bin``.
    Especially the shortcut computation and the boundary storage in there save a lot of reading and computation time, when deciding which timezone the coordinates are in.
    It will help to keep the package up to date, even when the timezone data should change in the future.


    .. _tz world data: <http://efele.net/maps/tz/world/>


