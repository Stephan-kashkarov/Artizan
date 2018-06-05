$( document ).ready( function() {
     $('.nav-tabs .nav-item').click(function(e){
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
		if ( $( this ).text() == 'Upload Art' ){
			$('.contents').children('Showcase').addClass('hidden');
			$(".contents .Showcase").addClass("hidden");
			$(".contents .Art").removeClass("hidden");
		}
	});
});
