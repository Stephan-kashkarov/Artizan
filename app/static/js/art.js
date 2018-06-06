$(document).ready(function($) {
	$('.dropdown-item').click(function(e){
		e.preventDefault();
		console.log($(this).text());
		playlist_id = await () => {
			$.ajax({
				method: 'POST',
				url: '/get_playlist/' + $(this).text(),
				succsess: (response) => {
					console.log(response);
				}
			}).response;
		}

		$.ajax({
			method: 'POST',
			url: '/add_to_playlist'
		})
	});
});
