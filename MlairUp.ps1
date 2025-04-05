# Run Jekyll Build
# Run RemoveHtmlExtension
# Run rsync command (while showing log in command-line)

# Stop on error
$ErrorActionPreference = "Stop"


# ---- TASKS ----

Write-Host "Running jJekyll build ..." -ForegroundColor Cyan
bundle exec jekyll build

Write-Host "`nRunning RemoveHtmlExtension.py ..." -ForegroundColor Cyan
py .\RemoveHtmlExtensionFromOutputFiles.py

Write-Host "`nUploading to Mlair via rsync ..." -ForegroundColor Cyan
wsl rsync --delete -avz "/mnt/d/M/Projects/Personal Website/manuellamas.github.io/docs/" m@vultrMlair:/var/www/htdocs

Write-Host "`nProcess completed!" -ForegroundColor Green

# ---- TASKS END ----
