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
        
        self.response.write(loadListPage.render({'lists' : past_lists}))
class newList(webapp2.RequestHandler):
    def get(self):
        newList = jinjaEnv.get_template('templates/newlist.html')
        self.response.write(newList.render())
    def post(self):
        nameOfFood = self.request.get('food-name')
        dateOfExpiration = self.request.get('expirationDate')
        pickYourTitle = self.request.get('title')
        saveToDB = grocery(title = pickYourTitle, food = nameOfFood, expirationDate = (datetime.strptime(dateOfExpiration, '%Y-%m-%d')))
        # pickYourTitle = self.request.get('title')
        # saveToDB = grocery(title = pickYourTitle, food = nameOfFood, expirationDate = (datetime.strptime(dateOfExpiration, '%Y-%m-%d')))
        saveToDB.put()
        #self.redirect('/newlist')

app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList)
], debug=True)
