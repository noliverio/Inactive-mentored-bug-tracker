import unittest
import inactive_mentored_bugs_tracker as imbt
import login_info


class Testimbtscript(unittest.TestCase):

    def setUp(self):
        self.tracker = imbt.inactive_bug_tracker()
        # user running the test enters bugzilla login information here #
        self.username = login_info.username
        self.password = login_info.password
        self.bzurl = "http://bugzilla.mozilla.org/rest"
        self.length_of_inactivity_period = 30
        self.test_params = """f1=days_elapsed&list_id=10008579&o1=equals&query
        _format=advanced&bug_status=ASSIGNED&v1=%s""" % self.length_of_inactivity_period
        self.tracker.bz.configure(self.bzurl, self.username, self.password)

    def tearDown(self):
        self.tracker = None

    def test_leave_reset_message(self):
        self.assertTrue(False)
    
    def test_revert_assignee_to_default(self):
        self.assertTrue(False)

    def test_request_needinfo(self):
        self.assertTrue(False)
