$(document).ready(function() {
	$('.sort-artists').click( () => {
		a = $('.artists-list');
		a.children().each( (i,li) => {
			a.prepend(li)
		});
		$('.artists').children('ul').append(a)
	});
	$('.sort-arts').click( () => {
		a = $('.arts-list');
		a.children().each( (i, li) => {
			a.prepend(li)
		});
		$('.arts').children('ul').append(a)
	});
	$('.sort-users').click( () => {
		a = $('.arts-list');
		a.children().each( (i, li) => {
			a.prepend(li)
		});
		$('.arts').children('ul').append(a)
	});
});
