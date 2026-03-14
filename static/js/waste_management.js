// Waste Management JavaScript
let residueChart, compostProgressChart, revenueChart;
let currentRecipe = null;

// Load dashboard stats on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
    loadCompostBatches();
});

// Load dashboard statistics
function loadDashboardStats() {
    fetch('/api/waste/dashboard')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalResidue').textContent = data.total_residue_kg.toLocaleString();
            document.getElementById('activeCompost').textContent = data.active_compost_batches;
            document.getElementById('potentialRevenue').textContent = data.potential_revenue.toLocaleString();
            document.getElementById('carbonSaved').textContent = data.carbon_saved_tons;
        })
        .catch(error => console.error('Error loading dashboard:', error));
}

// Crop Residue Form
document.getElementById('residueForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const cropName = document.getElementById('cropName').value;
    const yieldKg = document.getElementById('yieldKg').value;
    
    fetch('/api/waste/residue/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({crop_name: cropName, yield_kg: yieldKg})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayManagementOptions(data);
            updateResidueChart(data);
            loadDashboardStats();
        }
    })
    .catch(error => console.error('Error:', error));
});

// Display management options
function displayManagementOptions(data) {
    const options = data.management_options;
    
    document.getElementById('residueAmount').textContent = data.residue_quantity;
    document.getElementById('compostOutput').textContent = options.composting.output_kg;
    document.getElementById('compostRevenue').textContent = options.composting.revenue.toLocaleString();
    document.getElementById('compostDays').textContent = options.composting.time_days;
    
    document.getElementById('biogasVolume').textContent = options.biogas.gas_volume_m3;
    document.getElementById('biogasSavings').textContent = options.biogas.savings.toLocaleString();
    
    document.getElementById('cattleRevenue').textContent = options.cattle_feed.revenue.toLocaleString();
    
    if (options.mushroom.applicable) {
        document.getElementById('mushroomYield').textContent = options.mushroom.mushroom_yield_kg;
        document.getElementById('mushroomRevenue').textContent = options.mushroom.revenue.toLocaleString();
        document.getElementById('mushroomApplicable').textContent = options.mushroom.time_days + ' days';
    } else {
        document.getElementById('mushroomApplicable').textContent = 'Not applicable';
        document.getElementById('mushroomRevenue').textContent = '0';
    }
    
    document.getElementById('carbonAmount').textContent = options.carbon_credits.co2_saved_tons;
    document.getElementById('carbonValue').textContent = options.carbon_credits.credit_value.toLocaleString();
    
    document.getElementById('managementOptions').style.display = 'block';
}

// Update residue chart
function updateResidueChart(data) {
    const ctx = document.getElementById('residueChart').getContext('2d');
    const options = data.management_options;
    
    if (residueChart) residueChart.destroy();
    
    residueChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Composting', 'Biogas', 'Cattle Feed', 'Mushroom'],
            datasets: [{
                data: [
                    options.composting.revenue,
                    options.biogas.savings,
                    options.cattle_feed.revenue,
                    options.mushroom.revenue
                ],
                backgroundColor: ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {position: 'bottom'},
                title: {display: true, text: 'Revenue by Method (₹)'}
            }
        }
    });
}

// Compost Recipe Form
document.getElementById('compostRecipeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const greenWaste = document.getElementById('greenWaste').value;
    const brownWaste = document.getElementById('brownWaste').value;
    const manure = document.getElementById('manure').value;
    
    fetch('/api/waste/compost/recipe', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            green_waste: greenWaste,
            brown_waste: brownWaste,
            manure: manure
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentRecipe = data.recipe;
            displayRecipeResult(data.recipe);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Display recipe result
function displayRecipeResult(recipe) {
    document.getElementById('cnRatio').textContent = recipe.current_cn_ratio;
    document.getElementById('recipeStatus').textContent = recipe.optimal ? '✓ Optimal' : '⚠ Needs Adjustment';
    document.getElementById('recipeStatus').className = recipe.optimal ? 'text-success' : 'text-warning';
    document.getElementById('recipeRecommendation').textContent = recipe.recommendation;
    document.getElementById('totalInput').textContent = recipe.total_input_kg;
    document.getElementById('expectedOutput').textContent = recipe.expected_output_kg;
    document.getElementById('fertilizerValue').textContent = recipe.fertilizer_value.toLocaleString();
    
    document.getElementById('recipeResult').style.display = 'block';
}

// Create compost batch
function createBatch() {
    if (!currentRecipe) {
        alert('Please calculate recipe first');
        return;
    }
    
    const batchName = prompt('Enter batch name:', 'Batch ' + new Date().toLocaleDateString());
    if (!batchName) return;
    
    const method = prompt('Select method (hot/cold/vermi):', 'hot');
    if (!method) return;
    
    fetch('/api/waste/compost/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            batch_name: batchName,
            method: method,
            start_date: new Date().toISOString().split('T')[0],
            total_weight: currentRecipe.total_input_kg,
            green_waste: document.getElementById('greenWaste').value,
            brown_waste: document.getElementById('brownWaste').value,
            manure: document.getElementById('manure').value
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Compost batch created successfully!');
            loadCompostBatches();
            loadDashboardStats();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Load compost batches
function loadCompostBatches() {
    fetch('/api/waste/compost/batches')
        .then(response => response.json())
        .then(batches => {
            const container = document.getElementById('compostBatches');
            
            if (batches.length === 0) {
                container.innerHTML = '<p class="text-muted">No active batches</p>';
                return;
            }
            
            container.innerHTML = batches.map(batch => `
                <div class="card mb-3">
                    <div class="card-body">
                        <h6>${batch.batch_name} <span class="badge bg-${batch.status === 'active' ? 'success' : 'secondary'}">${batch.status}</span></h6>
                        <p class="mb-2"><small>Method: ${batch.method} | Started: ${batch.start_date}</small></p>
                        <div class="progress mb-2" style="height: 25px;">
                            <div class="progress-bar bg-success" style="width: ${batch.progress}%">
                                ${batch.progress}%
                            </div>
                        </div>
                        <p class="mb-0"><small>
                            <i class="fas fa-clock"></i> ${batch.days_remaining} days remaining | 
                            <i class="fas fa-weight"></i> ${batch.expected_output} kg expected
                        </small></p>
                    </div>
                </div>
            `).join('');
            
            updateCompostProgressChart(batches);
        })
        .catch(error => console.error('Error:', error));
}

// Update compost progress chart
function updateCompostProgressChart(batches) {
    const ctx = document.getElementById('compostProgressChart').getContext('2d');
    
    if (compostProgressChart) compostProgressChart.destroy();
    
    compostProgressChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: batches.map(b => b.batch_name),
            datasets: [{
                label: 'Progress (%)',
                data: batches.map(b => b.progress),
                backgroundColor: '#28a745'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {beginAtZero: true, max: 100}
            }
        }
    });
}

// Vermicompost Form
document.getElementById('vermiForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const dailyWaste = document.getElementById('dailyWaste').value;
    
    fetch('/api/waste/vermicompost/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({waste_per_day: dailyWaste})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayVermiResult(data.requirements);
            updateRevenueChart(data.requirements);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Display vermicompost result
function displayVermiResult(req) {
    document.getElementById('wormsNeeded').textContent = req.worms_needed_kg;
    document.getElementById('wormCost').textContent = req.worm_cost.toLocaleString();
    document.getElementById('binArea').textContent = req.bin_area_sqft;
    document.getElementById('monthlyOutput').textContent = req.monthly_output_kg;
    document.getElementById('monthlyRevenue').textContent = req.monthly_revenue.toLocaleString();
    
    document.getElementById('vermiResult').style.display = 'block';
}

// Update revenue comparison chart
function updateRevenueChart(req) {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    
    if (revenueChart) revenueChart.destroy();
    
    revenueChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
            datasets: [{
                label: 'Revenue (₹)',
                data: Array(6).fill(req.monthly_revenue),
                backgroundColor: '#28a745'
            }, {
                label: 'Cumulative (₹)',
                data: Array(6).fill(0).map((_, i) => req.monthly_revenue * (i + 1)),
                backgroundColor: '#17a2b8',
                type: 'line'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {display: true, text: '6-Month Revenue Projection'}
            }
        }
    });
}
