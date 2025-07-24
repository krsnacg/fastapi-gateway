from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..core.logging import request_logger

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gateway Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background-color: #f5f5f5; 
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background-color: white; 
                padding: 20px; 
                border-radius: 8px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            }
            h1 { 
                color: #333; 
                text-align: center; 
                margin-bottom: 30px; 
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-bottom: 30px; 
            }
            .stat-card { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center; 
            }
            .stat-number { 
                font-size: 2em; 
                font-weight: bold; 
            }
            .logs-table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 20px; 
            }
            .logs-table th, .logs-table td { 
                border: 1px solid #ddd; 
                padding: 8px; 
                text-align: left; 
            }
            .logs-table th { 
                background-color: #f2f2f2; 
                font-weight: bold; 
            }
            .logs-table tr:nth-child(even) { 
                background-color: #f9f9f9; 
            }
            .status-200 { color: #28a745; font-weight: bold; }
            .status-400 { color: #ffc107; font-weight: bold; }
            .status-500 { color: #dc3545; font-weight: bold; }
            .refresh-btn { 
                background-color: #007bff; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 4px; 
                cursor: pointer; 
                margin-bottom: 20px; 
            }
            .refresh-btn:hover { 
                background-color: #0056b3; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚪 Gateway Dashboard</h1>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
            
            <div class="stats" id="stats">
                <!-- Stats will be loaded here -->
            </div>
            
            <table class="logs-table" id="logsTable">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Method</th>
                        <th>Path</th>
                        <th>Status</th>
                        <th>Duration (s)</th>
                        <th>Client IP</th>
                    </tr>
                </thead>
                <tbody id="logsBody">
                    <!-- Logs will be loaded here -->
                </tbody>
            </table>
        </div>

        <script>
            async function loadLogs() {
                try {
                    const response = await fetch('/api/logs');
                    const logs = await response.json();
                    
                    // Update stats
                    const totalRequests = logs.length;
                    const successfulRequests = logs.filter(log => log.status_code < 400).length;
                    const avgDuration = logs.length > 0 ? 
                        (logs.reduce((sum, log) => sum + log.duration, 0) / logs.length).toFixed(4) : 0;
                    
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-number">${totalRequests}</div>
                            <div>Total Requests</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${successfulRequests}</div>
                            <div>Successful</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">${avgDuration}s</div>
                            <div>Avg Duration</div>
                        </div>
                    `;
                    
                    // Update logs table
                    const tbody = document.getElementById('logsBody');
                    tbody.innerHTML = logs.slice(-50).reverse().map(log => {
                        const statusClass = log.status_code < 300 ? 'status-200' : 
                                          log.status_code < 500 ? 'status-400' : 'status-500';
                        return `
                            <tr>
                                <td>${new Date(log.timestamp).toLocaleString()}</td>
                                <td><strong>${log.method}</strong></td>
                                <td>${log.path}</td>
                                <td class="${statusClass}">${log.status_code}</td>
                                <td>${log.duration}</td>
                                <td>${log.client_ip}</td>
                            </tr>
                        `;
                    }).join('');
                    
                } catch (error) {
                    console.error('Error loading logs:', error);
                }
            }
            
            // Load logs on page load
            loadLogs();
            
            // Auto-refresh every 10 seconds
            setInterval(loadLogs, 10000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/api/logs")
async def get_logs():
    return request_logger.get_logs()

@router.get("/api/stats")
async def get_stats():
    logs = request_logger.get_logs()
    if not logs:
        return {"total_requests": 0, "successful_requests": 0, "avg_duration": 0}
    
    total_requests = len(logs)
    successful_requests = len([log for log in logs if log["status_code"] < 400])
    avg_duration = sum(log["duration"] for log in logs) / total_requests
    
    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "avg_duration": round(avg_duration, 4)
    }