import os

from qgis.core import (
    QgsMapLayer,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsVectorFileWriter,
    QgsProject,
    QgsVectorLayer
)


class ExportarCamadasSelecionadasGpkgShp(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        """Define os parâmetros (nenhum necessário neste caso)."""
        pass

    def processAlgorithm(self, parameters, context, feedback):
        """Executa o processamento."""
        
        # Defina a pasta de saída
        pasta_saida = "/mnt/SSD/Profissional/2025 NTU Canela Capacitação/DADOS/exported"

        # Criar a pasta caso não exista
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
            feedback.pushInfo(f"Pasta criada: {pasta_saida}")

        # Obtenha as camadas selecionadas e filtre apenas as vetoriais
        camadas_selecionadas = [
            layer.layer() for layer in QgsProject.instance().layerTreeRoot().selectedLayersRecursive()
            if layer.layer() and layer.layer().type() == QgsMapLayer.VectorLayer
        ]

        # Verifique se há camadas selecionadas
        if not camadas_selecionadas:
            feedback.pushWarning("Nenhuma camada vetorial selecionada.")
            return {}

        # Itere sobre as camadas selecionadas e exporte
        for camada in camadas_selecionadas:
            nome_arquivo = os.path.join(pasta_saida, f"{camada.name()}.shp")

            erro = QgsVectorFileWriter.writeAsVectorFormat(
                camada, nome_arquivo, "UTF-8", camada.crs(), "ESRI Shapefile"
            )

            # Compatibilidade com diferentes assinaturas de retorno
            if isinstance(erro, int):
                sucesso = (erro == QgsVectorFileWriter.NoError)
                mensagem_erro = ""
            else:
                sucesso = (erro[0] == QgsVectorFileWriter.NoError)
                mensagem_erro = erro[1] if len(erro) > 1 else ""

            if sucesso:
                feedback.pushInfo(f"✅ Camada {camada.name()} exportada com sucesso.")
            else:
                feedback.pushWarning(f"❌ Erro ao exportar {camada.name()}: {mensagem_erro}")

        return {}

    def name(self):
        return 'exporta_camadas_selecionadas'

    def displayName(self):
        return 'Exportar Camadas Selecionadas'

    def group(self):
        return 'geofausto'

    def groupId(self):
        return 'geofausto'
    
    def shortHelpString(self) -> str:
        return (
            "....\n"
            "..."
        )

    def createInstance(self):
        return ExportarCamadasSelecionadasGpkgShp()
