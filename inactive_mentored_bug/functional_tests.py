import unittest
import inactive_mentored_bugs_tracker as imbt
import login_info

first_test = 1

class Testimbtscript(unittest.TestCase):

    def setUp(self):
        global first_test
        self.tracker = imbt.inactive_bug_tracker()
        self.username = login_info.username
        self.password = login_info.password
        self.bzurl = login_info.bugzilla_instance
        self.default_assignee = login_info.default_assignee
        
        self.length_of_inactivity_period = 30
        self.test_params = ("f1=days_elapsed&list_id=10008579&o1=equals&query"
        "_format=advanced&bug_status=ASSIGNED&v1=%s" % self.length_of_inactivity_period)
        self.tracker.bz.configure(self.bzurl, self.username, self.password)
        # select one bug to use throughout the tests
        if first_test:
            self.bug = self.tracker.get_inactive_mentored_bugs()[0]
            first_test = 0

        self.bug = self.tracker.bz.get_bug(self.id)

    def tearDown(self):
        self.tracker = None

    def get_latest_comment(self, id_, data = None):
        return self.bz.request("GET", "bug/%s/comment" % id_, data)['bugs']["%i"%id_]['comments'][-1]

    def test_revert_assignee_to_default(self):
        self.tracker.revert_assignee_to_default(self.bug['id'])
        self.updated_bug = self.tracker.bz.get_bug(self.bug['id'])
        self.assertEqual(self.updated_bug['assigned_to'], self.tracker.default_assignee)

    def test_leave_reset_message(self):
        self.tracker.leave_reset_message(self.bug['id'])
        message = self.get_latest_comment(self.bug['id'])['text']
        self.assertEquals(message, self.tracker.reset_message)
        
    def test_request_needinfo(self):
        self.tracker.request_needinfo(self.bug)
        self.updated_bug = self.tracker.bz.get_bug(self.bug['id'])
        try:
            self.assertTrue(self.updated_bug['flags'][0]['name'] == 'needinfo')
        except KeyError:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()