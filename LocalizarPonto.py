"""
Localizar Ponto (Processing algorithm)

Cria uma camada pontual com a coordenada fornecida e retorna como saída.
"""

from qgis.core import (
	QgsProcessingAlgorithm,
	QgsProcessingParameterNumber,
	QgsProcessingParameterCrs,
	QgsProcessingParameterFeatureSink,
	QgsProcessingContext,
	QgsProcessingFeedback,
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


class LocalizarPontoAlgorithm(QgsProcessingAlgorithm):
	LATITUDE = 'LATITUDE'
	LONGITUDE = 'LONGITUDE'
	CRS = 'CRS'
	OUTPUT = 'OUTPUT'

	def initAlgorithm(self, config=None):
		self.addParameter(
			QgsProcessingParameterNumber(self.LATITUDE, 'Latitude', type=QgsProcessingParameterNumber.Double, defaultValue=-12.4282)
		)
		self.addParameter(
			QgsProcessingParameterNumber(self.LONGITUDE, 'Longitude', type=QgsProcessingParameterNumber.Double, defaultValue=-55.0421)
		)
		self.addParameter(
			QgsProcessingParameterCrs(self.CRS, 'CRS', defaultValue=QgsCoordinateReferenceSystem('EPSG:4674'))
		)
		self.addParameter(
			QgsProcessingParameterFeatureSink(self.OUTPUT, 'Output point layer')
		)

	def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback: QgsProcessingFeedback):
		latitude = float(self.parameterAsDouble(parameters, self.LATITUDE, context))
		longitude = float(self.parameterAsDouble(parameters, self.LONGITUDE, context))
		crs = self.parameterAsCrs(parameters, self.CRS, context)

		fields = QgsFields()
		fields.append(QgsField('id', QVariant.Int))

		(sink, dest_id) = self.parameterAsSink(
			parameters,
			self.OUTPUT,
			context,
			fields,
			QgsWkbTypes.Point,
			crs,
		)

		feat = QgsFeature()
		feat.setFields(fields)
		feat.setAttribute('id', 1)
		feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(longitude, latitude)))

		sink.addFeature(feat, QgsFeatureSink.FastInsert)

		return {self.OUTPUT: dest_id}

	def name(self):
		return 'localizar_ponto'

	def displayName(self):
		return 'Localizar Ponto'

	def group(self):
		return 'geofausto'

	def groupId(self):
		return 'geofausto'

	def shortHelpString(self):
		return 'Cria uma camada pontual a partir de coordenadas informadas.'

	def createInstance(self):
		return LocalizarPontoAlgorithm()
