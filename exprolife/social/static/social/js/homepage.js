var isLoginFormShown = 0;
var isFNA = 0;
var isLNA = 0;
var isEMA = 0;
var isPAC = 0;
var isRPA = 0;
var isSXA = 0;
//regex of email address :(source: Q&A in => stackoverflow.com/questions/46155/validate-email-address-in-javascript)
function validateEmail(email) {
    var re = /^[a-zA-Z0-9\-_]+(\.[a-zA-Z0-9\-_]+)*@[a-z0-9]+(\-[a-z0-9]+)*(\.[a-z0-9]+(\-[a-z0-9]+)*)*\.[a-z]{2,}$/;
    return re.test(email);
}

$(document).ready(function(){
    $("#login").on("click" ,function(){
        if(!isLoginFormShown){
            $(this).find("h1").animate({
                "marginTop" : "-40px"
            } ,"fast");
            $("#loginClose").show();
        }
    });
    $("#loginClose").on("click" ,function(){
        $(this).next().find("h1").animate({
            "marginTop" : "20px"
        } ,"fast");
        $("#loginClose").hide();
    });

    $("#register").on("click" ,function(){
        $("#fadeLayer").show();
        $("#registerForm").show();
    });

    $("#registerCloseIcon").on("click" ,function(){
        $("#fadeLayer").hide();
        $("#registerForm").hide();

    });

    $('.RegisterInput').focusin(function(){
        $(this).next().animate({
            "opacity" : 1 ,
            "marginLeft" : "20px"
        }, "fast");
        $(this).next().next().animate({
            "opacity" : 1
        } ,"fast");
    })
    .focusout(function(){
        $(this).next().animate({
            "opacity" : 0 ,
            "marginLeft":"-30px"
        }, "fast");
        $(this).next().next().animate({
            "opacity" : 0
        } ,"fast");
    });

    $('.RegisterInput[name="firstname"] , .RegisterInput[name="lastname"]').keyup(function(){
        var correct = $(this).siblings(":last").prev();
        var notCorrect = $(this).siblings(":last");
        var value = $(this).val();
        var isAccepted = 0;
        for(var i=0 ;i<value.length ;i++){
            if((value.charCodeAt(i) >= 48 && value.charCodeAt(i) <= 57) ||
                (value.charCodeAt(i) >= 65 && value.charCodeAt(i) <= 90)||
                (value.charCodeAt(i) >= 97 && value.charCodeAt(i) <= 122)
                ){
                isAccepted =1;
            }
            else{
                isAccepted=0;
                break;
            }
        }
        if (!isAccepted){
            $(this).css({
                "background":"FFA798" ,
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            });
            correct.hide();
            notCorrect.show();
        }
        else{
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
            notCorrect.hide();
            correct.show();
        }
    });

    $('.RegisterInput[name="password"] ').keyup(function(){
        var correct = $(this).siblings(":last").prev();
        var notCorrect = $(this).siblings(":last");
        var value = $(this).val();
        var isAccepted = 0;
        if((value.length)>=6){
            isAccepted = 1;
        }
        if(!isAccepted){
            $(this).css({
                "background":"FFA798" ,
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            });
            correct.hide();
            notCorrect.show();
        }
        else{
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
            notCorrect.hide();
            correct.show();
        }

    });

    $('.RegisterInput[name="rePass"]').keyup(function(){
        var correct = $(this).siblings(":last").prev();
        var notCorrect = $(this).siblings(":last");
        var value = $(this).val();
        var checkValue = $('.RegisterInput[name="password"] ').val();
        var isAccepted = 0;
        if((value.length)>=6 && value==checkValue){
            isAccepted = 1;
        }
        if(!isAccepted){
            $(this).css({
                "background":"FFA798" , //red failed
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            });
            correct.hide();
            notCorrect.show();
        }
        else{
            $(this).css({
                "background" : "AFFF8E", //green accepted
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
            notCorrect.hide();
            correct.show();
        }
    });

    $('.RegisterInput[name="email"]').keyup(function(){
        var correct = $(this).siblings(":last").prev();
        var notCorrect = $(this).siblings(":last");
        var thisInput = $(this);
        var value = $(this).val();
        if(!validateEmail(value)){
            $(this).css({
                "background":"FFA798" ,
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            }, "fast")
            correct.hide();
            notCorrect.show();
        }
        else{
            var data = {
                query: value
            };
            $(".ajaxEmailCheck").show();
            $.ajax({
                url: '/ajax/emailCheck',
                data: data,
                dataType:'json',
                success:function(result){

                    if (result.found==1){//email currently in DB and input field must be red
                        $(thisInput).css({
                            "background":"FFA798" ,
                            "border-color": "FF2808",
                            "box-shadow" :"0 0 10px #FF2808"
                        }, "fast")
                        $(thisInput).next().css({
                            "border-right" : "10px solid #FFA798"

                        }, "fast");
                        $(thisInput).next().next().css({
                            "background" : "FFA798"
                        } ,"fast").text("email already taken");
                        $(".ajaxEmailCheck").hide();
                        correct.hide();
                        notCorrect.show();
                    }
                    else{
                        $(thisInput).css({
                            "background" : "AFFF8E", //green accepted
                            "border-color": "00FF31",
                            "box-shadow" :"0 0 10px #00FF31"
                        },"fast")

                        $(thisInput).next().css({
                            "border-right" : "10px solid #c9cbcd"

                        }, "fast");

                        $(thisInput).next().next().css({
                            "background" : "c9cbcd"
                        } ,"fast").text("Enter valid Email address");
                        $(".ajaxEmailCheck").hide();
                        notCorrect.hide();
                        correct.show();



                    }

                }
            });
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
        }
    });
});