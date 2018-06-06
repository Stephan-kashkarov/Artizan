$( document ).ready( function() {
	key = prompt('Server key');
	$('.btn-search').click((e) => {
		e.preventDefault();
		$.ajax({
			url: '/searchpst',
			data: JSON.stringify({
				key: key,
				term: $('.search-input')[0].value
			}),
			type: 'POST',
			processData: false,
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
	});
});
