from .base import FunctionalTest
from selenium.webdriver.common.by import By

class ItemValidationTest(FunctionalTest):
  def test_cannot_add_empty_list(self):
    self.browser.get(self.server_url)
    self.browser.find_element_by_id('id_new_item').send_keys('\n')

    error = self.browser.find_element(By.CSS_SELECTOR,'.has-error')
    self.assertEqual(error.text, "Element nie może być pusty")

    self.browser.find_element_by_id('id_new_item').send_keys('Kupić mleko\n')
    self.check_for_row_in_list_table('1: Kupić mleko')

    self.browser.find_element_by_id('id_new_item').send_keys('\n')

    self.check_for_row_in_list_table('1: Kupić mleko')
    error = self.browser.find_element(By.CSS_SELECTOR,'.has-error')
    self.assertEqual(error.text, "Element nie może być pusty")

    self.browser.find_element_by_id('id_new_item').send_keys('Zrobić herbatę\n')
    self.check_for_row_in_list_table('1: Kupić mleko')
    self.check_for_row_in_list_table('2: Zrobić herbatę')
