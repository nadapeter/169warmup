"""
Unit tests for the server.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

import unittest
import sys

import models
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"

class TestAdditional(unittest.TestCase):
    """
    Unittests for the Users model class (a sample, incomplete)
    """
    def setUp(self):
        print "setup"

        
    def testAdd1(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))

    def testAddExists(self):
        """
        Tests that adding a duplicate user name fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.ERR_USER_EXISTS, self.users.add("user1", "password"))

    def testAdd2(self):
        """
        Tests that adding two users works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.add("user2", "password"))

    def testAddEmptyUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add("", "password"))


# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()