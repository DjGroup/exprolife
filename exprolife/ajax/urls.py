from django.conf.urls import patterns, url
from ajax import views

urlpatterns = patterns('',
    #when search box in psychograph is typed autocompleteModel will call
    url(r'^search/$', views.autocompleteModel, name='ajaxSearch'),

    #when email appearance in register form is valid then must check in DB that is unique or not
    url(r'emailCheck/$', views.checkEmailInDB, name='ajaxEmailCheck'),

    #check that is fileds that in refister form is valid or not
    url(r'registercheck/$', views.registerCheck, name='ajaxRegisterCheck'),

    #check that is valid fileds in board from fields and then send isOK signal to DOM with js
    url(r'postboardcheck/$', views.postBoardCheck, name='ajaxPostBoardCheck'),

    #get posts that related to the current user and send them to DOM
    url(r'getposts/$', views.getPosts, name='ajaxBoardPostsCheck'),

    url(r'traceNum/$', views.traceNum, name='ajaxBoardPostsCheck'),

    #get competence that related to the current user and send them to DOM
    url(r'getCompetence/$', views.getCompetence, name='ajaxCompetence'),

    #check that is valid fields in competence and then send isOK signal to DOM with js
    url(r'competenceCheck/$', views.competenceCheck, name='ajaxcompetenceCheck'),

    #trace button in another users profile has a TRACE button that when press this function will call
    url(r'trace/$', views.traceShip, name='ajaxTraceShipRequest'),

    #get the notifications of the current user (trace back requests)
    url(r'getnot/$', views.getNotification, name='ajaxGetNotification'),

    #in trace back requests OK button will call this function that cause don't show again when user log in
    url(r'notshowagain/$', views.notShowAgain, name='ajaxNotShowAgain'),

    #don't show trace back notification in notBOX
    url(r'notshowagaintb/$', views.notShowAgainTB, name='ajaxNotShowAgainTraceBackRequest'),

    #traceback functionality : when someone click in the trace button in his/her notification box (box that contains OK
    #and TRACE button
    url(r'traceback/$', views.traceback, name='ajaxTraceback'),

    #get posts and competences in Feed
    url(r'getpac/$', views.getPAC, name='ajaxGetPostsAndCompetences'),

    url(r'comment/$', views.comment, name='comment'),

    url(r'reply/$', views.reply, name='reply'),

    url(r'remove/$', views.remove, name='remove'),

    url(r'reply_not/$', views.reply_not, name='replynotification'),

    url(r'comment_not/$', views.comment_not, name='commentnotification'),

    # rate a project with ajax
    url(r'rate/$', views.rateProject, name="rateProjectAjax"),

    # top users show in psychograph
    url(r'tusers/$', views.TUsers, name="topUsersAjax"),

    # top projects ...
    url(r'tprojects/$', views.TProjects, name="topProjectsAjax"),

    url(r'getid/$', views.getID, name="getUserId"),

    #show post information for edit
    url(r'postinfo/$', views.postinfo, name='info'),

    url(r'editpost/$', views.editpost, name='info'),

    url(r'editcomp/$', views.editcomp, name='info'),

    #show competence information for edit
    url(r'cominfo/$', views.cominfo, name='info'),

    url(r'removepost/$', views.removepost, name='rpost'),

    url(r'removecomp/$', views.removecomp, name='rpost'),

    )
