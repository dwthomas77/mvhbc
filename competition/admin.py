from django.contrib import admin
from competition.models import Submission, Address, BrewerProfile, Judge, Category, Style
from django.contrib.auth.models import User

class StyleInline(admin.StackedInline):
  model = Style
  extra = 1

class SubmissionAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','brewer','style','competition_id')

class SubmissionInline(admin.StackedInline):
  model = Submission

class BrewerAdmin(admin.ModelAdmin):
  inlines = [SubmissionInline]

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('order_by_id', 'category_type')
  inlines = [StyleInline]

class JudgeAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'qualification')

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Address)
admin.site.register(BrewerProfile, BrewerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Judge, JudgeAdmin)
