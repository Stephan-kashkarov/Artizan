$(document).ready(() => {
	$('.dropdown-menu a').click(function(e){
		if ($(this).text() != '+ New Playlist'){
			e.preventDefault();
			url = window.location.href.split('/');
			art_id = url[url.length - 1];
			playlist_id = $.ajax({
				async: false,
				method: 'POST',
				url: '/get_playlist/' + $(this).text(),
				succsess: (response) => {
					console.log(response);
				}
			});
			console.log(playlist_id);
			$.ajax({
				method: 'POST',
				url: '/add_to_playlist/' + playlist_id + '/' + art_id,
				succsess: (response) => {
					console.log(response);
				},
				error: (error) => {
					console.log(error);
				}
			});
		} else {
			$.ajax({
				method: 'POST',
				url: '/make_playlist/',
				data: JSON.stringify({'title':title, 'desc':desc}),
				succsess: (response) => {
					console.log(response);
				},
				error: function(error) {
					console.log(error);
				}
			});
		}
	});
});
