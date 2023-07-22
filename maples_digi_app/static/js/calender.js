
//
// Function to update the date and time elements in the HTML
function updateDateTime() {
    // Get the current date using JavaScript Date object
    var currentDate = new Date();

    // Update year, month, day, and time elements in the HTML
    document.getElementById("year").textContent = currentDate.getFullYear();
    document.getElementById("month").textContent = currentDate.getMonth() + 1; // Months are zero-indexed
    document.getElementById("day").textContent = currentDate.getDate();
    document.getElementById("time").textContent = currentDate.toLocaleTimeString();

}

// Call the updateDateTime function initially to set the date and time
updateDateTime();

// Update the date and time every second using setInterval
setInterval(updateDateTime, 1000);


// // Function to update the date and time elements in the HTML
// function updateDateTime() {
//     // Get the current date using JavaScript Date object
//     var currentDate = new Date();

//     // Update year, month, day, and time elements in the HTML
//     updateElement("year", currentDate.getFullYear());
//     updateElement("month", currentDate.getMonth() + 1); // Months are zero-indexed
//     updateElement("day", currentDate.getDate());
//     updateElement("time", currentDate.toLocaleTimeString());
// }

// // Function to update individual digits of the date and time
// function updateElement(elementId, value) {
//     var element = document.getElementById(elementId);
//     var valueString = value.toString();

//     // Split the value string into individual digits and wrap each digit in a <span> tag
//     var html = "";
//     for (var i = 0; i < valueString.length; i++) {
//         html += "<span>" + valueString[i] + "</span>";
//     }

//     element.innerHTML = html;
// }

// // Call the updateDateTime function initially to set the date and time
// updateDateTime();

// // Update the date and time every second using setInterval
// setInterval(updateDateTime, 1000);
