import ee
import ipyvuetify as v

from component.message import cm
from component import parameter as cp


ee.Initialize()

def display_result(ee_aoi, dataset, m, year_beg, year_end):
    """
    Display the results on the map 
    
    Args:
        ee_aoi: (ee.Geometry): the geometry of the aoi
        dataset (ee.Image): the image the display
        m (sw.SepalMap): the map used for the display
        db (bool): either to use the db scale or not
        
    Return:
        (sw.SepalMap): the map with the different layers added
    """
    # AOI borders in blue 
    empty   = ee.Image().byte()
    outline = empty.paint(featureCollection = ee_aoi, color = 1, width = 3)
   
    # Zoom to AOI
    m.zoom_ee_object(ee_aoi.geometry())
    
    cp.viz_param.update(
        min = year_beg,
        max = year_end
    )
        
    # Add objects
    m.addLayer(outline, {'palette': v.theme.themes.dark.info}, 'aoi')
    m.addLayer(dataset, cp.viz_param, cm.process.product) 
    
    return