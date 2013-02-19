from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
import os
import json
import sys
import tempfile
import traceback
import re
import StringIO
import unittest
from polls.unitTest import UnitTest
from django.views.decorators.csrf import csrf_exempt

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

MAX_USERNAME_LENGTH = 128
MAX_PASSWORD_LENGTH = 128

class User(models.Model):
    username = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128)
    count = models.IntegerField(default=0)


    def __unicode__(self):
    	return self.username

    def loginUser(self, username, password):
        try:
            user = User.objects.get(pk=username)        
        except (KeyError, User.DoesNotExist):
            return ERR_BAD_CREDENTIALS
        else:
            if user.password == password:
                user.count += 1
                user.save()
                return user.count
            else:
                return ERR_BAD_CREDENTIALS

    def valid_username(self, username):
        return username != "" and len(username) <= MAX_USERNAME_LENGTH
    def valid_password(self, password):
        return len(password) <= MAX_PASSWORD_LENGTH

    def addUser(self, username, password):
        try:
            u = User.objects.get(pk=username)
        except (KeyError, User.DoesNotExist):
            if not self.valid_username(username):
                return ERR_BAD_USERNAME
            if not self.valid_password(password):
                return ERR_BAD_PASSWORD
            new_user = User(username=username, password=password,count=1)
            new_user.save()
            return SUCCESS
        else:
            return ERR_USER_EXISTS

    def reset(self):
        User.objects.all().delete()

@csrf_exempt
def login(request):
    rdata = json.loads(request.body)
    username = rdata.get("user", "")
    password = rdata.get("password", "")
    code = User().loginUser(username, password)
    resp = {}
    if code > 0:
        resp = {"errCode" : SUCCESS, "count" : code}
    else:
        resp = {"errCode" : code}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def add(request):
    rdata = json.loads(request.body) #{"user":"pjlee", "password":"asdf"}#
    username = rdata.get("user", "")#request.POST['username']
    password = rdata.get("password", "")#request.POST['password']
    code = User().addUser(username, password)
    resp = {"errCode" : code}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

#    int TESTAPI_resetFixture();
#        Reset the database to the empty state.
#        Used for testing
@csrf_exempt
def TESTAPI_resetFixture(request):
    User().reset()
    resp = {"errCode" : SUCCESS}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder), content_type = "application/json")

@csrf_exempt
def TESTAPI_unitTests(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")