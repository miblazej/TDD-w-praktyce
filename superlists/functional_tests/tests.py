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
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')
    self.check_for_row_in_list_table('1: Kupić pawie pióra')
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Użyc pawich piór do zrobienia przynęty')
    inputbox.send_keys(Keys.ENTER)
    self.check_for_row_in_list_table('2: Użyc pawich piór do zrobienia przynęty')
    
    self.browser.quit()
    self.browser = webdriver.Chrome()
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupić pawie pióra',page_text)
    self.assertNotIn('zrobienia przynęty',page_text)

    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Kupić mleko')
    inputbox.send_keys(Keys.ENTER)

    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Kupić pawie pióra', page_text)
    self.assertIn('Kupić mleko', page_text)

  def test_layout_and_styling(self):
    self.browser.get(self.live_server_url)
    self.browser.set_window_size(1024,768)

    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)
    inputbox.send_keys('testing\n')
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10)
