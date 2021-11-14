from .base import FunctionalTest
from selenium.webdriver.common.by import By

class ItemValidationTest(FunctionalTest):
  def test_cannot_add_empty_list(self):
    self.browser.get(self.server_url)
    self.get_item_input_box().send_keys('\n')

    self.get_item_input_box().send_keys('Kupić mleko\n')
    self.check_for_row_in_list_table('1: Kupić mleko')

    self.get_item_input_box().send_keys('\n')

    self.get_item_input_box().send_keys('Zrobić herbatę\n')
    self.check_for_row_in_list_table('1: Kupić mleko')
    self.check_for_row_in_list_table('2: Zrobić herbatę')

