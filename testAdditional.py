"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

longString = "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"
        
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        expected = { 'errCode' : errCode }
        self.assertDictEqual(expected, respData)

    def testAddExisting(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData2, testLib.RestTestCase.ERR_USER_EXISTS)

    def testBadUsername(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : longString, 'password' : 'password'} )
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testBadPassword(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : longString} )
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_PASSWORD)

    def testAddMultiple(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : 'password'} )
        respData3 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user3', 'password' : 'password'} )
        respData4 = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user4', 'password' : 'password'} )
        self.assertResponse(respData4, testLib.RestTestCase.SUCCESS)

    def testEmptyUsername(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : "", 'password' : 'password'} )
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testExtraData(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : "user1", 'password' : "", 'extra' : "extra"} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    
class TestLogin(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, errCode, count = None):
        expected = { 'errCode' : errCode}
        if count != None:
            expected['count'] = count
        self.assertDictEqual(expected, respData)

    def testLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData2, testLib.RestTestCase.SUCCESS, 2)

    def testBadLogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'wrongpassword'} )
        self.assertResponse(respData2, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testBadLogin2(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'wrongusername', 'password' : 'password'} )
        self.assertResponse(respData2, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLoginCount(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData2 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData3 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData4 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        respData5 = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData5, testLib.RestTestCase.SUCCESS, 5)