import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
import unittest
from unittest import skip

class FunctionalTest(StaticLiveServerTestCase):

  @classmethod
  def setUpClass(cls):
    for arg in sys.argv:
      if 'liveserver' in arg:
        cls.server_url = 'http://' + arg.split('=')[1]
        return
    super().setUpClass()
    cls.server_url = cls.live_server_url
    
  
  @classmethod
  def tearDownClass(cls):
    if cls.server_url == cls.live_server_url:
      super().tearDownClass()

  def setUp(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(3)

  def tearDown(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element(By.ID,'id_list_table')
    rows = table.find_elements(By.TAG_NAME,'tr')
    self.assertIn(row_text,[row.text for row in rows])

  def get_item_input_box(self):
    return self.browser.find_element(By.ID, 'id_text')
