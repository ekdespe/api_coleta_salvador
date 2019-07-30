from mongoengine import connect
import os
from dotenv import load_dotenv
load_dotenv()

connect(
        db=os.getenv('name_database'),
        username=os.getenv('user_database'),
        password=os.getenv('passwd_database'),
        authentication_source=os.getenv('auth_src_database')
        )
        
        
        
        
