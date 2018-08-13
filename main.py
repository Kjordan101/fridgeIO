import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json
import model
from datetime import datetime
from model import grocery
from datetime import datetime

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
        loadListPage = jinjaEnv.get_template('templates/loadlist.html')
        past_lists = grocery.query().fetch()
        var_dict = {
        "list" : past_lists[0].title
        }
        #for food in past_lists[grocery]:
        self.response.write(loadListPage.render(var_dict))
        # self.response.write(loadListPage.render(var_dict))

class newList(webapp2.RequestHandler):
    def get(self):
        newList = jinjaEnv.get_template('templates/newlist.html')
        self.response.write(newList.render())
    def post(self):
        nameOfFood = self.request.get('food-name')
        dateOfExpiration = self.request.get('expirationDate')
        titleOfList = self.request.get('title')
        saveToDB = grocery(food = nameOfFood,
        expirationDate = (datetime.strptime(dateOfExpiration, '%Y-%m-%d')), title = titleOfList)
        saveToDB.put()
        #self.redirect('/newlist')

app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList)
], debug=True)
