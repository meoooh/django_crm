function connect_submit(pk){
	var item = $(this).parent();
	item.find("#save-form").submit(function(){
		submit_form.call(this, pk);
		return false;
	});
}

function init(){
	$("button#workDailyRecord-edit").click(get_form);
	$("button#workDailyRecord-del").click(del);
	
	$("button#workDailyRecord-check").toggle(function(){
		check.call(this);
	},
	function(){
		check.call(this);
	});
	
	$("form#save-form").submit(function(){
		add.call(this);
		return false;
	});
	
	$("button#workDailyRecord-end").toggle(function(){
		end.call(this);
	},
	function(){
		end.call(this);
	});
        
	$("textarea").autosize({className:"mirroredText"});
	
	$("textarea").keydown(function(e) { // textarea에서 엔터치면 submit되도록...
		if(e.keyCode == 13) {
			$(this).parent().submit();
		}
	});
}

function end(){
	var item = this;
	var pk = item.name;
	
	var className = 'btn btn-mini btn-inverse';
	var status = 'ongoing';
	
	if(item.className == className){
		className = 'btn btn-mini';
		status = 'end';
	}
	
	$.post(workDailyRecord+"?ajax&"+status, {pk:pk}, function(result){
		item.className=className;
		
		var td = $(item).parent();
		var tr = td.parent();
		
		td.remove();
		
		tr.append($("td", result).get(0));
			
		tr.find("#workDailyRecord-edit").click(get_form);
		tr.find("#workDailyRecord-del").click(del);
		
		if(status == 'end'){
			tr.find("#workDailyRecord-end").toggle(function(){
				end.call(this);
			},
			function(){
				end.call(this);
			});
			
			td.find("#workDailyRecord-check").remove();
		}
		else if(status == 'ongoing'){
			tr.find("#workDailyRecord-check").toggle(function(){
				check.call(this);
			},
			function(){
				check.call(this);
			});
			
			tr.find("#workDailyRecord-end").toggle(function(){
				end.call(this);
			},
			function(){
				end.call(this);
			});
		}
		
		isoFormat2localeString(tr);
	});
}

function check(){
	var item = this;
	var pk = item.name;
	
	var className = 'btn btn-mini btn-success';
	var status = 'uncheck';
	
	if(item.className == className){
		className = 'btn btn-mini';
		status = 'check';
	}
	
	$.post(workDailyRecord+"?ajax&"+status, {pk:pk}, function(result){
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
	item.load(workDailyRecord+"edit/?pk="+pk, null, function(){
		connect_submit.call(this, pk);
		
		item.find("#id_target_user").autocomplete(
			'/user/search/',
			{multiple: true, multipleSeparator: ','}
		);
		
		item.find('textarea').autosize({className:'mirroredText'});
		
		item.find("#id_contents").focus()
	});
}

function add(){
	var t = $(this)
	var item = t.parent(); //div
	
	$.post(workDailyRecord+"?ajax", t.serialize(), function(result){
			item.find("tbody").append($("tr", result).get(0));
			t.each(function(){
				this.reset();
			});
			
			t.children()[0].style.height="35px";
			
			var td = item.find("td").last();
			
			td.find("#workDailyRecord-edit").click(get_form);
			td.find("#workDailyRecord-del").click(del);
			
			td.find("#workDailyRecord-check").toggle(function(){
				check.call(this);
			},
			function(){
				check.call(this);
			});
			
			td.find("#workDailyRecord-end").toggle(function(){
				end.call(this);
			},
			function(){
				end.call(this);
			});
			
			isoFormat2localeString(td);
		});
}

function del(){
	if(confirm('삭제하시겠습니까?')){
		var item = $(this).parent().parent();
		var pk = $(this)[0].name;
		
		var data = {
			pk: pk,
		};
		
		$.post(workDailyRecord+"del/?ajax", data, function(result){
			if(result == '1'){
				item.remove();
			}
		});
	}
}

function submit_form(pk){
	var item = $(this).parent();
	
	$.post(workDailyRecord+"?ajax&edit", $(this).serialize()+'&pk='+pk, function(result){
			item.before($("td", result).get(0));
			
			item.parent().children().first().find("#workDailyRecord-edit").click(get_form);
			item.parent().children().first().find("#workDailyRecord-del").click(del);
			
			item.parent().children().first().find("#workDailyRecord-check").toggle(function(){
				check.call(this);
			},
			function(){
				check.call(this);
			});
			
			item.parent().children().first().find("#workDailyRecord-end").toggle(function(){
				end.call(this);
			},
			function(){
				end.call(this);
			});
			
			item.remove();
		});
}

$(document).ready(init);