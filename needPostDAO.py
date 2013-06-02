import sys
import re
import datetime

__author__ = 'anandkapoor'


class NeedPostDAO:
    def __init__(self, database):
        self.db = database
        self.needs = database.needs

    def insert_need(self, requestor, recipient, forwhen, skillset, location):
        need = {"requestor": requestor,
                "recipient": recipient,
                "forwhen": forwhen.strftime("%A, %B %d %Y at %I:%M%p"),
                "skillset": skillset,
                "location": location}
        try:
            id = self.needs.insert(need)
            print "Inserting the need"
        except:
            print "Error inserting need"
            print "Unexpected error:", sys.exc_info()[0]

        return id

    def get_needs_by_skill(self, skill, num_needs):
        cursor = self.needs.find({'skillset':skill}).sort('date', direction=-1).limit(num_needs)
        list_needs = []
        for need in cursor:
            need['forwhen'] = need['forwhen'].strftime("%A, %B %d %Y at %I:%M%p")
            list_needs({'requestor': need['requestor'],
                        'recipient': need['recipient'],
                        'forwhen': need['forwhen'],
                        'skillset': need['skillset'],
                        'location': need['location']
            })

        return list_needs

    def get_users_by_skill_location(self, skill, location, num_users):
        cursor = self.users.find({'skillset':skill, 'location':location}).sort('date', direction=-1).limit(num_users)
        list_users = []
        for user in cursor:
            list_users({'firstname': user['firstname'],
                        'lastname': user['lastname'],
                        'occupation': user['occupation'],
                        'reliability': user['reliability'],
                        'skillset': user['skillset'],
                        'location': user['location']
            })

        return list_users