"""
***************************************************************************
*                                                                         *
*   Script to export selected layers in QGIS                              *
*   Adapted for the Processing Framework                                  *
*                                                                         *
***************************************************************************
"""

from typing import Any, Optional
import os

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterFile,
    QgsProcessingParameterEnum,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.utils import iface  # Required to access selected layers


class ExportSelectedLayersToShp(QgsProcessingAlgorithm):
    """
    Processing algorithm to export selected layers in QGIS,
    allowing the user to choose whether the output filename
    is based on the layer name or the data source name.
    """

    OUTPUT_FOLDER = "OUTPUT_FOLDER"
    FILENAME_BASE = "FILENAME_BASE"

    def initAlgorithm(self, config: Optional[dict[str, Any]] = None):
        """
        Define the algorithm parameters.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_FOLDER,
                "Output folder",
                behavior=QgsProcessingParameterFile.Folder,  # Set as folder
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.FILENAME_BASE,
                "Use as filename:",
                options=["Layer Name", "Data Source Name"],
                defaultValue=0,  # Default to "Layer Name"
            )
        )

    def processAlgorithm(
        self,
        parameters: dict[str, Any],
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ) -> dict[str, Any]:
        """
        Main processing function.
        """

        # Get the output folder
        output_folder = self.parameterAsString(parameters, self.OUTPUT_FOLDER, context)

        # Get the user-selected filename option
        filename_option = self.parameterAsEnum(parameters, self.FILENAME_BASE, context)

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            feedback.pushInfo(f"Output folder created: {output_folder}")

        # Get the selected layers correctly
        selected_layers = [
            layer for layer in iface.layerTreeView().selectedLayers()
            if isinstance(layer, QgsVectorLayer)
        ]

        # If no vector layers are selected, abort
        if not selected_layers:
            feedback.pushWarning("No vector layers selected for export.")
            return {}

        # Iterate over the selected layers and export each one
        for layer in selected_layers:
            if filename_option == 0:
                # Option "Layer Name"
                filename_base = layer.name()
            else:
                # Option "Data Source Name"
                filename_base = self.get_source_name(layer)

            output_filename = os.path.join(output_folder, f"{filename_base}.shp")

            error = QgsVectorFileWriter.writeAsVectorFormat(
                layer, output_filename, "UTF-8", layer.crs(), "ESRI Shapefile"
            )

            if error[0] == QgsVectorFileWriter.NoError:
                feedback.pushInfo(f"✅ Layer {layer.name()} exported as {output_filename}")
            else:
                feedback.pushWarning(f"❌ Error exporting {layer.name()}: {error[1]}")

        return {}

    def get_source_name(self, layer: QgsVectorLayer) -> str:
        """
        Retrieves the data source name:
        - For GeoPackage, it returns the table name.
        - For other file formats, it returns the filename without extension.
        """
        source = layer.source()

        # If it's a GeoPackage
        if ".gpkg|" in source:
            table_name = source.split("table=")[-1]
            return table_name

        # If it's a file (SHP, CSV, etc.), get the filename without extension
        elif source.startswith("/") or source.startswith("C:"):
            return os.path.splitext(os.path.basename(source))[0]

        # If no valid source is found, return the layer name as a fallback
        return layer.name()

    def name(self) -> str:
        return "export_selected_layers"

    def displayName(self) -> str:
        return "Export selected sayers to .shp"

    def group(self) -> str:
        return "My Scripts"

    def groupId(self) -> str:
        return "my_scripts"

    def shortHelpString(self) -> str:
        return (
            "Exports all currently selected vector layers as .shp files in a specified folder.\n"
            "Allows choosing between using the layer name in QGIS or the data source name (e.g., table from GPKG or original SHP filename)."
        )

    def createInstance(self):
        return ExportSelectedLayersToShp()
