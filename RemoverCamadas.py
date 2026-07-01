from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProject,
)

from qgis.PyQt.QtWidgets import (
    QDialog,
    QListWidget,
    QVBoxLayout,
    QPushButton,
)


class LayerRemovalDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Remove Layers")
        self.setFixedSize(440, 380)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)

        self.populate_layers()
        layout.addWidget(self.list_widget)

        btn_remove = QPushButton("Remove Selected")
        btn_remove.clicked.connect(self.remove_selected_layers)
        layout.addWidget(btn_remove)

        self.setLayout(layout)

    def populate_layers(self):
        self.list_widget.clear()

        for layer in QgsProject.instance().mapLayers().values():
            epsg_code = layer.crs().authid()
            display_text = f"{layer.name()} [{epsg_code}]"
            self.list_widget.addItem(display_text)

    def remove_selected_layers(self):
        selected_items = [
            item.text().split(" [")[0]
            for item in self.list_widget.selectedItems()
        ]

        for layer_name in selected_items:
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if layers:
                QgsProject.instance().removeMapLayer(layers[0].id())

        # Atualiza lista
        self.populate_layers()


class RemoverCamadasAlgorithm(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        # Sem parâmetros — é um algoritmo interativo
        pass

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):

        dlg = LayerRemovalDialog()
        dlg.exec_()

        return {}

    def name(self):
        return 'remover_camadas'

    def displayName(self):
        return 'Remover Camadas (Interativo)'

    def group(self):
        return 'geofausto'

    def groupId(self):
        return 'geofausto'

    def shortHelpString(self):
        return 'Abre um diálogo para remover múltiplas camadas do projeto.'

    def createInstance(self):
        return RemoverCamadasAlgorithm()