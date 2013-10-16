

$(document).ready(function(){
    var currentRequest = null;
    $("#Search-input").keyup(function(){
        $(".itemSearch").remove();
        $(".notfound").hide();
        $("#searchResultSection").height("70px");

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

//                                searchResult.height("+=70px");
                            }
                            $("#innerSearch").append(content);
                        }
                        $(".itemSearch").hover(function(){
                            $(this).css({"background":"rgb(55, 108, 221)"});
                        },function(){
                            $(this).css({"background":"#658be6"});
                        });
                    }
                }
            });
        }
    });
});