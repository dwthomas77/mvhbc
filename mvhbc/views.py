from django.http import HttpResponse
from django.shortcuts import render

def home(request):
  return render(request, 'club_home.html')

def about(request):
  return render(request, 'club_about.html')

def membership(request):
  return render(request, 'club_membership.html')

def officers(request):
  return render(request, 'club_officers.html')

def resources(request):
  return render(request, 'club_resources.html')
