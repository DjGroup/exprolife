from django.http import HttpResponse
from social.models import *
from django.db.models import Q
import re
import json
import hashlib
from datetime import datetime

from itertools import chain

from django.utils import timezone


def autocompleteModel(request):
    response = {"users": [], "found": 0}
    splitter = request.REQUEST['query'].split()
    if len(splitter) == 1:
        # users
        users = User.objects.filter(Q(firstName__contains=splitter[0].lower()) |
                                    Q(lastName__contains=splitter[0].lower())
                                    )

        # TODO: projects and posts must search also ....

    elif len(splitter) == 2:
        users = User.objects.filter((Q(firstName__contains=splitter[0].lower()) |
                                    Q(lastName__contains=splitter[0].lower())) &
                                    (Q(firstName__contains=splitter[1].lower()) |
                                    Q(lastName__contains=splitter[1].lower())))

    else:
        # TODO: projects and posts must search also ....
        pass

    if not users:
        return HttpResponse(json.dumps(response), content_type='application.json')
    response["found"] = 1
    for member in users:
        response["users"].append({"firstname": member.firstName, "lastname": member.lastName})
    return HttpResponse(json.dumps(response), content_type='application.json')


def checkEmailInDB(request):
    response = {"found": 0}
    users = User.objects.filter(email=request.REQUEST['query'])
    if not users:
        return HttpResponse(json.dumps(response), content_type='application.json')
    else:
        response["found"] = 1
        return HttpResponse(json.dumps(response), content_type='application.json')


def registerCheck(request):
    #check that firstName is valid(containing number and letters only)
    firstName = request.REQUEST['firstname']

    firstAndLastNameRegex = r'^[a-zA-Z0-9]+$'
    emailRegex = r'[a-zA-Z0-9_]+(\.[a-zA-Z0-9_+])*@[a-zA-Z0-9_]+\.[a-zA-Z0-9_.+]{2,}$'

    isValidFirstName = re.match(firstAndLastNameRegex, firstName)

    lastName = request.REQUEST['lastname']
    isValidLastName = re.match(firstAndLastNameRegex, lastName)

    email = request.REQUEST['emailaddress']
    isValidEmailAddress = re.match(emailRegex, email)

    #email must be unique
    if isValidEmailAddress:
        if User.objects.filter(email=request.REQUEST['emailaddress']):
            isValidEmailAddress = 2
        else:
            isValidEmailAddress = 1
    else:
        isValidEmailAddress = 0

    sex = request.REQUEST['sex']
    isValidSex = 0 if (sex != "male" and sex != "female") else 1

    password = request.REQUEST['password']
    isPasswordValid = 1 if len(password) >= 6 else 0

    rePass = request.REQUEST['repass']
    isRePassValid = 1 if (len(rePass) >= 6 and rePass == password) else 0
    canGoHome = int(bool(
        isValidFirstName and
        isValidLastName and
        isValidEmailAddress and
        isValidSex and
        isPasswordValid and
        isRePassValid
    ))
    response = {"fn": int(bool(isValidFirstName)), "ln": int(bool(isValidLastName)), "email": isValidEmailAddress,
                "sex": isValidSex, "password": isPasswordValid, "rePass": isRePassValid,
                "isOK": canGoHome}

    return HttpResponse(json.dumps(response), content_type='application.json')


def postBoardCheck(request):
    response = {'isOK': 0, 'title': 1, 'content': 1, 'tagList': 1,
                'fn': None,
                'ln': None,
                'id': None,
                'year': None,
                'month': None,
                'day': None,
                'hour': None,
                'minute': None,
                'second': None
                }

    monthNames = {1: "January",
                  2: "February",
                  3: "March",
                  4: "April",
                  5: "May",
                  6: "June",
                  7: "July",
                  8: "August",
                  9: "September",
                  10: "October",
                  11: "November",
                  12: "December"
                  }
    content = request.REQUEST['content']
    tagList = request.REQUEST['tagList']

    title = request.REQUEST['title']
    if not content:
        response['content'] = 0
    if not tagList:
        response['tagList'] = 0
    if not title:
        response['title'] = 0
    if response['content'] and response['tagList'] and response['title']:
        response['isOK'] = 1
        user = User.objects.get(email=request.session['email'])
        STR = ""
        for i in tagList.split():
            STR += i + ","
        myPost = user.boardpost_set.create(date=timezone.now(), content=content, tagList=STR, title=title)
        response['fn'] = user.firstName
        response['ln'] = user.lastName
        response['id'] = myPost.id
        currentDateTime = timezone.now()
        response['year'] = currentDateTime.year
        response['month'] = monthNames[currentDateTime.month]
        response['day'] = currentDateTime.day
        response['hour'] = currentDateTime.hour
        response['minute'] = currentDateTime.minute
        response['second'] = currentDateTime.second

    return HttpResponse(json.dumps(response), content_type='application.json')


def getPosts(request):
    response = {'posts': {
                    "id":[],
                    "title": [],
                    "firstName": [],
                    "lastName": [],
                    "content": [],
                    "tagList": [],
                    "year": [],
                    "month": [],
                    "day": [],
                    "hour": [],
                    "minute": [],
                    "second": []},
                }   # another remaining

    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user']).split(".")
        user = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user[int(firstAndLastName[2])-1]
        else:
            user = user[0]
    except:
        user = User.objects.get(email=request.session['email'])

    #query for get tracing posts from 'TRACING USERs'

    tracingList = []
    for tracingUser in user.TraceShip_userSender.all():
        curUser = User.objects.get(pk=tracingUser.userReceiver_id)
        for post in curUser.boardpost_set.filter(date__gt=tracingUser.senderTime):
            tracingList.append(post)

    for tracingUser2 in user.TraceShip_userReceiver.filter(isUser2AcceptTrace=1):
        curUser = User.objects.get(pk=tracingUser2.userSender_id)
        for post in curUser.boardpost_set.filter(date__gt=tracingUser2.receiverTime):
            tracingList.append(post)

    #query for get the posts that `USER OWNS THEM`

    postsOfUser = user.boardpost_set.all()

    #combine all of queries to send to DOM

    allPosts = sorted(chain(postsOfUser, tracingList), key=lambda instance: instance.date,
                      reverse=True)
    for i in allPosts:
        user = User.objects.filter(pk=i.user_id)[0]
        response['posts']["firstName"].append(user.firstName)
        response['posts']["lastName"].append(user.lastName)
        response['posts']["id"].append(i.id)
        response['posts']["title"].append(i.title)
        response['posts']["content"].append(i.content)
        response['posts']['month'].append(i.date.month)
        response['posts']['day'].append(i.date.day)
        response['posts']['hour'].append(i.date.hour)
        response['posts']['minute'].append(i.date.minute)
        response['posts']['second'].append(i.date.second)
        response['posts']['year'].append(i.date.year)
        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' '))

        #else ?

    #another queries ..... (traceShip , ...)
    #......................

    return HttpResponse(json.dumps(response), content_type='application.json')


def getPAC(request):
    response = {'posts': {
                    "isPost": [],
                    "firstName": [],
                    "lastName": [],
                    "id": [],
                    "title": [],
                    "content": [],
                    "tagList": [],
                    "year": [],
                    "month": [],
                    "day": [],
                    "hour": [],
                    "minute": [],
                    "second": [],
                    "developers": [],
                    "manager": [],
                    "picture": [],
                    "sourceCode": [],
                    "usage": []}, }   # another remaining
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user']).split(".")
        user = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user[int(firstAndLastName[2])-1]
        else:
            user = user[0]
    except:
        user = User.objects.get(email=request.session['email'])

    #query for get tracing posts from 'TRACING USERs'

    tracingList = []
    for tracingUser in user.TraceShip_userSender.all():
        curUser = User.objects.get(pk=tracingUser.userReceiver_id)
        for post in curUser.boardpost_set.filter(date__gt=tracingUser.senderTime):
            tracingList.append(post)
        for competence in curUser.competence_set.filter(date__gt=tracingUser.senderTime):
            tracingList.append(competence)

    for tracingUser2 in user.TraceShip_userReceiver.filter(isUser2AcceptTrace=1):
        curUser = User.objects.get(pk=tracingUser2.userSender_id)
        for post in curUser.boardpost_set.filter(date__gt=tracingUser2.receiverTime):
            tracingList.append(post)
        for competence in curUser.competence_set.filter(date__gt=tracingUser2.receiverTime):
            tracingList.append(competence)

    #query for get the posts that `USER OWNS THEM`

    postsOfUser = user.boardpost_set.all()
    competencesOfUser = user.competence_set.all()

    #combine all of queries to send to DOM

    allPosts = sorted(chain(postsOfUser, competencesOfUser, tracingList), key=lambda instance: instance.date,
                      reverse=True)
    for i in allPosts:
        user = User.objects.filter(pk=i.user_id)[0]
        response['posts']["firstName"].append(user.firstName)
        response['posts']["lastName"].append(user.lastName)
        response['posts']["id"].append(i.id)
        response['posts']["title"].append(i.title)
        response['posts']["content"].append(i.content)
        response['posts']['month'].append(i.date.month)
        response['posts']['day'].append(i.date.day)
        response['posts']['hour'].append(i.date.hour)
        response['posts']['minute'].append(i.date.minute)
        response['posts']['second'].append(i.date.second)
        response['posts']['year'].append(i.date.year)
        # if i.picture.url[1] == 'm':
        try:
            if i.picture.url[1] == 'm':
                response['posts']['picture'].append(i.picture.url[13:])
            else:
                response['posts']['picture'].append(i.picture.url)
        except:
            response['posts']['picture'].append(None)

        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' '))

        try:
            response['posts']['sourceCode'].append(i.sourceCode.url[13:])
        except:
            response['posts']['sourceCode'].append(None)

        if isinstance(i, BoardPost):
            response['posts']["isPost"].append(1)
            response['posts']["developers"].append(None)
            response['posts']["manager"].append(None)
            response['posts']["usage"].append(None)
        elif isinstance(i, Competence):
            response['posts']["isPost"].append(0)
            response['posts']["developers"].append(i.developers)
            response['posts']["manager"].append(i.manager)
            response['posts']["usage"].append(i.usage)

        #else ?

    #another queries ..... (traceShip , ...)
    #......................

    return HttpResponse(json.dumps(response), content_type='application.json')


def getCompetence(request):
    response = {'posts': {
                    "id":[],
                    "firstName": [],
                    "lastName": [],
                    "title": [],
                    "content": [],
                    "tagList": [],
                    "year": [],
                    "month": [],
                    "day": [],
                    "hour": [],
                    "minute": [],
                    "second": [],
                    "developers": [],
                    "manager": [],
                    "picture": [],
                    "sourceCode": [],
                    "usage": []}, }   # another remaining
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user']).split(".")
        user = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user[int(firstAndLastName[2])-1]
        else:
            user = user[0]
    except:
        user = User.objects.get(email=request.session['email'])

    #query for get tracing posts from 'TRACING USERs'

    tracingList = []
    for tracingUser in user.TraceShip_userSender.all():
        curUser = User.objects.get(pk=tracingUser.userReceiver_id)
        for competence in curUser.competence_set.filter(date__gt=tracingUser.senderTime):
            tracingList.append(competence)

    for tracingUser2 in user.TraceShip_userReceiver.filter(isUser2AcceptTrace=1):
        curUser = User.objects.get(pk=tracingUser2.userSender_id)
        for competence in curUser.competence_set.filter(date__gt=tracingUser2.receiverTime):
            tracingList.append(competence)

    #query for get the posts that `USER OWNS THEM`

    competencesOfUser = user.competence_set.all()

    #combine all of queries to send to DOM

    allPosts = sorted(chain(competencesOfUser, tracingList), key=lambda instance: instance.date,
                      reverse=True)
    for i in allPosts:
        user = User.objects.filter(pk=i.user_id)[0]
        response['posts']["id"].append(i.id)
        response['posts']["firstName"].append(user.firstName)
        response['posts']["lastName"].append(user.lastName)
        response['posts']["title"].append(i.title)
        response['posts']["content"].append(i.content)
        response['posts']['month'].append(i.date.month)
        response['posts']['day'].append(i.date.day)
        response['posts']['hour'].append(i.date.hour)
        response['posts']['minute'].append(i.date.minute)
        response['posts']['second'].append(i.date.second)
        response['posts']['year'].append(i.date.year)
        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' '))
        response['posts']["developers"].append(i.developers)
        response['posts']["manager"].append(i.manager)
        response['posts']["usage"].append(i.usage)
        if i.picture.url[1] == 'm':
            response['posts']['picture'].append(i.picture.url[13:])
        else:
            response['posts']['picture'].append(i.picture.url)
        try:
            response['posts']['sourceCode'].append(i.sourceCode.url[13:])
        except:
            response['posts']['sourceCode'].append(None)

        #else ?

    #another queries ..... (traceShip , ...)
    #......................

    return HttpResponse(json.dumps(response), content_type='application.json')


def competenceCheck(request):
    response = {'isOK': 0, 'title': 1, 'content': 1, 'tagList': 1, 'developers': 1, 'manager': 1, 'picture': 1,
                'sourceCode': 1, 'usage': 1}
    title = request.REQUEST['title']
    content = request.REQUEST['content']
    tagList = request.REQUEST['tagList']
    developers = request.REQUEST['developers']
    manager = request.REQUEST['manager']
    picture = request.REQUEST['picture']
    sourceCode = request.REQUEST['sourceCode']
    usage = request.REQUEST['usage']
    time1 = datetime.today()
    if not title:
        response['title'] = 0
    if not tagList:
        response['tagList'] = 0
    if not developers:
        response['developers'] = 0
    if not manager:
        response['manager'] = 0
    if not picture:
        response['picture'] = 0
    if not content:
        response['content'] = 1
    if not usage:
        response['usage'] = 1
    if not sourceCode:
        response['sourceCode'] = 0
    return HttpResponse(json.dumps(response), content_type='application.json')


def traceShip(request):
    response = {'isOK': 0}
    userSender = User.objects.get(pk=request.session['user_id'])

    userReceiverFN = request.REQUEST['userReceiverFirstName']
    userReceiverLN = request.REQUEST['userReceiverLastName']
    userReceiverNUM = request.REQUEST['userReceiverNumber']
    userReceiver = User.objects.filter(firstName=userReceiverFN, lastName=userReceiverLN)
    if userReceiverNUM:
        userReceiver = userReceiver[int(userReceiverNUM)-1]
    else:
        userReceiver = userReceiver[0]
    if not (userSender.TraceShip_userSender.filter(userReceiver=userReceiver.id) or
            userReceiver.TraceShip_userSender.filter(userReceiver=userSender.id)):
        userSender.TraceShip_userSender.create(userReceiver=userReceiver,
                                               isUser2AcceptTrace=0,
                                               isShowNotificationToUser2=1,
                                               isShowNotificationToUser1=0,
                                               senderTime=timezone.now(),
                                               receiverTime=timezone.now())
    if userReceiver.TraceShip_userSender.filter(userReceiver=userSender.id):
        mustBeChange = userReceiver.TraceShip_userSender.get(userReceiver_id=request.session["user_id"])
        mustBeChange.isUser2AcceptTrace = True
        mustBeChange.isShowNotificationToUser1 = True
        mustBeChange.isShowNotificationToUser2 = False
        mustBeChange.save()
    response['isOK'] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')


def getNotification(request):
    response = {"traceUsers": [], "tracebackUsers": [],"post":[],"competence":[],"post1":[],"competence1":[]}
    curUser = User.objects.get(pk=request.session['user_id'])
    gravatar_url = "www.gravatar.com/avatar"
    for j in curUser.TraceShip_userReceiver.all():
        if j.isShowNotificationToUser2:
            destinationUser = User.objects.get(pk=j.userSender_id)
            response["traceUsers"].append({"firstname": destinationUser.firstName,
                                           "lastname": destinationUser.lastName})
    for j in curUser.TraceShip_userSender.all():
        if j.isShowNotificationToUser1:
            destinationUser = User.objects.get(pk=j.userReceiver_id)
            response["tracebackUsers"].append({"firstname": destinationUser.firstName,
                                               "lastname": destinationUser.lastName})


    for k in CommentCompetence.objects.filter(user=curUser.id):
        for j in CommentCompetence.objects.filter(referenceComment = k.id,user_notification='0'):
            replier = User.objects.get(id = j.user)
            main = Competence.objects.get(id = j.referenceCompetence_id)
            emailHash = hashlib.md5(replier.email).hexdigest()
            image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            if (curUser.id != replier.id):
                response["competence"].append({"firstname": replier.firstName,
                                               "lastname":replier.lastName,
                                               "hash":image_url1,
                                               "id":main.id,
                                               "title":main.title,
                                               "this":j.id
                })



    for j in Competence.objects.filter(user=curUser.id):

        for a in CommentCompetence.objects.filter(referenceCompetence=j.id,main_notification='0',referenceComment='0'):
            commenter = User.objects.get(id=a.user)
            emailHash = hashlib.md5(commenter.email).hexdigest()
            image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            if (curUser.id != commenter.id):

                response["competence1"].append({"firstname": commenter.firstName,
                                                "lastname":commenter.lastName,
                                                "hash":image_url1,
                                                "id":j.id,
                                                "title":j.title,
                                                "this":a.id

                })



    for j in BoardPost.objects.filter(user=curUser.id):
        for a in CommentPost.objects.filter(referencePost=j.id,main_notification='0',referenceComment='0'):
            commenter = User.objects.get(id=a.user)
            emailHash = hashlib.md5(commenter.email).hexdigest()
            image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            if (curUser.id != commenter.id):
                response["post1"].append({"firstname": commenter.firstName,
                                          "lastname":commenter.lastName,
                                          "hash":image_url1,
                                          "id":j.id,
                                          "title":j.title,
                                          "this":a.id

                })


    for k1 in CommentPost.objects.filter(user=curUser.id):
        for j in CommentPost.objects.filter(referenceComment = k1.id,user_notification='0'):
            replier = User.objects.get(id = j.user)
            main = BoardPost.objects.get(id = j.referencePost_id)
            emailHash = hashlib.md5(replier.email).hexdigest()
            image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
            if (curUser.id != replier.id):

                response["post"].append({"firstname": replier.firstName,
                                         "lastname":replier.lastName,
                                         "hash":image_url1,
                                         "id":main.id,
                                         "title":main.title,
                                         "this":j.id
                })



    return HttpResponse(json.dumps(response), content_type='application.json')


def notShowAgain(request):
    response = {"isOK": 0}

    #TODO:if two users with same firstName and lastName then this doesn't work => must be check with id
    # => (find a way to show number of user in DOM that user don't sense it like hidden paragraph)
    # => userFN.userLN & userFN.userLN.2 => if this two users send trace back request to a user DOM get don't work
    # => and cause exception

    curUser = User.objects.filter(firstName=request.REQUEST['firstName'].split()[0],
                                  lastName=request.REQUEST['lastName'].split()[0])
    curUser = curUser[0]
    mustBeChange = curUser.TraceShip_userSender.get(userReceiver_id=request.session["user_id"])
    mustBeChange.isShowNotificationToUser2 = False
    mustBeChange.save()

    response["isOK"] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')


def notShowAgainTB(request):
    response = {"isOK": 0}

    #TODO:if two users with same firstName and lastName then this doesn't work => must be check with id
    # => (find a way to show number of user in DOM that user don't sense it like hidden paragraph)
    # => userFN.userLN & userFN.userLN.2 => if this two users send trace back request to a user DOM get don't work
    # => and cause exception

    curUser = User.objects.filter(firstName=request.REQUEST['firstName'].split()[0],
                                  lastName=request.REQUEST['lastName'].split()[0])
    curUser = curUser[0]
    mustBeChange = curUser.TraceShip_userReceiver.get(userSender_id=request.session["user_id"])
    mustBeChange.isShowNotificationToUser1 = False
    mustBeChange.save()

    response["isOK"] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')


def traceback(request):
    response = {"isOK": 0}

    #TODO:if two users with same firstName and lastName then this doesn't work => must be check with id
    # => (find a way to show number of user in DOM that user don't sense it like hidden paragraph)
    # => userFN.userLN & userFN.userLN.2 => if this two users send trace back request to a user DOM get don't work
    # => and cause exception

    curUser = User.objects.filter(firstName=request.REQUEST['firstName'].split()[0],
                                  lastName=request.REQUEST['lastName'].split()[0])
    curUser = curUser[0]
    mustBeChange = curUser.TraceShip_userSender.get(userReceiver_id=request.session["user_id"])
    mustBeChange.isUser2AcceptTrace = True
    mustBeChange.isShowNotificationToUser1 = True
    mustBeChange.isShowNotificationToUser2 = False
    mustBeChange.receiverTime = timezone.now()
    mustBeChange.save()

    response["isOK"] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')

def traceNum(request):
    response = {'tracer': [], 'tracing': [], 'email': []}
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user1']).split(".")
        user2 = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user2[int(firstAndLastName[2]) - 1]
        else:
            user = user2[0]
    except:
        user = User.objects.get(email=request.session['email'])
    response['email'] = user.email
    a = TraceShip.objects.filter(userSender=user.id).count()
    b = TraceShip.objects.filter(userReceiver=user.id,isUser2AcceptTrace=1).count()
    c = a + b
    response['tracing'] = c
    d = TraceShip.objects.filter(userReceiver=user.id).count()
    e = TraceShip.objects.filter(userSender=user.id, isUser2AcceptTrace=1).count()
    response['tracer'] = d + e
    return HttpResponse(json.dumps(response), content_type='application.json')


def reply(request):
    response = {'isOk':0,'firstName':[],'lastName':[],
                'time':{'year':[],'month':[],'day':[],'hour':[],'minute':[],'second':[]},
                'depth':[],'content':[],'hash':[],}
    gravatar_url = "www.gravatar.com/avatar"
    reference = request.REQUEST['address'].split("/")
    idtemp = reference[2].split(".")
    monthNames = {1: "Jan",
                  2: "Feb",
                  3: "Mar",
                  4: "Apr",
                  5: "May",
                  6: "Jun",
                  7: "Jul",
                  8: "Aug",
                  9: "Sep",
                  10: "Oct",
                  11: "Nov",
                  12: "Dec"
    }
    content= request.REQUEST['content']
    comment_id =  request.REQUEST['comment_id']
    email =  request.REQUEST['email']
    user = User.objects.get(email=email)
    id1 =  request.REQUEST['id']
    if(reference[1]=="Post"):
        main = BoardPost.objects.get(id= id1 )
        comment1 = CommentPost.objects.get(id=comment_id)


    elif(reference[1]=="Competence"):
        main = Competence.objects.get(id= id1 )
        comment1 = CommentCompetence.objects.get(id=comment_id)


    depth = comment1.depth
    new_depth = depth+1
    emailHash = hashlib.md5(user.email).hexdigest()
    image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
    response['hash']=image_url1
    response['time']['year'] = timezone.now().year
    response['time']['month'] = monthNames[timezone.now().month]
    response['time']['day'] = timezone.now().day
    response['time']['hour'] = timezone.now().hour
    response['time']['minute'] = timezone.now().minute
    response['time']['second'] = timezone.now().second

    if(reference[1]=="Post"):
        main.commentpost_set.create(user=user.id,content=content,referencePost=main.id,referenceComment = comment1.id,user_notification=0,depth=new_depth,time = timezone.now())
        response['isOk'] = 1
    elif(reference[1]=="Competence"):
        main.commentcompetence_set.create(user=user.id,content=content,referenceCompetence=main.id,referenceComment = comment1.id,user_notification=0,depth=new_depth,time = timezone.now())
        response['isOk'] = 1
    response['firstName'] = user.firstName
    response['lastName'] = user.lastName
    response['content'] = content
    response['depth'] = new_depth*2
    return HttpResponse(json.dumps(response), content_type='application.json')


def comment(request):
    response = {'isOk': 0,'repeat':0,'name':[],'mohtava':[],'null':0,
                'email':[], 'time':{'year':[],'month':[],'day':[],'hour':[],'minute':[],'second':[]},}
    reference = request.REQUEST['address'].split("/")
    id1 = reference[2].split(".")
    content = request.REQUEST['content']
    a = content.replace("\n","")
    b = a.replace("\r","")
    owner = request.REQUEST['owner'].split(":")
    gravatar_url = "www.gravatar.com/avatar"
    monthNames = {1: "Jan",
                  2: "Feb",
                  3: "Mar",
                  4: "Apr",
                  5: "May",
                  6: "Jun",
                  7: "Jul",
                  8: "Aug",
                  9: "Sep",
                  10: "Oct",
                  11: "Nov",
                  12: "Dec"
    }
    x = owner[1].split(" ")
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user1']).split(".")
        post_id = firstAndLastName[2]
        user2 = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user2[int(firstAndLastName[2]) - 1]
        else:
            user = user2[0]
    except:
        user = User.objects.get(email=request.session['email'])

    print user.firstName + " "+ user.lastName
    response["name"]=user.firstName + " "+ user.lastName
    emailHash = hashlib.md5(user.email).hexdigest()
    image_url1 = "http://"+gravatar_url+"/"+emailHash+"?s=210&d=identicon&r=PG"
    print timezone.now().hour
    response['email']=image_url1
    response['time']['year'] = timezone.now().year
    response['time']['month'] = monthNames[timezone.now().month]
    response['time']['day'] = timezone.now().day
    response['time']['hour'] = timezone.now().hour
    response['time']['minute'] = timezone.now().minute
    response['time']['second'] = timezone.now().second
    response["mohtava"] =content
    print user.id
    print reference[1]
    print reference[2]
    print content
    print id1[0]
    print id1[1]
    if (b == ""):
        response['null'] = 1
    else:
        if(reference[1]=="Post"):
            id2 = BoardPost.objects.get(id=id1[1])
            id2.commentpost_set.create(user=user.id,content=content,referencePost=id2.id,time = timezone.now())
        elif(reference[1]=="Competence"):
            id2 = Competence.objects.get(id=id1[1])
            id2.commentcompetence_set.create(user=user.id,content=content,referenceCompetence=id2.id,time = timezone.now())

    response['isOk'] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')



def remove(request):
    def child1(a):
        children = CommentPost.objects.filter(referenceComment=a)
        for i in children:
            response["children"].append(i.id)
            if i.referenceComment != '0':
                child1(i.id)
            i.delete()
    def child2(a):
        children = CommentCompetence.objects.filter(referenceComment=a)
        for i in children:
            response["children"].append(i.id)
            if i.referenceComment != '0':
                child2(i.id)
            i.delete()
    response = {"isOK": 0,"children":[]}
    main = request.REQUEST["main"]
    myid = request.REQUEST["id"]
    id1 = main.split(".")
    type = id1[0].split("/")
    if type[1]=="Competence":
        mustBeDelete = CommentCompetence.objects.get(id=myid)
        if mustBeDelete.referenceComment != '0':
            child2(mustBeDelete.id)
        mustBeDelete.delete()
    elif type[1]=="Post":
        mustBeDelete = CommentPost.objects.get(id=myid)
        if mustBeDelete.referenceComment != '0':
            child1(mustBeDelete.id)
        mustBeDelete.delete()
        #children.delete()
    #mustBeDelete.delete()


    print "delete ok "
    response["isOK"] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')


def reply_not(request):
    response = {"isOK": 0}
    main = request.REQUEST["main"]
    page = request.REQUEST["page"]
    id1 = main.split(":")
    if id1[0]=="Competence":
        mustBeChange = CommentCompetence.objects.get(id=id1[1])
    elif id1[0]=="Post":
        mustBeChange = CommentPost.objects.get(id=id1[1])

    mustBeChange.user_notification = True
    mustBeChange.save()
    print "reply ok"
    response["isOK"] = 1

    return HttpResponse(json.dumps(response), content_type='application.json')


def comment_not(request):
    response = {"isOK": 0}
    main = request.REQUEST["main"]
    page = request.REQUEST["page"]
    id1 = main.split(":")


    if id1[0]=="Competence":
        mustBeChange = CommentCompetence.objects.get(id=id1[1])
    elif id1[0]=="Post":
        mustBeChange = CommentPost.objects.get(id=id1[1])

    mustBeChange.main_notification = True
    mustBeChange.save()
    print "comment ok "
    response["isOK"] = 1
    return HttpResponse(json.dumps(response), content_type='application.json')

