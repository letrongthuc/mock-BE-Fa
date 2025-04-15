
# Hiển thị cây thư mục đến cấp 2 với màu
Get-ChildItem -Path . | ForEach-Object {
    if ($_.PsIsContainer) {
        Write-Host "+ $($_.Name)" -ForegroundColor Cyan
        Get-ChildItem -Path $_.FullName | ForEach-Object {
            Write-Host "   - $($_.Name)" -ForegroundColor DarkCyan
        }
    }
    else {
        Write-Host "* $($_.Name)" -ForegroundColor Yellow
    }
}
