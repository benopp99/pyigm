#!/usr/bin/env python

"""
Script to show the contents of a JSON file
"""

import pdb
 
try:
    ustr = unicode
except NameError:
    ustr = str

def parser(options=None):
    import argparse
    # Parse
    parser = argparse.ArgumentParser(
        description='Show contents of a JSON file, assuming one of several formats.')
    parser.add_argument("jsonfile", help="Name of JSON file")
    #parser.add_argument("--epoch", default=2000., type=float, help="Epoch [Not functional]")

    if options is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(options)
    return args

def main(args=None):
    from linetools import utils as ltu

    pargs = parser()
    # Read
    jdict = ltu.loadjson(pargs.jsonfile)

    if 'class' not in jdict.keys():
        raise KeyError("This script only works with JSON files with named classes")
    if jdict['class'] == 'IGMSightline':
        from pyigm.igm.igmsightline import IGMSightline
        obj = IGMSightline.from_dict(jdict)
        flg_tbl = True
    elif jdict['class'] == 'DLASystem':
        from pyigm.abssys.dla import DLASystem
        obj = DLASystem.from_dict(jdict)
        flg_tbl = False
    elif jdict['class'] == 'LLSSystem':
        from pyigm.abssys.lls import LLSSystem
        obj = LLSSystem.from_dict(jdict)
        obj.fill_ionN()
        flg_tbl = True  # Column density table
    else:
        raise IOError("Not prepared for this class: {:s}".format(jdict['class']))

    # name
    try:
        name = jdict['name']
    except KeyError:
        try:
            name = jdict['Name']
        except:
            name = 'None'
    print("Name of object: {:s}".format(name))

    # Generate table
    if flg_tbl:
        if jdict['class'] == 'IGMSightline':
            tbl = obj.build_table()
        elif jdict['class'] == 'LLSSystem':
            tbl = obj._ionN
            tbl['logN'].format = '5.2f'
            tbl['sig_logN'].format = '5.2f'
            tbl['vmin'].format = '8.1f'
            tbl['vmax'].format = '8.1f'
        else:
            tbl = None
        # Print
        if len(tbl) > 0:
            tbl.pprint(99999, max_width=120)
        else:
            print("Table was empty..")


