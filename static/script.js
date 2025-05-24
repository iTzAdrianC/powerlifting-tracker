document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos al iniciar
    loadLifts();
    
    // Manejar el formulario
    document.getElementById('liftingForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const liftData = {
            name: document.getElementById('name').value,
            bodyWeight: parseFloat(document.getElementById('bodyWeight').value),
            squat: parseFloat(document.getElementById('squat').value),
            bench: parseFloat(document.getElementById('bench').value),
            deadlift: parseFloat(document.getElementById('deadlift').value)
        };
        
        fetch('/api/lifts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(liftData)
        })
        .then(response => response.json())
        .then(data => {
            loadLifts();
            document.getElementById('liftingForm').reset();
        })
        .catch(error => console.error('Error:', error));
    });
    
    // Manejar filtro de categoría
    document.getElementById('categoryFilter').addEventListener('change', function() {
        loadLifts(this.value);
    });
});

function loadLifts(category = 'all') {
    let url = '/api/lifts';
    if (category !== 'all') {
        url += `?category=${category}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('resultsTable');
            tableBody.innerHTML = '';
            
            data.forEach(lift => {
                const total = lift.squat + lift.bench + lift.deadlift;
                const row = document.createElement('tr');
                
                row.innerHTML = `
                    <td>${lift.name}</td>
                    <td>${lift.weight_category}</td>
                    <td>${lift.body_weight}</td>
                    <td>${lift.squat}</td>
                    <td>${lift.bench}</td>
                    <td>${lift.deadlift}</td>
                    <td>${total}</td>
                `;
                
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

function determineCategory(bodyWeight) {
    if (bodyWeight < 60) return "-60kg";
    if (bodyWeight < 70) return "60-70kg";
    if (bodyWeight < 80) return "70-80kg";
    if (bodyWeight < 90) return "80-90kg";
    if (bodyWeight < 100) return "90-100kg";
    return "+100kg";
}