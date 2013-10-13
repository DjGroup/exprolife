# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render

from social.models import *


def isset(dict, string):
    try:
        if dict[string]:
            return True
    except:
        return False


def index(request):
    #is currently logged in ?
    if isset(request.session, 'user_id') and isset(request.session, 'first_name') and isset(request.session, 'last_name') :
            template = loader.get_template('social/psychograph.html')
            context = RequestContext(request, )
            return HttpResponse(template.render(context))
    try:
        try:
                #register
                user = User.objects.create(firstName=request.POST['firstname'],
                                           lastName=request.POST['lastname'],
                                           password=request.POST['password'],
                                           email=request.POST['email'],
                                           sex=0 if request.POST['gender'] == 'male' else 1 if request.POST['gender'] ==
                                           'female' else -1,
                                           )
                user.save()
                #sessions that needed for User in pages
                request.session['user_id'] = user.id
                request.session['first_name'] = user.firstName
                request.session['last_name'] = user.lastName

                template = loader.get_template('social/psychograph.html')
                context = RequestContext(request, )
                return HttpResponse(template.render(context))
        #login
        except:
                #checking the username and password for correctness
                # this must be changed in later by encrypt the
                # password and change the logic of the login form(this may be hackable ....)

                loginedUser = User.objects.filter(email=request.POST['email'])

                #if user exists (means email exists )
                if loginedUser:
                    #check the password
                    if loginedUser[0].password == request.POST['password']:
                        request.session['user_id'] = loginedUser[0].id
                        request.session['first_name'] = loginedUser[0].firstName
                        request.session['last_name'] = loginedUser[0].lastName
                        template = loader.get_template('social/psychograph.html')
                        context = RequestContext(request, {
                        })
                        return HttpResponse(template.render(context))
                    else:
                        template = loader.get_template('social/index.html')
                        context = RequestContext(request, {
                            'error': 'your password is not correct !!'
                        })
                        return HttpResponse(template.render(context))
                else:
                    template = loader.get_template('social/index.html')
                    context = RequestContext(request, {
                        'error': "this email doesn't exist !!"
                    })
                    return HttpResponse(template.render(context))


    except:
        return render(request, 'social/index.html')