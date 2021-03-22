# minimum year for TMF
min_year = 1990

# maximum year for the ALOS images 
max_year = 2019


layer_select = [
        {'key': 0, 'label': 'Degradation',   'value': 'DEG'},
        {'key': 1, 'label': 'Deforestation', 'value': 'DEF'},
        #{'key': 2, 'label': 'Change Map',    'value': 'CHG'}
    ]


# name of the file in the output directory 
def asset_name(aoi_io, io):
    """return the standard name of your asset/file"""
 
    filename = f"tmf_{io.type_tmf}_{aoi_io.get_aoi_name()}_{io.year_beg}_{io.year_end}"
    return filename