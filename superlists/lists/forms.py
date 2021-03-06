from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "Element listy nie może być pusty"
DUPLICATE_ITEM_ERROR = "Podany element już istnieje na liście"

class ItemForm(forms.models.ModelForm):

  def save(self, for_list):
      self.instance.list = for_list
      return super().save()

  class Meta:
    model = Item
    fields = ('text',)
    widgets = {
      'text': forms.fields.TextInput( attrs = {
        'placeholder': 'Wpisz rzeczy do zrobienia',
        'class': 'form-control input-lg'
      }),
    }
    error_messages = {
      'text': {'required': EMPTY_LIST_ERROR}
    }

    