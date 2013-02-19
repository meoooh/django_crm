function init(){
	$("table#equipmentList .equipmentAdd").click(function(){
		getEquipmentAddForm.call(this);
	});
	
	$("div.addCustomerNotes form").submit(function(){
		saveCustomerNote.call(this);
		return false;
	});
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
	
		var li=document.createElement("li");
		li.className="customerDetailViewList";
		
		var time=document.createElement("span");
		time.innerText=result['date'];
		time.className="time";
		var contents=document.createElement("span");
		contents.innerText=result['contents'];
		contents.className="contents";
		var name=document.createElement("span");
		name.innerText="["+result['name']+"]";
		name.className="name";
		
		li.appendChild(time);
		li.appendChild(contents);
		li.appendChild(name);
		
		isoFormat2localeString($(li));
		
		_form.parent().parent().find('ul.customerDetailViewList').append(li);
	});
}

$(document).ready(init);