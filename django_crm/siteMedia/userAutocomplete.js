$(document).ready(function(){
	$("input#id_target_user").autocomplete(
		userSearch,
		{multiple: true, multipleSeparator: ','}
	);
});