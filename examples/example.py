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

import gadmpy
import numpy as np
import matplotlib.pyplot as plt

countrycodes = [c for c in gadmpy.countrycodes_ISO_3166_1_3.values()]
facecolors = plt.cm.viridis(np.linspace(0,1,len(countrycodes)))
coords = {}

print('###   Loading coordinates   ###')
for countrycode in countrycodes:
    gadmpy.download_shapefiles(countrycode,verbose=1)
    coords[countrycode] =  gadmpy.shapefile_coordinates(countrycode)
    
    
    
print('###   Plotting map   ###')
fig, ax = plt.subplots()
gadmpy.create_world_outline( ax,projection=gadmpy.projection.robinson )
gadmpy.create_map( ax,[c for c in coords.values()], facecolors=facecolors, projection=gadmpy.projection.robinson )
ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
plt.savefig('countries.pdf')
plt.show()
