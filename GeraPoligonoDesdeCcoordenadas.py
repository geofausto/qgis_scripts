"""
Gerar Polígono desde Coordenadas (Processing algorithm)

Gera um polígono retangular a partir dos limites xmin,ymin,xmax,ymax e retorna como camada de saída.
"""

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterCrs,
    QgsProcessingParameterFeatureSink,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingException,
    QgsFeature,
    QgsFields,
    QgsField,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateReferenceSystem,
)
from qgis.PyQt.QtCore import QVariant


class GeraPoligonoDesdeCoordenadasAlgorithm(QgsProcessingAlgorithm):
    COORDS = 'COORDS'
    CRS = 'CRS'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString(self.COORDS, 'Coordinates (xmin,ymin,xmax,ymax)', defaultValue='-57.40184023,-11.69750297,-57.36150352,-11.65855717'))
        self.addParameter(QgsProcessingParameterCrs(self.CRS, 'CRS', defaultValue=QgsCoordinateReferenceSystem('EPSG:4326')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, 'Output polygon layer'))

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
        coords_str = self.parameterAsString(parameters, self.COORDS, context)
        parts = [p.strip() for p in coords_str.split(',') if p.strip() != '']
        if len(parts) != 4:
            raise QgsProcessingException('Expected 4 comma-separated values: xmin,ymin,xmax,ymax')
        try:
            xmin, ymin, xmax, ymax = map(float, parts)
        except ValueError:
            raise QgsProcessingException('Coordinate values must be numeric')
        crs = self.parameterAsCrs(parameters, self.CRS, context)

        fields = QgsFields()
        fields.append(QgsField('id', QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            QgsWkbTypes.Polygon,
            crs,
        )

        ring = [
            QgsPointXY(xmin, ymin),
            QgsPointXY(xmax, ymin),
            QgsPointXY(xmax, ymax),
            QgsPointXY(xmin, ymax),
            QgsPointXY(xmin, ymin),
        ]

        feat = QgsFeature()
        feat.setFields(fields)
        feat.setAttribute('id', 1)
        feat.setGeometry(QgsGeometry.fromPolygonXY([ring]))

        sink.addFeature(feat, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}

    def name(self):
        return 'gera_poligono_desde_coordenadas'

    def displayName(self):
        return 'Gerar Polígono desde Coordenadas'

    def group(self):
        return 'geofausto'

    def groupId(self):
        return 'geofausto'

    def shortHelpString(self):
        return 'Gera um polígono retangular a partir de xmin,ymin,xmax,ymax.'

    def createInstance(self):
        return GeraPoligonoDesdeCoordenadasAlgorithm()