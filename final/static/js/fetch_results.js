// Variable to control the polling process
let stopPolling = false;

/**
 * Function to fetch prediction results from the server and update the results table.
 */
function fetchResults() {
    if (stopPolling) return; // Exit if polling is stopped

    // Make a GET request to the backend endpoint
    fetch('/fetch-results/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            // Check if polling should stop (based on backend response)
            if (data.stop) {
                stopPolling = true;
                console.log("Polling stopped by server.");
                return;
            }

            // Get the results-body element in the table
            const resultsBody = document.getElementById('results-body');
            resultsBody.innerHTML = ''; // Clear previous table content

            // Check if results are available
            if (data.results && data.results.length > 0) {
                // Iterate over the results and populate the table
                data.results.forEach(entry => {
                    const row = `
                        <tr>
                            <td>${entry.Second || 'N/A'}</td>
                            <td>${entry.final?.prediction || 'N/A'}</td>
                            <td>${entry.final?.Confidence ? entry.final.Confidence.toFixed(2) + '%' : 'N/A'}</td>
                        </tr>
                    `;
                    resultsBody.innerHTML += row; // Append the row to the table
                });
            } else {
                // If no results, display a message
                resultsBody.innerHTML = '<tr><td colspan="3">No results available.</td></tr>';
            }

            console.log("Results updated."); // Log success
            setTimeout(fetchResults, 1000); // Call fetchResults again after 1 second
        })
        .catch(error => {
            console.error("Error fetching results:", error);
            // Optionally, you can stop polling on error
            stopPolling = true;
        });
}

// Function to stop polling
function stopFetchResults() {
    stopPolling = true; // Set the stopPolling flag to true
    console.log("Polling has been stopped.");
}

// Start polling when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    fetchResults();

    // Attach event listener to the stop button
    const stopButton = document.getElementById('stop-button');
    if (stopButton) {
        stopButton.addEventListener('click', stopFetchResults);
    }
});