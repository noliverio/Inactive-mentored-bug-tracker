import bzrest.client
## this is necessary to create a secure connection
## without it an insecure platform warning is raised.
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import login_info


class inactive_bug_tracker(object):
    def __init__(self):

        ## set the params for the program
        self.username = login_info.username
        self.password = login_info.password

        ## Post this message as a comment on the bug
        self.reset_message = ("I have reset the assignee as a part of an automated cleanup"
        "since there has been no visible activity in this bug for some time. If this is"
        "incorrect, please let me know and I'll correct the error")
        
        ## Reassign the bug to the default assignee
        self.default_assignee = login_info.default_assignee
        self.bzurl = login_info.bugzilla_instance

        ## This search will return all bugs that meet the following criteria:
        ## 1) The bug is assigned to someone
        ## 2) There have been no updates in the last 30 days
        ## change 'length_on_inactivity_period' to extend or decrease
        ## how long an assigned mentored bug can be inactive
        self.length_of_inactivity_period = 30
        self.search_params = """f1=days_elapsed&list_id=10008579&o1=equals&
        query_format=advanced&bug_status=ASSIGNED&v1=%s""" % self.length_of_inactivity_period
        self.bz = bzrest.client.BugzillaClient()
    
    ## These are two are just further wrappers around the api
    def search_bugs(self, search_params, data=None):
        return self.bz.request("GET", "bug? % s" % search_params, data)

    def get_latest_comment(self, id_, data = None):
        return self.bz.request("GET", "bug/%s/comment" % id_, data)['bugs']["%i"%id_]['comments'][-1]
        

    def get_inactive_mentored_bugs(self):
        ## returns a dict with one entry named 'bugs'
        bugs = self.search_bugs(self.search_params)
        list_of_bugs = bugs['bugs']
        inactive_mentored_bugs = []
        for bug in list_of_bugs:
            if bug['mentors']:
                inactive_mentored_bugs.append(bug)
        return inactive_mentored_bugs

    def leave_reset_message(self, id):
        self.bz.add_comment(id_ = id, comment = self.reset_message)
    
    def revert_assignee_to_default(self, id):
        self.bz.update_bug(id_ = id, data = {'assigned_to':self.default_assignee})

    def request_needinfo(self, bug):
        # there has got to be a better way than this, but I can not find a way to avoid the nesting
        data =  {'flags': [{"name": "needinfo", "status":"?", "requestee": "%s" % bug['assigned_to']}]}
        id = bug['id']
        self.bz.update_bug(id_ = id, data = data)

    def main(self):
        self.bz.configure(self.bzurl, self.username, self.password)
        self.inactive_bugs = get_inactive_mentored_bugs()
        for bug in self.inactive_bugs:
            self.leave_resest_message(bug['id'])
            self.request_needinfo(bug)
            self.revert_assignee_to_default(bug['id'])


if __name__ == '__main__':
    IMBT = inactive_bug_tracker()
