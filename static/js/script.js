// Retrieve selected data from localStorage or sessionStorage
// const selectedYear = sessionStorage.getItem('selectedYear');  // Or sessionStorage
// const selectedState = sessionStorage.getItem('selectedState');  // Or sessionStorage

document.getElementById('homeLink').addEventListener('click', function() {
    console.log('Clear the selected year and state');
    sessionStorage.removeItem('selectedYear');
    sessionStorage.removeItem('selectedState');  // Remove any other items if needed
});

function initializeSection()
{
    const pathname = window.location.pathname;
    console.log(`URL PathName ${pathname}`);
    const selectedYear = getData('selectedYear');
    const selectedState = getData('selectedState');

    // Extract request parameters
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);

    // Read specific parameters
    // const year = params.get('year');
    // const state = params.get('state');
    const base_url = "/api/state-cases/all?";
    
    let route = base_url;

    if(selectedYear) {
        route += `year=${selectedYear}`;
        if(selectedState) {
            route += `&state=${selectedState}`;
        }
    }

    console.log(`Route: ${route}`);
    console.log(`Selected Year: ${selectedYear}`);
    console.log(`Selected State: ${selectedState}`);
    
    // if (pathname === '/state-cases') {
    //     const state_name = document.getElementById('stateDropdown').value;
    //     const year = document.getElementById('year-select').value;        
    //     d3.json('/api/state-cases/all?year=${year}&state=${state_name}').then(data => {
    //         plotBarChart(data);
    //         plotLineChart(data);
    //         plotPieChart(data);  // Adding pie chart
    //         plotOverlayingBarChart(data);
    //         plotBarChartUsingCharts(data);
    //     }).catch(error => console.error('Error:', error));
    if (pathname === '/summary') {
        //Only call this for the first loading of the page when year is not present
        if(!selectedYear)
        {
            // Call API for page 2
            d3.json(route).then(data => {
                console.log("No factor");
                console.log(data);
                plotBarChartUsingCharts(data);            
            }).catch(error => console.error('Error:', error));
        }

        d3.json(`${route}&factor=state`).then(data => {
            console.log("factor");
            console.log(data);
            plotStateTotalChart(data);             
        }).catch(error => console.error('Error:', error));

        d3.json(`${route}&factor=pop`).then(data => {
            console.log("No factor");
            console.log(data);
            plotStatePopulation(data);            
        }).catch(error => console.error('Error:', error));

        d3.json(`${route}&factor=weather`).then(data => {
            console.log("Weather factor");
            console.log(data);
            plotBarChart("Weather","Fatals","Weather","Fatals","Totals","weatherData",data);            
        }).catch(error => console.error('Error:', error));
    } 
    else {
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const pathname = window.location.pathname;
    console.log(`URL PathName ${pathname}`);
    const selectedYear = getData('selectedYear');
    const selectedState = getData('selectedState');

    // Extract request parameters
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);

    // Read specific parameters
    // const year = params.get('year');
    // const state = params.get('state');
    const base_url = "/api/state-cases/all?";
    
    let route = base_url;

    if(selectedYear) {
        route += `year=${selectedYear}`;
        if(selectedState) {
            route += `&state=${selectedState}`;
        }
    }

    console.log(`Route: ${route}`);
    console.log(`Selected Year: ${selectedYear}`);
    console.log(`Selected State: ${selectedState}`);

    // if (pathname === '/state-cases') {
    //     const state_name = document.getElementById('stateDropdown').value;
    //     const year = document.getElementById('year-select').value;        
    //     d3.json('/api/state-cases/all?year=${year}&state=${state_name}').then(data => {
    //         plotBarChart(data);
    //         plotLineChart(data);
    //         plotPieChart(data);  // Adding pie chart
    //         plotOverlayingBarChart(data);
    //         plotBarChartUsingCharts(data);
    //     }).catch(error => console.error('Error:', error));
    if (pathname === '/summary') {
        //Only call this for the first loading of the page when year is not present
        if(!selectedYear)
        {
            // Call API for page 2
            d3.json(route).then(data => {
                console.log("No factor");
                console.log(data);
                plotBarChartUsingCharts(data);            
            }).catch(error => console.error('Error:', error));
        }

        d3.json(`${route}&factor=state`).then(data => {
            console.log("factor");
            console.log(data);
            plotStateTotalChart(data);             
        }).catch(error => console.error('Error:', error));

        d3.json(`${route}&factor=pop`).then(data => {
            console.log("No factor");
            console.log(data);
            plotStatePopulation(data);            
        }).catch(error => console.error('Error:', error));

        d3.json(`${route}&factor=weather`).then(data => {
            console.log("Weather factor");
            console.log(data);
            plotBarChart("Weather","Fatals","Total Fatal count by weather (2019-2022)","Types","Total Fatals","weatherData",data);            
        }).catch(error => console.error('Error:', error));
    } 
    else {
        fetch('https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=Tr5W4bOznYidz3pT4LOHKlfGjhM52Ry3')
        .then(response => response.json())
        .then(data => {
            const articles = data.results.filter(article => article.abstract.includes('Democratic'));  // Get top 5 fatal accident articles
            const accidentsContent = document.getElementById('accidentsContent');
            console.log('**************************************************************************888888888888888888888888888888888');
            console.log(articles);
            articles.forEach(article => {
                const newsTitle = document.createElement('h2');
                const newsSummary = document.createElement('p');
                const newsLink = document.createElement('a');
                
                newsTitle.innerText = article.title;
                newsSummary.innerText = article.abstract;
                newsLink.href = article.url;
                newsLink.innerText = 'Read more';
                
                accidentsContent.appendChild(newsTitle);
                accidentsContent.appendChild(newsSummary);
                accidentsContent.appendChild(newsLink);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        
           accidentsContent.appendChild(newsTitle);
                accidentsContent.appendChild(newsSummary);
                accidentsContent.appendChild(newsLink);
            });
        }
    });


// Save data to sessionStorage
function saveData(key, value) {
    sessionStorage.setItem(key, JSON.stringify(value));
}

// Retrieve data from sessionStorage
function getData(key) {
    return JSON.parse(sessionStorage.getItem(key));
}


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

function stateMap(Data)
{
   // Initialize the map
    var map = L.map('map').setView([37.8, -96], 4);

    // Load and display a tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Load GeoJSON data and add it to the map
    d3.json('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json').then(function(geoData) {
        // Example data
        var data = {
            'Oregon': 2020,
            'New Mexico': 1582
            // Add more states
        };

        // Function to get color based on value
        function getColor(d) {
            return d > 2000 ? '#800026' :
                d > 1500 ? '#BD0026' :
                d > 1000 ? '#E31A1C' :
                d > 500  ? '#FC4E2A' :
                d > 200  ? '#FD8D3C' :
                d > 100  ? '#FEB24C' :
                d > 50   ? '#FED976' :
                            '#FFEDA0';
        }

        // Function to style each feature
        function style(feature) {
            return {
                fillColor: getColor(data[feature.properties.name]),
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
            };
        }

        // Add GeoJSON layer
        L.geoJson(geoData, {style: style}).addTo(map);
    });
}

function weatherHeatMap(data)
{
    // Create the plot
    const chart = Plot.plot({
        padding: 0,
        y: { tickFormat: Plot.formatMonth("en", "short") },
        marks: [
            Plot.cell(seattle, Plot.group({ fill: "max" }, {
                x: d => d.date.getUTCDate(),
                y: d => d.date.getUTCMonth(),
                fill: "temp_max",
                inset: 0.5
            }))
        ]
    });

    // Append the plot to the div
    document.getElementById('plot').appendChild(chart);
}

function plotBarChart(xColumnName, yColumnName,title, xtitle, ytitle, elementId, data) {
    console.log("Data received:", data);
    console.log("Expected xColumnName:", xColumnName);
    console.log("Expected yColumnName:", yColumnName);
    
    // Check if data is valid
    if (!data || !Array.isArray(data)) {
        console.error("Invalid data format:", data);
        return;
    }

    const trace = {
        x: data.map(d => d[xColumnName]),
        y: data.map(d => d[yColumnName]),
        type: 'bar'
    };

    const layout = {
        title: title,
        xaxis: { title: xtitle },
        yaxis: { title: ytitle }
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



// Function to display the selected label
function displaySelectedLabelYear(text) {
    const selectedLabel = document.getElementById('yearLabel');
    selectedLabel.innerText = `Year : ${text}`;
    selectedLabel.style.display = 'block'; // Show the div
}

// Function to display the selected label
function displaySelectedLabelState(text) {
    const selectedLabel = document.getElementById('stateLabel');
    selectedLabel.innerText = `State : ${text}`;
    selectedLabel.style.display = 'block'; // Show the div
}



// Function to reload the page with URL parameters
function reloadPageWithParamsByYear() {
    const url = new URL(window.location.href);
    url.pathname = '/summary';
    $('#sectionToReloadByYear').load(url.toString()+ ' #sectionToReloadByYear', function() {
        // Your initialization code here
        initializeSection();
    });
}

// Function to reload the page with URL parameters
function reloadPageWithParamsByState() {
    const url = new URL(window.location.href);
    url.pathname = '/summary';
    $('#sectionToReloadByState').load(url.toString()+ ' #sectionToReloadByState', function() {
        // Your initialization code here
        initializeSection();
    });
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
                onClick: (e) => {
                    const points = myChart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);

                    if (points.length) {
                        const firstPoint = points[0];
                        const label = myChart.data.labels[firstPoint.index];
                        displaySelectedLabelYear(label);
                        displaySelectedLabelState("<ALL>");
                        const value = myChart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
                        // Update background colors
                       // Update background colors
                       myChart.data.datasets[0].backgroundColor = myChart.data.labels.map((l, i) =>
                        i === firstPoint.index ? 'rgba(75, 192, 192, 1)' : 'rgba(200, 200, 200, 0.2)'
                        );
                        myChart.update();
                        console.log(`Label: ${label}`);
                        console.log(`Value: ${value}`);
                        // Example usage
                        saveData('selectedYear', label);
                        console.log(`Selected Year: ${label}`);
                        reloadPageWithParamsByYear();
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
        const myChart2 = new Chart(ctx, {
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
            onClick: (e) => {
                if(getData('selectedYear'))
                {
                    const points = myChart2.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);

                    if (points.length) {
                        const firstPoint = points[0];
                        const label = myChart2.data.labels[firstPoint.index];
                        displaySelectedLabelState(label);
                        const value = myChart2.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
                        // Update background colors
                       // Update background colors
                       myChart2.data.datasets[0].backgroundColor = myChart2.data.labels.map((l, i) =>
                        i === firstPoint.index ? 'rgba(75, 192, 192, 1)' : 'rgba(200, 200, 200, 0.2)'
                        );
                        myChart2.update();
                        console.log(`Label: ${label}`);
                        console.log(`Value: ${value}`);
                        // Example usage
                        saveData('selectedState', label);
                        console.log(`Selected State: ${label}`);
                        reloadPageWithParamsByState();
                    }
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