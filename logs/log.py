import logging as lg
import os

path_log = os.getenv('path_log')

lg.basicConfig(filename=path_log,
        level=lg.INFO,
        filemode='w',
        format="%(asctime)s:%(levelname)s:%(message)s"
        )

 
  
 
  
 
 

