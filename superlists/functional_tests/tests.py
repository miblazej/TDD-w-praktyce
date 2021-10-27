from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text,[row.text for row in rows])

    

  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get(self.live_server_url)
    self.assertIn('Listy', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('lista', header_text)
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(inputbox.get_attribute('placeholder'),'Wpisz rzecz do zrobienia')
    inputbox.send_keys('Kupić pawie pióra')
    inputbox.send_keys(Keys.ENTER)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Użyc pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('1: Kupić pawie pióra')
    self.check_for_row_in_list_table('2: Użyc pawich piór do zrobienia przynęty')
    self.fail('Zakonczenie testu')
    
