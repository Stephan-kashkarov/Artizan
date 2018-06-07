$(document).ready(() => {
	url = window.location.href.split('/');
	art_id = url[url.length - 1];
	$('.dropdown-menu a').click(function(e){
		var item = $(this).text();
		if (item != '+ New Playlist'){
			e.preventDefault();
			playlist_id = $.ajax({
				async: false,
				method: 'POST',
				url: '/get_playlist/' + item,
				succsess: (response) => {
					console.log(response);
				}
			});
			console.log(playlist_id);
			a = $.ajax({
				method: 'POST',
				url: '/add_to_playlist/' + playlist_id.responseText + '/' + art_id,
				succsess: (response) => {
					console.log(response);
				},
				error: (error) => {
					console.log(error);
				}
			});
			console.log(a);
		} else {
			e.preventDefault();
			var title;
			do {
				title = prompt('Title of playlist (No spaces)');
			} while (title.includes(' '));
			var desc = prompt('Desc of playlist');
			var a = $.ajax({
				async: false,
				method: 'POST',
				url: '/Make_playlist',
				data: JSON.stringify({
					"title":title,
					"desc":desc
				}),
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				succsess: (response) => {
					console.log(response);
				},
				error: function(error) {
					console.log(error);
				}
			});
			playlist_id = a.responseText;
			$.ajax({
				method: 'POST',
				url: '/add_to_playlist/' + playlist_id + '/' + art_id,
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
