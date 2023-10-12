import ipyvuetify as v
from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts.decorator import loading_button

from component import scripts
from component.message import cm
from component import parameter as pm


# the tiles should all be heriting from the sepal_ui Tile object
# if you want to create extra reusable object, you can define them in an extra widget.py file
class ExportTile(sw.Tile):
    def __init__(self, aoi_model, model, **kwargs):
        # gather the model
        self.aoi_model = aoi_model
        self.model = model

        self.scale = v.TextField(label=cm.export.scale, v_model=30)

        # create buttons
        self.asset_btn = sw.Btn(
            cm.export.asset_btn, "mdi-download", disabled=True, class_="ma-5"
        )
        self.sepal_btn = sw.Btn(
            cm.export.sepal_btn, "mdi-download", disabled=True, class_="ma-5"
        )

        # bindings
        self.model.bind(self.scale, "scale")

        # note that btn and alert are not a madatory attributes
        super().__init__(
            id_="export_widget",
            title=cm.export.title,
            inputs=[self.scale],
            alert=sw.Alert(),
            btn=v.Layout(row=True, children=[self.asset_btn, self.sepal_btn]),
        )

        # decorate the events

        self._on_asset_click = loading_button(alert=self.alert, button=self.asset_btn)(
            self._on_asset_click
        )

        self._on_sepal_click = loading_button(alert=self.alert, button=self.sepal_btn)(
            self._on_sepal_click
        )

        # link the btn
        self.asset_btn.on_event("click", self._on_asset_click)
        self.sepal_btn.on_event("click", self._on_sepal_click)

    def _on_asset_click(self, *args):
        dataset = self.model.dataset

        asset_id = scripts.export_to_asset(
            self.aoi_model,
            dataset,
            pm.asset_name(self.aoi_model, self.model),
            self.model.scale,
            self.alert,
        )

    def _on_sepal_click(self, *args):
        # get selected layers
        dataset = self.model.dataset

        if dataset:
            # export the results
            pathname = scripts.export_to_sepal(
                self.aoi_model,
                dataset,
                pm.asset_name(self.aoi_model, self.model),
                self.model.scale,
                self.alert,
            )
