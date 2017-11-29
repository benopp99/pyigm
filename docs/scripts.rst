*************
pyigm Scripts
*************

There are a number of scripts, many of which are GUIs,
provided with pyigm.  As regards the GUIs we warn
again that Mac users will need to set their matplotlib to
something other than MacOSX. See
`backends <http://matplotlib.org/faq/usage_faq.html#what-is-a-backend>`__.

pyigm_igmguesses
----------------

GUI for examining IGM sightlines.
See `ref:igmguesses` for details.

pyigm_mkigmsys
--------------

Generate a simple JSON file for an IGM System.
Useful for things like the GUI lt_xabssys in `linetools`.

Here is the usage::

    usage: pyigm_mkigmsys [-h] [--NHI NHI] [--jcoord JCOORD] [--zem ZEM]
                          [--sigNHI SIGNHI] [--vlim VLIM]
                          itype zabs outfile

    Show contents of a JSON file, assuming one of several formats. (v1.1)

    positional arguments:
      itype            Type of IGMSystem: dla, lls, mgii
      zabs             Absorption redshift
      outfile          Name of JSON file to create

    optional arguments:
      -h, --help       show this help message and exit
      --NHI NHI        log10 NHI value
      --jcoord JCOORD  Coordinates in JXXXXXXXX.X+XXXXXX.X format
      --zem ZEM        Emission redshift
      --sigNHI SIGNHI  Error in NHI
      --vlim VLIM      Velocity limits in format ###,###


And an example::

    pyigm_mkigmsys dla 3.0 tmp.json --zem=4. --vlim=-232,300 --NHI=20.5 --sigNHI=0.2

pyigm_showjson
--------------

Simple script to give a brief summary of stuff in a
JSON file.  Best to use on an IGMSightline file.