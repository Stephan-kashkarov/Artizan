$( document ).ready( function() {
	$('.btn-search').click((e) => {
		path = '127.0.0.1:5000/search/';
		e.preventDefault();
		window.location.href = '/search/'+$('.search-input')[0].value;
	});
});
