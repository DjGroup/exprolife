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

# for save_file function

from django.conf import settings
import os
from datetime import datetime


def save_file(f, whatIsType, title, userId, pacTime):
    original_name, file_extension = os.path.splitext(f.name)
    filename = str(title + '_' + str(userId) + '_' + str(pacTime) + file_extension)
    if whatIsType == 'picture':
        path = settings.MEDIA_ROOT + 'picture/' + filename
    else:
        path = settings.MEDIA_ROOT + 'source/' + filename
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return path

def isset(dict, string):
    try:
        if dict[string]:
            return True
    except:
        return False


def index(request):
    #is currently logged in
    if isset(request.session, 'user_id') and isset(request.session, 'first_name') and isset(request.session, 'last_name') :
        thisUser = User.objects.filter(id=request.session['user_id'])
        request.session['traceRequestNumber'] = thisUser[0].TraceShip_userReceiver.filter(
            isShowNotificationToUser2=1).count()
        request.session['tracebackRequestNumber'] = thisUser[0].TraceShip_userSender.filter(
            isShowNotificationToUser1=1).count()
        request.session['totalNotification'] = request.session['traceRequestNumber'] +\
                                               request.session['tracebackRequestNumber']
        gravatar_url = "www.gravatar.com/avatar"
        emailHash = hashlib.md5(request.session['email']).hexdigest()
        image_url = "http://" + gravatar_url + "/" + emailHash + "?s=210&d=identicon&r=PG"
        #This 'if' is for checking that save button in psychograph is clicked or not
        if request.POST.get('saveButton'):
            thisUser[0].firstName = request.POST['edit-first']
            request.session['first_name'] = thisUser[0].firstName  # Changing First Name in Session
            thisUser[0].lastName = request.POST['edit-last']  # changing Last Name in Database
            request.session['last_name'] = thisUser[0].lastName  # Changing Last Name in Session
            thisUser[0].email = request.POST['edit-email']  # changing Email in Database
            request.session['email'] = thisUser[0].email  # Changing Email in Session
            thisUser[0].save()

            #Reloading from Database
            template = loader.get_template('social/psychograph.html')
            context = RequestContext(request, {'myUser': thisUser[0], 'myUrl': image_url})
            return HttpResponse(template.render(context))

        elif request.POST.get('competenceAdd'):
            title = request.POST['comp-title']
            content = request.POST['comp-descript']
            tagList = request.POST['tagsinput']
            developers = request.POST['comp-developer']
            manager = request.POST['comp-manager']
            picture = request.FILES.get('comp-pic')
            code = request.FILES.get('comp-code')
            usage = request.POST['comp-usages']
            currentDate = datetime.now()
            if picture:
                picturePath = save_file(picture, 'picture', str(title), request.session['user_id'], currentDate)
            else:
                picturePath = '/static/social/images/logos/pylogo.png'
            if code:
                sourceCodePath = save_file(code, 'source', str(title), request.session['user_id'], currentDate)
            else:
                sourceCodePath = None
            STR = ""
            for i in tagList.split():
                STR += i + ","
            thisUser[0].competence_set.create(title=title, content=content, tagList=STR, developers=developers,
                                              manager=manager, picture=picturePath, date=currentDate,
                                              sourceCode=sourceCodePath,
                                              usage=usage)
            template = loader.get_template('social/psychograph.html')
            print request.FILES
            context = RequestContext(request, {'myUser': thisUser[0], 'myUrl': image_url})
            return HttpResponse(template.render(context))
        else:
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
                j=0
                j1=0
                c=0
                c1=0
                request.session['traceRequestNumber'] = loginedUser[0].TraceShip_userReceiver.filter(
                    isShowNotificationToUser2=1).count()
                request.session['tracebackRequestNumber'] = loginedUser[0].TraceShip_userSender.filter(
                    isShowNotificationToUser1=1).count()

                for k in CommentCompetence.objects.filter(user=loginedUser[0].id):
                    j = j+ CommentCompetence.objects.filter(referenceComment = k.id,user_notification='0').count()
                for k1 in CommentPost.objects.filter(user=loginedUser[0].id):
                    j1 =j1+ CommentPost.objects.filter(referenceComment = k1.id,user_notification='0').count()

                for k2 in Competence.objects.filter(user=loginedUser[0].id):

                    c = c+  CommentCompetence.objects.exclude(user = loginedUser[0].id).filter(referenceCompetence=k2.id,main_notification='0',referenceComment='0',).count()

                for k3 in BoardPost.objects.filter(user=loginedUser[0].id):
                    c1 = c1 + CommentPost.objects.exclude(user = loginedUser[0].id).filter(referencePost=k3.id,main_notification='0',referenceComment='0').count()
                request.session['totalNotification'] = request.session['traceRequestNumber'] +\
                                                       request.session['tracebackRequestNumber']+\
                                                       j+j1+c+c1

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
    print competence_title
    bb = User.objects.get(email=request.session['email'])
    me1 = bb.email
    gravatar_url = "www.gravatar.com/avatar"
    emailHash = hashlib.md5(me1).hexdigest()
    me = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
    comment = []
    gravatar_url = "www.gravatar.com/avatar"

    competence = Competence.objects.filter(id=competence_id, title=competence_title)
    if not competence:
        raise Http404
    ComTags = competence[0].tagList.split(',')
    try:
        ComTags.remove('')
    except:
        pass
    creationDate = str(competence[0].date.month)
    creationDate += ' ' + str(competence[0].date.day) + ' ' + str(competence[0].date.year) + ' at ' + \
                    str(competence[0].date.hour) + ':' + str(competence[0].date.minute) + ':' + \
                    str(competence[0].date.second)
    commentdb = CommentCompetence.objects.filter(referenceCompetence=competence_id).order_by("time")
    for i in commentdb:
        use = User.objects.get(id=i.user)
        temp = {}
        temp['id'] = i.id
        temp['firstName'] = use.firstName
        temp['lastName'] = use.lastName
        temp['content'] = i.content
        temp['time'] = i.time
        temp['refer'] = i.referenceComment
        emailHash = hashlib.md5(use.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        temp['email'] = image_url1
        temp['depth'] = i.depth*2
        comment.append(temp)

    template = loader.get_template('social/competence.html')
    pictureUrl = competence[0].picture.url[13:] if competence[0].picture.url[1] == 'm' else competence[0].picture.url

    context = RequestContext(request, {
        'comment' : comment,
        'me':me,
        'email':me1,
        'competence': competence[0],
        'comTags': ComTags,
        'creationDate': creationDate,
        'pictureUrl': pictureUrl
    })
    return HttpResponse(template.render(context))


def postLoader(request, post_title, post_id):
    print post_title
    bb = User.objects.get(email=request.session['email'])
    me1 = bb.email
    gravatar_url = "www.gravatar.com/avatar"
    emailHash = hashlib.md5(me1).hexdigest()
    me = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
    comment = []
    gravatar_url = "www.gravatar.com/avatar"
    post = BoardPost.objects.filter(id=post_id, title=post_title)
    if not post:
        raise Http404
    PostTags = post[0].tagList.split(',')
    try:
        PostTags.remove('')
    except:
        pass
    creationDate = str(post[0].date.month)
    creationDate += ' ' + str(post[0].date.day) + ' ' + str(post[0].date.year) + ' at ' + str(post[0].date.hour) + \
                    ':' + str(post[0].date.minute) + ':' + str(post[0].date.second)
    commentdb = CommentPost.objects.filter(referencePost=post_id).order_by("time")
    for i in commentdb:
        use = User.objects.get(id=i.user)
        temp = {}
        temp['id'] = i.id
        temp['firstName'] = use.firstName
        temp['lastName'] = use.lastName
        temp['content'] = i.content
        temp['time'] = i.time
        temp['refer'] = i.referenceComment
        emailHash = hashlib.md5(use.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        temp['email'] = image_url1
        temp['depth'] = i.depth*2
        comment.append(temp)

    template = loader.get_template('social/post.html')
    context = RequestContext(request, {
        'comment':comment,
        'me':me,
        'email':me1,
        'post': post[0],
        'postTags': PostTags,
        'creationDate': creationDate
    })
    return HttpResponse(template.render(context))

def traces(request):
    tracer = []
    tracing = []
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user1']).split(".")
        user2 = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user2[int(firstAndLastName[2])-1]
        else:
            user = user2[0]
    except:
        user = User.objects.get(email=request.session['email'])

    temp = TraceShip.objects.filter(userSender=user.id)
    for i in temp:
        tempDic1 = {}
        tempDic1['firstName'] = i.userReceiver.firstName
        tempDic1['lastName'] = i.userReceiver.lastName
        tempDic1['score'] = i.userReceiver.score
        gravatar_url = "www.gravatar.com/avatar"
        emailHash = hashlib.md5(i.userReceiver.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        tempDic1['email'] = image_url1
        tracing.append(tempDic1)

    temp = TraceShip.objects.filter(userReceiver=user.id,isUser2AcceptTrace=1)
    for i in temp:
        tempDic1={}
        tempDic1['firstName'] = i.userSender.firstName
        tempDic1['lastName'] = i.userSender.lastName
        tempDic1['score'] = i.userSender.score
        gravatar_url = "www.gravatar.com/avatar"
        emailHash = hashlib.md5(i.userSender.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        tempDic1['email'] = image_url1
        tracing.append(tempDic1)



    temp = TraceShip.objects.filter(userReceiver=user.id)
    for i in temp:
        tempDic = {}
        tempDic['firstName'] = i.userSender.firstName
        tempDic['lastName'] = i.userSender.lastName
        tempDic['score'] = i.userSender.score
        gravatar_url = "www.gravatar.com/avatar"
        emailHash = hashlib.md5(i.userSender.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        tempDic['email'] = image_url1
        tracer.append(tempDic)

    temp = TraceShip.objects.filter(userSender=user.id,isUser2AcceptTrace=1)
    for i in temp:
        tempDic = {}
        tempDic['firstName'] = i.userReceiver.firstName
        tempDic['lastName'] = i.userReceiver.lastName
        tempDic['score'] = i.userReceiver.score
        gravatar_url = "www.gravatar.com/avatar"
        emailHash = hashlib.md5(i.userReceiver.email).hexdigest()
        image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
        tempDic['email'] = image_url1
        tracer.append(tempDic)
    template = loader.get_template('social/trace.html')
    context = RequestContext(request,{'tracer':tracer,'tracing':tracing})
    return HttpResponse(template.render(context))
