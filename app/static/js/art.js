$(document).ready(() => {
	$('.dropdown-item').click((e) => {
		console.log($(this));
		url = window.location.href.split('/');
		art_id = url[url.length - 1];
		// playlist_id = (() => {
		// 	$.ajax({
		// 		async: false,
		// 		method: 'POST',
		// 		url: '/get_playlist/' + $(this).text(),
		// 		succsess: (response) => {
		// 			console.log(response);
		// 		}
		// 	}).response;
		// });
		// art_id = winow.location.href
		// $.ajax({
		// 	method: 'POST',
		// 	url: '/add_to_playlist/' + playlist_id + '/' + art_id
		// });
	});
});
