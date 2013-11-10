from django.http import HttpResponse
from social.models import *
from django.db.models import Q
import re
import json
from datetime import datetime

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
    response = {'ownPosts': {"title": [], "content": [], "tagList": [], "year": [], "month": [],
                             "day": [], "hour": [], "minute": [], "second": []},}   # another remaining
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

    #query for get the posts that `USER OWNS THEM`

    postsOfUser = user.boardpost_set.all().order_by("-date")
    for i in postsOfUser:
        response['ownPosts']["title"].append(i.title)
        response['ownPosts']["content"].append(i.content)
        response['ownPosts']['tagList'].append(i.tagList.replace(u'\xa0', u' ').split())
        response['ownPosts']['year'].append(i.date.year)
        response['ownPosts']['month'].append(i.date.month)
        response['ownPosts']['day'].append(i.date.day)
        response['ownPosts']['hour'].append(i.date.hour)
        response['ownPosts']['minute'].append(i.date.minute)
        response['ownPosts']['second'].append(i.date.second)


    #another queries ..... (traceShip , ...)
    #......................

    return HttpResponse(json.dumps(response), content_type='application.json')






def getCompetence(request):

    response = {'ownCompetences': {"title": [], "description": [], "tags": [], "developers": [], "manager": [], "picture": [],
                                   "year": [], "month": [], "day": [], "hour": [], "minute": [], "second": [],
                                   "sourceCode": [], "usage": []}, }
    user = User.objects.get(email=request.session['email'])
    competencesOfUser = user.competence_set.all().order_by("-date")
    for i in competencesOfUser:
        response['ownCompetences']["title"].append(i.title)
        response['ownCompetences']["description"].append(i.description)
        response['ownCompetences']['tags'].append(i.tags.replace(u'\xa0', u' ').split())
        response['ownCompetences']["developers"].append(i.developers)
        response['ownCompetences']["manager"].append(i.manager)
        response['ownCompetences']["year"].append(i.date.year)
        response['ownCompetences']["month"].append(i.date.month)
        response['ownCompetences']["day"].append(i.date.day)
        response['ownCompetences']["hour"].append(i.date.hour)
        response['ownCompetences']["minute"].append(i.date.minute)
        response['ownCompetences']["second"].append(i.date.second)

        response['ownCompetences']["usage"].append(i.usage)

    return HttpResponse(json.dumps(response), content_type='application.json')



def competenceCheck(request):
    response = {'isOK': 0, 'title': 1, 'description': 1, 'tags': 1, 'developers': 1, 'manager': 1, 'picture': 1,
                'sourceCode': 1, 'usage': 1}
    title = request.REQUEST['title']
    description = request.REQUEST['description']
    tags = request.REQUEST['tags']
    developers = request.REQUEST['developers']
    manager = request.REQUEST['manager']
    picture = request.REQUEST['picture']
    sourceCode = request.REQUEST['sourceCode']
    usage = request.REQUEST['usage']
    time1 = datetime.today()
    Date = time1.strftime('%Y-%m-%d')
    print request.session['first_name']
    if not title:
        response['title'] = 0
    if not tags:
        response['tags'] = 0
    if not developers:
        response['developers'] = 0
    if not manager:
        response['manager'] = 0
    if not picture:
        response['picture'] = 0
    if not description:
        response['description'] = 1
    if not usage:
        response['usage'] = 1
    if not sourceCode:
        response['sourceCode'] = 0
    if response['title'] and response['tags'] and response['developers'] and response['manager']:

        response['isOK'] = 1
        user = User.objects.get(email=request.session['email'])
        # print title+" "+description+" "+tags+" "+developers+" "+manager+" "+picture+" "+
        # str(timezone.now())+" "+sourceCode + " " + \
        #     usage
        user.competence_set.create(title=title, description=description, tags=tags, developers=developers,
                                  manager=manager, picture=picture, date=timezone.now(), sourceCode=sourceCode,
                                 usage=usage)
    return HttpResponse(json.dumps(response), content_type='application.json')
