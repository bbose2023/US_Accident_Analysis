// Example Call createGraph('bar', 'State', 'total_fatalities', sampleData);
function createGraph(graphType, xColumnName, yColumnName, data) {
    var ctx = document.getElementById('myChart').getContext('2d');

    var xData = data.map(item => item[xColumnName]);
    var yData = data.map(item => item[yColumnName]);

    var chartConfig = {
        type: graphType,
        data: {
            labels: xData,
            datasets: [{
                label: yColumnName,
                data: yData,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
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
    };

    var myChart = new Chart(ctx, chartConfig);
}

// Example Call createGraph('bar', 'State', ['total_fatalities', 'total_injuries','female'], sampleData);
function createGraph(graphType, xColumnName, yColumnNames, data) {
    var ctx = document.getElementById('myChart').getContext('2d');

    var xData = data.map(item => item[xColumnName]);
    var datasets = yColumnNames.map((col, index) => {
        return {
            label: col,
            data: data.map(item => item[col]),
            backgroundColor: `rgba(${255 - 50 * index}, 99, 132, 0.2)`,
            borderColor: `rgba(${255 - 50 * index}, 99, 132, 1)`,
            borderWidth: 1
        };
    });

    var chartConfig = {
        type: graphType,
        data: {
            labels: xData,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    var myChart = new Chart(ctx, chartConfig);
}

// Example Call createGraph('bar', 'State', ['total_fatalities', 'total_injuries','female'], sampleData);
function createStackedGraph(graphType, xColumnName, yColumnNames, data) {
    var ctx = document.getElementById('myChart').getContext('2d');

    var xData = data.map(item => item[xColumnName]);
    var datasets = yColumnNames.map((col, index) => {
        return {
            label: col,
            data: data.map(item => item[col]),
            backgroundColor: `rgba(${255 - 50 * index}, 99, 132, 0.2)`,
            borderColor: `rgba(${255 - 50 * index}, 99, 132, 1)`,
            borderWidth: 1
        };
    });

    var chartConfig = {
        type: graphType,
        data: {
            labels: xData,
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true
                }
            }
        }
    };

    var myChart = new Chart(ctx, chartConfig);
}
