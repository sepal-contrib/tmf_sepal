# minimum year for TMF
min_year = 1990

# maximum year for the ALOS images 
max_year = 2019


layer_select = [
        {'key': 0, 'label': 'Degradation',   'value': 'DEG'},
        {'key': 1, 'label': 'Deforestation', 'value': 'DEF'},
        {'key': 2, 'label': 'Annual change', 'value': 'CHG'}
    ]


# name of the file in the output directory 
def asset_name(aoi_model, model):
    """return the standard name of your asset/file"""
 
    filename = f"tmf_{model.type_tmf}_{aoi_model.name}_{model.year_beg}_{model.year_end}"
    
    return filename