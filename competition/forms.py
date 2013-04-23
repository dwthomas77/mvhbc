from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import FormActions
from competition.models import BrewerProfile, Address, Submission, Style, Category

def categories_as_choices():
  categories = []
  for category in Category.objects.all():
    new_category = []
    sub_categories = []
    for style in category.style_set.all():
      sub_categories.append([style.pk, style.style_name.encode('utf8')])
    tmp_name = str(category.category_id) + " " + category.category_name
    tmp_name2 = "lolz"
    new_category = [tmp_name.encode('utf8'), sub_categories]
    categories.append(new_category)

  return categories

class SubmissionForm(forms.ModelForm):
  mChoices = [
    ['Choice A', 
      [
        ['1', 'SubA1'],
        ['2', 'SubA2']
      ]
    ]
  ]

  myChoices = categories_as_choices()
  #style = forms.ChoiceField(choices=myChoices)
  class Meta:
    model = Submission
    fields = ('style', 'name', 'comments')
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'entrySubmissionForm'
    self.helper.form_class = 'blueForms'
    self.helper.form_method = 'post'
    self.helper.form_class = 'form-horizontal'
    self.helper.add_input(Submit('submit', 'Submit'))
    self.helper.layout = Layout(
      Fieldset(
        'Add New Entry',
        'style',
        'name',
        HTML("""
          <div style="width:75%; margin-left:25px"><small>Special Ingredients/Classic Style 
(required for categories 6D, 16E, 17F, 20, 21, 22B, 22C, 23, 25C, 26A, 26C, 27E, 28B-D)</small></div>
        """),
      ),
    )
    super(SubmissionForm, self).__init__(*args, **kwargs) 

class SubmissionFormUpdate(forms.ModelForm):
  mChoices = [
    ['Choice A',
      [
        ['1', 'SubA1'],
        ['2', 'SubA2']
      ]
    ]
  ]

  myChoices = categories_as_choices()
  #style = forms.ChoiceField(choices=mChoices)
  #comments = forms.CharField(required=False, initial=myChoices)
  class Meta:
    model = Submission
    fields = ('style', 'name', 'comments')
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'entrySubmissionForm'
    self.helper.form_class = 'blueForms'
    self.helper.form_method = 'post'
    self.helper.form_class = 'form-horizontal'
    self.helper.add_input(Submit('submit', 'Submit'))
    self.helper.layout = Layout(
      Fieldset(
        'Update Entry',
        'style',
        'name',
        HTML("""
          <div style="width:75%; margin-left:25px"><small>Special Ingredients/Classic Style
(required for categories 6D, 16E, 17F, 20, 21, 22B, 22C, 23, 25C, 26A, 26C, 27E, 28B-D)</small></div>
        """),
      ),
    )
    super(SubmissionFormUpdate, self).__init__(*args, **kwargs)


class SubmissionFormRemove(forms.ModelForm):
  style = forms.ModelChoiceField(queryset=Style.objects.all(), widget=forms.Select(attrs={'disabled':'disabled'}))
  name = forms.CharField(required=False, widget=forms.TextInput(attrs={'disabled':'disabled'}))
  comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'disabled':'disabled'}))
  class Meta:
    model = Submission
    fields = ('style', 'name', 'comments')
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'removeEntryForm'
    self.helper.form_class = 'blueForms'
    self.helper.form_method = 'post'
    self.helper.form_class = 'form-horizontal'
    self.helper.add_input(Submit('submit', 'Remove Entry', css_class='btn btn-danger'))
    super(SubmissionFormRemove, self).__init__(*args, **kwargs)

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  email = forms.CharField(max_length=75, required=True)
  first_name = forms.CharField(max_length=100, required=True)  
  last_name = forms.CharField(max_length=100, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'first_name', 'last_name', 'email')
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_tag = False
    super(UserForm, self).__init__(*args, **kwargs)
  def save(self, commit=True):
    user = super(UserForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password"])
    if commit:
      user.save()
    return user

class BrewerProfileForm(forms.ModelForm):
  class Meta:
    model = BrewerProfile
    fields = ('club',)
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_tag = False
    super(BrewerProfileForm, self).__init__(*args, **kwargs)

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_tag = False
    super(AddressForm, self).__init__(*args, **kwargs)
