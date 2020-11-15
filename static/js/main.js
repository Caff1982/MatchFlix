//For getting CSRF token
function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
               var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
             }
          }
      }
 return cookieValue;
}

//Prepare csrf token
var csrf_token = getCookie('csrftoken');

// Add friend button
$('#add-friend').on('click', function() {
	let url = $(this).attr("url");
	console.log('url: ', url)
	$.ajax({
		method: "POST",
		url: url,
		data: {'friend_id': $(this).attr('value'),
			     'csrfmiddlewaretoken': csrf_token},
		'dataType': 'json',
 	});
  $(this).html("Remove Friend");
  $(this).attr("id", "remove-friend");
  $(this).attr("url", "{% url 'remove_friend' %}");
});

// Remove friend button
$('#remove-friend').on('click', function() {
  let url = $(this).attr("url");
  console.log('url: ', url)
  $.ajax({
    method: "POST",
    url: url,
    data: {'friend_id': $(this).attr('value'),
           'csrfmiddlewaretoken': csrf_token},
    'dataType': 'json',
  });
  $(this).html("Add Friend");
  $(this).attr("id", "add-friend");
  $(this).attr("url", "{% url 'add_friend' %}");
});