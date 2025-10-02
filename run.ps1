# SwiftLogix Quick Start Script
# Run this from the swiftlogix directory

try {
    # Check if virtual environment exists
    $venvPath = "..\.venv\Scripts\python.exe"
    if (-not (Test-Path $venvPath)) {
        Write-Host "Virtual environment not found at $venvPath" -ForegroundColor Red
        Write-Host "Please create a virtual environment in the parent directory:" -ForegroundColor Yellow
        Write-Host "  python -m venv ..\.venv" -ForegroundColor White
        exit 1
    }

    Write-Host "Starting SwiftLogix..." -ForegroundColor Green
    Write-Host "Access the app at: http://127.0.0.1:5000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available pages:" -ForegroundColor Yellow
    Write-Host "  - Home: http://127.0.0.1:5000/" -ForegroundColor White
    Write-Host "  - Login: http://127.0.0.1:5000/login" -ForegroundColor White
    Write-Host "  - Register: http://127.0.0.1:5000/register" -ForegroundColor White
    Write-Host "  - Customer: http://127.0.0.1:5000/customer" -ForegroundColor White
    Write-Host "  - Driver: http://127.0.0.1:5000/driver" -ForegroundColor White
    Write-Host "  - Admin: http://127.0.0.1:5000/admin" -ForegroundColor White
    Write-Host ""
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""

    # Run the Flask application using our custom script
    & $venvPath "D:\coding python\swiftlogix\run_app.py"
}
catch {
    Write-Host "Error starting SwiftLogix:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Please check that all dependencies are installed and the database is accessible." -ForegroundColor Yellow
    pause
}