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
	
	$.post(this.baseURI+"notes/?ajax", _form.serialize(), function(result){
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
	});
}

$(document).ready(init);