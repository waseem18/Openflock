#Bismillah

from imports import *
from config import *
from routes import *
from handlers import *


app = webapp2.WSGIApplication(routes,config=config, debug=True)