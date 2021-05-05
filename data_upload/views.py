from django.shortcuts import render
from search.models import Laboratory
import csv
from io import TextIOWrapper, StringIO
from django.utils import timezone


def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            print(line)
            laboratory = Laboratory.objects.create(laboratory_name=line[0])
            laboratory.laboratory_name = line[0]
            laboratory.university = line[1]
            laboratory.department = line[2]
            laboratory.professor_name = line[3]
            laboratory.research_keywords = line[4]
            laboratory.research_info = line[5]
            laboratory.laboratory_website = line[6]
            laboratory.information_source = line[7]
            laboratory.create_date = timezone.now
            laboratory.update_date = timezone.now

            laboratory.save()

        return render(request, 'data_upload/upload.html')

    else:
        return render(request, 'data_upload/upload.html')