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

import numpy as np



def robinson(lon,lat):
    """
    Returns a Robinson projection
    
    Parameters
    ----------
    lon : number or np.array
        longitude in degrees
        
    lat : number or np.array
        latitude in degrees

    Notes
    -----
    https://en.wikipedia.org/wiki/Robinson_projection
    
    """
    
    table_lat  = np.array([0.    ,5.    ,10.   ,15.   ,20.   ,25.   ,30.   ,35.   ,40.   ,45.   ,50.   ,55.   ,60.   ,65.   ,70.   ,75.   ,80.   ,85.   ,90.   ])
    table_plen = np.array([1.0000,0.9986,0.9954,0.9900,0.9822,0.9730,0.9600,0.9427,0.9216,0.8962,0.8679,0.8350,0.7986,0.7597,0.7186,0.6732,0.6213,0.5722,0.5322])
    table_pdfe = np.array([0.0000,0.0620,0.1240,0.1860,0.2480,0.3100,0.3720,0.4340,0.4958,0.5571,0.6176,0.6769,0.7346,0.7903,0.8435,0.8936,0.9394,0.9761,1.0000])*0.5072
    
    plen = np.interp(abs(lat),table_lat,table_plen)
    pdfe = np.interp(abs(lat),table_lat,table_pdfe)
    
    x = lon/180.*plen
    y = np.sign(lat)*pdfe
    
    return x,y
    
    
def wagnerVI(lon,lat):
    """
    Returns a Robinson projection
    
    Parameters
    ----------
    lon : number or np.array
        longitude in degrees
        
    lat : number or np.array
        latitude in degrees

    Notes
    -----
    https://en.wikipedia.org/wiki/Robinson_projection
    
    """

    x = lon*(1.-3.*(lat/180.)**2)**0.5
    y = lat/90  
    
    
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    lat = np.hstack(( np.linspace(-90,90,30) , 90.*np.ones(30)         , np.linspace(90,-90,30), -90.*np.ones(30)         ))
    lon = np.hstack(( 180.*np.ones(30)       , np.linspace(180,-180,30), -180.*np.ones(30)     , np.linspace(-180,180,30) ))
 
    x,y = robinson(lon,lat)
    
    plt.plot(x,y)
    plt.xlim([-1,1])
    plt.axes().set_aspect('equal')
    plt.show()