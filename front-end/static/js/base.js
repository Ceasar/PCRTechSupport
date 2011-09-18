
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
	var urlCourse = ($(this).val()).replace(" ", "/") + "/";
	var url = "http://localhost:8000/course/" + urlCourse;
	$.get(url,
	      function(data) {
		  $.colorbox({html: data});
		  $("#addClass").click(function(data) {
		      $.colorbox.close();
		      $.get("http://localhost:8000/add/" + urlCourse,
			    function(data){
				$(".classList").html(data);
			    });
		  });
	      });
    });
   
    $.get("http://localhost:8000/add/0/0/",
	 function(data) {
	     $("div.classList").html(data);
	 });

    $.get("http://localhost:8000/recommendations/",
	  function(data) {
	      $("div.recommended").html(data);
	  });
});
