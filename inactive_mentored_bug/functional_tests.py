import unittest
import inactive_mentored_bugs_tracker as imbt
import login_info

first_test = 1

class Testimbtscript(unittest.TestCase):

    def setUp(self):
        self.tracker = imbt.inactive_bug_tracker()
        # user running the test enters bugzilla login information here #
        self.username = login_info.username
        self.password = login_info.password
        self.bzurl = "https://landfill.bugzilla.org/bugzilla-tip/rest/"
        self.id = 26743
        self.default_assignee = login_info.default_assignee
#         self.length_of_inactivity_period = 30
#         self.test_params = """f1=days_elapsed&list_id=10008579&o1=equals&query
#         _format=advanced&bug_status=ASSIGNED&v1=%s""" % self.length_of_inactivity_period
        self.tracker.bz.configure(self.bzurl, self.username, self.password)
#         # select one bug to use throughout the tests
#         if first_test:
#             self.bug = self.tracker.get_inactive_mentored_bugs()[0]
#             first_test = 0
        self.bug = self.tracker.bz.get_bug(self.id)

    def tearDown(self):
        self.tracker = None

    def test_revert_assignee_to_default(self):
        self.tracker.revert_assignee_to_default(self.bug['id'])
        self.updated_bug = self.tracker.bz.get_bug(self.bug['id'])
        # look up bzrest to for get_bug syntax
        self.assertEqual(False,True)
        
    def test_request_needinfo(self):
        self.tracker.request_needinfo(self.bug['id'])
        self.updated_bug = self.tracker.bz.get_bug(self.bug['id'])
        # look up bzrest to for get_bug syntax
        self.assertIn(self.updated_bug['flags'], {'name':'needinfo', 'status':'?', })

if __name__ == '__main__':
    unittest.main()