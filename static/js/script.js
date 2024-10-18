document.addEventListener('DOMContentLoaded', () => {
    const pathname = window.location.pathname;

    if (pathname === '/state-cases') {
        const state_name = document.getElementById('stateDropdown').value;
        const year = document.getElementById('year-select').value;        
        d3.json('/api/state-cases/all?year=${year}&state=${state_name}').then(data => {
            plotBarChart(data);
            plotLineChart(data);
            plotPieChart(data);  // Adding pie chart
            plotOverlayingBarChart(data);
            plotBarChartUsingCharts(data);
        }).catch(error => console.error('Error:', error));
    } else if (pathname === '/summary') {

        // Call API for page 2
        d3.json('/api/state-cases/all?').then(data => {
            console.log("No factor");
            console.log(data);
            plotBarChartUsingCharts(data);            
        }).catch(error => console.error('Error:', error));

        d3.json('/api/state-cases/all?factor=state').then(data => {
            console.log("factor");
            console.log(data);
            plotStateTotalChart(data);
            //Error: Error: Something went wrong with axis scaling
            //plotStateHeatMap(data);              
        }).catch(error => console.error('Error:', error));

        d3.json('/api/state-cases/all?factor=pop').then(data => {
            console.log("No factor");
            console.log(data);
            plotStatePopulation(data);            
        }).catch(error => console.error('Error:', error));

        d3.json('/api/state-cases/all?factor=weather').then(data => {
            console.log("Weather factor");
            console.log(data);
            plotBarChart("Weather","Fatals","","","weatherData",data);            
        }).catch(error => console.error('Error:', error));
    } 
    else if (pathname === '/map') {
        // Initialize the map, set the center and zoom level
        let map = L.map("map", {
            center: [39.828175, -98.5795],
            zoom: 5
        });

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);  
        // Plot the Markers 
        d3.json('/api/state-cases/all?factor=markers&year=${2019}').then(data => {
        plotAccidentDataMap(data);
    }).catch(error => console.error('Error:', error));
    }
    else {
    }
});

function plotOverlayingBarChart(xColumnName, yColumnNames,title, xtitle, ytitle, elementId, data) {
    const trace1 = {
        x: data.map(d => d[xColumnName]),
        y: data.map(d => d[yColumnNames[0]]),
        type: 'bar',
        name: 'Value 1'
    };

    const trace2 = {
        x: data.map(d => d[xColumnName]),
        y: data.map(d => d[yColumnNames[1]]),
        type: 'bar',
        name: 'Value 2'
    };

    const layout = {
        title: title,
        barmode: 'overlay', // Set barmode to 'overlay' for stacking bars
        xaxis: { title: xtitle },
        yaxis: { title: ytitle }
    };

    Plotly.newPlot(elementId, [trace1, trace2], layout);
}

function plotBarChart(xColumnName, yColumnName,title, xtitle, ytitle, elementId, data) {
    const trace = {
        x: data.map(d => d[xColumnName]),
        y: data.map(d => d[yColumnName]),
        type: 'bar'
    };

    const layout = {
        title: title,
        xaxis: xtitle,
        yaxis: ytitle
    };

    Plotly.newPlot(elementId, [trace], layout);
}

function plotLineChart(xColumnName, yColumnName,title, xtitle, ytitle, elementId, data) 
{
    const trace = {
        x: data.map(d =>  d[xColumnName]),
        y: data.map(d => d[yColumnName]),
        type: 'scatter',
        mode: 'lines+markers'
    };

    const layout = {
        title: title,
        xaxis: { title: xtitle },
        yaxis: { title: ytitle }
    };

    Plotly.newPlot(elementId, [trace], layout);
}

function plotPieChart(xColumnName, yColumnName,title, hoverinfo, textinfo, elementId, data) {
    const trace = {
        labels: data.map(d => d[xColumnName]),
        values: data.map(d => d[yColumnName]),
        type: 'pie',
        hoverinfo: hoverinfo, // Customize hover text here
        textinfo: textinfo
    };

    const layout = {
        title: title
    };

    Plotly.newPlot(elementId, [trace], layout);
}

function plotBarChartUsingCharts(data) {   
    if (Array.isArray(data)) { 
        const labels = data.map(d => d._id);
        const values = data.map(d => d.Fatals);

        var ctx = document.getElementById('accidentsByYearData').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Fatal Crashes',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                onClick: function(evt, elements) {
                    if (elements.length > 0) {
                        var elementIndex = elements[0].index;
                        var label = labels[elementIndex];
                        var value = values[elementIndex];
                        console.log('Clicked on: ' + label + ', Value: ' + value);
                        // Do something with the label and value here
                    }
                }
            }
            });
        }
}

function plotStatePopulation(data)
{
    if (Array.isArray(data)) {
        const states = data.map(d => d.StateName);
        const pops = data.map(d => parseInt(d.Population.replace(/,/g, ''))); // Remove commas and convert to number
        // Combine states and populations into an array of objects, then sort
        const sortedData = states.map((state, i) => ({ state, pop: pops[i] }))
                                  .sort((a, b) => b.pop - a.pop);

        // Extract sorted states and populations
        const sortedStates = sortedData.map(d => d.state);
        const sortedPops = sortedData.map(d => d.pop);
        const ctx = document.getElementById('statepopulation').getContext('2d');
        const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedStates,
            datasets: [{
                label: 'Total Population Per State for Year 2022',
                data: sortedPops,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                text: sortedStates.map((state, i) => `${state}<br>Population: ${sortedPops[i]}`),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
});

}
}

function plotStateTotalChart(data)
{
    if (Array.isArray(data)) {
        const states = data.map(d => d._id);
        const fatals = data.map(d => d.Fatals);
        const percents = data.map(d => d.percent);

        const ctx = document.getElementById('accidentsByStateYearData').getContext('2d');
        const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: states,
            datasets: [{
                label: 'Total Fatals Per State for Year 2019-2022',
                data: fatals,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                text: states.map((state, i) => `${state}<br>Fatals: ${fatals[i]}<br>Percent: ${percents[i]}`)
            }]
        },
        options: {
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    beginAtZero: true
                }
            }
        }
});

}}

function plotStateHeatMap(data)
{
    if (Array.isArray(data)) {
        const states = data.map(d => d.StateName);
            const fatals = data.map(d => d.Fatals);
            //const percents = data.map(d => d.percent);

            // Validate data
            if (states.length && fatals.length) {
                const trace = {
                    type: 'choropleth',
                    locationmode: 'USA-states',
                    locations: states,
                    z: fatals,
                    text: states.map((state, i) => `${state}<br>Fatals: ${fatals[i]}`),
                    colorscale: 'Blues',
                    colorbar: {
                        title: 'Fatals',
                    },
                };

            const layout = {
                title: `State Cases for 2021`,
                geo: {
                    scope: 'usa',
                    projection: {
                        type: 'albers usa',
                    },
                },
                xaxis: {
                    showgrid: true,
                    zeroline: true,
                    showline: true,
                    automargin: true,
                },
                yaxis: {
                    showgrid: true,
                    zeroline: true,
                    showline: true,
                    automargin: true,
                }
            };
            Plotly.newPlot('heatmap', [trace], layout);
        } else {
            console.error('Data arrays are empty or invalid');
        }
    } else {
        console.error('Data is not an array:', data);
    }
}


// Function to fetch accident data from Flask API and plot on the map
function plotAccidentDataMap(data) {
    // Loop through the accident data
    data.forEach(function(accident_data) {
        var lat = parseFloat(accident_data.LATITUDE);
        var lon = parseFloat(accident_data.LONGITUD);
        
        // Check if lat/lon are valid before adding markers
        if (!isNaN(lat) && !isNaN(lon)) {
            
            // Create a marker for each accident location
            var marker = L.marker([lat, lon]).addTo(map);
            // Create a more detailed popup with a table
            var tooltipContent = `
                <div class="tooltip-table">
                    <h3 class="tooltip-heading">Accident Details</h3>
                    <table>
                        <tr><td><strong>State:</strong></td><td>${accident_data.STATENAME}</td></tr>
                        <tr><td><strong>Date:</strong></td><td>${accident_data.MONTHNAME}/${accident_data.DAY}/${accident_data.YEAR}</td></tr>
                        <tr><td><strong>County:</strong></td><td>${accident_data.COUNTYNAME}</td></tr>
                        <tr><td><strong>City:</strong></td><td>${accident_data.CITYNAME|| "N/A"}</td></tr>
                        <tr><td><strong>Fatalities in the Crash:</strong></td><td>${accident_data.FATALS}</td></tr>
                        <tr><td><strong>Vehicles in the Crash:</strong></td><td>${accident_data.VE_TOTAL}</td></tr>
                    </table>
                </div>
            `;

            marker.bindTooltip(tooltipContent, {
                permanent: false,
                direction: 'top',
                offset: [0,-10],
                className: 'custom-tooltip'
            });

        }
    }). catch(error => console.error('Error fetching data:', error)); 
    };

