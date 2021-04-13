# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks. 
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v

from component import scripts as cs
from component.message import cm
from component import parameter as pm

# the tiles should all be heriting from the sepal_ui Tile object 
# if you want to create extra reusable object, you can define them in an extra widget.py file 
class ProcessTile(sw.Tile):
    
    def __init__(self, io, aoi_io, viz_tile,export_tile, **kwargs):
        
        # Define the io and the aoi_io as class attribute so that they can be manipulated in its custom methods
        self.io = io 
        self.aoi_io = aoi_io
        
        # LINK to the result tile 
        #self.result_tile = result_tile
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
            v_model = pm.layer_select[0]['value'],
            children = [v.Radio(key=  e['key'], 
                                label=e['label'], 
                                value=e['value']) for e in pm.layer_select]
        )
        
        #self.type_tmf.observe(self._on_change, 'v_model')
                
        # Create the output alert 
        self.output = sw.Alert() \
            .bind(self.year_beg,self.io,'year_beg')  \
            .bind(self.year_end,self.io,'year_end')  \
            .bind(self.type_tmf,self.io,'type_tmf')
        
        # Button to Launch Process)
        self.btn =  sw.Btn(cm.process.validate, 'mdi-check', disabled=False, class_='ma-5')
        
        # construct the Tile with the widget we have initialized 
        super().__init__(
            id_    = "process_widget", # the id will be used to make the Tile appear and disapear
            title  = cm.process.title, # the Title will be displayed on the top of the tile
            inputs = [self.year_beg,self.year_end,self.type_tmf], 
            btn    = self.btn,
            output = self.output
        )
                
        # now that the Tile is created we can link it to a specific function
        self.btn.on_event('click', self._on_run)
        
    # PROCESS AFTER ACTIVATING BUTTON
    def _on_run(self, widget, data, event): 
            
        # toggle the loading button (ensure that the user doesn't launch the process multiple times)
        widget.toggle_loading()

        # check that the input that you're gonna use are set (Not mandatory)
        if not self.output.check_input(self.aoi_io.get_aoi_name(), cm.process.no_aoi):       return widget.toggle_loading()
        if not self.output.check_input(self.io.year_beg,           cm.process.no_year_beg):  return widget.toggle_loading()
        if not self.output.check_input(self.io.year_end,           cm.process.no_year_end):  return widget.toggle_loading()
        #if not self.output.check_input(self.io.asset,              cm.process.no_textfield): return widget.toggle_loading()


        # Wrap the process in a try/catch statement 
        try:

            # Create the mosaic
            dataset = cs.create(
                self.aoi_io.get_aoi_ee(),
                self.io.year_beg,
                self.io.year_end,
                self.output,
                self.io.type_tmf
            )

            # change the io values as its a mutable object 
            # useful if the io is used as an input in another tile
            self.io.dataset = dataset

            # release the export btn
            #self.result_tile.down_btn.disabled = False
            self.export_tile.asset_btn.disabled = False
            self.export_tile.sepal_btn.disabled = False

            # conclude the computation with a message
            self.output.add_live_msg(cm.process.end_computation, 'success')

            # launch vizualisation
            #self.viz_tile._on_change(None)
            cs.display_result(
                self.aoi_io.get_aoi_ee(),
                self.io.dataset,
                self.viz_tile.m, 
                self.io.year_beg,
                self.io.year_end,
                self.io.type_tmf
        )

        except Exception as e: 
            self.output.add_live_msg(str(e), 'error')

        # release the btn
        widget.toggle_loading()

        return
        
        