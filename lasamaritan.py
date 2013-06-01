

import pymongo
import sessionDAO
import userDAO
import bottle
import cgi
import re

__author__ = 'anandkapoor'


@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")

    # set these up in case we have an error case
    errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
    if validate_signup(username, password, verify, email, errors):

        if not users.add_user(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return errors['username_error']

        session_id = sessions.start_session(username)
        print session_id
        bottle.response.set_cookie("session", session_id)
        return 'Ok'
    else:
        print "user did not validate"
        return 'Please sign up'


connection_string = "mongodb://<user>:<password>@linus.mongohq.com:10074/app16048987"
connection = pymongo.MongoClient(connection_string)
database = connection.app16048987

users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)


bottle.debug(True)
bottle.run(host='linus.mongohq.com', port=10074)         # Start the webserver running and wait for requests

