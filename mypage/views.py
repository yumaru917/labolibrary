from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from search.models import Laboratory, ResearchPaper


# Create your views here.

@login_required
def mypage(request):
    is_lab = request.user.is_lab
    if is_lab is True:
        try:
            laboratory = Laboratory.objects.filter(uploader=request.user.id)[0]
            try:
                paper_list = ResearchPaper.objects.filter(laboratory=laboratory.id)
                print(paper_list[0].paper_file)
            except:
                paper_list = None
        except:
            laboratory = None
            paper_list = None
        context = {
            'laboratory': laboratory,
            'paper_list': paper_list
            }

        return render(request, "mypage/lab_mypage.html", context)
    else:
        return render(request, "mypage/student_mypage.html", {})
