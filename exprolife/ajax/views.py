from django.http import HttpResponse
from social.models import *
from django.db.models import Q
import re
import json
from datetime import datetime


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
    response = {'isOK': 0, 'title': 1, 'content': 1, 'tagList': 1}
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
        user.boardpost_set.create(content=content, tagList=tagList, title=title)

    return HttpResponse(json.dumps(response), content_type='application.json')


def getPosts(request):
    response = {'ownPosts': {"title": [], "content": [], "tagList": []}, }   # another remaining
    try:
        pattern = "/"
        firstAndLastName = re.sub(pattern, "", request.REQUEST['user']).split(".")
        user = User.objects.filter(firstName=firstAndLastName[0], lastName=firstAndLastName[1])
        if len(firstAndLastName) == 3:
            user = user[firstAndLastName[2]-1]
        else:
            user = user[0]
    except:
        user = User.objects.get(email=request.session['email'])

    #query for get the posts that `USER OWNS THEM`
    postsOfUser = user.boardpost_set.all()
    for i in postsOfUser:
        response['ownPosts']["title"].append(i.title)
        response['ownPosts']["content"].append(i.content)
        response['ownPosts']['tagList'].append(i.tagList.replace(u'\xa0', u' ').split())

    #another queries ..... (traceShip , ...)
    #......................

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
    Date = time1.strftime('20%y-%m-%d')
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
    if response['title'] and response['tags'] and response['developers'] and response['manager'] and response['picture'] and response['sourceCode'] :
        response['isOK'] = 1
        user = User.objects.get(email=request.session['email'])
        print "ta inja"
        print title+" "+description+" "+tags+" "+developers+" "+manager+" "+picture+" "+Date+" "+sourceCode + " " + \
            usage
        user.competence_set.create(title=title, description=description, tags=tags, developers=developers,
                                   manager=manager, picture=picture,Date=Date , sourceCode=sourceCode, usage=usage)
        print "ok"

    return HttpResponse(json.dumps(response), content_type='application.json')
