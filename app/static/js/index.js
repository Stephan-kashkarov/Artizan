$(document).ready(function() {
	$(".login").on('click', function(e) {
		window.location.replace("/login");
	});
	$(".regester").on("click", function (e) {
		window.location.replace("/register");
	});
});
