from django.contrib import admin
from search.models import LaboratoryInfo, SearchText, ResearchPaper

# Register your models here.

admin.site.register(LaboratoryInfo)
admin.site.register(SearchText)
admin.site.register(ResearchPaper)
