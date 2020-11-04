var send_data = {}


$(document).ready(function () {
	// Reset all parameters on page load
	resetFilters();
	// Get all the data without filters
	getAPIData();
	// Get all Categories from Database
	getCategories();
	// Get all Countries from Database
	getCountries();
    // Get range of release years
    getYears();

    // Text search
    $('#title-search').on('keyup', function () {
        send_data['title'] = this.value;
        // Get API data with updated filters
        getAPIData()
    })

	// On selecting the category option
	$('#categories').on('change', function () {
		if (this.value == 'all')
			send_data['category'] = '';
		else
			send_data['category'] = this.value;
		// Get API data with updated filters
		getAPIData();
	})

	// On selecting the country option
	$('#countries').on('change', function () {
		if (this.value == 'all')
			send_data['country'] = '';
		else
			send_data['country'] = this.value;
		// Get API data with updated filters
		getAPIData();
	})

    // On selecting the year option
    $('#years').on('change', function () {
        if (this.value == 'all')
            send_data['year'] = '';
        else
            send_data['year'] = this.value;
        // Get API data with updated filters
        getAPIData();
    })

	// Reset the filters
	$("#display_all").click(function(){
        resetFilters();
        getAPIData();
    })
})


// Function to reset all filters
function resetFilters() {
	$("#categories").val("all");
	$("#countries").val("all");
    $("#years").val("all");

	send_data['category'] = '';
	send_data['country'] = '';
    send_data['year'] = '';
	send_data['format'] = 'json';
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
            row = "<tr> <td title=\"" + b.title + "\">" + b.title + "</td>" +
            "<td>" + b.release_year + "</td>" +
            "<td>" + b.description + "</td>" +
            "<td>" + b.category_string + "</td>" +
            "<td>" + b.country_string + "</td></tr>"
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
    // displaying result count
    $("#result-count span").html(result["count"]);
}

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

function getCategories() {
	let url = $("#categories").attr("url");
	$.ajax({
		method: 'GET',
		url: url,
		data: {},
		success: function (result) {
			categories_option = "<option value='all' selected>All Categories</option>";
            $.each(result["categories"], function (a, b) {
                categories_option += "<option>" + b + "</option>"
            });
            $("#categories").html(categories_option)
		},
		error: function(response){
            console.log(response)
        }
	});
}

function getCountries() {
    let url = $("#countries").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            countries_option = "<option value='all' selected>All Countries</option>";
            $.each(result["countries"], function (a, b) {
                countries_option += "<option>" + b + "</option>"
            });
            $("#countries").html(countries_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getYears() {
    let url = $("#years").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            years_option = "<option value='all' selected>All Years</option>";
            $.each(result["years"], function (a, b) {
                years_option += "<option>" + b + "</option>"
            });
            $("#years").html(years_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}



$("#next").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})

$("#previous").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function(response){
            console.log(response)
        }
    });
})


