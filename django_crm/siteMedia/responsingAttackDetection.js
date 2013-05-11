$(document).ready(function(){
	$("p>input#id_customer").typeahead({
		source: function(query, process){
			return $.getJSON(
				userSearch,
				{
					query: query,
					kind: 'customer',
					what: 'name'
				},
				function(result){
					return process(result);
				}
			);
		},
	});
});