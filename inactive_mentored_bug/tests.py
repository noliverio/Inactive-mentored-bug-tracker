import unittest
import inactive_mentored_bugs_tracker as imbt
import login_info


class Testimbtscript(unittest.TestCase):

    def setUp(self):
        self.tracker = imbt.inactive_bug_tracker()
        self.username = login_info.username
        self.password = login_info.password
        self.bzurl = login_info.bugzilla_instance
        self.length_of_inactivity_period = 30
        self.test_params = {'f1': 'bug_mentor',
                            'o1': 'isnotempty',
                            'f2': 'days_elapsed',
                            'o2': 'greaterthan',
                            'v2': self.length_of_inactivity_period,
                            'f3': 'assigned_to',
                            'o3': 'notequals',
                            'v3': login_info.default_assignee,
                              }
        self.tracker.bz.configure(self.bzurl, self.username, self.password)

    def tearDown(self):
        self.tracker = None

    def test_search_bugs_returns_dict(self):
        self.assertIs(type(self.tracker.search_bugs(self.test_params)), dict)

    def test_search_bug_returns_dict_with_value_of_list_of_dicts(self):
        bug_dict = self.tracker.search_bugs(self.test_params)
        self.assertIs(type(bug_dict['bugs']), list)

    def test_get_bugs_is_list_of_dicts(self):
        inactive_mentored_bugs = self.tracker.get_inactive_mentored_bugs()
        if inactive_mentored_bugs:
            self.assertIs(type(inactive_mentored_bugs[0]), dict)
        else:
            print 'no inactive mentored bugs were found with the search' 
            print 'params specified if you are sure that the search should'
            print 'have yeilded at least one such bug then please submit'
            print 'a bug report for this test'
            self.assertIs(type(inactive_mentored_bugs), list)


if __name__ == '__main__':
    unittest.main()
