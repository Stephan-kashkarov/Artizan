$( document ).ready( function() {
     $('.nav-tabs .nav-item').click(function(e){
		 $(".contents .Make").addClass("hidden");
		 $(".contents .Art").addClass("hidden");
         if (
            (!($(this).children().hasClass('disabled'))) ||
            ($(this).children().hasClass('active'))
            ){
            $(this).children().toggleClass('active');
			var div = $(this).children().text();
			var thing_list = [];
            var thing = $(this).siblings();
            thing.children('.active').removeClass('active');
			var list_of_names = thing.children().text().split(/(?=[A-Z])/);
			for (var i in list_of_names){
				$("." + list_of_names[i]).addClass('hidden');
			}
			var current_thing = $(this).children().text();
			$("." + current_thing).removeClass('hidden');
         }
     });

	$('.nav-tabs').click(function(e){
		e.preventDefault();
	});

	 $('.btn').click(function(e){
		if ( $( this ).text() === 'Upload Art' ){
			$('.contents').children('Showcase').addClass('hidden');
			$(".contents .Showcase").addClass("hidden");
			$(".contents .Art").removeClass("hidden");
		}
	});

	$('.delete-playlist').click( () => {
		playlist_id = $(this)[0].activeElement.parentElement.children[2].firstChild.data
		$.ajax({
			method: 'POST',
			url: '/delete_playlist/' + playlist_id,
			sucssess: (response) => {
				console.log(response);
			},
			error: (error) => {
				console.log(error);
			}
		});
		window.location.reload();
	});
});
