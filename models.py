from mongoengine import (Document,EmbeddedDocument)
from mongoengine.fields import (
     StringField,
    PointField
)



class Pontos_Coleta(Document):
    meta = {'collection':'pontos_coleta' }
    titulo = StringField()
    localizacao = PointField()
    end = StringField()
    tipo = StringField()
    tipo_descricao = StringField()
    ponto_referencia = StringField()



