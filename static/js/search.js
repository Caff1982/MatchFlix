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

	// on selecting the category option
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

	send_data['category'] = '';
	send_data['country'] = '';
	send_data['format'] = 'json';
}

function putTableData(result) {
	// Utility function to create HTML table to 
	// display data
	let row;
	console.log('Result length: ', result.length)
	if (result.length > 0) {
		console.log('Valid data');
		$("#no_results").hide();
        $("#list_data").show();
        $("#listing").html("");
        result.forEach(function (item, index) {
            row = "<tr> <td title=\"" + item.title + "\">" + item.title + "</td>" +
            "<td>" + item.description + "</td></tr>"
            $("#listing").append(row);   
        });
	}
	else {
		console.log('Invalid data')
	}
}

function getAPIData() {
	let url = $('#list_data').attr("url")
	console.log('URL: ', url)
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
    console.log('Countries url: ', url)
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