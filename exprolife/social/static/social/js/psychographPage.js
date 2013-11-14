
//*********************** CONSTANTS *****************************
var isContinueAjax=false;

var escapeTags = function(str) {
   return str.replace(/</g, '&lt;').replace(/>/g, '&gt;');
};



$(document).ready(function(){
//  migrated code from script.js
    var items = $('#v-nav>ul>li').each(function () {
        $(this).click(function () {
            //remove previous class and add it to clicked tab
            items.removeClass('current');
            $(this).addClass('current');

            //hide all content divs and show current one
            $('#v-nav>div.tab-content').hide().eq(items.index($(this))).fadeIn('fast');

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
//  end of migration
    $(".alert").animate({
         "right":"50px"
    } , 1500).delay(1000).fadeOut(1000);
//  when click somewhere else input search box must be slideUp();
    $(document).not("#Search-input, #searchResultSection").click(function(){
        $("#searchResultSection").slideUp();
    });

    var currentRequest = null;
    $("#Search-input").keyup(function(){
        $(".itemSearch").remove();
        $(".notfound").hide();
//        $("#searchResultSection").height("20px");

        if(!$("#Search-input").val()){
            $("#searchResultSection").slideUp();
            $(".ajaxLogoSearch").hide();
            $(".notfound").hide();
        }
        else{
            var data = {
                query: $("#Search-input").val()
            };
            $("#searchResultSection").slideDown();
            $(".ajaxLogoSearch").show();
            currentRequest = $.ajax({
                url: '/ajax/search',
                data: data,
                dataType:'json',
                beforeSend : function(){
                    if(currentRequest != null) {
                        currentRequest.abort();
                    }
                },
                success:function(result){
                    $(".itemSearch").remove();
                    if(result.found==0){
                        $(".ajaxLogoSearch").hide();
                        $(".notfound").show();
                    }
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
                    }
                }
            });
        }
    });

    $('.first').on("click", function(){
        $('#Col-1').fadeOut("slow", function(){
            $('#Col-2').animate({
                width:"1100px"
            }, "slow");
            $('.project-div, .post-div').delay(500).fadeIn("slow");
        });
    });
    $('#v-nav').children().first().children().not(".first").on("click", function(){
        $('#Col-2').animate({
                width:"800px"
            }, "slow");
        $('#Col-1').delay(500).fadeIn("slow");
        $('.project-div, .post-div').hide();
    });
    $("#Board-form").submit(function(event){
        $(".ajaxLogoBoard").show();
        event.preventDefault();
        var content = $("#text-area").val();
        var tags = $('.tag').find('span').text();
        var title = $('#title-board').val();
        var data ={
            content:content,
            tagList:tags,
            title:title
        };
        $.ajax({
            url: '/ajax/postboardcheck',
            data: data,
            dataType: 'json',
            success:function(result){
                if(result.title=='0'){
                    $('#title-board').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
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

                $(".ajaxLogoBoard").hide();
                if(result.isOK=='1'){
                    var title = escapeTags($('#title-board').val());
                    var content = escapeTags($('#Board-form').children().first().next().val());
                    var tags = escapeTags($('.tag').text());
                    var tagList = tags.split(String.fromCharCode(160)+String.fromCharCode(160));
                    tagList.splice(-1);
                    var tagSection = '';
                    for(var i=0; i<tagList.length; i++){
                        tagSection += '<div class="tag-span">'+tagList[i]+'</div>';
                    }
                    var mainContent = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+ title +'</h3>\
								<span>'+ content +'</span>\
								<div class="project-date">Created '   +result.month+   ' '   +result.day+   ', '   +result.year +   ' at '   +result.hour+   ':'   +result.minute+   ':'   +result.second+   '</div>\
								<div class="project-tag">'+tagSection +'</div>\
							</div>\
							<div class="project-image">\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/post.jpg);"></div>\
							</div>\
						</span>');
					document.getElementById("title-board").value="";
                    document.getElementById("text-area").value="";
                    $('.tag').remove();
                    mainContent.clone().hide().insertAfter($('#Board-div').children().first()).fadeIn("slow");
                }
            }
        });
    });
    var getInfoAjax = $('#getInfoAjax');
    getInfoAjax.show();
    var data ={
        user: window.location.pathname
    };
    $.ajax({
        url: '/ajax/getposts',
        dataType: 'json',
        data:data,
        success:function(result){
            for(var i=0; i<result.ownPosts.content.length; i++){
                var title = escapeTags(result.ownPosts.title[i]);
                var content = escapeTags(result.ownPosts.content[i]);
                var tagList = result.ownPosts.tagList[i];
                var tagSection = '';
                for(var j=0; j<tagList.length; j++){
                    tagSection += '<div class="tag-span">'+ tagList[j]+'</div>';
                }
                var currentDiv = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+ title +'</h3>\
								<h4>'+ content +'</h4>\
								<div class="project-date">Created '   +result.ownPosts.month[i]+   ' '   +result.ownPosts.day[i]+   ', '   +result.ownPosts.year[i] +   ' at '   +result.ownPosts.hour[i]+   ':'   +result.ownPosts.minute[i]+   ':'   +result.ownPosts.second[i]+   '</div>\
								<div class="project-tag">'+tagSection +'</div>\
							</div>\
							<div class="project-image">\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/post.jpg);"></div>\
							</div>\
						</span>')
                $('#Board-div').children().last().after(currentDiv);

            }
        }
    });
    getInfoAjax.hide("slow");


	var dataSend ={
        user: window.location.pathname
    };
    $.ajax({
        url: '/ajax/getCompetence',
        dataType: 'json',
        data: dataSend,
        success:function(result){
            for(var i=0; i<result.ownCompetences.title.length; i++){
                var title = result.ownCompetences.title[i];
                var description = result.ownCompetences.description[i];
                var tags = result.ownCompetences.tags[i];
                var developers = result.ownCompetences.developers[i];
                var manager = result.ownCompetences.manager[i];
//              var Date = result.ownCompetences.Date[i];
                var usage = result.ownCompetences.usage[i];
                var tagSection = '';
                for(var j=0; j<tags.length; j++){
                    tagSection += '<div class="tag-span">'+ tags[j]+'</div>';
                }
                var currentDiv = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+ title +'</h3>\
								<span>'+ description +'</span>\
								<div class="project-date">Created '   +result.ownCompetences.month[i]+   ' '   +result.ownCompetences.day[i]+   ', '   +result.ownCompetences.year[i] +   ' at '   +result.ownCompetences.hour[i]+   ':'   +result.ownCompetences.minute[i]+   ':'   +result.ownCompetences.second[i]+   '</div>\
								<div class="project-tag">'+tagSection +'</div>\
							</div>\
							<div class="project-image">\
								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
								<div class="score-number">0</div></div>\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/pylogo.png);"></div>\
							</div>\
							<span><center>'+ usage +'</center></span>\
						</span>')
                $('#Board-div').children().last().after(currentDiv);

            }
        }
    });


    $("#Competence-form").submit(function(event){
        var thisRegisterForm = $(this);
        $(".ajaxLogoBoard").show();
        event.preventDefault();
        var title = $("#Title-text").val();
        var description = $("#Description-text").val();
        var tags = $("#Tag-input1").val();
        var developers = $("#Developers-text").val();
        var manager = $("#Manager-text").val();
        var picture = $("#Picture-text").val();
        var sourceCode = $("#Code-text").val();
        var usage = $("#Usage-text").val();
        var check = 0;
        var data ={
            title:title,
            description:description,
            tags:tags,
            developers:developers,
            manager:manager,
            picture:picture,
            sourceCode:sourceCode,
            usage:usage
        };
        $.ajax({
            url: '/ajax/competenceCheck',
            data: data,
            dataType: 'json',
            success:function(result){
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
                if(result.tags=='0'){
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

                $(".ajaxLogoBoard").hide();
                if(result.manager=='1' && result.title=='1' && result.tags=='1' && result.developers=='1'){
                    showTab("#Board");
                    var tag = $("#Tag-input1").val().split(',');
                    var tagSection = '';
                    var d = new Date();
                    var month = d.getMonth()+1;
                    for(var i=0; i<tag.length; i++){
                        tagSection += '<div class="tag-span">'+tag[i]+'</div>';
                    }
                    var Content = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+ title +'</h3>\
								<span>'+ description +'</span>\
								<div class="project-tag">'+tagSection +'</div>\
								<div class="project-date">Created '   + month+   ' '   + d.getDate()+   ', '   + d.getFullYear() +   ' at '   + d.getHours()+   ':'   + d.getMinutes()+   ':'   + d.getSeconds()+   '</div>\
							</div>\
							<div class="project-image">\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/pylogo.png);"></div>\
							</div>\
						</span>');
					document.getElementById("Title-text").value="";
                    document.getElementById("Description-text").value="";
                    $('.tag').remove();
                    document.getElementById("Developers-text").value="";
                    document.getElementById("Manager-text").value="";
                    document.getElementById("Picture-text").value="";
                    document.getElementById("Code-text").value="";
                    document.getElementById("Usage-text").value="";
                    Content.clone().insertAfter($('#Board-div').children().first()).fadeIn("slow");
                }
            }
        });
    });

    $('#anotherUsersTitle').children().first().next().on("click", function(){
        buttonThis = $(this);
        $(this).val("Trace...");
        var receiver = location.pathname.split("/")[1].split(".");
        var receiverFN = receiver[0];
        var receiverLN = receiver[1];
        var receiverNUM = null;
        if(receiver.length==3){
            receiverNUM = receiver[2];
        }
        dataSend = {
            userReceiverFirstName: receiverFN,
            userReceiverLastName: receiverLN,
            userReceiverNumber: receiverNUM
        };
        $.ajax({
            url: '/ajax/trace',
            dataType: 'json',
            data: dataSend,
            success:function(result){
                if(result.isOK==1){
                    buttonThis.replaceWith("<div id='isTraced'>Traced &#10004</div>")
//                    change color of button
                }
            }
        });
    });


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
                        content='<div class="itemNotification"><img src="../../static/social/images/defaultMaleImage.png" height="50px">\
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
                    isContinueAjax = true;
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
                                    thisTraceButton.replaceWith("<div class='glass'>Traced</div>");
                                    $('.OK').fadeOut("fast");
                                }
                            }

                        });
                    });

                }
            });
        }
    });

});
