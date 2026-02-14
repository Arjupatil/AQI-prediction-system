let latestInputData = null;
let pollutantChart = null;
let trendChart = null;

// Populate cities on load
document.addEventListener('DOMContentLoaded', async () => {
    console.log("Loading cities...");
    const citySelect = document.getElementById('city');
    try {
        const response = await fetch('/cities');
        if (!response.ok) throw new Error('Failed to fetch cities: ' + response.statusText);
        const cities = await response.json();
        console.log("Cities received:", cities);

        // Remove existing options except the first one
        while (citySelect.options.length > 1) {
            citySelect.remove(1);
        }

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });

        // Default to Ahmedabad if present
        if (cities.includes('Ahmedabad')) {
            citySelect.value = 'Ahmedabad';
        }
    } catch (error) {
        console.error('Error fetching cities:', error);
        // Fallback cities if fetch fails
        const fallbacks = ["Ahmedabad", "Bengaluru", "Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"];
        fallbacks.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
        citySelect.value = "Ahmedabad";
    }
});

document.getElementById('aqiForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const btn = document.getElementById('predictBtn');
    const resultCard = document.getElementById('result');
    const scoreEl = document.getElementById('aqiScore');
    const catEl = document.getElementById('aqiCategory');

    // UI Loading State
    btn.classList.add('loading');
    btn.disabled = true;
    resultCard.classList.add('hidden');
    document.getElementById('visualizationSection').classList.add('hidden');

    // Gather Data
    const data = {
        city: document.getElementById('city').value,
        pm2_5: parseFloat(document.getElementById('pm2_5').value),
        pm10: parseFloat(document.getElementById('pm10').value),
        no2: parseFloat(document.getElementById('no2').value),
        so2: parseFloat(document.getElementById('so2').value),
        co: parseFloat(document.getElementById('co').value),
        o3: parseFloat(document.getElementById('o3').value)
    };
    latestInputData = data;

    try {
        // Call Backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const result = await response.json();

        // Update UI
        scoreEl.textContent = Math.round(result.aqi);
        catEl.textContent = result.category;

        // Dynamic Colors
        const catClass = `cat-${result.category.replace(' ', '-')}`;
        scoreEl.className = `score ${catClass}`;
        catEl.className = `category ${catClass} bg-opacity-20`;

        resultCard.classList.remove('hidden');
        document.getElementById('visualizationSection').classList.remove('hidden');
        await renderCharts();

    } catch (error) {
        alert("Failed to get prediction. Ensure the backend is running.\n\n" + error.message);
        console.error(error);
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
});


async function renderCharts() {
    // Global Chart Configuration for Theme
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.scale.grid.color = 'rgba(148, 163, 184, 0.1)';

    // 1. Pollutant Breakdown Chart
    const ctx1 = document.getElementById('pollutantChart').getContext('2d');
    if (pollutantChart) pollutantChart.destroy();

    pollutantChart = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'],
            datasets: [{
                label: 'Concentration (µg/m³)',
                data: [
                    latestInputData.pm2_5,
                    latestInputData.pm10,
                    latestInputData.no2,
                    latestInputData.so2,
                    latestInputData.co,
                    latestInputData.o3
                ],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // 2. Trend Chart (Fetch History)
    const ctx2 = document.getElementById('trendChart').getContext('2d');
    if (trendChart) trendChart.destroy();

    try {
        const response = await fetch('/history');
        const history = await response.json();

        // Reverse to show oldest to newest left to right if needed, but backend sends newest first.
        // Let's re-reverse here for the chart to go left->right (old->new)
        // Backend: `last_20 = df.tail(20).iloc[::-1]` -> Returns Newest First.
        // For line chart, we usually want time going left (old) to right (new).
        // So we reverse it back.
        const chartData = history.reverse();

        trendChart = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: chartData.map(d => d.Date), // Maybe truncate date?
                datasets: [{
                    label: 'AQI History',
                    data: chartData.map(d => d.AQI),
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.1)' } },
                    x: { grid: { display: false } }
                }
            }
        });

    } catch (e) {
        console.error("Error loading history chart", e);
    }
}

