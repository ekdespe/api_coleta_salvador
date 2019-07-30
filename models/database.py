from mongoengine import connect
import os

connect(os.getenv('name_database'),host=os.getenv('url_database'))
