import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json
from model import grocery

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
        self.response.write(loadListPage.render())

class newList(webapp2.RequestHandler):
    def get(self):
        newList = jinjaEnv.get_template('templates/newlist.html')
        self.response.write(newList.render())
    def post(self):
        nameOfFood = self.request.get('food')

app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList)
], debug=True)
