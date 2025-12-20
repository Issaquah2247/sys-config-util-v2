# Mira Bot - Quick Install & Run Script
# One-line PowerShell installer that auto-starts the bot

Write-Host "========================================" -ForegroundColor Green
Write-Host "   MIRA BOT - QUICK INSTALLER" -ForegroundColor Green  
Write-Host "   Installing & Starting Bot..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "install.bat")) {
    Write-Host "Error: Please run this from the bot directory!" -ForegroundColor Red
    exit 1
}

# Run the installer in background
Write-Host "[1/2] Running installer..." -ForegroundColor Cyan
Start-Process -FilePath "install.bat" -Wait -WindowStyle Hidden

# Auto-start in background mode
Write-Host "[2/2] Starting bot in background..." -ForegroundColor Cyan
Write-Host ""
Start-Process -FilePath "run_background.bat" -WindowStyle Minimized

Write-Host "✅ Bot is now running in background!" -ForegroundColor Green
Write-Host "The bot will stay online as long as your PC is on." -ForegroundColor Yellow
Write-Host "" 
Write-Host "To stop the bot: Open Task Manager and end Python process" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
