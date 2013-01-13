function checkValid(){
	var userInput = $(this).value;

	$.get('/userRegistration/?userInput='+userInput, function(result){
				var item = $(this).parent();
				if(result.indexOf("이미 등록된 아이디")){
					item.append($("<div>가입 불가 - 이미 등록된 아이디</div>"));
				}
				else if(result.indexOf("
			});
}

$(document).ready(function(){
			$('input').keyup(checkValid);
		});
