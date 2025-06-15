from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import unittest
import time

class FlaskAppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        self.driver.quit()

    def test_1_home_page_title(self):
        """Test if the home page title is correct"""
        self.assertEqual(self.driver.title, 'Flask Blog')

    def test_2_create_post_button_exists(self):
        """Test if the create post button is present"""
        create_button = self.driver.find_element(By.LINK_TEXT, 'Create New Post')
        self.assertTrue(create_button.is_displayed())

    def test_3_create_post_form_fields(self):
        """Test if create post form has required fields"""
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        title_field = self.driver.find_element(By.ID, 'title')
        content_field = self.driver.find_element(By.ID, 'content')
        self.assertTrue(title_field.is_displayed())
        self.assertTrue(content_field.is_displayed())

    def test_4_create_post_validation(self):
        """Test post creation validation"""
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertIn('Title is required!', self.driver.page_source)

    def test_5_create_post_success(self):
        """Test successful post creation"""
        self.driver.find_element(By.LINK_TEXT, 'Create New Post').click()
        self.driver.find_element(By.ID, 'title').send_keys('Test Post')
        self.driver.find_element(By.ID, 'content').send_keys('This is a test post.')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Test Post')))
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Test Post').is_displayed())

    def test_6_edit_post_button_exists(self):
        """Test if edit button exists for posts"""
        self.driver.find_element(By.LINK_TEXT, 'Test Post').click()
        edit_button = self.driver.find_element(By.LINK_TEXT, 'Edit')
        self.assertTrue(edit_button.is_displayed())

    def test_7_edit_post_form_prefilled(self):
        """Test if edit form is prefilled with post data"""
        self.driver.find_element(By.LINK_TEXT, 'Test Post').click()
        title_field = self.driver.find_element(By.ID, 'title')
        self.assertEqual(title_field.get_attribute('value'), 'Test Post')

    def test_8_edit_post_success(self):
        """Test successful post edit"""
        self.driver.find_element(By.LINK_TEXT, 'Test Post').click()
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys('Updated Test Post')
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Updated Test Post')))
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').is_displayed())

    def test_9_delete_post_confirmation(self):
        """Test delete post confirmation dialog"""
        self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').click()
        delete_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        self.assertTrue(delete_button.is_displayed())

    def test_10_delete_post_success(self):
        """Test successful post deletion"""
        self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').click()
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.LINK_TEXT, 'Updated Test Post')))
        self.assertFalse(self.driver.find_element(By.LINK_TEXT, 'Updated Test Post').is_displayed())

if __name__ == '__main__':
    unittest.main() 