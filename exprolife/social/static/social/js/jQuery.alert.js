/*function sex()
{
    confirm("yeah");
}*/

(function ($)
{

    $.alerts = {
        confirm : function(){
            $(".popup").css({"display":"block"});
        },
        cancelIt: function(){
            $(".popup").css({"display":"none"})
        },
        closeIt: function(){
            $(".popup2").css({"display":"none"});
        }
    }
    checkForContinue = function() {
		$.alerts.confirm();
	}
    loadPage = function(){
        $.alerts.nextPage();
    }
    cancelOp = function(){
        $.alerts.cancelIt();
    }
    closeOp = function(){
        $.alerts.closeIt();
    }

})(jQuery);