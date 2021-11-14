from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest, request, response
from django.template.loader import render_to_string
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_LIST_ERROR
from unittest import skip

# Create your tests here.
class HomePageTest(TestCase):
  maxDiff = None

  def test_home_page_renders_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_home_page_uses_item_form(self):
    response = self.client.get('/')
    self.assertIsInstance(response.context['form'], ItemForm)
    

class ListViewTest(TestCase):

  def test_uses_list_template(self):
    list_ = List.objects.create()
    response = self.client.get('/lists/%d/' % (list_.id,))
    self.assertTemplateUsed(response, 'list.html')  

  def test_home_page_displays_all_list_items(self):
    correct_list = List.objects.create()
    Item.objects.create(text='itemey 1', list=correct_list)
    Item.objects.create(text='itemey 2', list=correct_list)
    other_list = List.objects.create()
    Item.objects.create(text="Element pierwszy innej listy", list=other_list)
    Item.objects.create(text="Element drugi innej listy", list=other_list)

    response = self.client.get('/lists/%d/' % (correct_list.id,))

    self.assertContains(response, 'itemey 1')
    self.assertContains(response, 'itemey 2')
    self.assertNotContains(response, 'Element pierwszy innej listy')
    self.assertNotContains(response, 'Element drugi innej listy')
  
  def test_passes_correct_list_to_template(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = self.client.get('/lists/%d/' % (correct_list.id,))
    self.assertEqual(response.context['list'], correct_list)

  def test_can_save_a_POST_request_to_an_existing_list(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    self.client.post('/lists/%d/' % (correct_list.id,), data={'text':'Nowy element dla istniejącej listy'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'Nowy element dla istniejącej listy')
    self.assertEqual(new_item.list, correct_list)

  def test_saving_a_POST_request(self):
    self.client.post('/lists/new', data={'text':'Nowy element listy'})
    self.assertEqual(Item.objects.count(),1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'Nowy element listy')
  
  def test_redirects_after_POST(self):
    response = self.client.post('/lists/new', data = {'text':'Nowy element listy'})
    new_list = List.objects.first()
    self.assertRedirects(response, '/lists/%d/' % (new_list.id))

  def test_POST_redirects_to_list_view(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = self.client.post('/lists/%d/' % (correct_list.id,), data={'text': 'Nowy element dla istniejącej listy'})
    self.assertRedirects(response, '/lists/%d/' %(correct_list.id,))

  def test_invalid_list_arent_saved(self):
    self.client.post('/lists/new', data={'text':''})
    self.assertEqual(List.objects.count(),0)
    self.assertEqual(Item.objects.count(),0)
  
  def test_display_item_form(self):
    list_ = List.objects.create()
    response = self.client.get('/lists/%d/' %(list_.id,))
    self.assertIsInstance(response.context['form'], ItemForm)
    self.assertContains(response, 'name="text"')

  def post_invalid_input(self):
    list_ = List.objects.create()
    return self.client.post('/lists/%d/' % (list_.id,), data={'text': ''})

  def test_for_invalid_input_renders_list_template(self):
    response = self.post_invalid_input()
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'list.html')

  def test_for_invalid_input_passes_form_to_template(self):
    response = self.post_invalid_input()
    self.assertIsInstance(response.context['form'], ItemForm)
  @skip
  def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text='textey')
    response = self.client.post('/lists/%d/' % (list1.id,), data={'text':'textey'})
    expected_error = escape("Podany element już istnieje na liście")
    self.assertContains(response, expected_error)
    self.assertTemplateUsed(response, 'list.html')
    self.assertEqual(Item.objects.all().count(),1)

class NewListTest(TestCase):

  def test_validation_errors_are_sent_back_to_home_page_template(self):
    response = self.client.post('/lists/new', data={'text': ''})
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response,'home.html')
      
  def test_for_invalid_input_renders_home_template(self):
    response = self.client.post('/lists/new', data={'text': ''})
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')


  def test_for_invalid_input_passes_from_to_template(self):
    response = self.client.post('/lists/new', data={'text': ''})
    self.assertIsInstance(response.context['form'], ItemForm)



  
