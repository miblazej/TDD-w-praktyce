from django.shortcuts import redirect, render
from lists.forms import ItemForm, EMPTY_LIST_ERROR
from django.views.decorators.csrf import csrf_exempt
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.

@csrf_exempt
def home_page(request):
  return render(request, 'home.html', {'form': ItemForm()})

@csrf_exempt
def view_list(request, list_id):
  list_ = List.objects.get(id=list_id)
  error = None

  if request.method == 'POST':
    try:
      item = Item(text=request.POST['text'], list=list_)
      item.full_clean()
      item.save()
      return redirect(list_)
    except ValidationError:
      error = EMPTY_LIST_ERROR
      
  return render(request, 'list.html', {'list':list_, 'error': error,"form":ItemForm()})

@csrf_exempt
def new_list(request):
  error = EMPTY_LIST_ERROR
  form = ItemForm(data=request.POST)
  if form.is_valid():
    list_ = List.objects.create()
    Item.objects.create(text = request.POST['text'], list=list_)
    return redirect(list_)
  else:
    return render(request, 'home.html',{"form":form,"error": error})

