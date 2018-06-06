$(document).ready(() => {
	$('.dropdown-item').click((e) => {
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
		art_name = $(this).parents('.card-body').children('.card-title').text();
		art_id = await () => {
			$.ajax({
				method: 'POST',
				url: '/get_art/' + art_name,
				succsess: (response) => {
					console.log(response);
				}
			}).response;
		}
		$.ajax({
			method: 'POST',
			url: '/add_to_playlist/' + playlist_id + '/' + art_id
		});
	});
});
