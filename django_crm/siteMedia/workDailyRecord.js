function connect_submit(pk){
	var item = $(this).parent();
	item.find("#save-form").submit(function(){
		submit_form.call(this, pk);
		return false;
	});
}

function connect_button(){
	$("button#workDailyRecord-edit").click(get_form);
	$("button#workDailyRecord-del").click(del);
	$("button#workDailyRecord-check").toggle(function(){
		myToggle.call(this);
	},
	function(){
		myToggle.call(this);
	});
	$("form#save-form").submit(function(){
		add.call(this);
		return false;
	});
}

function myToggle(){
	var item = this;
	var pk = item.name;
	
	var className = 'btn btn-mini btn-success';
	var status = 'uncheck';
	
	if(item.className == className){
		className = 'btn btn-mini';
		status = 'check';
	}
	
	$.post("/workDailyRecord/?ajax&"+status, {pk:pk}, function(result){
			if(result == '1'){
				item.className=className;
			}
			else{
				alert('error');
			}
		});
}

function get_form(){
	var item = $(this).parent();
	var pk = $(this)[0].name;
	item.load("/workDailyRecord/edit/?pk="+pk, null, function(){
		connect_submit.call(this, pk);
		
		item.find("#id_target_user").autocomplete(
		'/user/search/',
		{multiple: true, multipleSeparator: ','}
		);
		
		item.find("#id_contents").focus()
	});
}

function add(){
	var t = $(this)
	var item = t.parent(); //div
	
	$.post("/workDailyRecord/?ajax", t.serialize(), function(result){
			item.find("tbody").append($("tr", result).get(0));
			t.each(function(){
				this.reset();
			});
			
			item.find("td").last().find("#workDailyRecord-edit").click(get_form);
			item.find("td").last().find("#workDailyRecord-del").click(del);
			
			item.find("td").last().find("#workDailyRecord-check").toggle(function(){
				myToggle.call(this);
			},
			function(){
				myToggle.call(this);
			});
		});
}

function del(){
	if(confirm('삭제하시겠습니까?')){
		var item = $(this).parent().parent();
		var pk = $(this)[0].name;
		
		var data = {
			pk: pk,
		};
		
		$.post("/workDailyRecord/del/?ajax", data, function(result){
			if(result == '1'){
				item.remove();
			}
		});
	}
}

function submit_form(pk){
	var item = $(this).parent();
	var data = {
		pk: pk,
		contents: item.find("#id_contents").val(),
		ongoing_or_end: item.find("#id_ongoing_or_end").val(),
	};
	
	$.post("/workDailyRecord/?ajax&edit", $(this).serialize()+'&pk='+pk, function(result){
			item.before($("td", result).get(0));
			
			item.parent().children().first().find("#workDailyRecord-edit").click(get_form);
			item.parent().children().first().find("#workDailyRecord-del").click(del);
			
			item.parent().children().first().find("#workDailyRecord-check").toggle(function(){
				myToggle.call(this);
			},
			function(){
				myToggle.call(this);
			});
			
			item.remove();
		});
}

$(document).ready(connect_button);