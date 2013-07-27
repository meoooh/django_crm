var conn = null;

if(conn===null){
    conn = new SockJS('http://meoooh.iptime.org:7070/chat');
}
else{
    conn.close();
    conn = new SockJS('http://meoooh.iptime.org:7070/chat');
}

function noti(obj, pk){ // ['noti', ['msg', {'roomId': roomId}]]
    var text = [];
    text.push("noti");
    text.push([]);
    text[1].push(obj);
    text[1].push({});
    text[1][1].roomId = pk;

    conn.send( JSON.stringify(text) );
}

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