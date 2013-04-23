from django.db import models
from django.forms import ModelForm, Form, CharField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.models import User
from django.contrib.localflavor.us.us_states import US_STATES
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField

class Address(models.Model):
  street_1 = models.CharField(max_length=100)
  street_2 = models.CharField(max_length=100, blank=True)
  city = models.CharField(max_length=100)
  state = USStateField(choices = US_STATES)
  zip = models.CharField(max_length=5)

class BrewerProfile(models.Model):
  user = models.OneToOneField(User)
  address = models.OneToOneField(Address)
  phone_number = PhoneNumberField(blank=True, null=True)
  club = models.CharField(max_length=200, blank=True, null=True)
  entries_paid = models.IntegerField(default=0)
  insert_date =  models.DateField('Registered On', auto_now_add=True)
  def __unicode__(self):
    name = self.user.last_name + ", " + self.user.first_name
    return name

class Category(models.Model):
  category_id = models.IntegerField()
  category_name = models.CharField(max_length=200)
  TYPE_CHOICES = (
    ('Lager', 'Lager'),
    ('Ale', 'Ale'),
    ('Mixed', 'Mixed'),
    ('Mead', 'Mead'),
    ('Cider', 'Cider'),
  )
  category_type = models.CharField(max_length=200, choices=TYPE_CHOICES, default='Lager')
  class Meta:
    ordering = ['category_id',]
    verbose_name = "category"
    verbose_name_plural = "categories"
  def __unicode__(self):
    str_id = str(self.category_id)
    name = str_id + ' ' + self.category_name
    return name
  def order_by_id(self):
    str_id = str(self.category_id)
    name = str_id + ' ' + self.category_name
    return name
  order_by_id.admin_order_field = 'category_id'

class Style(models.Model):
  category = models.ForeignKey(Category)
  style_id = models.CharField(max_length=1)
  style_name = models.CharField(max_length=200)
  def __unicode__(self):
    str_id = str(self.category.category_id)
    name = str_id + self.style_id + ' ' + self.style_name
    return name

class Submission(models.Model):
  competition_id = models.CharField(max_length=100, default=0)
  brewer = models.ForeignKey(BrewerProfile)
  style = models.ForeignKey(Style)
  name = models.CharField(max_length=200, blank=True, null=True)
  comments = models.TextField(blank=True)
  submitted_on = models.DateField('Submitted On', auto_now_add=True)
  received_on = models.DateField(blank=True, null=True)
  checked_in = models.DateField(blank=True, null=True)
  paid = models.BooleanField(default=False)
  score = models.IntegerField(blank=True, null=True)
  place = models.IntegerField(blank=True, null=True)
  def __unicode__(self):
    cat_id = str(self.style.category.pk)
    sub_id = str(self.pk)
    brewer_id = str(self.brewer.pk)
    uni_id = cat_id+sub_id+brewer_id
    return sub_id

class Judge(models.Model):
  first_name = models.CharField(max_length=100, blank=False)
  last_name = models.CharField(max_length=100, blank=False)
  phone_number = PhoneNumberField(blank=True)
  email = models.EmailField(max_length=254, blank=False)
  club_affiliation = models.CharField(max_length=200, blank=True);
  PREF_CHOICES = (
    ('Judge', 'Judge'),
    ('Steward', 'Steward'),
  )
  judge_pref = models.CharField('Judging Preference', max_length=100, choices=PREF_CHOICES, default='Judge', blank=False)
  APPRENTICE = 'AP'
  CERTIFIED = 'CT'
  RECOGNIZED = 'RC'
  NATIONAL = 'NT'
  MASTER = 'MA'
  GRAND_MASTER = 'GM'
  PROFESSIONAL_BREWER = 'PRO'
  QUALIFICATION_CHOICES = (
    (APPRENTICE, 'Apprentice'),
    (CERTIFIED, 'Certified'),
    (RECOGNIZED, 'Recognized'),
    (NATIONAL, 'National'),
    (MASTER, 'Master'),
    (GRAND_MASTER, 'Grand Master'),
    (PROFESSIONAL_BREWER, 'Professional Brewer'),
  )
  qualification = models.CharField(max_length=3, choices=QUALIFICATION_CHOICES, default=APPRENTICE)
  bjcp_registration = models.CharField('BJCP Registration Number (if appropriate)', max_length=100, blank=True)
  cat_pref_yes = models.ManyToManyField(Category, verbose_name='Categories Preferred To Judge', blank=True, null=True, related_name='yes+')
  cat_pref_no = models.ManyToManyField(Category, verbose_name='Categories Preferred Not To Judge', blank=True, null=True, related_name='no+')
  notes = models.TextField(blank=True)
  def __unicode__(self):
    name_str = self.first_name + " " + self.last_name
    return name_str

class JudgeForm(ModelForm):
  class Meta:
    model = Judge
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = 'id-exampleForm'
    self.helper.form_class = 'blueForms'
    self.helper.form_method = 'post'
    #self.helper.form_action = ''
    self.helper.form_class = 'form-horizontal'
    self.helper.layout = Layout(
      Fieldset(
        'Contact Information',
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'club_affiliation',
      ),
      Fieldset(
        'Competition Information',
        'judge_pref',
        'qualification',
        'bjcp_registration',
        'cat_pref_yes',
        'cat_pref_no',
        'notes',
      ),
      FormActions(
        HTML("""
          <p class="disclaimerTitle">Judge and Steward Waiver</p><p>My participation in this event is entirely voluntary. I know that participation in this judging involves consumption of alcoholic beverages and that this consumption may affect my perceptions and reactions. I accept responsibility for my conduct, behavior and actions, and completely absolve the competition organizers, Sponsors, and the Beer Judge Certification Program of responsibility for my conduct, behavior and actions. Clicking on the Submit Information button is your acknowlegement of this waiver.<br><input type="submit" value="Submit"></p>
        """),
      )
    )
    super(JudgeForm, self).__init__(*args, **kwargs)

