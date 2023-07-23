function redirectToProfile() {
    // Redirect to the specified URL using JavaScript
    window.location.href = "{{ url_for('logins.profile') }}";
}
function redirectToPassword() {
    // Redirect to the specified URL using JavaScript
    window.location.href = "{{ url_for('logins.profile') }}";
}
function redirectTologout() {
    // Redirect to the specified URL using JavaScript
    window.location.href = "{{ url_for('logins.logout') }}";
}