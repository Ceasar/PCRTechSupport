
// On ready
$(document).ready(function() {
    
    $(".chzn-select").chosen();
    $("#search-dept").change(function() {
	$("#search-course_chzn").remove();
	$("#search-course").removeClass("chzn-done").hide();
	$.get("http://localhost:8000/options", { dept: $(this).val() },
	      function(data) {
		  $("#search-course").html(data).show().chosen();
	      });
    });
    $("#search-course").change(function() {
	var urlCourse = ($(this).val()).replace(" ", "/") + "/";
	var url = "http://localhost:8000/course/" + urlCourse;
	$.get(url,
	      function(data) {
		  $.colorbox({html: data});
		  $("#addClass").click(function(data) {
		      $.colorbox.close();
		      $.get("http://localhost:8000/add/" + urlCourse,
			    function(data) {
				$("div.classList").html(data);
			    });
		      $("#search-course_chzn").hide();
		      $("#search-dept_chzn").find("option:selected").removedAttr("selected");
		      $("div.recommended").html('<img src="http://www.seas.upenn.edu/~kevinsu/spiral.gif" height="60">');
		      $.get("http://localhost:8000/recommendations-admin/generate",
			    function(data) {
				$("div.recommended").html(data);
			    });
		  });
	      });
    });
   
    $.get("http://localhost:8000/add/0/0/",
	 function(data) {
	     $("div.classList").html(data);
	 });
    $("div.recommended").html('<img src="http://www.seas.upenn.edu/~kevinsu/spiral.gif" height="60">');
    $.get("http://localhost:8000/recommendations-admin/generate",
	  function(data) {
	      $("div.recommended").html(data);
	  });
});
