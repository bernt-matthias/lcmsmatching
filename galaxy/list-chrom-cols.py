#!/usr/bin/env python

import argparse
import subprocess
import re
import urllib2
import json
import csv

def get_chrom_cols(dbtype, dburl, dbtoken = None, dbfields = None):
    
    cols = []
    
    if dbtype == 'peakforest':
        url = dburl + ( dburl[-1] == '/' ? '' : '/' ) + 'metadata/lc/list-code-columns'
        if dbtoken is not None:
            url += '?token=' + dbtoken
        result = urllib2.urlopen(url).read()
        v = json.JSONDecoder().decode(result)
        i = 0
        for colid, coldesc in v.iteritems():
            cols.append( (coldesc['name'], colid, i == 0) )
            ++i
        
    elif dbtype == 'inhouse':
        # Get field for chromatographic column name
        col_field = 'col'
        if dbfields is not None:
            fields = dict(u.split("=") for u in dbfields.split(","))
            if 'col' in fields:
                col_field = fields['col']
                
        # Get all column names from file
        with open(dburl, 'rb') as dbfile:
            reader = csv.reader(dbfile, delimiter = "\t", quotechar='"')
            header = reader.next()
            i = header.index(col_field)
            allcols = []
            for row in reader:
                col = row[i]
                if col not in allcols:
                    allcols.append(col)
            for i, c in enumerate(allcols):
                cols.append( (c, c, i == 0) )
    
    return cols

########
# MAIN #
########

if __name__ == '__main__':
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for getting chromatographic columns of an RMSDB database for Galaxy tool lcmsmatching.')
    parser.add_argument('-d', help = 'Database type',       dest = 'dbtype',    required = True)
    parser.add_argument('-u', help = 'Database URL',        dest = 'dburl',     required = True)
    parser.add_argument('-t', help = 'Database token',      dest = 'dbtoken',   required = False)
    parser.add_argument('-f', help = 'Database fields',     dest = 'dbfields',  required = False)
    args = parser.parse_args()
    args_dict = vars(args)
    
    print(get_chrom_cols(**args_dict))
