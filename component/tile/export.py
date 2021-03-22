# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts
from component.message import cm
from component import parameter as pm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class ExportTile(sw.Tile):
    
    def __init__(self, aoi_io, io, **kwargs):

        # gather the io
        self.aoi_io = aoi_io
        self.io = io

        # create an output alert 
        self.output = sw.Alert()

        self.scale = v.TextField(
            label   = cm.export.scale,
            v_model = 30
        )
        
        
        # create buttons
        self.asset_btn = sw.Btn(cm.export.asset_btn, 'mdi-download', disabled=True, class_='ma-5')
        self.sepal_btn = sw.Btn(cm.export.sepal_btn, 'mdi-download', disabled=True, class_='ma-5')
        #self.download_image = sw.DownloadBtn(ms.export.down_btn)

        # bindings
        self.output = sw.Alert() \
            .bind(self.scale, self.io, 'scale') \

        # note that btn and output are not a madatory attributes 
        super().__init__(
            id_ = "export_widget",
            title = cm.export.title,
            inputs = [self.scale],
            output = self.output,
            btn = v.Layout(row=True, children = [self.asset_btn, self.sepal_btn])
        )

        #link the btn 
        self.asset_btn.on_event('click', self._on_asset_click)
        self.sepal_btn.on_event('click', self._on_sepal_click)

    def _select_layers(self):
        
        dataset = self.io.dataset#.select(['HH', 'HV', 'HHHV_ratio'])
        return dataset
        
    def _on_asset_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        dataset = self._select_layers()
        
        #try:
        # export the results
        
        if dataset: 
            asset_id = scripts.export_to_asset(
                self.aoi_io, 
                dataset, 
                pm.asset_name(self.aoi_io, self.io),
                self.io.scale,
                self.output
            )


        #except Exception as e:
        #    self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        self.sepal_btn.toggle_loading()
        
        return
    
    def _on_sepal_click(self, widget, data, event):
        
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        # get selected layers
        dataset = self._select_layers()
        
        try:
            
            if dataset:
                # export the results 
                pathname = scripts.export_to_sepal(
                    self.aoi_io, 
                    dataset, 
                    pm.asset_name(self.aoi_io, self.io), 
                    self.io.scale, 
                    self.output
                )
            
                
            # link it in the download btn 
            #self.download_image.set_url(str(pathname))
            #self.download_image.set_url(str(pathname_fnf))
        
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
            
        widget.toggle_loading()
        self.asset_btn.toggle_loading()
        
        return