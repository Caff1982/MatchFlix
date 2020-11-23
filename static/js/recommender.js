var send_data = {};
const modals = document.getElementsByClassName('thumbnail')
console.log('len modals: ', modals.length)

$(document).ready(function($) {
    // Get user's friends from Database
    getFriends();

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

});

// // Close modal popup
// $(document).click(function(e) {
//     $('.popup-content').hide();
// });
// $('.popup-content').click(function(e) {
//     e.stopPropagation();
// });




// // Function to get data from the API
// function getAPIData() {
// 	let url = $('#list_data').attr("url")
// 	$.ajax({
// 		method: 'GET',
// 		url: url,
// 		data: send_data,
// 		beforeSend: function () {
// 			$("#no_results h5").html("Loading data...");
// 		},
// 		success: function (result) {
//             putTableData(result);
//         },
//         error: function (response) {
//             $("#no_results h5").html("Something went wrong");
//             $("#list_data").hide();
//         }
// 	});
// }

// function putTableData(result) {
// 	// Utility function to create HTML table to 
// 	// display data
// 	let row;
// 	if (result['results'].length > 0) {
// 		$("#no_results").hide();
//         $("#list_data").show();
//         $("#listing").html("");
//         $.each(result["results"], function (a, b) {
//             // detail_url = '/shows/detail/' + b.id
//             // row = `<tr onclick="window.location='${detail_url}';">
//             let img_url = `http://res.cloudinary.com/matchflix/image/upload/${b.show_id}tn.jpg`;
//             console.log('img url: ', img_url)
//             row = `
//                      <div id="thumbnail${a}">
//                        <center><h5>${b.title}</h5></center>
//                        <img src=${img_url}>
    
//                    </div>`

//             // <td>${b.title}</td>
//             // <td>${b.release_year}</td>
//             // <td>${b.description}</td>
//             // <td>${b.category_string}</td>
//             // <td>${b.country_string}</td></tr>
//             $("#listing").append(row);   
//         });
// 	}
// 	else {
// 		// if no result found for the given filter, then display no result
// 	}
// 	// setting previous and next page url for the given result
//     let prev_url = result["previous"];
//     let next_url = result["next"];

//     // disabling-enabling button depending on existence of next/prev page. 
//     if (prev_url === null) {
//         $("#previous").addClass("disabled");
//         $("#previous").prop('disabled', true);
//     } else {
//         $("#previous").removeClass("disabled");
//         $("#previous").prop('disabled', false);
//     }
//     if (next_url === null) {
//         $("#next").addClass("disabled");
//         $("#next").prop('disabled', true);
//     } else {
//         $("#next").removeClass("disabled");
//         $("#next").prop('disabled', false);
//     }
//     // setting the url
//     $("#previous").attr("url", result["previous"]);
//     $("#next").attr("url", result["next"]);
// }

// Gets list of user's friends
function getFriends() {
    let url = $('#friends').attr('url');
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            friends_option = "<a class='dropdown-item'>Choose a friend...</a>";
            $.each(result['friends'], function (a, b) {
                let friend = b;
                friends_option += `<a class='dropdown-item' href="/recommendations/friend/${b}">${b}</a>`
            });
            $('#friends-dropdown').html(friends_option)
        },
        error: function(response) {
            console.log(response)
        }
    });
}

// // Get's Friend data from API
// function loadFriend (friend) {
//     console.log('loadFriend');
//     console.log(friend);
//     $('#results-table').css('display', 'inline-block');
//     send_data['type'] = 'friend';
//     send_data['friend'] = friend;
//     // Get API data with updated params
//     getAPIData();
// }


// Next page button
$("#next").click(function () {
    console.log('next clicked')
    let url = $(this).attr("url");
    $.ajax({
        method: 'GET',
        url: url,
    });
})
// Previous page button
$("#previous").click(function () {
    let url = $(this).attr("url");
    $.ajax({
        method: 'GET',
        url: url,
    });
})