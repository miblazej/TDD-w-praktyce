from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lists.models import Item, List

# Create your views here.

@csrf_exempt
def home_page(request):
  return render(request, 'home.html')

@csrf_exempt
def view_list(request):
  items = Item.objects.all()
  return render(request, 'list.html', {'items':items})

@csrf_exempt
def new_list(request):
  list_ = List.objects.create()
  Item.objects.create(text=request.POST['item_text'], list=list_)
  return redirect('/lists/the-only-list-in-the-world/')