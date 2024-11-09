document.getElementById('create-new-link').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default anchor click behavior
    window.location.href = 'signup1.html'; // Redirect to signup.html
});


// Redirect to dashboard.html when the "Login" button is clicked
document.getElementById('login-button').addEventListener('click', function() {
    window.location.href = 'studdashboard.html'; // Redirect to dashboard.html
});

// script.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('signup-button').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the form from submitting
        window.location.href = 'signup2.html'; // Redirect to signup2.html
    });
});
