# It is strongly suggested to use a separate file to define the tiles of your process and then call them in your notebooks.
# it will help you to have control over their fonctionalities using object oriented programming

from sepal_ui import sepalwidgets as sw
import ipyvuetify as v
from sepal_ui.scripts.decorator import loading_button

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
        self.w_years = v.RangeSlider(
            label=cm.process.slider,
            v_model=[pm.min_year, pm.max_year],
            min=pm.min_year,
            max=pm.max_year,
            step=1,
            thumb_label="always",
            ticks=False,
        )

        self.type_tmf = v.RadioGroup(
            row=True,
            v_model=pm.layer_select[0]["value"],
            children=[
                v.Radio(key=e["key"], label=e["label"], value=e["value"])
                for e in pm.layer_select
            ],
        )

        # self.type_tmf.observe(self._on_change, 'v_model')

        # Create the alert alert
        self.model.bind(self.w_years, "years").bind(self.type_tmf, "type_tmf")

        # construct the Tile with the widget we have initialized
        super().__init__(
            id_="process_widget",  # the id will be used to make the Tile appear and disapear
            title=cm.process.title,  # the Title will be displayed on the top of the tile
            inputs=[self.w_years, self.type_tmf],
            btn=sw.Btn(cm.process.validate, "mdi-check", disabled=False, class_="ma-5"),
            alert=sw.Alert(),
        )

        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)

    # PROCESS AFTER ACTIVATING BUTTON
    @loading_button()
    def _on_run(self, widget, data, event):
        # check that the input that you're gonna use are set (Not mandatory)
        if not self.alert.check_input(self.aoi_model.name, cm.process.no_aoi):
            return
        if not self.alert.check_input(self.model.years, cm.process.no_year_beg):
            return

        # Create the mosaic
        dataset = cs.create(
            self.aoi_model.feature_collection,
            self.model.years,
            self.alert,
            self.model.type_tmf,
        )

        # change the model values as its a mutable object
        # useful if the model is used as an input in another tile
        self.model.dataset = dataset

        # release the export btn
        # self.result_tile.down_btn.disabled = False
        self.export_tile.asset_btn.disabled = False
        self.export_tile.sepal_btn.disabled = False

        # launch vizualisation
        # self.viz_tile._on_change(None)
        cs.display_result(
            self.aoi_model.feature_collection,
            self.model.dataset,
            self.viz_tile.m,
            self.model.years,
            self.model.type_tmf,
        )
        # conclude the computation with a message
        self.alert.add_live_msg(cm.process.end_computation, "success")
