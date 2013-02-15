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

class User(models.Model):
    username = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=128)
    count = models.IntegerField(default=0)

    def __unicode__(self):
    	return self.username

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

MAX_USERNAME_LENGTH = 128
MAX_PASSWORD_LENGTH = 128

def login(request):
    try:
        rdata = json.loads(request.body)
        username = rdata.get("username", None)
        user = User.objects.get(pk=username)        
    except (KeyError, User.DoesNotExist):
        resp = {"errCode" : ERR_BAD_CREDENTIALS}
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
    else:
        password = rdata.get("pwd", None)
        if user.password == password:
            user.count += 1
            user.save()
            resp = {"errCode" : SUCCESS, "count" : user.count}
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
        else:
            resp = {"errCode" : ERR_BAD_CREDENTIALS}
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))


def valid_username(username):
    return username != "" and len(username) <= MAX_USERNAME_LENGTH
def valid_password(password):
    return len(password) <= MAX_PASSWORD_LENGTH

def add(request):
    rdata = json.loads(request.body)
    username = rdata.get("username", None)#request.POST['username']
    password = rdata.get("pwd", None)#request.POST['pwd']
    resp = {"errCode" : ERR_USER_EXISTS}
    try:
        u = User.objects.get(pk=username)
    except (KeyError, User.DoesNotExist):
        if not valid_username(username):
            resp["errCode"] = ERR_BAD_USERNAME
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
        if not valid_password(username):
            resp["errCode"] = ERR_BAD_PASSWORD
            return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
        new_user = User(username=username, password=password,count=1)
        new_user.save()
        resp["errCode"] = SUCCESS
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
    else:
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))


#    int TESTAPI_resetFixture();
#        Reset the database to the empty state.
#        Used for testing
def TESTAPI_resetFixture(request):
    User.objects.all().delete()
    resp = {"errCode" : SUCCESS}
    return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))

def TESTAPI_unitTests(request):
    (ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
    try:
        errMsg = ""     # We accumulate here error messages
        output = ""     # Some default values
        totalTests = 0
        nrFailed   = 0
        while True:  # Give us a way to break
            # Find the path to the server installation
            thisDir = os.path.dirname(os.path.abspath(__file__))
            cmd = "make -C "+thisDir+" unit_tests >"+ofileName+" 2>&1"
            print "Executing "+cmd
            code = os.system(cmd)
            if code != 0:
                # There was some error running the tests.
                # This happens even if we just have some failing tests
                errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
                # Continue to get the output, and to parse it

            # Now get the output
            try:
                ofileFile = open(ofileName, "r")
                output = ofileFile.read()
                ofileFile.close ()
            except:
                errMsg += "Error reading the output "+traceback.format_exc()
                # No point in continuing
                break
            
            print "Got "+output
            # Python unittest prints a line like the following line at the end
            # Ran 4 tests in 0.001s
            m = re.search(r'Ran (\d+) tests', output)
            if not m:
                errMsg += "Cannot extract the number of tests\n"
                break
            totalTests = int(m.group(1))
            # If there are failures, we will see a line like the following
            # FAILED (failures=1)
            m = re.search('rFAILED.*\(failures=(\d+)\)', output)
            if m:
                nrFailures = int(m.group(1))
            break # Exit while

        # End while
        resp = { 'output' : errMsg + output,
                 'totalTests' : totalTests,
                 'nrFailed' : nrFailed }
        return HttpResponse(json.dumps(resp, cls=DjangoJSONEncoder))
    finally:
        os.unlink(ofileName)