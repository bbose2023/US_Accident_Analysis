function getQueryParams() {
    // Split the pathname (e.g., '/map/2022/Alabama') and extract the year and state
    if( window.location.pathname === '/map')
    {
        const pathParts = window.location.pathname.split('/');
           let YEAR=parseInt(pathParts[2]);  // The 3rd part of the path (index 2) is the year
           let STATE= pathParts[3];  // The 4th part of the path (index 3) is the state
        if(!YEAR ) {YEAR=2022;}
        if (!STATE) {STATE="Alabama";}   
        return {
            YEAR: YEAR ,  // The 3rd part of the path (index 2) is the year
            STATE: STATE  // The 4th part of the path (index 3) is the state
        };
    }
}

// Get year and state from the URL
const { YEAR, STATE} = getQueryParams();

// Initialize the map, set the center and zoom level
let map = L.map("map", {
    center: [39.828175, -98.5795],
    zoom: 5
  });

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Function to fetch accident data from Flask API and plot on the map
function fetchAccidentData(YEAR,STATE) {
    const url = `/api/state-cases/all?&factor=markers&year=${YEAR}&state=${STATE}`;  // Adjust this URL to match your Flask API endpoint
    
    fetch(url)
        .then(response =>  response.json())  // Parse the JSON response
        .then(data => {
            console.log(data);
            if (Array.isArray(data)) {
                console.log(data);
            // Loop through the accident data
                data.map(function(accident_data) {
                    var lat = parseFloat(accident_data.LATITUDE);
                    var lon = parseFloat(accident_data.LONGITUD);
                    
                    // Check if lat/lon are valid before adding markers
                    if (!isNaN(lat) && !isNaN(lon)) {
                        
                        // Create a marker for each accident location
                        var marker = L.marker([lat, lon]).addTo(map);
                        // Create a more detailed popup with a table
                        let tooltipContent = `
                            <div class="tooltip-table">
                                <h3 class="tooltip-heading">Accident Details</h3>
                                <table>
                                    <tr><td><strong>State:</strong></td><td>${accident_data.STATENAME || "Unknown"}</td></tr>
                                    <tr><td><strong>Date:</strong></td><td>${accident_data.MONTHNAME || "Unknown"}/${accident_data.DAY || "Unknown"}/${accident_data.YEAR || "Unknown"}</td></tr>
                                    <tr><td><strong>County:</strong></td><td>${accident_data.COUNTYNAME || "Unknown"}</td></tr>
                                    <tr><td><strong>City:</strong></td><td>${accident_data.CITYNAME || "N/A"}</td></tr>
                                    <tr><td><strong>Fatalities in the Crash:</strong></td><td>${accident_data.FATALS || "0"}</td></tr>
                                    <tr><td><strong>Vehicles in the Crash:</strong></td><td>${accident_data.VE_TOTAL || "Unknown"}</td></tr>
                                </table>
                            </div>
                        `;
                    setTimeout(()=> {
                        marker.bindTooltip(tooltipContent, {
                            permanent: false,
                            direction: 'top',
                            offset: [0,-10],
                            className: 'custom-tooltip'
                        });

                }, 500);
            }
        }
        )};      
})
    
            .catch(error => console.error('Error fetching data:', error)); 
    };
    
// Call the function to fetch and display accident data
fetchAccidentData(YEAR, STATE);