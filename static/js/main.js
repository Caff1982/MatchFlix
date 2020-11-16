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

// add/remove friend button
$('#add-friend-btn').on('click', function() {
  console.log('clicked');
  console.log($(this).html());
  let url = '/accounts/ajax/';
  url = ($(this).html() == 'Add Friend') ? url += 'add-friend/' : url += 'remove-friend/';
  console.log(url);
  $.ajax({
    method: "POST",
    url: url,
    data: {'friend_id': $(this).attr('value'),
           'csrfmiddlewaretoken': csrf_token},
    'dataType': 'json',
  });
  if ($(this).html() == 'Add Friend') {
    $(this).html('Remove Friend')
  }
  else {
    $(this).html('Add Friend')
  }
});

// Like/Un-like button
$('#like-button').on('click', function() {
  console.log('clicked');
  console.log($(this).html());
  let url = '/shows/ajax/';
  url = ($(this).html() == 'Like') ? url += 'add-like/' : url += 'remove-like/';
  console.log(url);
  $.ajax({
    method: "POST",
    url: url,
    data: {'show_id': $(this).attr('value'),
           'csrfmiddlewaretoken': csrf_token},
    'dataType': 'json',
  });
  if ($(this).html() == 'Like') {
    $(this).html('Remove from likes')
  }
  else {
    $(this).html('Like')
  }
});
