# PowerShell script to help process Excel data for roadmap visualization
# Run this script in PowerShell to get instructions for your roadmap data

Write-Host "🚀 Me@Sams Roadmap Setup Assistant" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if Excel file exists
$excelFile = "FY26_27 Me@Sams Roadmap data file.xlsx"
if (Test-Path $excelFile) {
    Write-Host "✅ Found Excel file: $excelFile" -ForegroundColor Green
} else {
    Write-Host "❌ Excel file not found: $excelFile" -ForegroundColor Red
    Write-Host "Available files:" -ForegroundColor Yellow
    Get-ChildItem -Filter "*.xlsx" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Yellow }
}

Write-Host ""
Write-Host "📋 Instructions to Create Your Visual Roadmap:" -ForegroundColor Green
Write-Host ""

Write-Host "Option 1: Interactive Web Dashboard (Recommended)" -ForegroundColor Yellow
Write-Host "1. Open 'interactive_roadmap.html' in your web browser (should have opened automatically)"
Write-Host "2. The dashboard has sample data loaded to show you how it works"
Write-Host "3. To use your data:"
Write-Host "   a. Export your Excel file to CSV format:"
Write-Host "      - Open Excel file"
Write-Host "      - File > Save As > CSV (Comma delimited)"
Write-Host "      - Save as 'roadmap_data.csv'"
Write-Host "   b. Click 'Upload Data' button in the dashboard"
Write-Host "   c. Select your CSV file"
Write-Host ""

Write-Host "Option 2: Manual CSV Creation" -ForegroundColor Yellow
Write-Host "1. Create a CSV file with these columns:"
Write-Host "   - Title (name of the initiative/feature)"
Write-Host "   - Quarter (format: 'FY26 Q1', 'FY26 Q2', etc.)"
Write-Host "   - Category (Technology, Operations, etc.)"
Write-Host "   - Status (Planning, In Progress, etc.)"
Write-Host "2. Upload to the interactive dashboard"
Write-Host ""

Write-Host "📊 Expected Data Format:" -ForegroundColor Magenta
Write-Host "Title,Quarter,Category,Status"
Write-Host "Mobile App Enhancement,FY26 Q1,Technology,In Progress"
Write-Host "Member Rewards Program,FY26 Q1,Member Experience,Planning"
Write-Host "Inventory Management System,FY26 Q2,Operations,Planning"
Write-Host ""

Write-Host "🎯 Dashboard Features:" -ForegroundColor Cyan
Write-Host "- Timeline View: Shows releases chronologically"
Write-Host "- Quarterly View: Groups releases by quarter"
Write-Host "- Gantt Chart: Shows duration and overlap"
Write-Host "- Filter by Category: Focus on specific areas"
Write-Host "- Summary Cards: Quick overview of your roadmap"
Write-Host ""

Write-Host "🔧 Troubleshooting:" -ForegroundColor Red
Write-Host "- Make sure your quarter format is 'FY26 Q1', 'FY26 Q2', etc."
Write-Host "- Ensure CSV file has headers in the first row"
Write-Host "- Check that dates are in the expected format"
Write-Host ""

Write-Host "✨ Pro Tips:" -ForegroundColor Green
Write-Host "- Use consistent category names for better visualization"
Write-Host "- Include priority or status information for richer data"
Write-Host "- The dashboard works entirely in your browser - no software installation needed!"
Write-Host ""

# Try to open the HTML file
Write-Host "🌐 Opening interactive dashboard..." -ForegroundColor Cyan
try {
    Start-Process "interactive_roadmap.html"
    Write-Host "✅ Dashboard opened in your default browser" -ForegroundColor Green
} catch {
    Write-Host "❌ Could not auto-open dashboard. Please manually open 'interactive_roadmap.html'" -ForegroundColor Red
}

Write-Host ""
Write-Host "📞 Need Help?" -ForegroundColor Yellow
Write-Host "The interactive dashboard includes:"
Write-Host "- Sample data to show you the format"
Write-Host "- File upload instructions"
Write-Host "- Multiple visualization options"
Write-Host "- Export capabilities for sharing"

Read-Host "Press Enter to continue"