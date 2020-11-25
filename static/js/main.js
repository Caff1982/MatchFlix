$(document).ready(function($) {
    // Open modal popup
    $('.thumbnail').click(function() {
        console.log('clicked');
        let modal_id = $(this).attr('id');
        console.log('modal_id: ', modal_id);
        $('#modal-popup' + modal_id).show();
    });
    // Close modal popup
    $('.close-btn').click(function() {
        console.log('close clicked');
        $('.modal').hide();

    });

    // Like/Un-like button
    $('.like-button').on('click', function() {
      console.log('like button clicked');
      let url = '/shows/ajax/';
      url = ($(this).html() == 'Like') ? url += 'add-like/' : url += 'remove-like/';
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

    // Reset the filters
    $('#display_all').click(function() {
          $('#id_title').val('');
          $('#id_category').val('all');
          $('#id_country').val('all');
          $('#id_year').val('all');
      });


});


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
    let url = '/accounts/ajax/';
    url = ($(this).html() == 'Add Friend') ? url += 'add-friend/' : url += 'remove-friend/';
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

