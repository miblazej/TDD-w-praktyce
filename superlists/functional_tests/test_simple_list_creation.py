from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest



class NewVisitorTest(FunctionalTest):
  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get(self.server_url)
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element(By.TAG_NAME,'h1').text
    self.assertIn('listę', header_text)
    inputbox = self.get_item_input_box()
    self.assertEqual(inputbox.get_attribute('placeholder'),'Wpisz rzeczy do zrobienia')
    inputbox.send_keys('Kupić pawie pióra')
    inputbox.send_keys(Keys.ENTER)
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    self.check_for_row_in_list_table('1: Kupić pawie pióra')
    inputbox = self.get_item_input_box()
    inputbox.send_keys('Użyc pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('2: Użyc pawich piór do zrobienia przynęty')
    
    self.browser.quit()
    self.browser = webdriver.Chrome()
    self.browser.get(self.server_url)
    page_text = self.browser.find_element(By.TAG_NAME,'body').text
    self.assertNotIn('Kupić pawie pióra',page_text)
    self.assertNotIn('zrobienia przynęty',page_text)

    inputbox = self.get_item_input_box()
    inputbox.send_keys('Kupić mleko')
    inputbox.send_keys(Keys.ENTER)

    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    page_text = self.browser.find_element(By.TAG_NAME,'body').text
    self.assertNotIn('Kupić pawie pióra', page_text)
    self.assertIn('Kupić mleko', page_text)

