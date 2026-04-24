function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) {
        console.log(message);
        return;
    }

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-bg-' + type + ' border-0';
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastEl);
    const toast = new bootstrap.Toast(toastEl, { delay: 2800 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// Expense Form
document.getElementById('expenseForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        type: document.getElementById('transactionType').value,
        description: document.getElementById('description').value,
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value
    };

    fetch('/api/add_expense', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(data => {
        if(data.success) {
            showToast('Transaction added successfully', 'success');
            setTimeout(() => location.reload(), 700);
        }
    });
});

// Pest Detection Form
document.getElementById('pestDetectionForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('image', document.getElementById('cropImage').files[0]);

    fetch('/api/pest_detection', {
        method: 'POST',
        body: formData
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('detectionResult').innerHTML = `
            <div class="alert alert-${data.severity === 'high' ? 'danger' : 'warning'}">
                <h6>${data.disease}</h6>
                <p>Confidence: ${data.confidence}%</p>
                <p>${data.treatment}</p>
            </div>
        `;
        showToast('Analysis completed', 'info');
    });
});

// Chatbot
function sendChat() {
    const input = document.getElementById('chatInput');
    const question = input.value;
    if(!question) return;

    document.getElementById('chatMessages').innerHTML += `
        <div class="alert alert-secondary"><strong>You:</strong> ${question}</div>
    `;

    fetch('/api/chatbot', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question})
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('chatMessages').innerHTML += `
            <div class="alert alert-info"><strong>AI:</strong> ${data.response}</div>
        `;
        input.value = '';
    });
}

// Marketplace functions
function contactSeller(id, title) {
    showToast(`Contact seller for: ${title}`, 'info');
}

function postNewListing() {
    showToast('Post new listing feature', 'primary');
}

// Loan & Insurance
function applyForLoan() {
    showToast('Loan application feature', 'success');
}

function getInsuranceQuote(plan) {
    showToast(`Get quote for: ${plan}`, 'info');
}

// Video Library
function watchVideo(id, title) {
    // Create modal for video playback
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'videoModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="ratio ratio-16x9">
                        <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
                                title="${title}" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                allowfullscreen>
                        </iframe>
                    </div>
                    <div class="mt-3">
                        <p class="text-muted">This is a demo video. In production, this would load the actual educational content.</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.addEventListener('hidden.bs.modal', () => {
        modal.remove();
    });
}

function viewAllVideos() {
    showToast('Loading video library...', 'info');
    // In production, this would navigate to a dedicated video library page
    setTimeout(() => {
        showToast('Video library feature - Navigate to dedicated page', 'success');
    }, 500);
}

// SMS Alerts
function saveAlertSettings() {
    showToast('Alert settings saved', 'info');
}

// Documentation
function openDocumentation(type) {
    showToast(`Open documentation: ${type}`, 'secondary');
}
