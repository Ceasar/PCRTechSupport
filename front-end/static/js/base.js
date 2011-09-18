
// On ready
$(document).ready(function() {
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
	var url = "http://localhost:8000/course/" + ($(this).val()).replace(" ", "/") + "/";
	$.get(url,
	      function(data) {
		  $("div#classInfo").html(data);
	      });
    });
});
