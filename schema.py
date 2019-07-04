import graphene
import datetime
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import models as m
from models import database
import settings

class Pontos_Coleta(MongoengineObjectType):

    class Meta:
        model = m.Pontos_Coleta
        interfaces = (Node,)




class Query(graphene.ObjectType):
    node = Node.Field()
    points = MongoengineConnectionField(Pontos_Coleta)



    
schema = graphene.Schema(query=Query, types=[Pontos_Coleta])
