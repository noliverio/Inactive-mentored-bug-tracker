import bzrest.client
import sys
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
        ## 1) The bug has mentors
        ## 2) There have been no updates in the last 30 days
        ## 3) The bug is assigned to someone, not the default assignee
        ## change 'length_on_inactivity_period' to extend or decrease
        ## how long an assigned mentored bug can be inactive
        self.length_of_inactivity_period = 30
        self.search_params = {'f1': 'bug_mentor',
                              'o1': 'isnotempty',
                              'f2': 'days_elapsed',
                              'o2': 'greaterthan',
                              'v2': self.length_of_inactivity_period,
                              'f3': 'assigned_to',
                              'o3': 'notequals',
                              'v3': login_info.default_assignee,
                              }
        self.bz = bzrest.client.BugzillaClient()
    
    ## This is just further wrappers around the api
    ## With the params above it will return just the inactive mentored bugs
    def search_bugs(self, data):
        param_list = ["%s=%s"%(key,data[key]) for key in data]
        params = '&'.join(param_list)
        return self.bz.request("GET", "bug?%s" % params)
        

    def get_inactive_mentored_bugs(self):
        ## returns a dict with one entry named 'bugs'
        bugs = self.search_bugs(self.search_params)
        list_of_bugs = bugs['bugs']
        if list_of_bugs:
            return list_of_bugs
        else:
            print 'No bugs were found'
            sys.exit()

    def leave_reset_message(self, id):
        self.bz.add_comment(id_ = id, comment = self.reset_message)
    
    def revert_assignee_to_default(self, id):
        self.bz.update_bug(id_ = id, data = {'assigned_to':self.default_assignee})

    def main(self):
        self.bz.configure(self.bzurl, self.username, self.password)
        print 'fetching bugs'
        self.inactive_bugs = self.get_inactive_mentored_bugs()
        print 'reseting bugs'
        for bug in self.inactive_bugs:
            self.leave_resest_message(bug['id'])
            self.revert_assignee_to_default(bug['id'])
        print 'finished reseting bugs'


if __name__ == '__main__':
    IMBT = inactive_bug_tracker()
    IMBT.main()
