window.chartInstances = {};

window.updateUrl = function (newUrl) {
    window.history.replaceState(null, "", newUrl);
};

window.loadDriverStandingsChart = (driverNames, driverPoints) => {
    var ctx = document.getElementById('driverStandingsChart').getContext('2d');

    // Check if there is an existing chart instance and destroy it
    if (window.chartInstances['driverStandingsChart']) {
        window.chartInstances['driverStandingsChart'].destroy();
    }

    // Create a new chart instance
    window.chartInstances['driverStandingsChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: driverNames,
            datasets: [{
                label: 'Driver Points',
                data: driverPoints,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


const predefinedColors = [
    '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC'
];

window.chartInstances = window.chartInstances || {};

window.loadWholeSeasonChart = (raceNames, driverNames, pointsForRaces) => {
    var ctx = document.getElementById('wholeSeasonChart').getContext('2d');

    // Check if there is an existing chart instance and destroy it
    if (window.chartInstances['wholeSeasonChart']) {
        window.chartInstances['wholeSeasonChart'].destroy();
    }

    // Prepare the datasets
    var datasets = driverNames.map((driverName, index) => {
        return {
            label: driverName,
            data: pointsForRaces.map(row => row[index]),
            fill: false,
            borderColor: predefinedColors[index % predefinedColors.length],
            tension: 0.1
        };
    });

    // Create a new chart instance
    window.chartInstances['wholeSeasonChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: raceNames,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    type: 'log2'
                }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        enabled: true,
                        mode: 'xy',
                    }
                }
            }
        }
        
    });
}

window.loadWholeSeasonResultsChart = (raceNames, driverNames, pointsForRaces) => {
    var ctx = document.getElementById('wholeSeasonChart').getContext('2d');

    // Check if there is an existing chart instance and destroy it
    if (window.chartInstances['wholeSeasonChart']) {
        window.chartInstances['wholeSeasonChart'].destroy();
    }

    // Prepare the datasets
    var datasets = driverNames.map((driverName, index) => {
        return {
            label: driverName,
            data: pointsForRaces.map(row => row[index]),
            fill: false,
            borderColor: predefinedColors[index % predefinedColors.length],
            tension: 0
        };
    });

    // Create a new chart instance
    window.chartInstances['wholeSeasonChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: raceNames,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    type: 'linear'
                }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        enabled: true,
                        mode: 'x',
                    }
                }
            }
        }

    });
}

window.loadLapTimesChart = (driverNames, lapTimesForDrivers, laps) => {
    var ctx = document.getElementById('lapTimesChart').getContext('2d');

    // Check if there is an existing chart instance and destroy it
    if (window.chartInstances['lapTimesChart']) {
        window.chartInstances['lapTimesChart'].destroy();
    }

    // Prepare the datasets
    var datasets = driverNames.map((driverName, index) => {
        // Sample data if necessary
        return {
            label: driverName,
            data: lapTimesForDrivers[index],
            fill: false,
            borderColor: predefinedColors[index % predefinedColors.length],
            tension: 0.1
        };
    });

    // Create a new chart instance
    window.chartInstances['lapTimesChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: laps,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {  
                y: {
                    beginAtZero: true,
                    type: 'log2',
                }
            },
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x'
                    },
                    zoom: {
                        enabled: true,
                        mode: 'x',
                    }
                }
            }
        }
    });
};



function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

