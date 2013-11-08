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




    var currentRequest = null;
    $("#Search-input").keyup(function(){
        $(".itemSearch").remove();
        $(".notfound").hide();
//        $("#searchResultSection").height("70px");

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
                            $(this).css({"background":"rgb(55, 108, 221)"});
                        },function(){
                            $(this).css({"background":"#658be6"});
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
        var thisRegisterForm = $(this);
        $(".ajaxLogoBoard").show();
        event.preventDefault();
        var content = $("textarea.psychograph-input").val();
        var tags = $('.tag').find('span').text();
        var title = $('#title-board').val();
        var data ={
            content:content,
            tagList:tags,
            title:title
        };
        $.ajax({
            url: 'ajax/postboardcheck',
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
                    $('textarea.psychograph-input').css({
                        "background" : "rgba(255, 82, 82, 0.5)"
                    });
                }
                else{
                    $('textarea.psychograph-input').css({
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
                    var content = $('#Board-form').children().first().val();
                    var tags = $('.tag').text();
                    var tagList = tags.split(String.fromCharCode(160)+String.fromCharCode(160))
                    tagList.splice(-1);
                    var tagSection = '';

                    for(var i=0; i<tagList.length; i++){
                        tagSection += '<div class="tag-span">'+tagList[i]+'</div>';
                    }
                    var mainContent = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+$('#title-board').val() +'</h3>\
								<span>'+ content +'</span>\
								<div class="project-date">Created Mar 22, 2012 at 8:45 am</div>\
								<div class="project-tag">'+tagSection +'</div>\
							</div>\
							<div class="project-image">\
								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
								<div class="score-number">0</div></div>\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/Java_Logo.png);"></div>\
							</div>\
						</span>');
                    mainContent.clone().hide().insertAfter($('#Board-div').children().first()).fadeIn("slow");
                }
            }
        });
    });
    var getInfoAjax = $('#getInfoAjax');
    getInfoAjax.show();
    alert(123);
    $.ajax({
        url: 'ajax/getposts',
        dataType: 'json',
        success:function(result){

            for(var i=0; i<result.ownPosts.content.length; i++){
                var title = result.ownPosts.title[i];
                var content = result.ownPosts.content[i];
                var tagList = result.ownPosts.tagList[i];
                var tagSection = '';
                for(var j=0; j<tagList.length; j++){
                    tagSection += '<div class="tag-span">'+ tagList[j]+'</div>';
                }
                var currentDiv = $('<span class="project-div">\
							<div class="project-desc">\
								<h3>'+ title +'</h3>\
								<span>'+ content +'</span>\
								<div class="project-date">Created Mar 22, 2012 at 8:45 am</div>\
								<div class="project-tag">'+tagSection +'</div>\
							</div>\
							<div class="project-image">\
								<div class="project-score" style="background-image: url(../../static/social/images/logos/green_sea.png);">\
								<div class="score-number">0</div></div>\
								<div class="project-logo" style="background-image: url(../../static/social/images/logos/Java_Logo.png);"></div>\
							</div>\
						</span>')
                $('#Board-div').children().last().after(currentDiv);

            }
        }
    });
    getInfoAjax.hide("slow");
});
