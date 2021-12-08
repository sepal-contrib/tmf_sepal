import time

import numpy as np
import pandas as pd
import ee
import ipyvuetify as v
from matplotlib import pyplot as plt

from component.message import cm
from component import parameter as pm

ee.Initialize()


def create(ee_aoi, year_beg, year_end, output, type_tmf):

    if type_tmf == "DEG":
        collection = ee.ImageCollection("projects/JRC/TMF/v1_2020/DegradationYear")
    elif type_tmf == "DEF":
        collection = ee.ImageCollection("projects/JRC/TMF/v1_2020/DeforestationYear")
    elif type_tmf == "CHG":
        collection = ee.ImageCollection("projects/JRC/TMF/v1_2020/AnnualChanges")

    # we call the collection and apply the pre-processing steps
    mosaic = collection.mosaic().clip(ee_aoi)

    # Option for change: combine both dates
    if type_tmf == "CHG":
        band_beg = year_beg - 1990
        band_end = year_end - 1990
        image = mosaic.select(ee.List.sequence(band_beg, band_end))
    else:
        mask = (
            mosaic.lte(ee.Number(year_end))
            .And(mosaic.gte(ee.Number(year_beg)))
            .selfMask()
        )
        image = mosaic.mask(mask)

    # let the user know that you managed to do something
    output.add_live_msg(cm.process.end_computation, "success")

    return image
