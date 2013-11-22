from django.http import HttpResponse
from social.models import *
from django.db.models import Q
import re
import json
from datetime import datetime

from itertools import chain

from django.utils import timezone


def autocompleteModel(request):
    response = {"users": [], "found": 0}
    splitter = request.REQUEST['query'].split()
    if len(splitter) == 1:
        # users
        users = User.objects.filter(Q(firstName__contains=splitter[0]) |
                                    Q(lastName__contains=splitter[0])
                                    )

        # TODO: projects and posts must search also ....

    elif len(splitter) == 2:
        print splitter
        users = User.objects.filter((Q(firstName__contains=splitter[0]) |
                                    Q(lastName__contains=splitter[0])) &
                                    (Q(firstName__contains=splitter[1]) |
                                    Q(lastName__contains=splitter[1])))

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
    # print request.session['first_name']
    if not content:
        response['content'] = 0
    if not tagList:
        response['tagList'] = 0
    if not title:
        response['title'] = 0
    if response['content'] and response['tagList'] and response['title']:
        response['isOK'] = 1
        user = User.objects.get(email=request.session['email'])
        user.boardpost_set.create(date=timezone.now(), content=content, tagList=tagList, title=title)
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
        response['posts']["title"].append(i.title)
        response['posts']["content"].append(i.content)
        response['posts']['month'].append(i.date.month)
        response['posts']['day'].append(i.date.day)
        response['posts']['hour'].append(i.date.hour)
        response['posts']['minute'].append(i.date.minute)
        response['posts']['second'].append(i.date.second)
        response['posts']['year'].append(i.date.year)
        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' ').split())

        #else ?

    #another queries ..... (traceShip , ...)
    #......................

    return HttpResponse(json.dumps(response), content_type='application.json')


def getPAC(request):
    response = {'posts': {
                    "isPost": [],
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
        response['posts']["title"].append(i.title)
        response['posts']["content"].append(i.content)
        response['posts']['month'].append(i.date.month)
        response['posts']['day'].append(i.date.day)
        response['posts']['hour'].append(i.date.hour)
        response['posts']['minute'].append(i.date.minute)
        response['posts']['second'].append(i.date.second)
        response['posts']['year'].append(i.date.year)
        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' ').split())
        if isinstance(i, BoardPost):
            response['posts']["isPost"].append(1)
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
        response['posts']['tagList'].append(i.tagList.replace(u'\xa0', u' ').split())
        response['posts']["developers"].append(i.developers)
        response['posts']["manager"].append(i.manager)
        response['posts']["usage"].append(i.usage)

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
    if response['title'] and response['tagList'] and response['developers'] and response['manager']:

        response['isOK'] = 1
        user = User.objects.get(email=request.session['email'])
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
    response = {"traceUsers": [], "tracebackUsers": []}
    curUser = User.objects.get(pk=request.session['user_id'])
    for j in curUser.TraceShip_userReceiver.all():
        if j.isShowNotificationToUser2:
            destinationUser = User.objects.get(pk=j.userSender_id)
            response["traceUsers"].append({"firstname": destinationUser.firstName, "lastname": destinationUser.lastName})
    for j in curUser.TraceShip_userSender.all():
        if j.isShowNotificationToUser1:
            destinationUser = User.objects.get(pk=j.userReceiver_id)
            response["tracebackUsers"].append({"firstname": destinationUser.firstName, "lastname": destinationUser.lastName})
    print response
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