from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get("http://moja-witryna.pl:8000")
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
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])
    self.assertIn('2: Użyc pawich piór do zrobienia przynęty', [row.text for row in rows])
    self.fail('Zakonczenie testu')
    

if __name__ == '__main__':
  unittest.main(warnings='ignore')