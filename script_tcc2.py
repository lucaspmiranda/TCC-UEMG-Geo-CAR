# Importar os módulos necessários do QGIS
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsProject

# Caminho para o arquivo da camada vetorial
caminho_arquivo = 'C:\TCC-UEMG\AREA_IMOVEL.shp'

# Carregar a camada vetorial
camada = QgsVectorLayer(caminho_arquivo, 'AREA_IMOVEL', 'ogr')

# Verificar se a camada foi carregada corretamente
if not camada.isValid():
    print('Falha ao carregar a camada vetorial.')
    exit(1)

# Criar uma nova camada vetorial para as sobreposições
nome_camada_sobreposicoes = 'Sobreposições'
camada_sobreposicoes = QgsVectorLayer("Polygon?crs=epsg:4326", nome_camada_sobreposicoes, "memory")

# Adicionar os campos da camada original à camada de sobreposições
camada_sobreposicoes_data_provider = camada_sobreposicoes.dataProvider()
camada_sobreposicoes_data_provider.addAttributes(camada.fields())

# Criar a camada de sobreposições no projeto
projeto = QgsProject.instance()
projeto.addMapLayer(camada_sobreposicoes)

# Iniciar a edição da camada de sobreposições
camada_sobreposicoes.startEditing()

# Iterar sobre as feições da camada original
for feicao in camada.getFeatures():
    geometria = feicao.geometry()

    # Verificar se a feição se sobrepõe a outras feições
    for outra_feicao in camada.getFeatures():
        if outra_feicao.id() != feicao.id():
            outra_geometria = outra_feicao.geometry()
            if geometria.intersects(outra_geometria):
                sobreposicao = geometria.intersection(outra_geometria)
                atributos = feicao.attributes()
                nova_feicao = QgsFeature(len(camada.fields()))
                nova_feicao.setAttributes(atributos)
                nova_feicao.setGeometry(sobreposicao)
                camada_sobreposicoes_data_provider.addFeature(nova_feicao)

# Salvar as alterações na camada de sobreposições
camada_sobreposicoes.commitChanges()

# Atualizar o projeto do QGIS
projeto.addMapLayer(camada_sobreposicoes)

# Salvar o projeto do QGIS
projeto.write('caminho/para/seu/projeto.qgs')

# Fechar as camadas
camada.dataProvider().clearErrors()
camada_sobreposicoes_data_provider.clearErrors()
del camada, camada_sobreposicoes
