$(document).ready(function() {
	$('.remove').click( (e) => {
		p_id = $(this).siblings('.data').children('playlist_id')[0].value;
		a_id = $(this).siblings('.data').children('art_id')[0].value;
		$.ajax({
			method: 'post',
			url: '/remove_from_playlist/' + p_id + '/' + a_id
		});
	});
	$('.delete').click( (e) => {
		p_id = $(this).siblings('.data').children('playlist_id')[0].value;
		$.ajax({
			method: 'post',
			url: '/delete_playlist/' + p_id
		});
	});
});
