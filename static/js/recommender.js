var send_data = {};

$(document).ready(function($) {
    // Get user's friends from Database
    getFriends();
    
    // Get type of recommendations
	$('.rec-type').on('click', function () {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
        type = this.id
        // Don't update for friend recommendations
        if (type != 'friends') {
            $('#results-table').css('display', 'inline-block');
            send_data['type'] = type;
            // Get API data with updated params
            getAPIData();
        }
	}); 
});

// Function to get data from the API
function getAPIData() {
	let url = $('#list_data').attr("url")
	$.ajax({
		method: 'GET',
		url: url,
		data: send_data,
		beforeSend: function () {
			$("#no_results h5").html("Loading data...");
		},
		success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
	});
}

function putTableData(result) {
	// Utility function to create HTML table to 
	// display data
	let row;
    console.log(result['results'].length);
	if (result['results'].length > 0) {
		$("#no_results").hide();
        $("#list_data").show();
        $("#listing").html("");
        $.each(result["results"], function (a, b) {
            detail_url = '/shows/detail/' + b.id
            row = `<tr onclick="window.location='${detail_url}';">
            <td>${b.title}</td>
            <td>${b.release_year}</td>
            <td>${b.description}</td>
            <td>${b.category_string}</td>
            <td>${b.country_string}</td></tr>`
            $("#listing").append(row);   
        });
	}
	else {
		// if no result found for the given filter, then display no result
        $("#no_results h5").html("You need to like some shows to get recommendations");
        $("#list_data").hide();
        $("#no_results").show();
	}
	// setting previous and next page url for the given result
    let prev_url = result["previous"];
    let next_url = result["next"];

    // disabling-enabling button depending on existence of next/prev page. 
    if (prev_url === null) {
        $("#previous").addClass("disabled");
        $("#previous").prop('disabled', true);
    } else {
        $("#previous").removeClass("disabled");
        $("#previous").prop('disabled', false);
    }
    if (next_url === null) {
        $("#next").addClass("disabled");
        $("#next").prop('disabled', true);
    } else {
        $("#next").removeClass("disabled");
        $("#next").prop('disabled', false);
    }
    // setting the url
    $("#previous").attr("url", result["previous"]);
    $("#next").attr("url", result["next"]);
}

// Gets list of user's friends
function getFriends() {
    console.log('get friends');
    let url = $('#friends').attr('url');
    console.log('url: ', url);
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            friends_option = "<a class='dropdown-item'>Choose a friend...</a>";
            $.each(result['friends'], function (a, b) {
                let friend = b;
                friends_option += `<a class='dropdown-item' onclick="loadFriend('${b}')">${b}</a>`
            });
            $('#friends-dropdown').html(friends_option)
        },
        error: function(response) {
            console.log(response)
        }
    });
}

// Get's Friend data from API
function loadFriend (friend) {
    console.log('loadFriend');
    console.log(friend);
    $('#results-table').css('display', 'inline-block');
    send_data['type'] = 'friend';
    send_data['friend'] = friend;
    // Get API data with updated params
    getAPIData();
}

// Next page button
$("#next").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function(result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})
// Previous page button
$("#previous").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function(result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})