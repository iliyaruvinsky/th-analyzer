.\CLEANUP_WORKTREES.ps1
# Git Worktree Cleanup Script
# Removes all Cursor worktrees to fix workspace switching problem
#
# CRITICAL: Close Cursor before running this script!
# Cursor locks worktree files, preventing deletion

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Git Worktree Cleanup Script" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "WARNING: Close Cursor before running this script!" -ForegroundColor Red
Write-Host "Cursor locks worktree files, causing 'Permission denied' errors." -ForegroundColor Red
Write-Host ""
$confirm = Read-Host "Have you closed Cursor? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Please close Cursor and run this script again." -ForegroundColor Red
    exit
}

Write-Host "`nStarting worktree cleanup..." -ForegroundColor Yellow

# Go to main directory
Set-Location "C:\Users\USER\Desktop\tha-new"

# Step 1: Prune broken worktrees (removes ones with missing gitdir files)
Write-Host "`nStep 1: Pruning broken worktrees..." -ForegroundColor Cyan
git worktree prune
Write-Host "Prune complete." -ForegroundColor Green

# Step 2: Get list of remaining worktrees
Write-Host "`nStep 2: Listing remaining worktrees..." -ForegroundColor Cyan
$worktrees = git worktree list | Select-String -Pattern "\.cursor/worktrees" | ForEach-Object {
    if ($_ -match 'C:/Users/USER/\.cursor/worktrees/tha-new/(\w+)') {
        $matches[1]
    }
}

Write-Host "Found $($worktrees.Count) Cursor worktrees to remove" -ForegroundColor Yellow

# Step 3: Remove each Cursor worktree
Write-Host "`nStep 3: Removing Cursor worktrees..." -ForegroundColor Cyan
$removed = 0
$failed = 0

foreach ($wt in $worktrees) {
    $path = "C:\Users\USER\.cursor\worktrees\tha-new\$wt"
    Write-Host "  Removing: $wt" -NoNewline
    
    try {
        git worktree remove $path --force 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host " ✓" -ForegroundColor Green
            $removed++
        } else {
            Write-Host " ✗ (may be already broken)" -ForegroundColor Yellow
            $failed++
        }
    } catch {
        Write-Host " ✗ Error: $_" -ForegroundColor Red
        $failed++
    }
}

# Step 4: Final prune
Write-Host "`nStep 4: Final prune..." -ForegroundColor Cyan
git worktree prune

# Step 5: Verify
Write-Host "`nStep 5: Verifying cleanup..." -ForegroundColor Cyan
$final = git worktree list
Write-Host "`nFinal worktree list:" -ForegroundColor Cyan
$final

$remaining = ($final | Select-String -Pattern "\.cursor/worktrees").Count
if ($remaining -eq 0) {
    Write-Host "`n✓ SUCCESS: All Cursor worktrees removed!" -ForegroundColor Green
    Write-Host "Cursor will now use main directory only." -ForegroundColor Green
} else {
    Write-Host "`n⚠ WARNING: $remaining Cursor worktrees still remain" -ForegroundColor Yellow
    Write-Host "This usually means Cursor is still open and has files locked." -ForegroundColor Yellow
    Write-Host "`nOption 1: Close Cursor and run this script again" -ForegroundColor Cyan
    Write-Host "Option 2: Manually delete (if Cursor must stay open):" -ForegroundColor Cyan
    Write-Host "  Remove-Item -Recurse -Force 'C:\Users\USER\.cursor\worktrees\tha-new\*' -ErrorAction SilentlyContinue" -ForegroundColor Yellow
    Write-Host "  Remove-Item -Recurse -Force '.git\worktrees\*' -ErrorAction SilentlyContinue" -ForegroundColor Yellow
    Write-Host "  git worktree prune" -ForegroundColor Yellow
}

Write-Host "`nCleanup complete!" -ForegroundColor Green

