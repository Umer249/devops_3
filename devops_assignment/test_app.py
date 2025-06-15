from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.quit()

    def test_home_page_title(self):
        self.assertEqual(self.driver.title, 'Flask Blog')

    def test_create_post(self):
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        self.driver.find_element(By.ID, 'title').send_keys('Test Post')
        self.driver.find_element(By.ID, 'content').send_keys('This is a test post.')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Test Post')))
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Test Post').is_displayed())

    def test_edit_post(self):
        self.driver.find_element(By.LINK_TEXT, 'Test Post').click()
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys('Updated Test Post')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Updated Test Post')))
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').is_displayed())

    def test_delete_post(self):
        self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').click()
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.LINK_TEXT, 'Updated Test Post')))
        self.assertFalse(self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').is_displayed())

if __name__ == '__main__':
    unittest.main() 