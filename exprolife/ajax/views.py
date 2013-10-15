from django.http import HttpResponse
from social.models import *
from django.db.models import Q
import re
import json
from datetime import datetime


def autocompleteModel(request):
    response = {"users": [], "found": 0}
    users = User.objects.filter(Q(firstName__startswith=request.REQUEST['query']) |
                                Q(lastName__startswith=request.REQUEST['query']))
    if not users:
        return HttpResponse(json.dumps(response), content_type='application.json')
    response["found"] = 1
    for member in users:
        response["users"].append({"firstname": member.firstName, "lastname": member.lastName})
    return HttpResponse(json.dumps(response), content_type='application.json')