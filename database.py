from mongoengine import connect
import config as c


connect('apiColeta',host=c.CONFIG['url_database'])
