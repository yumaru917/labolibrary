from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

from accounts.models import User
from mypage.models import Laboratory
from search.models import LaboratoryInfo, ResearchPaper, Image


# Create your views here.


@login_required
def lab_page(request):
    is_lab = request.user.is_lab_member
    if is_lab is True:
        laboratory = request.user.laboratory
        lab_notifications = laboratory.notification_for_laboratory.all()
        laboratory_members = laboratory.user_belong_to_laboratory.all()
        try:
            laboratory_info = LaboratoryInfo.objects.get(laboratory=laboratory.id)
            user_who_like_this_laboratory = User.objects.filter(favorite_laboratory=laboratory_info)
        except:
            laboratory_info = None
            user_who_like_this_laboratory = None
        try:
            paper_list = ResearchPaper.objects.filter(laboratory=laboratory_info.id)
            print(paper_list[0].paper_file)
        except:
            paper_list = None
            print('except happened')
        try:
            image_list = Image.objects.filter(laboratory_info=laboratory_info.id)
            print(image_list[0].title)
        except:
            image_list = None
            print('except happened')
        context = {
            'laboratory': laboratory,
            'laboratory_info': laboratory_info,
            'paper_list': paper_list,
            'image_list': image_list,
            'liked_by': user_who_like_this_laboratory,
            'lab_notifications': lab_notifications,
            'laboratory_members': laboratory_members
            }

        return render(request, "laboratory_page/laboratory_page_home.html", context)
    else:
        return render(request, "mypage/student_mypage.html", {})


def favorite_user_profile(request, pk):
    user = User.objects.get(pk=pk)
    try:
        profile = user.profile
    except User.profile.RelatedObjectDoesNotExist:
        profile = None

    return render(request, 'mypage/user_profile.html', {'user': user, 'profile': profile})


def notification_detail(request, pk):
    laboratory = request.user.laboratory
    lab_notification = laboratory.notification_for_laboratory.get(pk=pk)
    context = {
        'laboratory': laboratory,
        'notification': lab_notification
    }
    return render(request, 'laboratory_page/notification_detail.html', context)


class LabInfoDeleteView(generic.View):
    def get(self, *args, **kwargs):
        laboratory = self.request.user.laboratory
        LaboratoryInfo.objects.get(laboratory=laboratory.id).delete()
        lab_info_delete = True
        laboratory = self.request.user.laboratory
        try:
            laboratory_info = LaboratoryInfo.objects.get(laboratory=laboratory.id)
            user_who_like_this_laboratory = User.objects.filter(favorite_laboratory=laboratory_info)
        except:
            laboratory_info = None
            user_who_like_this_laboratory = None
        try:
            paper_list = ResearchPaper.objects.filter(laboratory=laboratory_info.id)
            print(paper_list[0].paper_file)
        except:
            paper_list = None
            print('except happened')
        context = {
            'lab_info_delete': lab_info_delete,
            'laboratory': laboratory,
            'laboratory_info': laboratory_info,
            'paper_list': paper_list,
            'liked_by': user_who_like_this_laboratory,
        }
        return render(self.request, "laboratory_page/laboratory_page_home.html", context)
