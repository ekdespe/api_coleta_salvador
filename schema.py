import graphene
import datetime
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Pontos_Coleta as PontosColetaModel
import database

class Pontos_Coleta(MongoengineObjectType):

    class Meta:
        model = PontosColetaModel
        interfaces = (Node,)




class Query(graphene.ObjectType):
    node = Node.Field()
    points = MongoengineConnectionField(Pontos_Coleta)
    



    
schema = graphene.Schema(query=Query, types=[Pontos_Coleta])
