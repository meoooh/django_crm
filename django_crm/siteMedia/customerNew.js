$(document).ready(function(){
	$("input#id_workers").typeahead({
        source: function(query, process){
            return $.getJSON(
                userSearch,
                {
                    query: query,
                    kind: 'UserProfile',
                    what: 'name'
                },
                function(result){
                    return process(result);
                }
            );
        },
    });

    $("input#id_salespersons").typeahead({
        source: function(query, process){
            return $.getJSON(
                userSearch,
                {
                    query: query,
                    kind: 'UserProfile',
                    what: 'name'
                },
                function(result){
                    return process(result);
                }
            );
        },
    });
});