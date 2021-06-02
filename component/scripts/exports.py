from pathlib import Path

import ee

from matplotlib import pyplot as plt

from component.message import cm
from component import parameter as pm

from .gee import *
from .gdrive import *
from .download import digest_tiles

ee.Initialize()


def export_to_asset(aoi_model, dataset, filename, scale, output):
    """
    Export the dataset as an asset in GEE
    
     Args: 
        aoi_model (sw.aoi_model): the aoi to clip on
        dataset (ee.Image): the image to export 
        filename (str): the name of the final file
        output (sw.Alert): the alert used to display informations to the end user
        
    return: 
        (str): asset link
        
    """
    # get the root folder of the user 
    folder = Path(ee.data.getAssetRoots()[0]['id'])
    asset_name = folder.joinpath(filename)
    
    # check if the asset already exist
    if is_asset(str(asset_name)):
        output.add_live_msg(cm.gee.asset_exist.format(asset_name), 'warning')
        return asset_name
    
    # launch the export
    task_config = {
        'image': dataset,
        'description': filename,
        'assetId': str(asset_name),
        'scale': int(scale), 
        'region': aoi_model.feature_collection.geometry(),
        'maxPixels': 1e13
    }
    
    task = ee.batch.Export.image.toAsset(**task_config)
    task.start()
       
    output.add_live_msg(cm.process.task_start.format(asset_name), 'success')
    
    # tell me if you want to display the exportation status live or not
    return asset_name


def export_to_sepal(aoi_model, dataset, filename, scale, output):
    """
    Export the dataset to gdrive and then to sepal. All buffer files will be deleted
    
    Args: 
        aoi_model (sw.aoi_model): the aoi to clip on
        dataset (ee.Image): the image to export 
        filename (str): the name of the final file
        output (sw.Alert): the alert used to display informations to the end user
        
    return: 
        (str): download pathname
        
    """
    # create the result_dir 
    pm.result_dir.mkdir(exist_ok=True)
    
    # create merge name 
    filename_merge = pm.result_dir.joinpath(f'{filename}_merge.tif')
    if filename_merge.is_file():
        output.add_live_msg(cm.download.file_exist.format(filename_merge), 'warning')
        return filename_merge
    
    output.add_live_msg(cm.download.start_download)
    
    # get the root folder of the user 
    folder = Path(ee.data.getAssetRoots()[0]['id'])
    asset_name = folder.joinpath(filename)
        
    # load the drive_handler
    drive_handler = gdrive()
    
    # clip the image
    dataset = dataset.clip(aoi_model.geature_collection)
        
    # download the tiled files
    downloads = drive_handler.download_to_disk(filename, dataset.int(), aoi_model, int(scale), output)
        
    # wait for the end of the download process
    if downloads:
        wait_for_completion([filename], output)
    output.add_live_msg(cm.gee.tasks_completed, 'success') 

    # digest the tiles
    digest_tiles(aoi_model, filename, pm.result_dir, output, filename_merge)
        
    output.add_live_msg(cm.download.remove_gdrive)
    # remove the files from drive
    drive_handler.delete_files(drive_handler.get_files(filename))
        
    # display msg 
    output.add_live_msg(cm.download.completed, 'success')

    return filename_merge
    
    