from google.appengine.ext import ndb
from datetime import datetime

class grocery(ndb.Model):
    food = ndb.StringProperty(required=True)
    expirationDate = ndb.DateProperty(required=True)
    
