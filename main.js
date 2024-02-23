// main.js

// Get the access token from local storage
const accessToken = localStorage.getItem('access_token');

// Make a GET request to the protected route on your FastAPI backend
fetch('http://127.0.0.1:8000/test', {
    headers: {
        'Authorization': `Bearer ${accessToken}`,
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();  // You may want to use response.json() if the response is JSON
})
.then(responseText => {
    // Handle the successful response from the protected route
    console.log('Success:', responseText);
})
.catch(error => {
    // Handle errors, e.g., unauthorized access
    console.error('Error:', error);
});
