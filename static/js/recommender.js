var send_data = {};

$(document).ready(function($) {
	// Get recommendations for self from API
	$('#self').on('click', function() {
		$('#self').addClass('active');
		send_data['type'] = 'self';
	getAPIData();
	});

	$('#friend').on('click', function() {
		send_data['type'] = 'friend';
	getAPIData();
	});

	$('#random').on('click', function() {
		send_data['type'] = 'random';
	// Get API data with updated params
	getAPIData();
	});
});

// Function to get data from the API
function getAPIData() {
	let url = $('#list_data').attr("url")
	$.ajax({
		method: 'GET',
		url: url,
		data: send_data,
		beforeSend: function() {
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
        $("#no_results h5").html("No results found");
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