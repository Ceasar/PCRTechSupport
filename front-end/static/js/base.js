
// On ready
$(document).ready(function() {
    var urlCourse = " ";
    $(".chzn-select").chosen();
    $("#search-dept").change(function() {
	$.get("http://localhost:8000/options", { dept: $(this).val() },
	      function(data) {
		  $("#search-course_chzn").remove();
		  $("#search-course").removeClass("chzn-done");
		  $("#search-course").html(data).show().chosen();
	      });
    });
    $("#search-course").change(function() {
	$("div#classInfo").html('<img src="http://www.seas.upenn.edu/~kevinsu/spiral.gif" height="200" />');
	urlCourse = ($(this).val()).replace(" ", "/") + "/";
	var url = "http://localhost:8000/course/" + ($(this).val()).replace(" ", "/") + "/";
	$.get(url,
	      function(data) {
		  $.colorbox({html: data});
	      });
    });
    $('#


});
