import ee
import ipyvuetify as v

from component.message import cm
from component import parameter as cp


ee.Initialize()


def display_result(ee_aoi, dataset, m, years, type_tmf):
    """Display the results on the map

    Args:
        ee_aoi: (ee.Geometry): the geometry of the aoi
        dataset (ee.Image): the image the display
        m (sw.SepalMap): the map used for the display
        db (bool): either to use the db scale or not

    Return:
        (sw.SepalMap): the map with the different layers added
    """

    year_beg, year_end = years

    # AOI borders in blue
    empty = ee.Image().byte()
    outline = empty.paint(featureCollection=ee_aoi, color=1, width=3)

    # Zoom to AOI
    m.zoom_ee_object(ee_aoi.geometry())

    cp.viz_paramDD.update(min=year_beg, max=year_end)

    cp.viz_paramCH.update(
        bands=["Dec" + str(year_beg), "Dec" + str(year_beg), "Dec" + str(year_end)]
    )

    if type_tmf == "DEG":
        vizParam = cp.viz_paramDD
    elif type_tmf == "DEF":
        vizParam = cp.viz_paramDD
    elif type_tmf == "CHG":
        vizParam = cp.viz_paramCH

    # Add objects
    m.addLayer(outline, {"palette": v.theme.themes.dark.info}, "aoi")
    m.addLayer(dataset, vizParam, cm.process.product)

    return
