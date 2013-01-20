$(document).ready(function(){
	$("input#id_target_user").autocomplete(
		'/user/search/',
		{multiple: true, multipleSeparator: ','}
	);
});