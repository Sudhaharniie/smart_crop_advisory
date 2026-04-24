// FIXED: Charts with proper dates, dark mode colors, and better visibility
function initializeCharts(force = false) {
    console.log('🎨 Initializing charts with fixes...');
    const isDark = document.body.classList.contains('theme-dark') || document.body.classList.contains('dark-mode');

    // Enhanced Chart.js defaults for both light and dark mode
    Chart.defaults.font.family = 'Inter, Arial, sans-serif';
    Chart.defaults.font.size = 16;
    Chart.defaults.color = isDark ? '#e5e7eb' : '#1f2937';
    Chart.defaults.animation = { duration: 900, easing: 'easeOutQuart' };

    // Better color palette for dark mode visibility
    const palette = {
        grid: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
        text: isDark ? '#e5e7eb' : '#1f2937',
        // Vibrant colors visible in both modes
        colors: {
            green: isDark ? '#4ade80' : '#22c55e',
            blue: isDark ? '#60a5fa' : '#3b82f6',
            yellow: isDark ? '#fbbf24' : '#f59e0b',
            purple: isDark ? '#a78bfa' : '#8b5cf6',
            red: isDark ? '#f87171' : '#ef4444',
            cyan: isDark ? '#22d3ee' : '#06b6d4',
            orange: isDark ? '#fb923c' : '#f97316'
        }
    };

    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    usePointStyle: true,
                    pointStyle: 'circle',
                    boxWidth: 12,
                    padding: 24,
                    font: { size: 17, weight: '600' },
                    color: palette.text
                }
            },
            tooltip: {
                backgroundColor: isDark ? 'rgba(30,30,30,0.95)' : 'rgba(0,0,0,0.85)',
                padding: 16,
                cornerRadius: 10,
                titleFont: { size: 17, weight: '700' },
                bodyFont: { size: 16 },
                titleColor: '#ffffff',
                bodyColor: '#ffffff',
                borderColor: isDark ? palette.colors.blue : palette.colors.green,
                borderWidth: 2
            }
        },
        scales: {
            x: {
                grid: { 
                    color: palette.grid, 
                    drawBorder: false,
                    lineWidth: 1
                },
                ticks: { 
                    font: { size: 14, weight: '600' }, 
                    color: palette.text,
                    maxRotation: 45,
                    minRotation: 0
                }
            },
            y: {
                grid: { 
                    color: palette.grid, 
                    drawBorder: false,
                    lineWidth: 1
                },
                ticks: { 
                    font: { size: 14, weight: '600' }, 
                    color: palette.text 
                }
            }
        }
    };

    const gradient = (ctx, a, b) => {
        const g = ctx.createLinearGradient(0, 0, 0, 320);
        g.addColorStop(0, a);
        g.addColorStop(1, b);
        return g;
    };

    const charts = {
        weatherOverviewChart: (ctx) => ({
            type: 'bar',
            data: {
                labels: ['Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)'],
                datasets: [{
                    label: 'Current Weather',
                    data: [chartData.weather.temperature, chartData.weather.humidity, chartData.weather.rainfall],
                    backgroundColor: [
                        palette.colors.red,
                        palette.colors.cyan,
                        palette.colors.blue
                    ],
                    borderColor: [
                        palette.colors.red,
                        palette.colors.cyan,
                        palette.colors.blue
                    ],
                    borderWidth: 2,
                    borderRadius: 12,
                    borderSkipped: false,
                    maxBarThickness: 60
                }]
            },
            options: {
                ...baseOptions,
                scales: { ...baseOptions.scales, y: { ...baseOptions.scales.y, beginAtZero: true } }
            }
        }),

        soilNutrientsChart: () => ({
            type: 'doughnut',
            data: {
                labels: ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
                datasets: [{
                    data: chartData.soil,
                    backgroundColor: [
                        palette.colors.green,
                        palette.colors.yellow,
                        palette.colors.blue
                    ],
                    borderColor: isDark ? '#1f2937' : '#ffffff',
                    borderWidth: 4,
                    hoverOffset: 15,
                    hoverBorderWidth: 6
                }]
            },
            options: {
                ...baseOptions,
                cutout: '60%',
                plugins: { 
                    ...baseOptions.plugins, 
                    legend: { 
                        ...baseOptions.plugins.legend, 
                        position: 'bottom',
                        labels: {
                            ...baseOptions.plugins.legend.labels,
                            padding: 20,
                            font: { size: 15, weight: '600' }
                        }
                    }
                }
            }
        }),

        weatherChart: (ctx) => {
            // Generate actual dates for next 7 days
            const today = new Date();
            const dateLabels = [];
            for (let i = 0; i < 7; i++) {
                const date = new Date(today);
                date.setDate(today.getDate() + i);
                const month = date.toLocaleString('en-US', { month: 'short' });
                const day = date.getDate();
                dateLabels.push(`${month} ${day}`);
            }
            
            const tempData = Array.isArray(chartData.forecast) && chartData.forecast.length > 0
                ? chartData.forecast.map(item => typeof item === 'object' ? item.temp : item)
                : [25, 26, 24, 27, 25, 26, 25];

            return {
                type: 'line',
                data: {
                    labels: dateLabels,
                    datasets: [{
                        label: 'Temperature (°C)',
                        data: tempData,
                        borderColor: palette.colors.green,
                        backgroundColor: gradient(ctx, 
                            isDark ? 'rgba(74,222,128,0.3)' : 'rgba(34,197,94,0.3)', 
                            'rgba(34,197,94,0.05)'
                        ),
                        fill: true,
                        tension: 0.4,
                        pointRadius: 7,
                        pointHoverRadius: 10,
                        pointBackgroundColor: palette.colors.green,
                        pointBorderColor: isDark ? '#1f2937' : '#ffffff',
                        pointBorderWidth: 3,
                        borderWidth: 4
                    }]
                },
                options: {
                    ...baseOptions,
                    scales: { 
                        ...baseOptions.scales, 
                        y: { 
                            ...baseOptions.scales.y, 
                            beginAtZero: false,
                            min: Math.min(...tempData) - 5,
                            max: Math.max(...tempData) + 5
                        } 
                    }
                }
            };
        },

        soilChart: (ctx) => ({
            type: 'bar',
            data: {
                labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'pH x10', 'Moisture'],
                datasets: [{
                    label: 'Soil Parameters',
                    data: [
                        soilData.nitrogen, 
                        soilData.phosphorus, 
                        soilData.potassium / 2, 
                        soilData.ph * 10, 
                        soilData.moisture
                    ],
                    backgroundColor: [
                        palette.colors.green,
                        palette.colors.yellow,
                        palette.colors.blue,
                        palette.colors.purple,
                        palette.colors.cyan
                    ],
                    borderColor: [
                        palette.colors.green,
                        palette.colors.yellow,
                        palette.colors.blue,
                        palette.colors.purple,
                        palette.colors.cyan
                    ],
                    borderWidth: 2,
                    borderRadius: 12,
                    maxBarThickness: 50,
                    borderSkipped: false
                }]
            },
            options: {
                ...baseOptions,
                scales: { ...baseOptions.scales, y: { ...baseOptions.scales.y, beginAtZero: true } }
            }
        }),

        sustainabilityChart: (ctx) => ({
            type: 'bar',
            data: {
                labels: ['Soil Health', 'Water Efficiency', 'Organic Usage', 'Biodiversity'],
                datasets: [{
                    label: 'Score (%)',
                    data: [
                        chartData.sustainability.soil_health,
                        chartData.sustainability.water_efficiency,
                        chartData.sustainability.organic_usage,
                        chartData.sustainability.biodiversity
                    ],
                    backgroundColor: [
                        palette.colors.green,
                        palette.colors.cyan,
                        palette.colors.yellow,
                        palette.colors.purple
                    ],
                    borderRadius: 8,
                    maxBarThickness: 50
                }]
            },
            options: {
                ...baseOptions,
                scales: {
                    x: { ...baseOptions.scales.x },
                    y: { 
                        ...baseOptions.scales.y, 
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        }),

        marketTrendsChart: (ctx) => {
            if (!Array.isArray(chartData.market_trends) || chartData.market_trends.length === 0) {
                console.warn('⚠️ No market trends data');
                return null;
            }
            
            const labels = (typeof marketLabels !== 'undefined' && Array.isArray(marketLabels) && marketLabels.length > 0)
                ? marketLabels.slice(0, chartData.market_trends.length).map(name => 
                    name.charAt(0).toUpperCase() + name.slice(1)
                )
                : chartData.market_trends.map((_, i) => `Crop ${i + 1}`);
            
            const values = chartData.market_trends.map(item => item.current_price || 0);

            return {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Price (₹/quintal)',
                        data: values,
                        backgroundColor: [
                            palette.colors.green,
                            palette.colors.blue,
                            palette.colors.purple,
                            palette.colors.cyan,
                            palette.colors.yellow,
                            palette.colors.orange
                        ],
                        borderColor: [
                            palette.colors.green,
                            palette.colors.blue,
                            palette.colors.purple,
                            palette.colors.cyan,
                            palette.colors.yellow,
                            palette.colors.orange
                        ],
                        borderWidth: 2,
                        borderRadius: 12,
                        maxBarThickness: 55,
                        borderSkipped: false
                    }]
                },
                options: {
                    ...baseOptions,
                    scales: { ...baseOptions.scales, y: { ...baseOptions.scales.y, beginAtZero: true } }
                }
            };
        },

        profitComparisonChart: (ctx) => {
            const crops = Array.isArray(chartData.top_crops) && chartData.top_crops.length > 0
                ? chartData.top_crops
                : [
                    { name: 'Crop 1', profit: chartData.profit || 50000 },
                    { name: 'Crop 2', profit: (chartData.profit || 50000) * 0.85 },
                    { name: 'Crop 3', profit: (chartData.profit || 50000) * 0.7 }
                ];

            const labels = crops.map(c => (c.name || 'Crop').toString().toUpperCase());
            const profits = crops.map(c => Math.abs(Math.round(c.profit || 0)));

            return {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Estimated Profit (₹)',
                        data: profits,
                        backgroundColor: [
                            palette.colors.green,
                            palette.colors.blue,
                            palette.colors.orange
                        ],
                        borderRadius: 10,
                        maxBarThickness: 70
                    }]
                },
                options: {
                    ...baseOptions,
                    scales: {
                        x: { ...baseOptions.scales.x },
                        y: {
                            ...baseOptions.scales.y,
                            beginAtZero: true,
                            ticks: {
                                ...baseOptions.scales.y.ticks,
                                callback: function(value) {
                                    return value >= 1000 ? (value / 1000).toFixed(0) + 'K' : value;
                                }
                            }
                        }
                    }
                }
            };
        }
    };

    const rendered = new Set();

    const buildChart = (canvas) => {
        if (!canvas || rendered.has(canvas.id)) return;
        console.log('📊 Building chart:', canvas.id);
        const builder = charts[canvas.id];
        if (!builder) {
            console.warn('⚠️ No builder for:', canvas.id);
            return;
        }

        const ctx = canvas.getContext('2d');
        const config = builder(ctx);
        if (!config) {
            canvas.closest('.chart-panel')?.classList.add('ready');
            rendered.add(canvas.id);
            return;
        }

        try {
            new Chart(ctx, config);
            canvas.style.display = 'block';
            canvas.style.visibility = 'visible';
            canvas.closest('.chart-panel')?.classList.add('ready');
            rendered.add(canvas.id);
            console.log('✅ Chart rendered:', canvas.id);
        } catch (error) {
            console.error('❌ Chart error:', canvas.id, error);
        }
    };

    const canvases = Array.from(document.querySelectorAll('canvas[data-chart="true"]'));

    if (force || !('IntersectionObserver' in window)) {
        canvases.forEach(buildChart);
        return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                buildChart(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { rootMargin: '150px 0px', threshold: 0.01 });

    canvases.forEach((canvas) => observer.observe(canvas));
}

// Re-render charts when theme changes
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            setTimeout(() => {
                // Clear all charts and re-render
                document.querySelectorAll('canvas[data-chart="true"]').forEach(canvas => {
                    const chart = Chart.getChart(canvas);
                    if (chart) {
                        chart.destroy();
                    }
                });
                initializeCharts(true);
            }, 100);
        });
    }
});
