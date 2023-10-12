import time

import rasterio as rio
from rasterio.merge import merge
from matplotlib.colors import to_rgba

from component.message import cm
from component import parameter as pm
from .gdrive import GDrive


def digest_tiles(aoi_io, filename, result_dir, output, final_path):
    if final_path.is_file():
        output.add_live_msg(cm.download.file_exist.format(final_path), "warning")
        time.sleep(2)
        return

    drive_handler = GDrive()
    files = drive_handler.get_files(filename)

    # if no file, it means that the download had failed
    if not len(files):
        raise Exception(cm.gdrive.error.no_file)

    drive_handler.download_files(files, result_dir)

    pathname = f"{filename}*.tif"

    files = [file for file in result_dir.glob(pathname)]

    # run the merge process
    output.add_live_msg(cm.download.merge_tile)
    time.sleep(2)

    #    # manual open and close because I don't know how many file there are
    #    sources = [rio.open(file) for file in files]
    #
    #    data, output_transform = merge(sources)
    #
    #    out_meta = sources[0].meta.copy()
    #    out_meta.update(nodata=0)
    #    out_meta.update(
    #        driver    = "GTiff",
    #        height    =  data.shape[1],
    #        width     =  data.shape[2],
    #        transform = output_transform,
    #        compress  = 'lzw'
    #   )
    #
    #   with rio.open(final_path, "w", **out_meta) as dest:
    #       dest.write(data)
    #
    #   # manually close the files
    #   [src.close() for src in sources]
    #
    #   # delete local files
    #   #[file.unlink() for file in files]

    return
