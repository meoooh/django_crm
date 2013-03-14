function isoFormat2localeString(obj){
		if(!obj){
			$("span.time").each(function(){
				change.call(this);
			});
		}
		else{
			obj.find("span.time").each(function(){
				change.call(this);
			});
		}
}

function change(){
	if(!$(this).attr('title')){
		$(this).attr('title', $(this).html());
		$(this).html("("+new Date($(this).html()).toLocaleString()+")");
	}
}

function init(){
	isoFormat2localeString();
}

$(document).ready(init);