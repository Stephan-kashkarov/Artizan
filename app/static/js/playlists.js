$(document).ready(function() {
	$('.remove').click( (e) => {
		p_id = $(this).siblings('.data').children('playlist_id').text();
		a_id = $(this).siblings('.data').children('art_id').text();
		$.ajax({
			method: 'post',
			url: '/remove_from_playlist/' + p_id + '/' + a_id
		});
	});
	$('.delete').click( (e) => {
		p_id = $(this).siblings('.data').children('playlist_id').text();
		$.ajax({
			method: 'post',
			url: '/delete_playlist/' + p_id,
			succsess: () => {
				window.location.href='/browse';
			}
		});
	});
});
