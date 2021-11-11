from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest, request, response
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):

  def test_root_url_resolves_to_home_page_view(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_home_page_return_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    expected_html = render_to_string('home.html')
    self.assertEqual(response.content.decode(), expected_html)
    

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

class NewListTest(TestCase):

  def test_saving_a_POST_request(self):
    self.client.post('/lists/new', data={'item_text':'Nowy element listy'})
    self.assertEqual(Item.objects.count(),1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'Nowy element listy')
  
  def test_redirects_after_POST(self):
    response = self.client.post('/lists/new', data = {'item_text':'Nowy element listy'})
    new_list = List.objects.first()
    self.assertRedirects(response, '/lists/%d/' % (new_list.id))

  def test_can_save_a_POST_request_to_an_existing_list(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text':'Nowy element dla istniejącej listy'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'Nowy element dla istniejącej listy')
    self.assertEqual(new_item.list, correct_list)
  
  def test_redirects_to_list_view(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()

    response = self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text': 'Nowy element dla istniejącej listy'})
    self.assertRedirects(response, '/lists/%d/' %(correct_list.id,))