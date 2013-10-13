var isLoginFormShown = 0;

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
        var value = $(this).val();
        var isAccepted = 0;
        for(var i=0 ;i<value.length ;i++){
            if((value.charCodeAt(i)>=48 && value.charCodeAt(i)<=57) ||
                (value.charCodeAt(i) >= 65 && value.charCodeAt(i) <= 90)||
                (value.charCodeAt(i) >= 97 && value.charCodeAt(i) <=122)
                ){
                isAccepted =1;
            }
            else{
                isAccepted=0;
                break;
            }
        }
//        Ajax check for DataBase
        if (!isAccepted){
            $(this).css({
                "background":"FFA798" ,
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            });
        }
        else{
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
        }
    });

    $('.RegisterInput[name="password"] ').keyup(function(){
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
        }
        else{
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
        }

    });

    $('.RegisterInput[name="rePass"]').keyup(function(){
        var value = $(this).val();
        var checkValue = $('.RegisterInput[name="password"] ').val();
        var isAccepted = 0;
        if((value.length)>=6 && value==checkValue){
            isAccepted = 1;
        }
        if(!isAccepted){
            $(this).css({
                "background":"FFA798" ,
                "border-color": "FF2808",
                "box-shadow" :"0 0 10px #FF2808"
            });
        }
        else{
            $(this).css({
                "background" : "AFFF8E",
                "border-color": "00FF31",
                "box-shadow" :"0 0 10px #00FF31"
            },"fast")
        }
    });

});