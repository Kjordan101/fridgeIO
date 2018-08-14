import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json
from datetime import datetime
from model import Grocery, Food

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
        #testing fetch to database with mutipule tables
        loadListPage = jinjaEnv.get_template('templates/loadlist.html')
        past_lists = Grocery.query().fetch()
        

        self.response.write(loadListPage.render({"debug":past_lists}))
class newList(webapp2.RequestHandler):
    def get(self):
        newList = jinjaEnv.get_template('templates/newlist.html')
        self.response.write(newList.render())
    def post(self):
        nameOfFood = self.request.get('food-name', allow_multiple=True)
        dateOfExpiration = self.request.get('expirationDate',allow_multiple=True)
        pickYourTitle = self.request.get('title')

        #fill list with key values
        listOfFoods = []
        for i in range(len(nameOfFood)):
            food = Food(food = nameOfFood[i], expirationDate = datetime.strptime(dateOfExpiration[i],'%Y-%m-%d'))
            foodKey = food.put()
            listOfFoods.append(foodKey)

        #save to grocery list to database
        groceryToSave = Grocery(title = pickYourTitle, foods = listOfFoods)
        groceryToSave.put()
        self.redirect('/loadlist')
class updateHandler(webapp2.RequestHandler):
    def get(self):
        previousPage = jinjaEnv.get_template('templates/loadlist.html')
        updatePage = jinjaEnv.get_template('templates/updatepage.html')
        edit_list = Grocery.query().fetch()
        self.response.write(updatePage.render({"edit_list":edit_list}))

app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList),
    ('/update',updateHandler)
], debug=True)
