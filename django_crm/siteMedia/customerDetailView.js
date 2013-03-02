function init(){
	$("table#equipmentList .equipmentAdd").click(function(){
		getEquipmentAddForm.call(this);
	});
	
	$("div.addCustomerNotes form").submit(function(){
		saveCustomerNote.call(this);
		return false;
	});
	
	$("li.customerDetailViewList button.delete").click(function(){
		deleteCustomerNote.call(this);
	});
	
	$("li.customerDetailViewList button.modify").click(function(){
		ModifyCustomerNote.call(this);
	});
	
	$("textarea").autosize({className:"mirroredText"}); // textarea 늘어나는거...
	
	$("textarea").keydown(function(e) { // textarea에서 엔터치면 submit되도록...
		if(e.keyCode == 13) {
			$(this).parent().submit();
		}
	});
	
	$("div.addCustomerIPaddrs form").submit(function(){
		saveCustomerIPaddrs.call(this);
		return false;
	});
}

function saveCustomerIPaddrs(){
	var _form = $(this);
	var _div = _form.parent().parent()
	
	$.post(customerIPaddrURL+"?ajax", _form.serialize(), function(result){
		if(result != "0"){
			$.each(result, function(){
				_div.find("ul.customerDetailViewList").append('<li class="customerDetailViewList" id="'+this.pk+'"><span class="ipaddr">'+this.addr+'</span> - <span class="note">'+_form.find("input[name=note]").val()+'</span></li>');
			});
			_form[0].reset();
		}
		else{
			$('#myModal').modal('show');
			$('#myModal').on('hide', function(){
				_form.find("input[name=ip]").focus();
			});
		}
	});
}

function ModifyCustomerNote(){
	var _button = this;
	var _li = $(_button).parent().parent();
	var _div = _li.parent().parent().parent();
	
	_div.find("form.form-inline").children().each(function(){
		$(this).attr("disabled", true)
	});
	
	$.get(customerNoteURL+_li.attr("id")+"/?ajax", function(result){
		var backup_li = _li.html();
		_li.html('<form method="post" style="margin-bottom: 0" action="/" class="form-inline"><textarea name="contents" placeholder="내용" style="width:714px; height:35px;">'+result['contents']+'</textarea><button class="btn btn-mini" type="submit">완료</button></form>');
		
		_li.find("form").submit(backup_li, function(){
			saveModifyCustomerNote.call(this, backup_li);
			return false;
		});
		
		_li.find("textarea").autosize({className:"mirroredText"}); // textarea 늘어나는거...
	
		_li.find("textarea").keydown(function(e){ // textarea에서 엔터치면 submit되도록...
			if(e.keyCode == 13){
				$(this).parent().submit();
			}
		});
	});
}

function saveModifyCustomerNote(li){
			var _form = $(this);
			var contents = _form.children().first().val()
			$.ajax({
				url: customerNoteURL+_form.parent().attr("id")+"/?ajax",
				type: "PUT",
				data: _form.serialize(),
				success: function(result){
					if(result == "1"){
						var _li=_form.parent().html(li).find("strong").html(contents).parent();
						
						_li.parent().find('button.delete').click(function(){
							deleteCustomerNote.call(this);
						});
						
						_li.parent().find("button.modify").click(function(){
							ModifyCustomerNote.call(this);
						});
						
						_li.parent().parent().parent().parent().find(".addCustomerNotes form").children().each(function(){
							$(this).attr("disabled", false)
						});
					}
					else{
						alert("실패");
					}
				}
			});
}

function deleteCustomerNote(){
	var _button=this;
	var li=$(_button).parent().parent(); // li
	
	if(confirm('삭제하시겠습니까?')){
		$.ajax({
			url: customerNoteURL+li.attr("id")+"/?ajax",
			type: "DELETE",
			success: function(result){
				if(result == "1"){
					li.remove();
				}
				else{
					alert("실패");
				}
			}
		});
	}
}

function getEquipmentAddForm(){
	var _button=this;
	var equipmentListTable = $(_button).parent();
}

function saveCustomerNote(){
	var _form=$(this);
	
	$.post(customerNoteURL+"?ajax", _form.serialize(), function(result){
		_form.each(function(){
			this.reset();
		});
		_form.children()[0].style.height="35px";
		
		var _li = $('<li class="customerDetailViewList" id='+result['id']+'></li>').append('<span class="time">'+result['date']+'</span>').append('<span class="contents"><strong>'+result['contents']+'</strong></span>').append('<span class="name">['+result['name']+']</span>').append('<span class="button"><button class="btn btn-mini modify" type="button">수정</button><button class="btn btn-mini delete" type="button">삭제</button></span>');
		
		isoFormat2localeString(_li);
		
		_form.parent().parent().find('ul.customerDetailViewList').append(_li);
		
		_li.find('button.delete').click(function(){
			deleteCustomerNote.call(this);
		});
		
		_li.find("button.modify").click(function(){
			ModifyCustomerNote.call(this);
		});
	});
}

$(document).ready(init);