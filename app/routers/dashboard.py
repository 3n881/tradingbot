from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Bot Performance Dashboard</h1>
        <canvas id="myChart" width="400" height="200"></canvas>
        <script>
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Activations', 'Executions', 'Buy', 'Sell', 'Hold'],
                    datasets: [{
                        label: 'Bot Actions',
                        data: [10, 20, 5, 3, 2],  // Replace with API data dynamically
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
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content
