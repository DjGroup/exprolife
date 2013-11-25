# Create your views here.
from urllib import thishost
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
#these libraries have used for generate gravatar image
#please download django-gravatar2-1.1.3 and instal setup.py file
from django import template
import hashlib
#for password hashing
#Download link of pyCrypto: http://www.voidspace.org.uk/python/modules.shtml#pycrypto
from Crypto.Hash import MD5
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from social.models import *
import re


def isset(dict, string):
    try:
        if dict[string]:
            return True
    except:
        return False


def index(request):
    #is currently logged in
    if isset(request.session, 'user_id') and isset(request.session, 'first_name') and isset(request.session, 'last_name') :
        #This 'if' is for checking that save button in psychograph is clicked or not
        if request.POST.get('saveButton'):
            gravatar_url = "www.gravatar.com/avatar"
            emailHash = hashlib.md5(request.POST['edit-email']).hexdigest()
            image_url = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            user_edit = User.objects.get(id=request.session['user_id'])
            user_edit.firstName = request.POST['edit-first']
            request.session['first_name'] = user_edit.firstName  # Changing First Name in Session
            user_edit.lastName = request.POST['edit-last']  # changing Last Name in Database
            request.session['last_name'] = user_edit.lastName  # Changing Last Name in Session
            user_edit.email = request.POST['edit-email']  # changing Email in Database
            request.session['email'] = user_edit.email  # Changing Email in Session
            user_edit.save()

            #Reloading from Database
            changedUser = User.objects.filter(id=request.session['user_id'])
            template = loader.get_template('social/psychograph.html')
            context = RequestContext(request, {'myUser': changedUser[0], 'myUrl': image_url})
            return HttpResponse(template.render(context))

        else:
            thisUser = User.objects.filter(id=request.session['user_id'])
            request.session['traceRequestNumber'] = thisUser[0].TraceShip_userReceiver.filter(
                isShowNotificationToUser2=1).count()
            request.session['tracebackRequestNumber'] = thisUser[0].TraceShip_userSender.filter(
                isShowNotificationToUser1=1).count()
            request.session['totalNotification'] = request.session['traceRequestNumber'] +\
                                                   request.session['tracebackRequestNumber']
            gravatar_url = "www.gravatar.com/avatar"
            emailHash = hashlib.md5(request.session['email']).hexdigest()
            image_url = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            template = loader.get_template('social/psychograph.html')
            context = RequestContext(request, {'myUser': thisUser[0], 'myUrl': image_url})
            return HttpResponse(template.render(context))

    if request.POST.get('registerButton'):
        #check that firstName is valid(containing number and letters only)
        firstName = request.POST['firstname'].lower()
        print firstName
        lastName = request.POST['lastname'].lower()
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
            #register with password hashing
            hashed_password = MD5.new()
            hashed_password.update(request.POST['password'])
            gravatar_url = "www.gravatar.com/avatar"
            emailHash = hashlib.md5(request.POST['email']).hexdigest()
            image_url = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            user = User.objects.create(firstName=request.POST['firstname'].lower(),
                                       lastName=request.POST['lastname'].lower(),
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
            context = RequestContext(request, {'myUser': theUser[0], 'myUrl': image_url, 'alert': 1})
            return HttpResponse(template.render(context))
        else:
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
            gravatar_url = "www.gravatar.com/avatar"
            emailHash = hashlib.md5(loginedUser[0].email).hexdigest()
            image_url = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            #check the password
            hashed_password = MD5.new()
            hashed_password.update(request.POST['password'])
            if loginedUser[0].password == hashed_password.hexdigest():
                request.session['user_id'] = loginedUser[0].id
                request.session['first_name'] = loginedUser[0].firstName
                request.session['last_name'] = loginedUser[0].lastName
                request.session['email'] = loginedUser[0].email
                request.session['traceRequestNumber'] = loginedUser[0].TraceShip_userReceiver.filter(
                    isShowNotificationToUser2=1).count()
                request.session['tracebackRequestNumber'] = loginedUser[0].TraceShip_userSender.filter(
                    isShowNotificationToUser1=1).count()
                request.session['totalNotification'] = request.session['traceRequestNumber'] +\
                                                       request.session['tracebackRequestNumber']
                a = TraceShip.objects.filter(userSender=loginedUser[0].id).count()
                b = TraceShip.objects.filter(userReceiver=loginedUser[0].id,isUser2AcceptTrace=1).count()
                c = a+b
                request.session['tracing'] = c
                d = TraceShip.objects.filter(userReceiver=loginedUser[0].id).count()
                request.session['tracer'] = d
                template = loader.get_template('social/psychograph.html')
                context = RequestContext(request, {'myUser': loginedUser[0], 'myUrl': image_url})
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


def nameDetailIndex(request, first_name, last_name, queueNumber=None):
    try:
        anotherUser = User.objects.filter(firstName=first_name, lastName=last_name)
        if anotherUser:
            if not queueNumber:
                anotherUser = anotherUser[0]
            else:
                #start id counter from 1 not 0 because style of URL :D

                anotherUser = anotherUser[int(queueNumber)-1]
        else:
            raise Http404
        isTraced = anotherUser.TraceShip_userReceiver.filter(userSender_id=request.session.get("user_id")).count()
        if not isTraced:
            isTraced = anotherUser.TraceShip_userSender.filter(userReceiver_id=request.session.get("user_id"),
                                                               isUser2AcceptTrace=1).count()
        thisUser = User.objects.filter(id=request.session['user_id'])
        request.session['traceRequestNumber'] = thisUser[0].TraceShip_userReceiver.filter(
            isShowNotificationToUser2=1).count()
        request.session['tracebackRequestNumber'] = thisUser[0].TraceShip_userSender.filter(
            isShowNotificationToUser1=1).count()
        request.session['totalNotification'] = request.session['traceRequestNumber'] +\
                                               request.session['tracebackRequestNumber']
        template = loader.get_template('social/psychograph.html')
        context = RequestContext(request, {'anotherUser': anotherUser, 'isTraced': isTraced})
        return HttpResponse(template.render(context))
    except:
        raise Http404

def idDetailIndex(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return redirect('FLSocial', first_name=user.firstName, last_name=user.lastName)

def competenceLoader(request, competence_title, competence_id):
    competence = Competence.objects.filter(id = competence_id, title = competence_title)
    if not(competence) :
        raise Http404
    ComTags = competence[0].tagList.split(',')
    ComTags.remove('')
    creationDate = str(competence[0].date.month)
    creationDate += ' '+str(competence[0].date.day)+' '+str(competence[0].date.year)+' at '+str(competence[0].date.hour)+':'+str(competence[0].date.minute)+':'+str(competence[0].date.second)
    template = loader.get_template('social/competence.html')
    context = RequestContext(request, {'competence':competence[0], 'comTags':ComTags,'creationDate':creationDate})
    return HttpResponse(template.render(context))

def postLoader(request, post_title, post_id):
    post = BoardPost.objects.filter(id = post_id, title = post_title)
    PostTags = post[0].tagList.split(',')
    PostTags.remove('')
    creationDate = str(post[0].date.month)
    creationDate += ' '+str(post[0].date.day)+' '+str(post[0].date.year)+' at '+str(post[0].date.hour)+':'+str(post[0].date.minute)+':'+str(post[0].date.second)
    template = loader.get_template('social/post.html')
    context = RequestContext(request, {'post':post[0], 'postTags':PostTags ,'creationDate':creationDate})
    return HttpResponse(template.render(context))