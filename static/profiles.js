// load profiles.json
$.getJSON('profiles.json', function(data) {
  // get list of all courses from profiles
  var courses = [];
  $.each(data, function(username, profile) {
    $.each(profile.courses, function(index, course) {
      if ($.inArray(course, courses) == -1) {
        courses.push(course);
      }
    });
  });
  
  // initialize autocomplete widget
  $('#course-input').autocomplete({
    source: courses,
    select: function(event, ui) {
      // add selected course to list
      var course = ui.item.value;
      $('#selected-courses').append('<li>' + course + ' <button class="remove-course">X</button></li>');
      // clear input
      $('#course-input').val('');
      return false;
    }
  });
  
  // add event listener for removing course
  $('#selected-courses').on('click', '.remove-course', function() {
    $(this).parent().remove();
  });
});

// function to get list of selected courses
function getSelectedCourses() {
  var courses = [];
  $('#selected-courses li').each(function(index, element) {
    courses.push($(element).text().trim().slice(0, -1));
  });
  return courses;
}

