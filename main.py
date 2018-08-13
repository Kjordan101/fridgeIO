import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json
# import model
from datetime import datetime
from model import Grocery, Food
# from datetime import datetime

jinjaEnv = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class homePage(webapp2.RequestHandler):
    def get(self):
        homePage = jinjaEnv.get_template('templates/homepage.html')
        self.response.write(homePage.render())

class loadList(webapp2.RequestHandler):
    def get(self):
        # loadListPage = jinjaEnv.get_template('templates/loadlist.html')
        #testing fetch to database with mutipule tables
        loadListPage = jinjaEnv.get_template('templates/debug.html')
        past_lists = Grocery.query().fetch()
        current_items = Food.query().fetch()
        dict = {
        "debug": past_lists
        }
        self.response.write(loadListPage.render({"debug":current_items}))
        # self.response.write(loadListPage.render({'lists' : past_lists}))
class newList(webapp2.RequestHandler):
    def get(self):
        newList = jinjaEnv.get_template('templates/newlist.html')
        self.response.write(newList.render())
    def post(self):
        nameOfFood = self.request.get('food-name', allow_multiple=True)
        dateOfExpiration = self.request.get('expirationDate',allow_multiple=True)
        pickYourTitle = self.request.get('title')

        listOfFoods = []
        for i in range(len(nameOfFood)):
            food = Food(food = nameOfFood[i], expirationDate = datetime.strptime(dateOfExpiration[i],'%Y-%m-%d'))
            foodKey = food.put()
            listOfFoods.append(foodKey)

        # saveToDB = grocery(title = pickYourTitle, food = nameOfFood, expirationDate = (datetime.strptime(dateOfExpiration, '%Y-%m-%d')))
        groceryToSave = Grocery(title = pickYourTitle, foods = listOfFoods)
        groceryToSave.put()
        self.redirect('/loadlist')

app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList)
], debug=True)
