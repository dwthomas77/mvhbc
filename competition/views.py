# Create your views here.
import math
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from competition.models import Submission, Style, Category, Judge, JudgeForm, Address, BrewerProfile, CompetitionTable
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

def ot_categories(request):
  #users_in_group = Group.objects.get(name="officer").user_set.all()
  if request.user.groups.filter(name="officer").count():
    cats = []
    for c in Category.objects.all():
      total_count = 0
      style_q = Style.objects.filter(category=c)
      styles = []
      for s in style_q:
        entry_count = Submission.objects.filter(style=s).count()
        entries = Submission.objects.filter(style=s)
        total_count += entry_count
        styles.append({
          "name": s.style_name,
          "count": entry_count,
          "entries": entries
        })
      cats.append({
        "name": c.category_name,
        "id": c.pk,
        "total_count": total_count,
        "styles": styles
      })
    ot_dict = {
      "is_officer": True,
      "cats": cats
    }
    return render(request, "ot_categories.html", ot_dict)
  else:
    return redirect('login')

def ot_judges(request):
  if request.user.groups.filter(name="officer").count():
    judges = Judge.objects.filter(judge_pref="Judge")
    stewards = Judge.objects.filter(judge_pref="Steward")
    ot_dict={
      "is_officer": True,
      "judges": judges,
      "stewards": stewards
    }
    return render(request, "ot_judges.html", ot_dict)
  else:
    return redirect('login')

def ot_tables(request):
  if request.user.groups.filter(name="officer").count():
    tables = []
    tables_d = []
    tables_p = []
    if not tables:
      table_id = len(tables)+1
      tables.insert(0,{
        "categories":[],
        "total_count": 0,
        "status": "new"
      })
    cur_table = tables[0]
    max_table_size = 12
    hold_table_size = 8
    categories = []
    tables_q = CompetitionTable.objects.all()
    cats_q = Category.objects.all()
    jq = Judge.objects.filter(judge_pref="Judge")
    for c in cats_q:
      # Get all entries for the styles associated with the category
      style_q = Style.objects.filter(category=c)      
      entries = []
      for s in style_q:
        entries_q = Submission.objects.filter(style=s)
        for e in entries_q:
          entries.append({
            "id": e.pk,
            "style": e.style
          })
      # build category object to add to a table
      cur_cat = {
        "category":c,
        "entries":entries
        }
      # 1 A
      if(len(entries)):
        added = False
        # 2
        for i,t in enumerate(tables):
          # 2 A if there is room in current table for next category
          if((t["total_count"] + len(entries)) <= max_table_size):
            # 2 B Add it
            t["categories"].append(cur_cat)
            t["total_count"] += len(entries)
            added = True
            # 2 C if the table is big enough to hold
            if(t["total_count"] >= hold_table_size):
              # 2 D add it to done tables
              tables_d.append(t)
              tables.remove(t)
            break
            
        #3 If not added yet make new table
        if not added:
          # 3A if there is enough entries in this cat to hold a full table
          if(len(entries) >= hold_table_size):
            # 3 B add full table to done list
            tables_d.append({
              "categories":[cur_cat],
              "total_count": len(entries),
              "status": "new"
             })
          else:
            #3 C else add to reuglar table list
            tables.append({
              "categories":[cur_cat],
              "total_count": len(entries),
              "status": "new"
             })
    
    tables_d.extend(tables)

    if((jq.count()/2)<=len(tables_d)):
      sessions=2
      tables_per_session=math.ceil(len(tables_d)/2)
      judges_per_session=tables_per_session * 2
    else:
      sessions=1
      tables_per_session=len(tables_d)
      judges_per_session=len(tables_d)*2
    ot_dict={
      "is_officer": True,
      "tables": tables_d,
      "judges": jq,
      "sessions": sessions,
      "tables_per_session": tables_per_session,
      "judges_per_session": judges_per_session
    }
    return render(request, "ot_tables.html", ot_dict)
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
    if request.user.groups.filter(name="officer").count():
      isOfficer = True
    else:
      isOfficer = False
    login_dict = {
      'is_officer': isOfficer,
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
