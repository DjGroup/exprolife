/********************  BEGIN  ******************/
/****************** CONSTANTS ******************/
/************ AND REQUIRED FUNCTIONS ***********/
/***********************************************/

var isContinueAjax=false;

var escapeTags = function(str) {
    return str.replace(/</g, '&lt;').replace(/>/g, '&gt;');
};

//use this function to send ajax post, project and PAC queries (code bloat)
function ajaxer(type, content, result){
    if (!(type=='getTUsers') && !(type=='getTProjects') ){
        for(var i=0; i<result.posts.title.length; i++){
            var gID = result.posts.id[i];
            var title = result.posts.title[i];
            var description = result.posts.content[i];
            var tags = result.posts.tagList[i].split(',');
            var length = tags.length;
            if(tags[length-1]==""){
                tags.splice(-1);
            }
            var tagSection = '';
            if(type=='getCompetence' ||(type=='getPAC' && result.posts.isPost[i]=='0')){
                var developers = result.posts.developers[i];
                var manager = result.posts.manager[i];
                var usage = result.posts.usage[i];
                var picture = result.posts.picture[i];
                var sourceCode = result.posts.sourceCode[i];
            }
            for(var j=0; j<tags.length; j++){
                tagSection += '<div class="tag-span">'+ tags[j]+'</div>';
            }
            var currentDiv = '';
            if(type=='getPosts'|| (type=='getPAC' && result.posts.isPost[i]=='1')){
                currentDiv = $('<a class="post-link"><span class="project-div">\
                                    <h3>'+ result.posts.firstName[i] +' '+result.posts.lastName[i] + ' '+ 'Writes:</h3>\
        							<div class="project-desc">\
        							    <span style="display:none;">'+ gID +'</span><h3>'+ title +'</h3>\
        								<h4>'+ description +'</h4>\
        								<div class="project-date">Created '   +result.posts.month[i]+   ' '   +result.posts.day[i]+   ', '   +result.posts.year[i] +   ' at '   +result.posts.hour[i]+   ':'   +result.posts.minute[i]+   ':'   +result.posts.second[i]+   '</div>\
        								<div class="project-tag">'+tagSection +'</div>\
        							</div>\
        							<div class="project-image">\
        							    <div class="project-logo" style="background-image: url(../../static/social/images/logos/post.jpg);"></div>\
        							</div>\
        						</span></a>');
            }else if(type=='getCompetence' || (type=='getPAC' && result.posts.isPost[i]=='0')){
                currentDiv = $('<a class="project-link"><span class="project-div">\
                                    <h3>'+ result.posts.firstName[i] +' '+result.posts.lastName[i] + ' '+ 'Writes:</h3>\
        							<div class="project-desc">\
        								<span style="display:none;">'+ gID +'</span><h3>'+ title +'</h3>\
        								<span>'+ description +'</span>\
        								<div class="project-date">Created '   +result.posts.month[i]+   ' '   +result.posts.day[i]+   ', '   +result.posts.year[i] +   ' at '   +result.posts.hour[i]+   ':'   +result.posts.minute[i]+   ':'   +result.posts.second[i]+   '</div>\
        								<div class="project-tag">'+tagSection +'</div>\
        							</div>\
        							<div class="project-image">\
        								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
        								<div class="score-number">' + result.posts.rate[i] + '</div></div>\
        								<div class="project-logo" style="background-image: url(../..'+ picture + ');"></div>\
        							</div>\
        							<span><center>'+ usage +'</center></span>\
        						</span></a>');
            }
            content.append(currentDiv);
        }
        $(".project-link").on("click", function(){
            var ID = $(this).children().first().children().first().next().children().first().text();
            var title = $(this).children().first().children().first().next().children().first().next().text();
            document.location.href = '/Competence/' + encodeURIComponent(title) + '.' + ID;
        });
        $(".post-link").on("click", function(){
            var ID = $(this).children().first().children().first().next().children().first().text();
            var title = $(this).children().first().children().first().next().children().first().next().text();
            document.location.href = '/Post/' + encodeURIComponent(title) + '.' + ID;
        });
    }
    else{
        if (type=='getTUsers'){
            for(var i=0; i<result.users.FN.length; i++){
                currentDiv = $('<a class="project-link"><span class="project-div">\
        							<div class="project-desc">\
        								<span style="display:none;"></span><h3>'+ result.users.FN[i] + ' ' + result.users.LN[i] +'</h3>\
        							</div>\
        							<div class="project-image">\
        								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
        								<div class="score-number">' + result.users.score[i] + '</div></div>\
        								<div class="project-logo" style="background-image: url('+ result.users.url[i] + ');"></div>\
        							</div>\
        						</span></a>');
                content.append(currentDiv);
            }
            $(".project-link").on("click", function(){
                var FN = $(this).children().first().children().first().find('h3').text().split(" ")[0];
                var LN = $(this).children().first().children().first().find('h3').text().split(" ")[1];
                document.location.href = "/" + FN + "." + LN;
            });
        }
        else{

            for(var i=0; i<result.projects.title.length; i++){
                var tagSection = '';
                tags = result.projects.tagList[i].split(',');
                var length = tags.length;
                if(tags[length-1]==""){
                    tags.splice(-1);
                }
                for(var j=0; j<tags.length; j++){
                    tagSection += '<div class="tag-span">'+ tags[j]+'</div>';
                }
                currentDiv = $('<a class="project-link"><span class="project-div">\
                                    <h3>'+ result.projects.firstName[i] +' '+result.projects.lastName[i] + ' '+ 'Writes:</h3>\
        							<div class="project-desc">\
        								<span style="display:none;">'+ result.projects.id[i] +'</span><h3>'+ result.projects.title[i] +'</h3>\
        								<span>'+ result.projects.content[i] +'</span>\
        								<div class="project-date">Created '   +result.projects.month[i]+   ' '   +result.projects.day[i]+   ', '   +result.projects.year[i] +   ' at '   +result.projects.hour[i]+   ':'   +result.projects.minute[i]+   ':'   +result.projects.second[i]+   '</div>\
        								<div class="project-tag">'+tagSection +'</div>\
        							</div>\
        							<div class="project-image">\
        								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
        								<div class="score-number">' + result.projects.rate[i] + '</div></div>\
        								<div class="project-logo" style="background-image: url(../..'+ result.projects.picture[i] + ');"></div>\
        							</div>\
        							<span><center>'+ result.projects.usage[i] +'</center></span>\
        						</span></a>');
                content.append(currentDiv);
            }
            $(".project-link").on("click", function(){
                var ID = $(this).children().first().children().first().next().children().first().text();
                var title = $(this).children().first().children().first().next().children().first().next().text();
                document.location.href = '/Competence/' + encodeURIComponent(title) + '.' + ID;
            });
        }
    }
}

function removeClick(button){

    $(button).on("click",function(){
        var comment_id = $(this).parent().next().next().text();
        var com = $(this).parent().parent();

        var vars={
            id:comment_id,
            main:window.location.pathname
        };
        $.ajax({
            url: '/ajax/remove',
            dataType: 'json',
            data:vars,
            success:function(result){
                if(result.isOK==1){
                    com.fadeOut("slow");
                    var x = result.children;
                    y = result.children.length;
                    for(i=0;i<y;i++){
                        var me = $('span:contains("'+result.children[i]+'")');
                        me.parent().fadeOut("slow");
                    }
                }
            }
        });
    });
}
function upload(field, upload_url) {
    if (field.files.length == 0) {
        return;
    }
    var file = field.files[0];
    var formData = new FormData();
    formData.append('file_upload', file);
    $.ajax({
        url: upload_url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: console.log('success!')
    });
}

/*******************   END   *******************/
/****************** CONSTANTS ******************/
/************ AND REQUIRED FUNCTIONS ***********/
/***********************************************/

$(document).ready(function(){

/////////////////   BEGIN   ///////////////////////
////////////////   NODE.JS   //////////////////////
///////////////////////////////////////////////////
    var socket = io.connect('localhost', {port: 4000});
    $.ajax({
        url: '/ajax/getid',
        type: 'get',
        success:function(result){
            socket.emit('checkRDB', {ID: result.ID});
        }
    });

    socket.on('show_in_dom_rate', function(data){
        $('.button').text(data.title + " : " + data.change + " unit changed.")
            .fadeIn("fast").delay(8000).fadeOut("slow").on("click", function(){
            window.location.href = "/Competence/" + data.title + "." + data.projID;
        });
    });

    socket.on('show_in_dom_comment', function(data){
        $('.button').text(data.firstName + " " + data.lastName + " comments on '" + data.title +"'")
            .fadeIn("fast").delay(8000).fadeOut("slow").on("click", function(){
                if(!data.isPost){
                    window.location.href = "/Competence/" + data.title + "." + data.ID;
                }else{
                    window.location.href = "/Post/" + data.title + "." + data.ID;
                }
        });
    });


//////////////////   END   ////////////////////////
////////////////   NODE.JS   //////////////////////
///////////////////////////////////////////////////

/////////////////   BEGIN   ///////////////////////
////////// navigation bar in the left /////////////
///////////////////////////////////////////////////
    $(document).keyup(function(key){
        if(key.which==27){
            $('#holder').detach();
            fad = $("#fader");
            fad.css({
                "height":0
            });
            fad.fadeOut("slow");
        }
    });
    var url = window.location.hash;
    url = url.replace("#","");
    url1 = url.split("+");
    var this1 = $("span:contains('"+url1[1]+"')").parent();
    for(i=0;i<3;i++){
        this1.fadeTo("slow",0);
        this1.fadeTo("slow",1);
    }
    var nav = $('#v-nav');
    var items = nav.children('ul').children('li').each(function () {
        $(this).click(function () {
            //remove previous class and add it to clicked tab
            items.removeClass('current');
            $(this).addClass('current');

            //hide all content divs and show current one
            nav.children('div.tab-content').hide().eq(items.index($(this))).fadeIn('fast');

            window.location.hash = $(this).attr('tab');
        });
    });

    if (location.hash) {
        showTab(location.hash);
    }
    else {
        showTab("#Board");
    }

    function showTab(tab) {
        $('#v-nav').children().first().children().each(function(){
            if("#" + $(this).text()==tab){
                $(this).click();
            }
        });
    }

/////////////////    END    ///////////////////////
////////// navigation bar in the left /////////////
///////////////////////////////////////////////////


/////////////////  BEGIN    ///////////////////////
///// Welcome message when login or register //////
///////////////////////////////////////////////////


    $(".alert").animate({
        "right":"50px"
    } , 1500).delay(1000).fadeOut(1000);

/////////////////  END    /////////////////////////
///// Welcome message when login or register //////
///////////////////////////////////////////////////


/////////////////  BEGIN    ///////////////////////
//////// search input box in psychoGraph //////////
///////////////////////////////////////////////////

    // when click somewhere else input search box must be slideUp();
    $(document).not("#Search-input, #searchResultSection").click(function(){
        $("#searchResultSection").slideUp();
    });

    var currentRequest = null;

    // when a key pressed in Keyboard then call this function
    $("#Search-input").keyup(function(){
        var notFound = $(".notfound");
        var searchResultSection = $("#searchResultSection");
        var searchInput = $("#Search-input");
        var itemSearch = $(".itemSearch");
        //remove previous items in search results
        itemSearch.remove();

        // not found text hide  =>  ["Nothing found please try something else"]
        notFound.hide();


        searchResultSection.height("70px");
        // if search input box is empty (by delete all chars or backspace or ...)
        if(!searchInput.val()){

            //slide up search result and hide ajax logo and not found text.
            searchResultSection.slideUp();
            $(".ajaxLogoSearch").hide();
            notFound.hide();
        }

        // else search input box is not empty and search logic works with AJAX
        else{

            // getting value of search input box
            var data = {
                query: searchInput.val()
            };

            //search result slide down and show ajax logo in it
            searchResultSection.slideDown();
            $(".ajaxLogoSearch").show();

            //send AJAX to /ajax/search
            currentRequest = $.ajax({
                url: '/ajax/search',
                data: data,
                dataType:'json',

                // optimize bandwith of server => if two request comes first request aborted <=
                beforeSend : function(){
                    if(currentRequest != null) {
                        currentRequest.abort();
                    }
                },

                //if AJAX success :
                success:function(result){

                    //remove previous results in search result section
                    itemSearch.remove();

                    //if not found:
                    if(result.found==0){
                        $(".ajaxLogoSearch").hide();
                        notFound.show();
                    }

                    //else add to DOM
                    else{
                        var searchResult = $("#searchResultSection");
                        $(".ajaxLogoSearch").hide();
                        searchResult.height("20px");

                        for(var i=0;i<result.users.length;i++){
                            var content = '<div class="itemSearch">\
                    <img src="../../static/social/images/defaultMaleImage.png" height="50px">\
                    <p class="firstname">'+ result.users[i].firstname+ '</p><p class="lastname">'+ result.users[i].lastname +'</p></div>';
                            if(searchResult.height() < 370){
                                searchResult.height("+=70px");
                            }
                            $("#innerSearch").append(content);
                        }

                        /************************   BEGIN   **************************/
                        /************ bind hover and click after AJAX call ***********/
                        /*************************************************************/

                        $(".itemSearch").hover(function(){
                            $(this).css({"background-color":"rgba(85,230,201,0.5)"});
                        },function(){
                            $(this).css({"background-color":"rgba(72,201,176,0.5)"});
                        })
                            .on("click", function(){
                                var first = $(this).children().first().next().text();
                                var last = $(this).children().first().next().next().text();
                                document.location.href= '/' + first + '.' + last;
                            });

                        /************************   END   **************************/
                        /************ bind hover and click after AJAX call ***********/
                        /*************************************************************/
                    }
                }
            });
        }
    });

/////////////////  END    ///////////////////////
//////// search input box in psychoGraph //////////
///////////////////////////////////////////////////




////////////////////// BEGIN  //////////////////////////////
// when click on .first navigation bar its width INCREASE //
////////////////////////////////////////////////////////////

    $('.first, .third').on("click", function(){
        $('#Col-1').fadeOut("slow", function(){
            $('#Col-2').animate({
                width:"1100px"
            }, "slow");
            $('.project-div, .post-div').delay(500).fadeIn("slow");
        });
    });

////////////////////// END  //////////////////////////////
// when click on .first navigation bar its width INCREASE //
////////////////////////////////////////////////////////////


//////////////////////// BEGIN  ////////////////////////////////
// when click on not .first navigation bar its width DECREASE //
////////////////////////////////////////////////////////////////

    nav.children().first().children().not(".first, .third").on("click", function(){
        $('#Col-2').animate({
            width:"800px"
        }, "slow");
        $('#Col-1').delay(500).fadeIn("slow");
        $('.project-div, .post-div').hide();
    });

///////////////////////// END  /////////////////////////////////
// when click on not .first navigation bar its width DECREASE //
////////////////////////////////////////////////////////////////


////////////////////////// BEGIN  /////////////////////////////////
// when submit on board post form in Board section of navigation //
/////// without refreshing added to the DOM with fadeIn ///////////
///////////////////////////////////////////////////////////////////

    $("#Board-form").submit(function(event){
        var tag = $('.tag');
        $(".ajaxLogoBoard").show();

        // prevent send to SERVER
        //TODO:submit must change to normal button because never submit occur
        event.preventDefault();

        // get values from DOM
        var content = $("#text-area").val();
        var tags = tag.find('span').text();
        var title = $('#title-board').val();
        var data ={
            content:content,
            tagList:tags,
            title:title
        };

        //send AJAX to /ajax/postboardcheck
        $.ajax({
            url: '/ajax/postboardcheck',
            data: data,
            dataType: 'json',
            success:function(result){

                // if any field is empty turn its color to light pink => rgba(255, 82, 82, 0.5)
                if(result.title=='0'){
                    $('#title-board').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                // else turn color to white => #FFFFFF
                else{
                    $('#title-board').css({
                        "background" : "#FFFFFF"
                    });
                }
                if(result.content=='0'){
                    $("#Board-form").find('#text-area').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $("#Board-form").find('#text-area').css({
                        "background" : "#FFFFFF"
                    });
                }
                if(result.tagList=='0'){
                    $('#Tag-input_tagsinput').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('#Tag-input_tagsinput').css({
                        "background" : "#FFFFFF"
                    });
                }

                //TODO:ajax logo must hide here ? or must hide end of block ?

                $(".ajaxLogoBoard").hide();

                //if evrything is OK and post can post in board then DO:
                if(result.isOK=='1'){
                    var gID = result.id;
                    var title = escapeTags($('#title-board').val());
                    var description = escapeTags($('#Board-form').children().first().next().val());
                    var tags = escapeTags(tag.text());
                    var tagList = tags.split(String.fromCharCode(160)+String.fromCharCode(160));
                    tagList.splice(-1);
                    var tagSection = '';
                    for(var i=0; i<tagList.length; i++){
                        tagSection += '<div class="tag-span">'+tagList[i]+'</div>';
                    }
                    var mainContent = $('<a class="post-link"><span class="project-div">\
                                <h3>'+ result.fn +' '+ result.ln + ' '+ 'Writes:</h3>\
    							<div class="project-desc">\
    							    <span style="display:none;">'+ gID +'</span><h3>'+ title +'</h3>\
    								<h4>'+ description +'</h4>\
    								<div class="project-date">Created '   +result.month+   ' '   +result.day+   ', '   +result.year +   ' at '   +result.hour +   ':'   +result.minute +  ':'   + result.second +   '</div>\
    								<div class="project-tag">'+tagSection +'</div>\
    							</div>\
    							<div class="project-image">\
    							    <div class="project-logo" style="background-image: url(../../static/social/images/logos/post.jpg);"></div>\
    							</div>\
    						</span></a>');
                    document.getElementById("title-board").value="";
                    document.getElementById("text-area").value="";
                    tag.remove();
                    mainContent.clone().hide().insertAfter($('.content').children().first()).fadeIn("slow");
                    $(".post-link").on("click", function(){
                        var ID = $(this).children().first().children().first().next().children().first().text();
                        var title = $(this).children().first().children().first().next().children().first().next().text();
                        title = title.split(' ').join('%20');
                        document.location.href = '/Post/' + encodeURIComponent(title) + '.' + ID;
                    });
                }
            }
        });
    });

//////////////////////////// END //////////////////////////////////
// when submit on board post form in Board section of navigation //
/////// without refreshing added to the DOM with fadeIn ///////////
///////////////////////////////////////////////////////////////////


///////////////////////   BEGIN  ///////////////////////////////
// every time page loads it get POSTs and PROJECTs from DB in //
///////////////////// behind of door :D/////////////////////////

    var getInfoAjax = $('#getInfoAjax');
    getInfoAjax.show();
    var data ={
        user: window.location.pathname
    };

    //get post and projects every time page loading

    var content = $('.content');
    var isSession = 0;
    if(location.pathname == "/"){
        isSession = 1;
        $.ajax({
            url: '/ajax/getpac',
            dataType: 'json',
            data: data,
            success:function(result){

                //getPAC (PAC => Post And Projects)
                ajaxer('getPAC', content, result);
            }
        });
    }
    if(isSession){
        $(window).hashchange(function(){
            if(location.hash == "#Top"){
                $.ajax({
                    url:'/ajax/tusers',
                    dataType: 'json',
                    success:function(result){
                        content.children().not('#switchAjax').remove();
                        ajaxer('getTUsers', content, result);
                        $('#switchAjax').hide("fast");
                        content.css({
                            "opacity": "1.0"
                        }, "fast");
                    }
                });
            }
            else if(location.hash == "#Board"){
                $.ajax({
                    url: '/ajax/getpac',
                    dataType: 'json',
                    success:function(result){
                        content.children().not('#switchAjax').remove();
                        //getPAC (PAC => Post And Projects)
                        ajaxer('getPAC', content, result);
                        $('#switchAjax').hide("fast");
                        content.css({
                            "opacity": "1.0"
                        }, "fast");
                    }
                });
            }
        });
    }
    else{

        $.ajax({
            url: '/ajax/getpac',
            dataType: 'json',
            data:data,
            success:function(result){
                content.children().not('#switchAjax').remove();
                //getPAC (PAC => Post And Projects)
                ajaxer('getPAC', content, result);
                $('#switchAjax').hide("fast");
                content.css({
                    "opacity": "1.0"
                }, "fast");
            }
        });
    }

    getInfoAjax.hide("slow");

//////////////////////// END ///////////////////////////////////
// every time page loads it get POSTs and PROJECTs from DB in //
///////////////////// behind of door :D/////////////////////////


///////////////////////// BEGIN ////////////////////////////////
////// competence form in navigation bar => Competence /////////
///////////////////// behind of door :D/////////////////////////

    $("#Competence-form").submit(function(event){
        var thisCompetenceForm = $(this);
        $(".ajaxLogoBoard").show();

        //prevent normal submit when submit button click because check something ...
        event.preventDefault();

        //getting values
        var title = $("#Title-text").val();
        var content = $("#Description-text").val();
        var tagList = $("#Tag-input1").val();
        var developers = $("#Developers-text").val();
        var manager = $("#Manager-text").val();
        var picture = $("#Picture-text").val();
        var sourceCode = $("#Code-text").val();
        var usage = $("#Usage-text").val();
        var check = 0;
        var data ={
            title:title,
            content:content,
            tagList:tagList,
            developers:developers,
            manager:manager,
            picture:picture,
            sourceCode:sourceCode,
            usage:usage
        };

        //send AJAX
        $.ajax({
            url: '/ajax/competenceCheck',
            data: data,
            dataType: 'json',
            success:function(result){
                //if something wrong then :
                if(result.title=='0'){
                    check  =1;
                    $('#Title-text').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('#Title-text').css({
                        "background" : "#FFFFFF"
                    });
                }
                if(result.tagList=='0'){
                    check=1;
                    $('#Tag-input1_tagsinput').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('#Tag-input1_tagsinput').css({
                        "background" : "#FFFFFF"
                    });
                }
                if(result.developers=='0'){
                    check =1 ;
                    $('#Developers-text').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('#Developers-text').css({
                        "background" : "#FFFFFF"
                    });
                }
                if(result.manager=='0'){
                    check =1 ;
                    $('#Manager-text').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('#Manager-text').css({
                        "background" : "#FFFFFF"
                    });
                }
                //TODO:is ajax logo must hide here ? or end of the block ?
                $(".ajaxLogoBoard").hide();

                //if every thing is OK then add to DOM
                if(result.manager=='1' && result.title=='1' && result.tagList=='1' && result.developers=='1'){
                    thisCompetenceForm.unbind('submit');
                    thisCompetenceForm.submit();
//                    showTab("#Board");
//                    var tag = $("#Tag-input1").val().split(',');
//                    var tagSection = '';
//                    var d = new Date();
//                    var month = d.getMonth()+1;
//                    for(var i=0; i<tag.length; i++){
//                        tagSection += '<div class="tag-span">'+tag[i]+'</div>';
//                    }
//                    var Content = $('<span class="project-div">\
//							<div class="project-desc">\
//								<h3>'+ title +'</h3>\
//								<span>'+ content +'</span>\
//								<div class="project-date">Created '   + month+   ' '   + d.getDate()+   ', '   + d.getFullYear() +   ' at '   + d.getHours()+   ':'   + d.getMinutes()+   ':'   + d.getSeconds()+   '</div>\
//								<div class="project-tag">'+tagSection +'</div>\
//							</div>\
//							<div class="project-image">\
//								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
//    								<div class="score-number">0</div></div>\
//								<div class="project-logo" style="background-image: url(../../static/social/images/logos/pylogo.png);"></div>\
//							</div>\
//						</span>');
//
//                    //clear all fileds after submit
//                    $('#Title-text, #Description-text, #Developers-text, #Manager-text, #Picture-text, #Code-text, #Usage-text').val("");
//                    $('.tag').remove();
//
//                    //add content to DOM
//                    Content.clone().hide().delay(1000).insertAfter($('.content').children().first()).fadeIn("slow");
                }
            }
        });
    });

////////////////////////// END /////////////////////////////////
////// competence form in navigation bar => Competence /////////
///////////////////// behind of door :D/////////////////////////


///////////////////////// BEGIN ////////////////////////////////
//// TRACE a user that redirect from search box(currently) /////
////////////////////////////////////////////////////////////////

    //when TRACE button clicked DO:
    $('#anotherUsersTitle').children().first().next().on("click", function(){

        //this button may be needed in later
        var buttonThis = $(this);

        //instead of ajax logo add 3 dot at end of the TRACE button text
        $(this).val("Trace...");

        //get the firstName and lastName from URL and split it to send to server
        var receiver = location.pathname.split("/")[1].split(".");
        var receiverFN = receiver[0];
        var receiverLN = receiver[1];
        var receiverNUM = null;
        if(receiver.length==3){
            receiverNUM = receiver[2];
        }
        var dataSend = {
            userReceiverFirstName: receiverFN,
            userReceiverLastName: receiverLN,
            userReceiverNumber: receiverNUM
        };
        //ajax send
        $.ajax({
            url: '/ajax/trace',
            dataType: 'json',
            data: dataSend,
            success:function(result){
                if(result.isOK==1){
                    //change the text of button to trace + tick and change button to div
                    buttonThis.replaceWith("<div id='isTraced'>Traced &#10004</div>")

                }
            }
        });
    });

////////////////////////// END /////////////////////////////////
//// TRACE a user that redirect from search box(currently) /////
////////////////////////////////////////////////////////////////


///////////////////////// BEGIN ////////////////////////////////
//// when notification box clicked then trace ship and other ///
///////////// requests must be shown to user ///////////////////

    $("#notification-icon").on("click", function(){
        $('#notificationNumber').hide();
        var ajaxLogo = $(".ajaxLogoNotification");
        var notificationBox = $("#notificationBox");
        notificationBox.slideToggle();
        if((notificationBox).is(":visible") && !isContinueAjax){
            ajaxLogo.show();
            $.ajax({
                url:'/ajax/getnot',
                success:function(result){
                    ajaxLogo.hide();
                    for(var i=0; i<result.traceUsers.length; i++){
                        var content='<div class="itemNotification"><img src="../../static/social/images/defaultMaleImage.png" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.traceUsers[i].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.traceUsers[i].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction"> traced you  </p>\
                    <button class="button glass blue trace" >trace</button>\
                    <button class="button glass blue OKT" >OK</button></div>';
                        $("#notificationBox").prepend(content);
                    }
                    for(var j=0; j<result.tracebackUsers.length; j++){
                        content=' <div class="itemNotification"><img src="../../static/social/images/defaultMaleImage.png" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.tracebackUsers[j].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.tracebackUsers[j].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction"> you are now have traceship with this user</p>\
                    <button class="button glass blue OKTB" >OK</button></div>';
                        $("#notificationBox").prepend(content);
                    }
                    for (var x=0;x<result.post.length;x++){
                        content='<div class="itemNotification"><img src="'+result.post[x].hash+'" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.post[x].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.post[x].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction">has replied on your comment</p>\
                    <span style="display:none">Post/'+result.post[x].title +'.'+result.post[x].id+'</span>\
                    <button class="button glass blue Reply" id="see">See More</button>\
                    <span style="display:none">Post:'+result.post[x].this +'</span></div>';

                        $("#notificationBox").append(content);

                    }

                    for (var x=0;x<result.post1.length;x++){
                        content='<div class="itemNotification"><img src="'+result.post1[x].hash+'" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.post1[x].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.post1[x].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction">has commented on your post</p>\
                    <span style="display:none">Post/'+result.post1[x].title +'.'+result.post1[x].id+'</span>\
                    <button class="button glass blue Comment" id="see">See More</button>\
                    <span style="display:none">Post:'+result.post1[x].this+'</span></div>';

                        $("#notificationBox").append(content);

                    }

                    for(var x=0;x<result.competence.length;x++){
                        content='<div class="itemNotification"><img src="'+result.competence[x].hash+'" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.competence[x].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.competence[x].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction"> has replied on your comment</p>\
                    <span style="display:none">Competence/'+result.competence[x].title+'.'+result.competence[x].id+'</span>\
                    <button class="button glass blue Reply" id="see">See More</button>\
                    <span style="display:none">Competence:'+result.competence[x].this+'</span></div>';

                        $("#notificationBox").append(content);

                    }

                    for(var x=0;x<result.competence1.length;x++){
                        content='<div class="itemNotification"><img src="'+result.competence1[x].hash+'" height="50px">\
                    <p class="firstname">\
                        <strong>' + result.competence1[x].firstname +  '</strong>\
                    </p>\
                    <p class="lastname">\
                        <strong>'+  result.competence1[x].lastname + '</strong>\
                    </p>\
                    <br />\
                    <p class="notificationAction"> has commented on your competence</p>\
                    <span style="display:none">Competence/'+result.competence1[x].title+'.'+result.competence1[x].id+'</span>\
                    <button class="button glass blue Comment" id="see">See More</button>\
                    <span style="display:none">Competence:'+result.competence1[x].this+'</span></div>';

                        $("#notificationBox").append(content);

                    }



                    isContinueAjax = true;
                    $('.Reply').on("click",function(){
                        var me = $(this);
                        var page =me.prev().text();
                        var main = me.next().text();
                        var send ={
                            page:page,
                            main:main
                        };
                        $.ajax({
                            data:send,
                            url:'/ajax/reply_not',
                            success:function(result){
                                if(result.isOK=='1'){
                                    var t = main.split(":");
                                    //alert(page+":");
                                    me.parent().fadeOut("fast");
                                    window.location.href = "/"+page + "#myID+"+t[1];
                                    var url = window.location.hash;
                                    url = url.replace("#","");
                                    url1 = url.split("+");
                                    var this1 = $("span:contains('"+url1[1]+"')").parent();
                                    for(i=0;i<3;i++){
                                        this1.fadeTo("slow",0);
                                        this1.fadeTo("slow",1);
                                    }
                                }
                            }

                        });
                    });

                    $('.Comment').on("click",function(){
                        var me = $(this);
                        var page =me.prev().text();
                        var main = me.next().text();
                        var send ={
                            page:page,
                            main:main
                        };
                        $.ajax({
                            data:send,
                            url:'/ajax/comment_not',
                            success:function(result){
                                if(result.isOK=='1'){
                                    var t = main.split(":");
                                    me.parent().fadeOut("fast");
                                    window.location.href = "/"+page + "#myID+"+t[1];
                                    var url = window.location.hash;
                                    url = url.replace("#","");
                                    url1 = url.split("+");
                                    var this1 = $("span:contains('"+url1[1]+"')").parent();
                                    for(i=0;i<3;i++){
                                        this1.fadeTo("slow",0);
                                        this1.fadeTo("slow",1);
                                    }
                                }
                            }

                        });
                    });


                    $('.OKT').on("click", function(){
                        var thisOKButton = $(this);
                        thisOKButton.text('OK...');
                        var data={
                            firstName: $('.firstname').text(),
                            lastName: $('.lastname').text()
                        };
                        $.ajax({
                            data:data,
                            url:'/ajax/notshowagain',
                            success:function(result){
                                if(result.isOK=='1'){
                                    thisOKButton.parent().fadeOut("fast");
                                }
                            }

                        });
                    });

                    $('.OKTB').on("click", function(){
                        var thisOKButton = $(this);
                        thisOKButton.text('OK...');
                        var data={
                            firstName: $('.firstname').text(),
                            lastName: $('.lastname').text()
                        };
                        $.ajax({
                            data:data,
                            url:'/ajax/notshowagaintb',
                            success:function(result){
                                if(result.isOK=='1'){
                                    thisOKButton.parent().fadeOut("fast");
                                }
                            }

                        });
                    });

                    $('.trace').on("click", function(){
                        var thisTraceButton = $(this);
                        thisTraceButton.text('trace...');
                        var data={
                            firstName: $('.firstname').text(),
                            lastName: $('.lastname').text()
                        };
                        $.ajax({
                            data:data,
                            url:'/ajax/traceback',
                            success:function(result){
                                if(result.isOK=='1'){
                                    thisTraceButton.next().fadeOut("fast");
                                    thisTraceButton.replaceWith("<div class='button glass blue accept'>traced &#10004</div>");
                                }
                            }
                        });
                    });
                }
            });
        }
    });

////////////////////////// END /////////////////////////////////
//// when notification box clicked then trace ship and other ///
///////////// requests must be shown to user ///////////////////


///////////////////////// BEGIN ////////////////////////////////
/////////// filter searching with ALL, POST, PROJECT ///////////
////////////////////////////////////////////////////////////////

    $("input[name='view']").change(function(){
        var content = $('.content');
        $('#switchAjax').show("fast");
        content.css({
            "opacity": "0.3"
        }, "fast");
        var state = $("input[name='view']:checked").val();
        var data ={
            user: window.location.pathname
        };
        if(state=="post"){
            $.ajax({
                data:data,
                url:'/ajax/getposts',
                success:function(result){
                    content.children().not('#switchAjax').remove();
                    ajaxer('getPosts', content, result);
                    $('#switchAjax').hide("fast");
                    content.css({
                        "opacity": "1.0"
                    }, "fast");

                }
            });
        }
        else if(state=="project"){
            $.ajax({
                data:data,
                url:'/ajax/getCompetence',
                success:function(result){
                    content.children().not('#switchAjax').remove();
                    ajaxer('getCompetence', content, result);
                    $('#switchAjax').hide("fast");
                    content.css({
                        "opacity": "1.0"
                    }, "fast");
                }
            });
        }
        else{
            $.ajax({
                url: '/ajax/getpac',
                dataType: 'json',
                data: data,
                success:function(result){
                    content.children().not('#switchAjax').remove();
                    ajaxer('getPAC', content, result);
                    $('#switchAjax').hide("fast");
                    content.css({
                        "opacity": "1.0"
                    }, "fast");
                }
            });
        }
    });


////////////////////////// END /////////////////////////////////
/////////// filter searching with ALL, POST, PROJECT ///////////
////////////////////////////////////////////////////////////////
        $("input[name='tops']").change(function(){
            var content = $('.content');
            $('#topSwitchAjax').show("fast");
            content.css({
                "opacity": "0.3"
            }, "fast");
            var state = $("input[name='tops']:checked").val();
            if(state=="users"){
                $.ajax({
                    url:'/ajax/tusers',
                    dataType: 'json',
                    success:function(result){
                        content.children().not('#switchAjax').remove();
                        ajaxer('getTUsers', content, result);
                        $('#switchAjax').hide("fast");
                        content.css({
                            "opacity": "1.0"
                        }, "fast");

                    }
                });
            }else{
                $.ajax({
                    url: '/ajax/tprojects',
                    dataType: 'json',
                    success:function(result){
                        content.children().not('#switchAjax').remove();
                        ajaxer('getTProjects', content, result);
                        $('#switchAjax').hide("fast");
                        content.css({
                            "opacity": "1.0"
                        }, "fast");
                    }
                });
            }

        });
///////////////////////// BEGIN ////////////////////////////////
/////////// filter top Users and Projects with Ajax ////////////
////////////////////////////////////////////////////////////////


});
////////////////////////// END /////////////////////////////////
/////////// filter top Users and Projects with Ajax ////////////
////////////////////////////////////////////////////////////////

////////////////////////// Begin ///////////////////////////////
//// go to trace page and showing the tracers and tracings ////
///////////////////////////////////////////////////////////////

$("#tracer").on("click", function(){
    var dataa ={
        user1: window.location.pathname
    };
    window.location.href = "/traces" ;

    $.ajax({
        url: '/traces',
        dataType: 'json',
        data: dataa,
        success:function(result){
            if(result.isOK==1){
//                    change color of button
            }
        }
    });
});
$("#tracing").on("click", function(){
    var dataa ={
        user1: window.location.pathname
    };
    window.location.href = "/traces" ;
    $.ajax({
        url: '/traces',
        dataType: 'json',
        data:dataa,
        success:function(result){
            if(result.isOK==1){
//                    change color of button
            }
        }
    });
});

////////////////////////// END /////////////////////////////////
//// go to trace page and showing the tracers and tracings ////
////////////////////////////////////////////////////////////////



////////////////////////// Begin ///////////////////////////////
////// Showing Tracer and Tracing number in Psycograph ////////
///////////////////////////////////////////////////////////////

$(window).load(function(){
    var dat = { address : window.location.pathname};
    $.ajax({
        url: '/ajax/traceNum',
        dataType: 'json',
        data:dat,
        success:function(response){
            if(response.isOK==1){
//                    change color of button
            }
            $(".circle").last().text(response['tracing']);
            $(".circle").first().text(response['tracer']);
        }

    });
});

////////////////////////// END ////////////////////////////////
////// Showing Tracer and Tracing number in Psycograph ////////
///////////////////////////////////////////////////////////////

$("#submit_comment").on("click",function(e){
    e.preventDefault();
    var content = $("textarea").val();
    if (content ==""){
        alert("You must type something");
    }
    else {
        if ($("#label").closest("p").text() != ""){
            var owner = $("#label").closest("p").text();}
        else
        {
            var owner = $("#com").closest("p").text();}
        var da = { address : window.location.pathname,
            owner:owner,
            content:content};
        $.ajax({
            url: '/ajax/comment',
            dataType: 'json',
            data:da,
            success:function(result){
                if(result.repeat == 1){
                    alert("You can't comment again :D");
//                    change color of button
                }
                else if(result.isOk==1 && result.null=='0'){
                    var x = "" ;
                    if(result.time.hour>=12){
                        x = "p.m" ;
                        result.time.hour = result.time.hour-12;
                    }
                    else{
                        x = "a.m"
                    }
                    var content1 = $('<li class="comment">\
                    <a href="/" title="View this user profile" class="photo"><img style="width: 35px" src='+result.email+'  ></a>\
                    <div class="meta">'+result.name +' | '+result.time.month+', '+ result.time.day+', '+result.time.year+', '+result.time.hour+':'+result.time.minute+' '+x+'</div>\
                    <div class="body">'+result.mohtava+'</div>\
                    </li>\
                </ul>') ;
                    $('ul.comments').css({
                        "display": "block"
                    }, "slow");
                    content1.clone().hide().appendTo($('ul.comments')).fadeIn("slow");
                    if(result.isMe == 0){
                        var socket = io.connect('localhost', {port: 4000});
                        socket.emit('comment_message', {DBID: result.DBID, title: result.title, PID: result.ID,
                                                                FN: result.FN,
                                                                LN: result.LN,
                                                                isPost: result.isPost});
                    }

                }
                else if (result.null == '1'){
                    alert("You must type something");
                }
            }

        });
        //removeClick('.remove');
    }
});

$(".reply").on("click",function(){
    var id1 = document.getElementById("id");
    var id = id1.innerHTML;
    var but = $(this);
    var comment_id = $(this).parent().next().next().text();
    var b = document.getElementById("email");
    var c = document.getElementById("hash");
    var hash = c.innerHTML;
    var mail = b.innerHTML;
    // alert(c);
    //alert(mail1[0]);
    var cont = $('<div id="holder" style="">\
        <div class="box">\
            <div class="user-pic"><img style="width:70px"src='+ hash+' /></div>\
            <div class="comment-box">\
                <textarea id="reply-comment" placeholder="Write something..."></textarea>\
            </div>\
        </div>\
    </div>');
    cont.clone().hide().insertBefore($('#table')).fadeIn("slow");
    var fader = $('#fader');
    fader.css({
        "height": document.body.scrollHeight
    });
    fader.fadeIn("slow");
    var msg = $('#reply-comment');
    $('#reply-comment').keydown(function(key){
        if(msg.val().length > 0){
            if(key.which == 13){
                var content= msg.val();
                //alert(msg.val());
                $('#holder').detach();
                fader.css({
                    "height":0
                });
                fader.fadeOut("slow");
                but.hide();
                var vars={
                    address : window.location.pathname,
                    id: id,
                    comment_id:comment_id,
                    email:mail,
                    content:content
                };
                $.ajax({
                    url: '/ajax/reply',
                    dataType: 'json',
                    data:vars,
                    success:function(result){
                        if(result.isOk==1){
                            var x = ""
                            if(result.time.hour>=12){
                                x = "p.m"
                                result.time.hour = result.time.hour-12;
                            }
                            else{
                                x = "a.m"
                            }
                            var test=$(' <li class="comment level-'+result.depth+'">\
                    <a href="/'+result.firstName+' .'+result.lastName+'" title="View this user profile" class="photo"><img style="width: 35px" src='+ hash+'  > </a>\
                    <div class="meta" >'+ result.firstName+' '+result.lastName+' | '+result.time.month+', '+ result.time.day+', '+result.time.year+', '+result.time.hour+':'+result.time.minute+' '+x+'</div>\
                    <div class="body">'+ msg.val()+'</div>\
                </li>');
                            test.clone().hide().insertAfter(but.parent().parent()).fadeIn();//                    change color of button
                        }
                        if(result.isOk==0){
                            alert("You have replied once before");
                        }
                    }
                });
                //removeClick(".remove");

            }

        }
    });

});

removeClick(".remove");
//$(".remove").on("click",function(){
//    var comment_id = $(this).parent().next().next().text();
//    var com = $(this).parent().parent();
//
//    var vars={
//       id:comment_id,
//       main:window.location.pathname
//    };
//    $.ajax({
//        url: '/ajax/remove',
//        dataType: 'json',
//        data:vars,
//        success:function(result){
//            if(result.isOK==1){
//                com.fadeOut("slow");
//                var x = result.children;
//                y = result.children.length;
//                for(i=0;i<y;i++){
//                    var me = $('span:contains("'+result.children[i]+'")');
//                    me.parent().fadeOut("slow");
//                }
//            }
//        }
//    });
//});

//Animation is for Webkit Browser Only :)
//To be updated soon...

//Animation is for Webkit Browser Only :)
//To be updated soon...

