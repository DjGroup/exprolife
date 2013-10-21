# Create your views here.
from urllib import thishost
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render

#for password hashing
#Download link of pyCrypto: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
from Crypto.Hash import MD5

from social.models import *
import re

def isset(dict, string):
    try:
        if dict[string]:
            return True
    except:
        return False


def index(request):
    #is currently logged in ?
    if isset(request.session, 'user_id') and isset(request.session, 'first_name') and isset(request.session, 'last_name') :
            #This 'if' is for checking that save button in psychograph is clicked or not
            if request.POST.get('saveButton'):
                user_edit = User.objects.get(id=request.session['user_id'])
                user_edit.firstName = request.POST['edit-first']  #changing First Name in Database
                request.session['first_name'] = user_edit.firstName #Changing First Name in Session

                user_edit.lastName = request.POST['edit-last']  #changing Last Name in Database
                request.session['last_name'] = user_edit.lastName #Changing Last Name in Session

                user_edit.email = request.POST['edit-email']  #changing Email in Database
                request.session['email'] = user_edit.email #Changing Email in Session

                user_edit.save()
				
				#Reloading from Database
                changedUser = User.objects.filter(id=request.session['user_id'])
                template = loader.get_template('social/psychograph.html')
                context = RequestContext(request, {'myUser': changedUser[0]})
                return HttpResponse(template.render(context))
            else:
                thisUser = User.objects.filter(id=request.session['user_id'])
                template = loader.get_template('social/psychograph.html')
                context = RequestContext(request, {'myUser': thisUser[0]})
                return HttpResponse(template.render(context))
    if request.POST.get('registerButton'):
        #check that firstName is valid(containing number and letters only)
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        email = request.POST['email']
        firstAndLastNameRegex = r'^[a-zA-Z0-9]+$'
        emailRegex = r'[a-zA-Z0-9_]+(\.[a-zA-Z0-9_+])*@[a-zA-Z0-9_]+\.[a-zA-Z0-9_.+]{2,}$'
        isValidFirstName = re.match(firstAndLastNameRegex, firstName)
        isValidLastName = re.match(firstAndLastNameRegex, lastName)
        isValidEmailAddress = re.match(emailRegex, email)
        #email must be unique
        if isValidEmailAddress:
            if User.objects.filter(email=request.REQUEST['email']):
                isValidEmailAddress = 2
            else:
                isValidEmailAddress = 1
        else:
            isValidEmailAddress = 0
        sex = request.POST.get('gender', 'unKnown')
        isValidSex = 0 if (sex != "male" and sex != "female") else 1
        password = request.POST['password']
        isPasswordValid = 1 if len(password) >= 6 else 0
        rePass = request.POST['rePass']
        isRePassValid = 1 if (len(rePass) >= 6 and rePass == password) else 0
        canGoHome = int(bool(
            isValidFirstName and
            isValidLastName and
            isValidEmailAddress and
            isValidSex and
            isPasswordValid and
            isRePassValid
        ))
        if canGoHome:
            print 234
            #register with password hashing
            hashed_password = MD5.new()
            hashed_password.update(request.POST['password'])
            user = User.objects.create(firstName=request.POST['firstname'],
                                        lastName=request.POST['lastname'],
                                        password=hashed_password.hexdigest(),
                                        email=request.POST['email'],
                                        sex=0 if request.POST['gender'] == 'male' else 1 if request.POST['gender'] ==
                                        'female' else -1,
                                        )
            user.save()
            #sessions that needed for User in pages
            request.session['user_id'] = user.id
            request.session['first_name'] = user.firstName
            request.session['last_name'] = user.lastName
            request.session['email'] = user.email
			
			theUser = User.objects.filter(id=request.session['user_id'])
            template = loader.get_template('social/psychograph.html')
            context = RequestContext(request, {'myUser': theUser[0]})
            return HttpResponse(template.render(context))
        else:
            print 123
            sendError = {"isNOTOK": True}
            if not isValidFirstName:
                sendError["FNE"] = "First name must containing letters and numbers"
            if not isValidLastName:
                sendError["LNE"] = "Last name must containing letters and numbers"
            if isValidEmailAddress == 0:
                sendError["EME"] = "Enter valid Email address"
            elif isValidEmailAddress == 2:
                sendError["EME"] = "This Email is currently registered please try something else"
            if not isValidSex:
                sendError["SXE"] = "please select Male or Female option"
            if not isPasswordValid:
                sendError["PAE"] = "please Enter password at least 6 characters"
            if not isRePassValid:
                sendError["RPE"] = "please retype your password"
            template = loader.get_template('social/index.html')
            context = RequestContext(request, sendError)
            return HttpResponse(template.render(context))
    #login
    elif request.POST.get('loginSubmit'):
            #checking the username and password for correctness
            # this must be changed in later by encrypt the
            # password and change the logic of the login form(this may be hackable ....)
            loginedUser = User.objects.filter(email=request.POST['email'])
            #if user exists (means email exists )
            if loginedUser:
                #check the password
                hashed_password = MD5.new()
                hashed_password.update(request.POST['password'])
                if loginedUser[0].password == hashed_password.hexdigest():
                    request.session['user_id'] = loginedUser[0].id
                    request.session['first_name'] = loginedUser[0].firstName
                    request.session['last_name'] = loginedUser[0].lastName
                    request.session['email'] = loginedUser[0].email
                    template = loader.get_template('social/psychograph.html')
                    context = RequestContext(request, {'myUser': loginedUser[0]})
                    return HttpResponse(template.render(context))
                else:
                    template = loader.get_template('social/index.html')
                    context = RequestContext(request, {
                        'error': 'Password is not correct !!'
                    })
                    return HttpResponse(template.render(context))
            else:
                template = loader.get_template('social/index.html')
                context = RequestContext(request, {
                    'error': "Email doesn't exist !!"
                })
                return HttpResponse(template.render(context))
    else:
        return render(request, 'social/index.html')
    #is this except really need ? => must be think later
