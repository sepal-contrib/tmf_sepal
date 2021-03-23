import time

import numpy as np
import pandas as pd
import ee
import ipyvuetify as v
from matplotlib import pyplot as plt

from component.message import cm
from component import parameter as pm

ee.Initialize()

def create(ee_aoi,year_beg,year_end,output,type_tmf):
    
    if   type_tmf == 'DEG':
        collection = ee.ImageCollection('projects/JRC/TMF/v1_2019/DegradationYear')
    elif type_tmf == 'DEF':
        collection = ee.ImageCollection('projects/JRC/TMF/v1_2019/DeforestationYear')
            
    # we call the collection and apply the pre-processing steps
    mosaic = collection.mosaic().clip(ee_aoi)

    image = mosaic.lte(year_end).gte(year_beg).updateMask(mosaic)
    
    # let the user know that you managed to do something
    output.add_live_msg(cm.process.end_computation, 'success')
    
    return image



    

