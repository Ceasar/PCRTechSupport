
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
});
