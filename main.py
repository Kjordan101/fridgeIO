import webapp2
import os
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json
from datetime import datetime
from model import Grocery, Food, CssiUser
from google.appengine.api import users

jinjaEnv = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class homePage(webapp2.RequestHandler):
    def get(self):
        homePage = jinjaEnv.get_template('templates/homepage.html')
        self.response.write(homePage.render())
        user = users.get_current_user()

        if user:
            email_address = user.nickname()
            cssi_user = CssiUser.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            if cssi_user:
                self.response.write('''
                Welcome %s %s (%s)! <br> %s <br>''' % (
                cssi_user.first_name,
                cssi_user.last_name,
                email_address,
                signout_link_html))
            else:
                self.response.write('''
                Welcome to our site, %s!  Please sign up! <br>
                <form method="post" action="/">
                <input type="text" name="first_name">
                <input type="text" name="last_name">
                <input type="submit">
                </form><br> %s <br>
                ''' % (email_address, signout_link_html))
        else:
            self.response.write('''
            Please log in to use our site! <br>
            <a href="%s">Sign in</a>''' % (
            users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            id=user.user_id())
        cssi_user.put()
        self.response.write('Thanks for signing up, %s!' %
            cssi_user.first_name)


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
class aboutPage(webapp2.RequestHandler):
    def get(self):
        about_page = jinjaEnv.get_template('templates/about.html')
        self.response.write(about_page.render())
app = webapp2.WSGIApplication([
    ('/', homePage),
    ('/loadlist', loadList),
    ('/newlist', newList),
    ('/about',aboutPage)
], debug=True)
