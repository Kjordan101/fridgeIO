from google.appengine.ext import ndb
from datetime import datetime

class Food(ndb.Model):
    food = ndb.StringProperty(required=True)
    expirationDate = ndb.DateProperty(required=True)
class Grocery(ndb.Model):
    title = ndb.StringProperty(required=True)
    foods = ndb.KeyProperty(Food, repeated=True)
