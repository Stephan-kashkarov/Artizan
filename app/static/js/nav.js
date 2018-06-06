$( document ).ready( function() {
	$('#nav-search').click(() => {
		e.preventDefault();
		$.ajax({
			url: '/search',
			data: $('.search-input')[0].value,
			type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});
