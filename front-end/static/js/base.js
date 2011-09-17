
// On ready
$(document).ready(function() {
    $(".chzn-select").chosen();
    $("#search-dept").change(function() {
	$.get("http://localhost:8000/options.html", { dept: $(this).val() },
	      function(data) {
		  $("#search-course").append(data).show().chosen();
	      });
    });
});
