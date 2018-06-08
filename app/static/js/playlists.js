$(document).ready(function() {
	$('.remove').click(function(e) {
		p_id = $(this).parent().children('.data').children('.playlist_id').text();
		a_id = $(this).parent().children('.data').children('.art_id').text();
		$.ajax({
			method: 'post',
			url: '/remove_from_playlist/' + p_id + '/' + a_id
		});
	});
	$('.delete').click(function(e) {
		p_id = $(this).parent()[0].className;
		console.log($(this).parent());
		$.ajax({
			method: 'post',
			url: '/delete_playlist/' + p_id,
			success: () => {
				window.location.href='/browse';
			}
		});
	});
	$('.view').click(function(e){
		a_id = $(this).parent().children('.data').children('.art_id').text();
		window.location.href = '/browse/art/' + a_id;
	});
});
