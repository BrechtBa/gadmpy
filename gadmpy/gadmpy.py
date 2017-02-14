#!/usr/bin/env/ python
################################################################################
#    Copyright (c) 2017 Brecht Baeten
#    This file is part of gadmpy.
#    
#    Permission is hereby granted, free of charge, to any person obtaining a
#    copy of this software and associated documentation files (the "Software"), 
#    to deal in the Software without restriction, including without limitation 
#    the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#    and/or sell copies of the Software, and to permit persons to whom the 
#    Software is furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in 
#    all copies or substantial portions of the Software.
################################################################################

import os
import sys
import zipfile
import shapefile

if sys.version_info < (3, ):
    import urllib as request
else: 
    import urllib.request as request

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
   
data_path = os.path.join( os.path.dirname(os.path.realpath(__file__)),'data')


# reads country codes from a tab spaced file copied from wikipedia
# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
countrycodes_ISO_3166_1_3 = {}
with open(os.path.join(data_path,'countrycodes_ISO_3166_1_3.dat'),'r') as f:
    for l in f:
        s = l.split('\t')
        if len(s) == 2:
            countrycodes_ISO_3166_1_3[s[1].rstrip()] = s[0]

# reads country codes from a tab spaced file copied from wikipedia
# https://en.wikipedia.org/wiki/ISO_3166-2
countrycodes_ISO_3166_1_2 = {}
with open(os.path.join(data_path,'countrycodes_ISO_3166_1_2.dat'),'r') as f:
    for l in f:
        s = l.split('\t')
        if len(s) == 3:
            countrycodes_ISO_3166_1_2[s[1].rstrip()] = s[0]


            
def download_shapefiles(countrycode,level=0,force=False,verbose=0):            
    """
    Downloads a shapefile from gadm to the data/shapefiles folder
    
    Parameters
    ----------
    countrycode : str
        Three letter ISO 3166-1 alpha-3 country code
        
    level : int
        Administrative level 0-5
        
    force : boolean
        Set to true to force the download and overwrite existing files
        
    verbose : int
        Specify output printing during the process
        
    """
    
    shpname = '{}_adm{}.shp'.format(countrycode,level)
    shxname = '{}_adm{}.shx'.format(countrycode,level)
    dbfname = '{}_adm{}.dbf'.format(countrycode,level)
    
    # all extensions in the zip file are:
    # '.cpg','.csv','.dbf','.prj','.shp','.shx'
    
    unzip = False
    for filename in [shpname,shxname,dbfname]:
        if force or not os.path.isfile( os.path.join(data_path,'shapefiles',format(filename)) ):
            unzip = True
            break
            
    if unzip:
        zipname = '{}_adm_shp.zip'.format(countrycode)
        zippath = os.path.join(data_path,'shapefiles',zipname)
        if force or not os.path.isfile( zippath ):
            # download the file
            # http://biogeo.ucdavis.edu/data/gadm2.8/shp/DZA_adm_shp.zip
            url = 'http://biogeo.ucdavis.edu/data/gadm2.8/shp/{}'.format(zipname)
            if verbose > 0:
                print('downloading shapefile for {} from:\n {}'.format(countrycode,url))
                    
            try:
                request.urlretrieve(url, zippath)
            except:
                raise Exception('Could not download the shp file from {}'.format(url))

        # unzip
        if verbose > 0:
            print('unzipping files')
                
        with zipfile.ZipFile(zippath, 'r') as zfile:
            for filename in [shpname,shxname,dbfname]:
                zfile.extract(filename, os.path.join(data_path,'shapefiles'))

        if verbose > 0:
            print('done')
        

def shapefile_coordinates(countrycode,level=0):
    """
    Creates a list of patches from a shapefile specified by the country code and
    administrative level
    
    Parameters
    ----------
    countrycode : str
        Three letter ISO 3166-1 alpha-3 country code
        
    level : int
        Administrative level 0-5
    
    """
    
    filename = os.path.join(data_path,'shapefiles','{}_adm{}'.format(countrycode,level))

    for ext in ['.shp','.shx','.dbf']:
        if not os.path.isfile( filename+ext ):
            raise Exception('Could not find shapefiles, download the first using the download_shapefiles function: download_shapefiles(\'{}\',{})'.format(countrycode,level))

    sf = shapefile.Reader(filename)
    shapes  = sf.shapes()
    
    coords = []
 
    
    for shape in shapes:
        parts = shape.parts
        parts.append(len(shape.points)-1)
    
        dxdy_lim = 1

        sub_coords = []

        for i in range(len(parts)-1):
            xi = [shape.points[j][0] for j in range(parts[i],parts[i+1]) ]
            yi = [shape.points[j][1] for j in range(parts[i],parts[i+1]) ]

            # remove very small shapes
            if max(xi)-min(xi) > 1 or max(yi)-min(yi) > dxdy_lim:
            
                # remove points that are close together
                si = np.cumsum( [0] + [( (xi[j]-xi[j+1])**2 + (yi[j]-yi[j+1])**2)**0.5  for j in range(len(xi)-1)] )

                if len(si) > 100:
                    xi = np.interp(np.linspace(0,max(si),max(100,int(len(si)/1000))), si,xi)
                    yi = np.interp(np.linspace(0,max(si),max(100,int(len(si)/1000))), si,yi)
                    
                sub_coords.append((xi,yi))    
                
        coords.append(sub_coords)    

    return coords
    
    
def create_world_outline(ax,projection=None,facecolor='none',edgecolor='k',linewidth=0.2):
    """
    """
    # input handling
    if projection is None:
        projection = lambda lon,lat: (lon/180.,lat/90.)
        
    lat = np.hstack(( np.linspace(-90,90,30) , 90.*np.ones(30)         , np.linspace(90,-90,30), -90.*np.ones(30)         ))
    lon = np.hstack(( 180.*np.ones(30)       , np.linspace(180,-180,30), -180.*np.ones(30)     , np.linspace(-180,180,30) ))
    
    

    patches = [ Polygon( [projection(lo,la) for lo,la in zip(lon,lat)] ) ]
    p = PatchCollection(patches, facecolor=facecolor, edgecolor=edgecolor, linewidths=linewidth)
    ax.add_collection(p)
    
    return p
    
    
def create_map(ax,coordinates,projection=None,facecolors='#222222',edgecolors='k',linewidths=0.2):
    """
    """

    # input handling
    if projection is None:
        projection = lambda lon,lat: (lon/180.,lat/90.)
    
    if len(facecolors) == 3 and not len(coordinates) == 3:
        facecolors = [facecolors]*len(coordinates)
    if len(facecolors) == 4 and not len(coordinates) == 4:
        facecolors = [facecolors]*len(coordinates)
    if not hasattr(facecolors, '__iter__'):
        facecolors = [facecolors]*len(coordinates)
    
    if len(edgecolors) == 3 and not len(coordinates) == 3:
        edgecolors = [edgecolors]*len(coordinates)
    if len(edgecolors) == 4 and not len(coordinates) == 4:
        edgecolors = [edgecolors]*len(coordinates)    
    if not hasattr(edgecolors, '__iter__'):
        edgecolors = [edgecolors]*len(coordinates)
        
    if not hasattr(linewidths, '__iter__'):
        linewidths = [linewidths]*len(coordinates)
        
    patchcollections = []
    for coords,f,e,l in zip(coordinates,facecolors,edgecolors,linewidths):
        
        if not hasattr(coords, '__iter__'):
            coords = [coords]
    
        patches = []
        for sub_coords in coords:
            for part in sub_coords:
                patches.append( Polygon( [projection(lon,lat) for lon,lat in zip(part[0],part[1])] ) )
            
        p = PatchCollection(patches, facecolor=f, edgecolor=e, linewidths=l)
        ax.add_collection(p)
        patchcollections.append(p)
        
    return patchcollections