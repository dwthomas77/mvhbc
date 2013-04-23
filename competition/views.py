# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from competition.models import Submission, Style, Category, Judge, JudgeForm, Address, BrewerProfile
from django.forms.models import modelform_factory, modelformset_factory
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from competition.forms import UserForm, BrewerProfileForm, AddressForm, SubmissionForm, SubmissionFormRemove, SubmissionFormUpdate
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

def index(request):
  return render(request, "competition_base.html")

def competition_home(request, authentication_form=AuthenticationForm):
  form = authentication_form(request)
  return render(request, "competition_home.html", {'form':form})

def competition_info(request):
  return render(request, "competition_info.html")

def competition_sponsors(request):
  return render(request, "competition_sponsors.html")

def competition_results(request):
  return render(request, "competition_results.html")

def competition_locations(request):
  return render(request, "competition_locations.html")

def ot_home(request):
  #users_in_group = Group.objects.get(name="officer").user_set.all()
  if request.user.groups.filter(name="officer").count():
    ot_dict = {
      "is_officer": True,
      "ot_info_entries": Submission.objects.count(),
      "ot_info_paid": Submission.objects.filter(paid=True).count(),
      "ot_info_brewers": BrewerProfile.objects.count()
    }
    return render(request, "ot_home.html", ot_dict)
  else:
    return redirect('login')

def ot_entries(request):
  #users_in_group = Group.objects.get(name="officer").user_set.all()
  if request.user.groups.filter(name="officer").count():
    ot_dict = {
      "is_officer": True,
      "entries": Submission.objects.all()
    }
    return render(request, "ot_entries.html", ot_dict)
  else:
    return redirect('login')

def ot_brewers(request):
  #users_in_group = Group.objects.get(name="officer").user_set.all()
  if request.user.groups.filter(name="officer").count():
    
    brewers = []
    for b in BrewerProfile.objects.all():
      address = b.address.street_1 + "<br>"
      if b.address.street_2:
        address+= b.address.street_2 + "<br>"
      address+= b.address.city+", "+b.address.state+" "+b.address.zip
      brewers.append({
        "name": b,
        "id": b.pk,
        "address": address,
        "email": b.user.email,
        "entries": Submission.objects.filter(brewer=b)
      })
    ot_dict = {
      "is_officer": True,
      "entries": Submission.objects.all(),
      "brewers": brewers
    }
    return render(request, "ot_brewers.html", ot_dict)
  else:
    return redirect('login')

def print_label(request, e_pk):
  if e_pk == '0':
    user_brewer = request.user.brewerprofile
    a = []
    for e in Submission.objects.filter(brewer = user_brewer):
      a.append(e)
    return render(request, "print_label.html", {'elist':a})
  else:
    e = get_object_or_404(Submission, pk=e_pk)
    a = [e]
    return render(request, "print_label.html", {'elist':a})

def entry_update(request, e_pk):
  e = get_object_or_404(Submission, pk=e_pk)
  b = BrewerProfile.objects.get(pk=e.brewer.pk)
  if not request.user.is_authenticated():
    return redirect('register')
  elif request.user.get_profile() != b:
    return redirect('logout')
  else:
    if request.method == 'POST' and request.user.brewerprofile:
      user_brewer = request.user.brewerprofile
      
      entryData = {
        'style': request.POST['style'],
        'name': request.POST['name'],
        'comments': request.POST['comments']
      }
      entry_form = SubmissionFormUpdate(entryData)
      if entry_form.is_valid():
        cur_style = Style.objects.get(pk=request.POST['style'])
        e.style = cur_style
        e.name = request.POST['name']
        e.comments = request.POST['comments']
        c_id = str(e.style.category.pk)
        s_id = str(e.pk)
        b_id = str(e.brewer.pk)
        comp_id = c_id+s_id+b_id
        e.competition_id=comp_id
        e.save()
        return redirect('brewer_profile')
      else:
        return render(request, "brewer_entry_update.html", {'form':entry_form})
    else:
      user_brewer = request.user.brewerprofile
      entryData = {
        'style': e.style,
        'name': e.name,
        'comments': e.comments,
      }
      entry_form = SubmissionFormUpdate(entryData)
      return render(request, "brewer_entry_update.html", {'form':entry_form})

def entry_remove(request, e_pk):
  e = get_object_or_404(Submission, pk=e_pk)
  b = BrewerProfile.objects.get(pk=e.brewer.pk)
  if not request.user.is_authenticated():
    return redirect('register')
  elif request.user.get_profile() != b:
    return redirect('logout')
  else:
    if request.method == 'POST':
      e.delete()
      return redirect('brewer_profile')
    else:
      user_brewer = request.user.brewerprofile
      entryData = {
        'style': e.style,
        'name': e.name,
        'comments': e.comments,
      }
      entry_form = SubmissionFormRemove(entryData)
      return render(request, "brewer_entry_remove.html", {'form':entry_form})

def address_change(request):
  if not request.user.is_authenticated():
    return redirect('register')
  else:
    if request.method == 'POST' and request.user.brewerprofile:
      user_brewer = request.user.brewerprofile
      addressData = {
        'street_1': request.POST['street_1'],
        'street_2': request.POST['street_2'],
        'city': request.POST['city'],
        'state': request.POST['state'],
        'zip': request.POST['zip']
      }
      address_form = AddressForm(addressData)
      if address_form.is_valid():
        a = user_brewer.address
        a.street_1 = request.POST['street_1']
        a.street_2 = request.POST['street_2']
        a.city = request.POST['city']
        a.state = request.POST['state']
        a.zip = request.POST['zip']
        a.save() 
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.save()
        msgAddress = "You have successfully updated your address!"
        return redirect('brewer_profile') 
      else:
        return render(request, "brewer_address_change.html", {'form':address_form})
    else:
      user_brewer = request.user.brewerprofile
      addressData = {
        'street_1': user_brewer.address.street_1,
        'street_2': user_brewer.address.street_2,
        'city': user_brewer.address.city,
        'state': user_brewer.address.state,
        'zip': user_brewer.address.zip
      }
      address_form = AddressForm(addressData)
      return render(request, "brewer_address_change.html", {'form':address_form})

def login_result(request):
  brewer_exists = True
  try:
    request.user.brewerprofile
  except:
    brewer_exists = False  
  if not request.user.is_authenticated() or not brewer_exists:
    return render(request, "competition_login.html")
  else:
    user_brewer = request.user.brewerprofile
    submission_query = Submission.objects.filter(brewer = user_brewer)
    dollarsSpent = submission_query.count() * 6
    dollarsPaid = 0
    dollarsOwed = dollarsSpent - dollarsPaid    
    login_dict = {
      'var1': 'test',
      'dollarsSpent': dollarsSpent,
      'dollarsPaid': dollarsPaid,
      'dollarsOwed': dollarsOwed,
      'entries': submission_query,
      'profile_address': request.user.brewerprofile.address
    }
    return render(request, "brewer_profile.html", login_dict)

def add_entry(request):
  if not request.user.is_authenticated():
    return redirect('register')
  else:
    if request.method == 'POST' and request.user.brewerprofile:
      entry_data = {
        'style': request.POST['style'],
        'brewer': request.user.brewerprofile.pk
      }
      form = SubmissionForm(entry_data)
#test
      if form.is_valid():
        s = form.save(commit=False)
        s.brewer = request.user.brewerprofile
        s.name = request.POST['name']
        s.comments = request.POST['comments']
        s.save()
        c_id = str(s.style.category.pk)
        s_id = str(s.pk)
        b_id = str(s.brewer.pk)
        comp_id = c_id+s_id+b_id
        s2 = Submission.objects.get(pk=s.pk)
        s2.competition_id=comp_id
        s2.save()
        return redirect('brewer_profile')
      else:
        entry_dict = {
        'submission_form' : form
        }
        return render(request, "brewer_entry.html", entry_dict)
    else:
      entry_dict = {
        'submission_form' : SubmissionForm()
      }
      return render(request, "brewer_entry.html", entry_dict)

def category(request):
  category_all_list = Category.objects.all()
  template = loader.get_template('category/index.html')
  context = Context({
    'category_all_list' : category_all_list,
  })
  return HttpResponse(template.render(context))

def style(request, style_id):
  return HttpResponse("You're looking at Style %s." % style_id)

def register(request):
  if request.method == 'POST':
    userData = {
      'username':  request.POST['username'],
      'first_name': request.POST['first_name'],
      'last_name': request.POST['last_name'],      
      'email': request.POST['email'],
      'password': request.POST['password']}
    addressData = {
      'street_1': request.POST['street_1'],
      'street_2': request.POST['street_2'],
      'city': request.POST['city'],
      'state': request.POST['state'],
      'zip': request.POST['zip']}
    brewerData = {
      'club': request.POST['club']}
    myUserForm = UserForm(userData)
    addressForm = AddressForm(addressData)
    brewerForm = BrewerProfileForm(brewerData)
    if myUserForm.is_valid() and addressForm.is_valid():
      u = myUserForm.save()
      a = addressForm.save()
      b = BrewerProfile(user=u, address=a, club=request.POST['club'])
      b.save()
      user = authenticate(username=request.POST['username'], password=request.POST['password'])
      if user is not None:
      # the password verified for the user
        if user.is_active:
          login(request, user)
          return redirect('brewer_profile')
        else:
          return redirect('register') 
      else:
        return redirect('register')
    else:    
      return render(request, 'competition_register.html', {
        'myUserForm' : myUserForm,
        'addressForm' : addressForm,
        'brewerForm' : brewerForm,
      })
  else:
    myUserForm = UserForm()
    addressForm = AddressForm()
    brewerForm = BrewerProfileForm()
    return render(request, 'competition_register.html', {
      'myUserForm' : myUserForm,
      'addressForm' : addressForm,
      'brewerForm' : brewerForm,
    })

def judge_register(request):
  if request.method == 'POST':
    form = JudgeForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return render(request, 'judge/judge_confirm.html') # Redirect after POST
    else: 
      return render(request, "judge/judge_register.html", {"form": form,})
  else:
    form = JudgeForm()
    return render(request, "judge/judge_register.html", {"form": form,})

def judge_confirm(request):
  return render(request, "judge/judge_confirm.html")
