# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v
from sepal_ui.scripts import utils as su

from component import scripts as cs
from component.message import cm
from component import parameter as pm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class ProcessTile(sw.Tile):
    
    def __init__(self, model, aoi_model, viz_tile, export_tile, **kwargs):
        
        # Define the model and the aoi_model as class attribute so that they can be manipulated in its custom methods
        self.model = model 
        self.aoi_model = aoi_model
        
        # LINK to the result tile 
        self.viz_tile = viz_tile
        self.export_tile = export_tile
        
        # WIDGETS
        self.year_beg   = v.Select(
            label   = cm.process.slider_b,
            v_model = None,
            items   = [i for i in range(pm.max_year, pm.min_year-1, -1)]
        )
        
        self.year_end   = v.Select(
            label   = cm.process.slider_e,
            v_model = None,
            items   = [i for i in range(pm.max_year, pm.min_year-1, -1)]
        )
        
        self.type_tmf = v.RadioGroup(
            row=True,
            v_model = pm.layer_select[0]['value'],
            children = [v.Radio(key=  e['key'], 
                                label=e['label'], 
                                value=e['value']) for e in pm.layer_select]
        )
        
        #self.type_tmf.observe(self._on_change, 'v_model')
                
        # Create the alert alert 
        self.model \
            .bind(self.year_beg, 'year_beg')  \
            .bind(self.year_end, 'year_end')  \
            .bind(self.type_tmf, 'type_tmf')
         
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "process_widget", # the id will be used to make the Tile appear and disapear
            title  = cm.process.title, # the Title will be displayed on the top of the tile
            inputs = [self.year_beg,self.year_end,self.type_tmf], 
            btn    = sw.Btn(cm.process.validate, 'mdi-check', disabled=False, class_='ma-5'),
            alert = sw.Alert()
        )
                
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event('click', self._on_run)
        
    # PROCESS AFTER ACTIVATING BUTTON
    @su.loading_button(debug=False)
    def _on_run(self, widget, data, event): 

        # check that the input that you're gonna use are set (Not mandatory)
        if not self.alert.check_input(self.aoi_model.name, cm.process.no_aoi): return
        if not self.alert.check_input(self.model.year_beg, cm.process.no_year_beg): return
        if not self.alert.check_input(self.model.year_end, cm.process.no_year_end): return

        # Create the mosaic
        dataset = cs.create(
            self.aoi_model.feature_collection,
            self.model.year_beg,
            self.model.year_end,
            self.alert,
            self.model.type_tmf
        )

        # change the model values as its a mutable object 
        # useful if the model is used as an input in another tile
        self.model.dataset = dataset

        # release the export btn
        #self.result_tile.down_btn.disabled = False
        self.export_tile.asset_btn.disabled = False
        self.export_tile.sepal_btn.disabled = False

        # conclude the computation with a message
        self.alert.add_live_msg(cm.process.end_computation, 'success')

        # launch vizualisation
        #self.viz_tile._on_change(None)
        cs.display_result(
            self.aoi_model.feature_collection,
            self.model.dataset,
            self.viz_tile.m, 
            self.model.year_beg,
            self.model.year_end,
            self.model.type_tmf
        )

        return
        
        