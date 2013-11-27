/**
 * Created with PyCharm.
 * User: Farshad1428
 * Date: 11/23/13
 * Time: 12:30 AM
 * To change this template use File | Settings | File Templates.
 */

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

    $("#tracer").on("click", function(){
        window.location.href = "/traces" ;
    });
    $("#tracing").on("click", function(){
        window.location.href = "/traces" ;
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

