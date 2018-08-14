from google.appengine.ext import ndb
from datetime import datetime
from google.appengine.api import users

class Food(ndb.Model):
    food = ndb.StringProperty(required=True)
    expirationDate = ndb.DateProperty(required=True)
class Grocery(ndb.Model):
    title = ndb.StringProperty(required=True)
    foods = ndb.KeyProperty(Food, repeated=True)

class CssiUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    grocery_link = ndb.KeyProperty(Grocery, repeated=True)
