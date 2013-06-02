

import pymongo
import sessionDAO
import needPostDAO
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
            return errors

        session_id = sessions.start_session(username)
        print session_id
        bottle.response.set_cookie("session", session_id)
        return bottle.redirect("/welcome")
    else:
        print "user did not validate"
        return errors

@bottle.get("/welcome")
def present_welcome():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    if username is None:
        print "Welcome: can't identify User...redirecting to signup"
        bottle.redirect("/signup")

    welcome = {'username': username}
    return welcome

@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error' : "System has encountered a DB error"}


@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("signup")

@bottle.post('/newneed')
def post_new_need():
    cookie = bottle.request.get_cookie("session")
    requestor = sessions.get_username(cookie)
    recipient = bottle.request.forms.get("recipient")
    forwhen = bottle.request.forms.get("forwhen")
    skills_requested = bottle.request.forms.get("skillsetrequested")
    location = bottle.request.forms.get("location")

    skill_sets = cgi.escape(skills_requested)
    skill_set_array = extract_skill_set(skill_sets)
    id = needs.insert_need(requestor, recipient, forwhen, skill_set_array, location)

    bottle.redirect("/need/" + id)

@bottle.get("/need/<id>")
def show_need(permalink="notfound"):
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    permalink = cgi.escape(id)

    need = needs.get_need_by_permalink(id)

    if need is None:
        bottle.redirect("/need_not_found")

    return need



# Helper functions

def extract_skill_set(skill_sets):
    whitespace = re.compile('\s')

    nowhite = whitespace.sub("",skill_sets)
    skill_sets_array = nowhite.split(',')

    # let's clean it up
    cleaned = []
    for skill in skill_sets_array:
        if skill not in cleaned and skill != "":
            cleaned.append(skill)

    return cleaned

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.lasamaritan

needs = needPostDAO.NeedPostDAO(database)
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)


bottle.debug(True)
bottle.run(host='ec2-54-224-222-165.compute-1.amazonaws.com', port=8082)         # Start the webserver running and wait for requests

