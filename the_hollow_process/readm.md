## TryHackMe room The Hollow Process
### https://tryhackme.com/room/thehollowprocess
### YouTube video link https://youtu.be/T7hUWxWNchw

### commands used on the video:

```
.\kansa.ps1 -Target 10.129.140.119 -Credential $cred -Authentication Negotiate -ModulePath .\Modules -Verbose
```

```
Invoke-Command -ComputerName $target -Credential $cred -ScriptBlock {
    (Get-Item 'C:\Windows\Temp\svchost32.exe').VersionInfo |
        Select-Object OriginalFilename, InternalName, FileDescription, ProductName
}
```

### script used on the video:

```
.\Modules\Get-RegistryStartup.ps1
```
```
# OUTPUT csv

$paths = @(
    'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon'
    'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows'
    'HKLM:\SOFTWARE\Microsoft\Command Processor'
    'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        $key = Get-Item $path

        foreach ($name in $key.GetValueNames()) {
            [pscustomobject]@{
                Key       = $key.Name
                ValueName = $name
                ValueData = ($key.GetValue($name) -join '; ')
            }
        }
    }
}
```

```
.\kansa.ps1 -Target 10.129.140.119 -Credential $cred -Authentication Negotiate -ModulePath .\Modules\Get-RegistryStartup.ps1 -Verbose
```
