from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5000"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


# Test - is homepage accessible
def test_access_homepage():
    driver.get(BASE_URL)
    page_title = driver.title

    assert page_title == "QA Shop", f"Actual page title '{page_title}'"


# Test - is login page accessible
def test_access_login():
    login_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
    )
    login_link.click()

    header_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    header_text = header_element.text

    assert header_text == "Login", f"Actual header '{header_text}'"


# Test - can user login
def test_can_user_login():
    username_field = wait.until(
        EC.element_to_be_clickable((By.NAME, "username"))
    )
    password_field = wait.until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )

    username_field.clear()
    username_field.send_keys("alice")
    password_field.clear()
    password_field.send_keys("Password123!")

    button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
    )
    button.click()

    logout_link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout']"))
    )

    logout_text = logout_link.get_attribute("innerHTML")
    assert "Logout" in logout_text, f"Actual span text '{logout_text}'"


# Test - can user logout
def test_can_user_logout():
    logout_link = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    )
    logout_link.click()

    login = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login']"))
    )

    login_text = login.get_attribute("innerHTML")
    assert "Login" in login_text, f"Actual span text '{login_text}'"
